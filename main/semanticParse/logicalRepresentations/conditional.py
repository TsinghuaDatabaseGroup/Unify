CONDITIONAL_LR = {
    "Question": "Return whether [Number] exceeds [Number].",
    "IDQuestion": "Return whether [Number1] exceeds [Number2].",
    "Plan": [
        {
            "Conditional": []
        }
    ],
    "IDPlan": [
        {
            "Operator": "Conditional",
            "Parameter": ["Count", ">", "[Number2]"],
            "Followup Plan": []
        }
    ],
    "Return": "Yes/No"
}

CONDITIONAL_LR_2 = {
    "Question": "Return whether [Number] is less than [Number].",
    "IDQuestion": "Return whether [Number1] is less than [Number2].",
    "Plan": [
        {
            "Conditional": []
        }
    ],
    "IDPlan": [
        {
            "Operator": "Conditional",
            "Parameter": ["Count", "<", "[Number2]"],
            "Followup Plan": []
        }
    ],
    "Return": "Yes/No"
}

CONDITIONAL_LR_3 = {
    "Question": "Is the count of documents less than [Number].",
    "IDQuestion": "Is the count of documents less than [Number1].",
    "Plan": [
        {
            "Conditional": []
        }
    ],
    "IDPlan": [
        {
            "Operator": "Conditional",
            "Parameter": ["Count", "<", "[Number1]"],
            "Followup Plan": []
        }
    ],
    "Return": "Yes/No"
}

CONDITIONAL_LR_4 = {
    "Question": "Is the count of documents greater than [Number].",
    "IDQuestion": "Is the count of documents greater than [Number1].",
    "Plan": [
        {
            "Conditional": []
        }
    ],
    "IDPlan": [
        {
            "Operator": "Conditional",
            "Parameter": ["Count", ">", "[Number1]"],
            "Followup Plan": []
        }
    ],
    "Return": "Yes/No"
}