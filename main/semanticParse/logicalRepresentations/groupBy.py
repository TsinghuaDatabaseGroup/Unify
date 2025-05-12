GROUPBY_LR = {
    "Question": "Group documents by [Entity]",
    "IDQuestion": "Group documents by [Entity1]",
    "Plan": [
        {
            "GroupBy": []
        }
    ],
    "IDPlan": [
        {
            "Operator": "GroupBy",
            "Parameter": ["[Entity1]"],
            "Followup Plan": []
        }
    ],
    "Return":  "dictionary"                 #"{[Entity1_value1]: documents, [Entity1_value2]: documents, ...}"
}


GROUPBY_LR_2 = {
        "Question": "Group documents by [Entity] [Condition]",
        "IDQuestion": "Group documents by [Entity1] [Condition1]",
        "Plan": [
            {
                "Filter": [
                    {"groupBy" : []}
                ]
            }
        ],
        "IDPlan":[
                {
                    "Operator":"Filter",
                    "Parameter":["follow_0", "[Condition1]"],
                    "Followup Plan" : [
                        {
                            "Operator":"groupBy",
                            "Parameter":["follow_0", "[Entity1]"],
                            "Followup Plan" : []
                        }
                    ]
                }
        ],
        "Return": "groups"
    }