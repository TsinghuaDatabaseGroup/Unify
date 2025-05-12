PERCENTILE_LR = {
        "Question": "[Number]-th percentile of document lengths",
        "IDQuestion": "[Number1]-th percentile of document lengths",
        "Plan": [
            {
                "Percentile": [
                    {
                        "Compute": []
                    }
                ]
            }
        ],
        "IDPlan":[
                {
                    "Operator":"Percentile",
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
