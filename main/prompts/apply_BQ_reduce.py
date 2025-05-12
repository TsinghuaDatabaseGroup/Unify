import json
from embed import EmbedModel

# Load the knowledge base
with open("./knowledge_base/BQReductionKnowledgeBase.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

DEFAULT_EXAMPLE_IDS = ["example_1","example_2","example_3", "example_4", "example_5", "example_6", "example_7", "example_8", "example_9", "example_10", "example_18", "example_19"] 

def retrieve_relevant_examples(original_query, parsed_query, bq_question, bq_result, embed_model, top_k=12, threshold=0.1):
    """
    Retrieve the top-K most relevant examples from the knowledge base.
    """
    # Combine the current input into a query string
    query = f"{original_query} | {parsed_query} | {bq_question} | {bq_result}"
    query_embedding = embed_model.calculate_embeddings([query])[0]

    # Calculate the embeddings of each example in the knowledge base and compare similarities
    example_embeddings = []
    for entry in knowledge_base:
        example_str = f"{entry['query']['original']} | {entry['query']['parsed']} | {entry['BQ']['question']} | {entry['BQ']['return']}"
        example_embedding = embed_model.calculate_embeddings([example_str])[0]
        example_embeddings.append((entry, example_embedding))

    # Calculate the cosine similarity and sort
    cosine_scores = [
        (entry, sum(q * e for q, e in zip(query_embedding, emb))) 
        for entry, emb in example_embeddings
    ]
    cosine_scores.sort(key=lambda x: x[1], reverse=True)

    # Check if the similarity is valid
    top_scores = [score for _, score in cosine_scores[:top_k]]
    if not top_scores or max(top_scores) < threshold:
        # logger.warning(f"All cosine similarities are below threshold {threshold} or zero for query: {query}")
        # Return default examples
        default_examples = [entry for entry in knowledge_base if entry['id'] in DEFAULT_EXAMPLE_IDS]
        return default_examples[:top_k]  # Ensure the number does not exceed top_k

    # Return Top-K examples
    return [entry for entry, score in cosine_scores[:top_k]]

def format_example(entry):
    """
    Format the examples in the knowledge base into a prompt string.
    """
    return f"""
    ### Example {entry['id'].split('_')[1]}:
    Original Query: "{entry['query']['original']}"
    Semantic Parsed Query: "{entry['query']['parsed']}"
    Candidate Basic Question: "{entry['BQ']['question']}"
    Result of the Basic Question: "{entry['BQ']['return']}"
    Output: {json.dumps(entry['judgment'], indent=4)}
    Reasoning: {entry['explanation']}
    """

def apply_BQ_prompt(original_question, parsed_question,  BQ_Question, BQ_Return, embed_model):
    # Retrieve relevant examples
    relevant_examples = retrieve_relevant_examples(original_question, parsed_question, BQ_Question, BQ_Return, embed_model, top_k=12)
    examples_str = "\n".join(format_example(entry) for entry in relevant_examples)
    
    PROMPT = f"""
            ## Task:
            You are given four inputs:

            1. An original query.
            2. The semantically parsed version of the original query.
            3. A candidate basic question
            4. The result of the basic question (expressed in logical representation form).
            Your task is to determine whether the basic question and its result can fully or partially solve the original query and parsed query. 
            If they can, transform both the original query and the parsed query using the result from the basic question. If they cannot, or if the prerequisites for solving the query are not met, output "No" in the result.



            ## Instructions:
            Check Compatibility: Verify if the basic question and its result can solve the original query and its parsed version.

            Determine the Type of Solution:

            - If the basic question fully solves the query, mark it as "fully solved".
            - If the basic question only partially solves the query, mark it as "partially solved".
            - If the basic question does not help solve any part of the query, mark it as "no solution".
            
            Provide Results:

            - If the basic question fully solves the query, transform both the original and parsed queries based on the result.
            - If the basic question partially solves the query, reduce both queries using the basic question, e.g. modify the part of the query that can be solved, and leave the rest unchanged, or you can rewrite it. The rewrite rules are as follows:
                - If sub-problems are needed:
                    - Set "transformed_original_query" to exact string "sub_problems"
                    - Define sub-problems list in "sub_problems" field
                - If no sub-problems needed:
                    - reduce the query directly and set "sub_problems" to "No".
            If the basic question does not solve any part of the query, return "No" for both the original and parsed queries.


            ## Output:

            Return a JSON object in the following format:
            {{
                "fully_solved": <true/false>,
                "partially_solved": <true/false>,
                "transformed_original_query": "<transformed original query | sub_problems>",
                "sub_problems": "<list of sub-queries | No>",
                "transformed_parsed_query": "<transformed parsed query>"
            }}

            ## Detailed Scenarios:
            ### Fully Solved:

            The basic question completely solves the original and parsed queries.
                - Set "fully_solved" to true, "partially_solved" to false.
                - Provide the transformed versions of both the original and parsed queries.


            ### Partially Solved:

            The basic question solves part of the original and parsed queries.
                - Set "fully_solved" to false, "partially_solved" to true.
                - Provide the transformed versions of both the original and parsed queries, reflecting only the part that can be solved.


            ### Not solved:

            The basic question does not help solve any part of the query.
                - Set "fully_solved" and "partially_solved" to false.
                - Set "transformed_original_query" and "transformed_parsed_query" to "No".

            ## Examples:
            {examples_str}

            
            Now, for the current input:

            Original Query: "{original_question}"
            Semantic Parsed Query: "{parsed_question}"
            Candidate Basic Question: "{BQ_Question}"
            Result of the Basic Question: "{BQ_Return}"

            Please provide the result in the JSON format described above like above examples. Do not output any other thing except the JSON.
        """

    return PROMPT