def fill_OP_condition_ifUseLLM_for_cost_in_advance(query, BQ_list):
    prompt = f"""
    You are given a query and a list of basic questions. Each basic question is a template containing placeholders (e.g., [Condition], [Entity]).

    Your task is to:

    Break down the query into parts that can be matched with the basic questions.
    For each matching basic question, determine the appropriate inputs (replace placeholders in the question and the plan with values from the query).
    Identify whether semantic understanding is required for each match (e.g., if a term from the query is abstract or requires external knowledge to match a basic question template).
    Output the operator, the specific input parameters, and whether semantic understanding is required in JSON format.

    ## Input format:
    Query: A natural language question, e.g., "Among documents with over 500 views, group documents by sports."
    Basic Questions: A list of basic question templates, each having a "Question," an "IDQuestion," a "Plan," an "IDPlan," and a "Return."
    ## Example:
    Query: "Among documents with over 500 views, group documents by sports."

    Basic Questions:
    [
       {{
         "Question": "Documents with [Condition]",
         "IDQuestion": "Documents with [Condition1]",
         "Plan": [{{"Scan": []}}],
         "IDPlan": [{{"Operator": "Scan", "Parameter": ["[Condition1]"], "Followup Plan": []}}],
         "Return": "documents"
       }},
       {{
         "Question": "Group documents by [Entity]",
         "IDQuestion": "Group documents by [Entity1]",
         "Plan": [{{"GroupBy": []}}],
         "IDPlan": [{{"Operator": "GroupBy", "Parameter": ["[Entity1]"], "Followup Plan": []}}],
         "Return": "groups"
       }}
    ]

    ## Output format:
    For each basic question that matches a part of the query, output in the json format.

    Operator: The operation being performed (e.g., "Scan," "GroupBy").
    Condition: The condition of the operator that it needs to operate by. For example, the condition for Filter is the filtering condition.
    Requires Semantic Understanding: Indicate "Yes" if semantic understanding is needed, otherwise "No."

    ## Example output:
    [
      {{
        "Operator": "Scan",
        "Parameters": {{"Condition1": "over 500 views"}},
        "Requires Semantic Understanding": "No"
      }},
      {{
        "Operator": "GroupBy",
        "Parameters": {{"Entity1": "sports"}},
        "Requires Semantic Understanding": "Yes"
      }}
    ]

    Here is your input.

    Query: {query}
    Basic Questions: {BQ_list}

    Please provide the output strictly in the specified format.
    """
    return prompt





def fill_OP_condition_ifUseLLM_for_cost_for_op(query, op):
    prompt = f"""
    You are given a query and an operator. 

    Your task is to:

    Check if the operator requires filtering over the data and whether it needs semantic understanding.
    

    ## Input format:
    Query: A natural language question, e.g., "Among documents with over 500 views, group documents by sports."
    Operator: A json describing the operator, each having a "Question" denoting its use case, an "IDQuestion", a "Plan" an "IDPlan", and a "Return" denoting what it should return.
    
    
    ## Example 1:
    Query: "Among documents with over 500 views, group documents by sports."

    Operator:
       {{
         "Question": "Documents with [Condition]",
         "IDQuestion": "Documents with [Condition1]",
         "Plan": [{{"Scan": []}}],
         "IDPlan": [{{"Operator": "Scan", "Parameter": ["[Condition1]"], "Followup Plan": []}}],
         "Return": "documents"
       }}

    ## Example output:
      {{
        "Operator": "Scan",
        "Condition": "over 500 views",
        "Requires Semantic Understanding": "No"
      }}
      
      
      
      
    ## Example 2:
    Query: "What is the number of documents related to injury"

    Operator:
    {{
        "Question": "How many documents are [Condition]",
        "IDQuestion": "How many documents are [Condition1]",
        "Plan": [
            {{
                "Count": [
                    {{"Scan": []}}
                ]
            }}
        ],
        "IDPlan":[{{
                "Operator":"Count",
                "Parameter":["follow_0","Doc"],
                "Followup Plan":[
                    {{
                        "Operator":"Scan",
                        "Parameter":["[Condition1]"],
                        "Followup Plan" : []
                    }}
                ]
            }}
        ],
        "Return": "[Number]"
    }}

    ## Example output:
      {{
        "Operator": "Count",
        "Condition": "related to injury",
        "Requires Semantic Understanding": "Yes"
      }}
      
      
    ## Example 3:
    Query: "What is the number of documents explicitly containing keyword NBA"

    Operator:
    {{
        "Question": "How many documents are [Condition]",
        "IDQuestion": "How many documents are [Condition1]",
        "Plan": [
            {{
                "Count": [
                    {{"Scan": []}}
                ]
            }}
        ],
        "IDPlan":[{{
                "Operator":"Count",
                "Parameter":["follow_0","Doc"],
                "Followup Plan":[
                    {{
                        "Operator":"Scan",
                        "Parameter":["[Condition1]"],
                        "Followup Plan" : []
                    }}
                ]
            }}
        ],
        "Return": "[Number]"
    }}

    ## Example output:
      {{
        "Operator": "Count",
        "Condition": "explicitly containing keyword NBA",
        "Requires Semantic Understanding": "No"
      }}
    
    
    ## Example 4:
    Query: "Extract the number of views for the documents"

    Operator:
    {{
        "Question": "Extract the number of views for the documents",
        "IDQuestion": "Extract the number of views for the documents",
        "Plan": [
            {{
                "Extract": []
            }}
        ],
        "IDPlan":[
                {{
                    "Operator":"Extract",
                    "Parameter":[],
                    "Followup Plan" : []
                }}
        ],
        "Return": "List"
    }}

    ## Example output:
      {{
        "Operator": "Extract",
        "Condition": "None",
        "Requires Semantic Understanding": "No"
      }}
    

        
    
    
    Here is your input.

    Query: 
    {query}
    Operator: 
    {op}

    Please provide the output strictly in the specified format.
    """
    return prompt