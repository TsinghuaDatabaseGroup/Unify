from flask import Flask, request, Response, stream_with_context
import json
from openai import OpenAI
from utils.contextManager import LLMContextManager
from semanticParse import semantic_parse, replace_parsed_elements_with_identifiers, BQMatcher
from embed import EmbedModel
from PlanManager import *
from unify import *
from chunk import load_process_data_chunks, ChunkExtractor
from index import indexHNSW
from utils.placeholders import *
from utils.llm_config import ModelConfig, DEBUG_MODEL_CONFIG
import time
import os

app = Flask(__name__)

# class ModelConfig:
#     def __init__(self, model_path):
#         self.model_path = model_path

def process_query_generator(query, dataset_path, model_path, tokenizer_path, sentence_model_path, openai_api_key, openai_api_base):
    # Initialize the OpenAI client
    client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)
    chatModel = ModelConfig(model_path)

    # Load and process the dataset
    chunkExtractor = ChunkExtractor()
    embedModel = EmbedModel(tokenizer_path=tokenizer_path, sentence_model_path=sentence_model_path)
    all_file_data, all_chunks, all_ids, all_embeds, all_chunk_locs = load_process_data_chunks(
        embedModel, chunkExtractor, dataset_path
    )
    index = indexHNSW(all_chunks, all_embeds, all_ids, all_chunk_locs)

    # Semantic parsing
    yield "Start semantic parsing...\n"
    parsed_result = semantic_parse(query, client, chatModel)
    yield f"parsing result: {json.dumps(parsed_result)}\n"

    # Transform the question
    transformed_question = replace_parsed_elements_with_identifiers(query, parsed_result)
    yield f"The transformed problem: {transformed_question}\n"

    # Plan generation
    BQMatcher_instance = BQMatcher(embedModel)
    final_flag, final_plan, final_BQ_list, partial_question_list = recursive_plan_generation(
        query, transformed_question, BQMatcher_instance, client, chatModel, embedModel, current_plan=[], use_BQ_list=[], partial_question_list=[], depth=0
    )
    yield f"Finally the plan is successfully selected: {final_flag}\n"
    yield f"The final plan is: {json.dumps(final_plan)}\n"
    yield f"The final BQ list is: {json.dumps(final_BQ_list)}\n"
    yield f"List of partial questions: {json.dumps(partial_question_list)}\n"

    # Plan execution
    PM = planManager(
        query, final_plan, client, chatModel, final_BQ_list, all_file_data, parsed_result, partial_question_list,
        embedModel, index
    )
    yield "Execute the plan...\n"
    PM.execute_without_plan()

    # Stream the final result
    if PM.BQ_list and "IDPlan" in PM.BQ_list[-1] and PM.BQ_list[-1]["IDPlan"]:
        final_result = PM.BQ_list[-1]["IDPlan"][0].get("Result", "No result found.")
        yield f"Final result: {final_result}\n"
    else:
        yield "No available final result.\n"

@app.route('/process_query', methods=['POST'])
def process_query():
    data = request.json
    query = data.get("query")
    dataset_path = data.get("dataset_path")
    model_path = data.get("model_path")
    tokenizer_path = data.get("tokenizer_path","/home/fit/liguol/Macly/tokenizer")
    sentence_model_path = data.get("sentence_model_path")
    openai_api_key = data.get("openai_api_key", "EMPTY")
    openai_api_base = data.get("openai_api_base", "http://localhost:8001/v1")

    required_params = ["query", "dataset_path", "model_path", "tokenizer_path", "sentence_model_path"]
    missing_params = [param for param in required_params if not data.get(param)]
    if missing_params:
        return {"error": f"Missing required parameters: {', '.join(missing_params)}"}, 400

    # Stream response
    return Response(
        stream_with_context(process_query_generator(query, dataset_path, model_path, tokenizer_path, sentence_model_path, openai_api_key, openai_api_base)),
        content_type='text/plain'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)