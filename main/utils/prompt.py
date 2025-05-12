GET_PLAN_PROMPT = """
 Question: {}.
 The operators for planning the workflow are as follows: {}. 
 Please give me the most effective and efficient plan that only consists of the operators above for answering the above question. 
 The selected plan will be executed by you step by step to finally answer the original query correctly. 
 So please plan based on the information you already have to answer the query. 
 You do not have to use all operators and please make sure the plan is the one you think is accurate with the highest efficiency. 
 Please only output the operators separated by space without any other explanation.
"""

EXPLAIN_PLAN_PROMPT = """
Please explain your plan. Describe what you plan to do for each step (operator) in the plan.
"""

EXEC_OP_PROMPT = """
Please continue the plan execution step by step. 
The next operator is {}, which is to {}.
Please execute it and output the result.
"""

FINAL_ANSWER_PROMPT = """
Please now generate the answer to the question:
"{}"
"""

EXPLAIN_ANSWER_PROMPT = "Please explain your answer, such as the source of the information, or your reasoning process."

OP_EXPLANATION = {
    "Retrieve" : "Searches external databases, documents, or knowledge bases to find relevant information based on a query. Enhances the LLM's responses with up-to-date or specific information not contained within the model. ",
    "Rank" : "Orders the retrieved documents or information based on relevance to the query. Ensures the most relevant information is prioritized for use in the final response. ",
    "Summarize" : "Condenses longer pieces of text into shorter, more manageable summaries while retaining key information. Provides concise information that is easier to process and understand. ",
    "Generate" : "Produces coherent text based on the processed input and any retrieved information. Forms the primary response or continuation of the input text. ",
    "Refine" : "Iteratively improves or adjusts the generated text to better meet the requirements or improve coherence. Enhances the quality and accuracy of the response. ",
    "Classify" : "Assigns categories or labels to the input text based on its content. Helps in understanding the context, intent, or sentiment of the input. ",
    "Translate" : "Converts text from one language to another. Makes the information accessible to a wider audience. ",
    "Filter" : "Removes irrelevant or inappropriate information from the retrieved or generated text. Ensures the output is relevant and appropriate for the context. ",
    "Evaluate" : "Assesses the quality or relevance of the text generated or retrieved. Provides feedback for refining and improving the response. ",
    "Explain" : "Provides explanations or reasoning for a given response or decision made by the model. Enhances transparency and understanding of the model's outputs. ",
    # "Integrate" : "Combines information from multiple sources into a cohesive response. Ensures a comprehensive and well-rounded answer. ",
    # "Conceptualize" : "Extracts and identifies the core concept or noun corresponding to the given content. Simplifies complex information by pinpointing the main idea or subject, facilitating better understanding. ",
    # "Align" : "Adjusts the output to match the user's intent or preferences more closely. Ensures that the generated response aligns with the specific needs and preferences of the user. ",
    # "Store" : "Saves interactions or generated data for future reference or learning. Allows for the retention of useful information that can be referred back to or used to improve future interactions. ",
    "Extract" : "Identifies and pulls out specific pieces of information from text (e.g., named entities, dates, facts). Isolates crucial details to answer specific queries or for further processing. ",
    "Validate" : "Checks the accuracy and reliability of generated or retrieved information. Ensures that the information provided is correct and trustworthy. ",
    # "Combine" : "Merges information from multiple sources or different parts of a text to form a cohesive response. Creates a comprehensive and integrated answer from various pieces of information. ",
    # "Paraphrase" : "Rewrites text in different words while retaining the original meaning. Provides alternative expressions of the same information, which can aid understanding or avoid repetition. ",
    # "Reason" : "Applies logical inference to derive conclusions or solve problems based on given information. Enhances the response by adding logical consistency and deriving deeper insights. "

    "Reduction" : "Reduces the original problem into several sub-problems that are easier to solve."
}
