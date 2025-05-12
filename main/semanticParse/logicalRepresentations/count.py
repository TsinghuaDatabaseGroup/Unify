COUNT_LR = {
    "Question": "How many documents are [Condition]",
    "IDQuestion": "How many documents are [Condition1]",
    "Plan": [
        {
            "Count": [
                {"Scan": []}
            ]
        }
    ],
    "IDPlan":[{
            "Operator":"Count",
            "Parameter":["follow_0","Doc","[Condition1]"],
            "Followup Plan":[
                {
                    "Operator":"Scan",
                    "Parameter":["[Condition1]"],
                    "Followup Plan" : []
                }
            ]
        }
    ],
    "Return": "[Number]"
}



COUNT_LR_2 = {
    "Question": "Count the number of documents that satisfy [Condition]",
    "IDQuestion": "Count the number of documents that satisfy [Condition1]",
    "Plan": [
        {
            "Count": [
                {"Scan": []}
            ]
        }
    ],
    "IDPlan":[{
            "Operator":"Count",
            "Parameter":["follow_0","Doc","[Condition1]"],
            "Followup Plan":[
                {
                    "Operator":"Scan",
                    "Parameter":["[Condition1]"],
                    "Followup Plan" : []
                }
            ]
        }
    ],
    "Return": "Dict" 
}

COUNT_LR_3 = {
    "Question": "Count the [Number] of documents",
    "IDQuestion": "Count the [Number1] of documents",
    "Plan": [
        {
            "Count": [
        
            ]
        }
    ],
    "IDPlan":[{
            "Operator":"Count",
            "Parameter":["Doc"],
            "Followup Plan":[]
        }
    ],
    "Return": "[Number]" 
}