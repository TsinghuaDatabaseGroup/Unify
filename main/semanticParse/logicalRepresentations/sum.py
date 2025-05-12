SUM_LR = {
        "Question": "sum length of documents",
        "IDQuestion": "sum length of documents",
        "Plan": [
            {
                "Sum": [
                    {
                        "Compute": []
                    }
                ]
            }
        ],
        "IDPlan":[
                {
                    "Operator":"Sum",
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

