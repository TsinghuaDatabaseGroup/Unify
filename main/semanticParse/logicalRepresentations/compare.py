COMPARE_LR = {
    "Question": "Which is larger between [Entity] with [Number] and [Entity] with [Number]?",
    "IDQuestion": "Which is larger between [Entity1] with [Number1] and [Entity2] with [Number2]?",
    "Plan": [
        {
            "Compare": []
        }
    ],
    "IDPlan" :[{
        "Operator" :"Compare",
        "Parameter" :["max", "Count", "[Entity1]", "[Entity2]"],  # cmpTarget, Avalue, Bvalue, A, B
        "Followup Plan" :[]}
    ],

    "Return" : "[Entity]"
}

COMPARE_LR_2 = {
    "Question": "Which is smaller between [Entity] with [Number] and [Entity] with [Number]?",
    "IDQuestion": "Which is smaller between [Entity1] with [Number1] and [Entity2] with [Number2]?",
    "Plan": [
        {
            "Compare": []
        }
    ],
    "IDPlan" :[{
        "Operator" :"Compare",
        "Parameter" :["min", "Count", "[Entity1]", "[Entity2]"],  # cmpTarget, Avalue, Bvalue, A, B
        "Followup Plan" :[]}
    ],

    "Return" : "[Entity]"
}

COMPARE_MULTIPLE_LR = {
    "Question": "Which [Entity] has the highest ratio?",
    "IDQuestion": "Which [Entity1] has the highest ratio?",
    "Plan": [
        {
            "Compare": []
        }
    ],
    "IDPlan": [
        {
            "Operator": "Compare",
            "Parameter": ["max", "Ratio"],
            "Followup Plan": []
        }
    ],
    "Return": "[Entity]"
}
