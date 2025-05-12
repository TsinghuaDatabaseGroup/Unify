FILTER_LR = {
        "Question": "Documents related to [Entity]",
        "IDQuestion": "Documents related to [Entity1]",
        "Plan": [
            {
                "Scan": []
            }
        ],
        "IDPlan":[
                {
                    "Operator":"Scan",
                    "Parameter":["related to [Entity1]"],
                    "Followup Plan" : []
                }
        ],
        "Return": "documents"
}

FILTER_LR_2 =  {
        "Question": "Documents with [Condition]",
        "IDQuestion": "Documents with [Condition1]",
        "Plan": [
            {
                "Scan": []
            }
        ],
        "IDPlan":[
                {
                    "Operator":"Scan",
                    "Parameter":["[Condition1]"],
                    "Followup Plan" : []
                }
        ],
        "Return": "documents"
    }

FILTER_LR_3 =  {
        "Question": "Groups that [Condition]",
        "IDQuestion": "Groups that [Condition1]",
        "Plan": [
            {
                "Scan": []
            }
        ],
        "IDPlan":[
                {
                    "Operator":"Scan",
                    "Parameter":["[Condition1]"],
                    "Followup Plan" : []
                }
        ],
        "Return": "groups"
    }
