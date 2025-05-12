MAX_LR = {
        "Question": "max length of documents",
        "IDQuestion": "max length of documents",
        "Plan": [
            {
                "Max": [
                    {
                        "Compute": []
                    }
                ]
            }
        ],
        "IDPlan":[
                {
                    "Operator":"Max",
                    "Parameter":["follow_0"],
                    "Followup Plan" : [
                        {
                            "Operator":"Compute", 
                            "Parameter": [],
                            "Followup Plan" : []
                        }
                    ]
                }
        ],
        "Return": "Number"
    }

