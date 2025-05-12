MIN_LR = {
        "Question": "minimum length of documents",
        "IDQuestion": "minimum length of documents",
        "Plan": [
            {
                "Min": [
                    {
                        "Compute": []
                    }
                ]
            }
        ],
        "IDPlan":[
                {
                    "Operator":"Min",
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

