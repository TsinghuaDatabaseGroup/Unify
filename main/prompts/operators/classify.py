def get_classify_prompt(condition, data):
    classify_prompt = f"""
    Task: Classify the input data based on the given condition.
    
    Examples:
    1. Data: {"text": "The weather is sunny."}, Condition: "weather"
       Classification: "sunny"
    
    2. Data: {"text": "The stock market is bullish."}, Condition: "stock market"
       Classification: "bullish"
    
    3. Data: {"text": "The patient is showing symptoms of flu."}, Condition: "medical"
       Classification: "flu"
    
    Input:
    Data: {data}
    Condition: {condition}
    
    Classification:
    """
    return classify_prompt