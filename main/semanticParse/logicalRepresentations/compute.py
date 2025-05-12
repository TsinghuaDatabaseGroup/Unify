COMPUTE_LR = {
        "Question": "percentage of [Condition]",
        "IDQuestion": "percentage of [Condition1]",
        "Plan": [
            {
                "groupBy": []
            }
        ],
        "IDPlan":[
                {
                    "Operator":"groupBy",
                    "Parameter":["follow_0", "[Entity1]"],
                    "Followup Plan" : []
                }
        ],
        "Return": "number"
    }


COMPUTE_LR_2 = {
        "Question": "Group that owns the highest percentage of [Condition]",
        "IDQuestion": "Group that owns the highest percentage of [Condition1]",
        "Plan": [
            {
                "groupBy": []
            }
        ],
        "IDPlan":[
                {
                    "Operator":"groupBy",
                    "Parameter":["follow_0", "[Entity1]"],
                    "Followup Plan" : []
                }
        ],
        "Return": "[Entity]"
    }

COMPUTE_RATIO_LR = {
    "Question": "Compute the ratio of [Condition] to [Condition] for each [Entity] in grouped documents.",
    "IDQuestion": "Compute the ratio of [Condition1] to [Condition2] for each [Entity1] in grouped documents.",
    "Plan": [
        {
            "Ratio": []
        }
    ],
    "IDPlan": [
        {
            "Operator": "Ratio",
            "Parameter": ["GroupBy", "[Condition1]", "[Condition2]"],  # follow_0: Count of ConditionA, follow_1: Count of ConditionB
            "Followup Plan": []
        }
    ],
    "Return": "Dict"
}