MEDIAN_LR = {
        "Question": "median length of documents",
        "IDQuestion": "median length of documents",
        "Plan": [
            {
                "Median": [
                    {
                        "Compute": []
                    }
                ]
            }
        ],
        "IDPlan":[
                {
                    "Operator":"Median",
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

