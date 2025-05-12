def check_prerequisite_prompt(original_question, parsed_question, bq):
    prompt = f"""
    ## Task:
    You are given a current original question, a current parsed question and a candidate basic question (BQ).
    The current parsed question is the semantically parsed result of the current original question.  
    Your goal is to determine if the prerequisites to conduct the BQ over the current original question and current parsed question are satisfied.

    ## Instructions:
    Please check if the prerequisites for BQ to be applied to the current original question and current parsed question are met. If the prerequisites are satisfied, return "true". Otherwise, return "false".


    ## Output:
    Return "true" if the prerequisites are satisfied, otherwise return "false".

    ## Examples:

        Example 1:
        Current Original Question: "For documents over 100 views, group them by sports, find the group with minimum total answers"
        Current Parsed Question: "For documents [Condition], group them by [Entity], find the group with minimum [Entity]"
        Candidate Basic Question: "group with smallest number of [Entity]"
        Output: false

        # Explanation of Example 1 (not in the output)
        The current question requires the documents to be filtered by [Condition] and grouped by [Entity] before we can find the group with the minimum [Entity]. So the answer is false.


        Example 2:

        Current Original Question: "Among documents over 100 views, group them by sports, which sports is most discussed?"
        Current Parsed Question: "Among documents [Condition], group them by [Entity], which [Entity] is most discussed?"
        Candidate Basic Question: "Documents that [Condition]"
        Output: true

        # Explanation of Example 2 (not in the output)
        Filtering the documents based on [Condition] does not require any other prerequisites. Therefore, the BQ can be applied to the current question, so the answer is true.        


        Example 3:

        Current Original Question: "Group documents with over 200 views by Sports,  which of those groups about ball game has the highest percentage related to injury?"
        Current Parsed Question: "Group documents with [Condition] by [Entity],  which of those groups [Condition] has the highest percentage related to [Entity]?"
        Candidate Basic Question: "Group that owns the highest percentage of [Condition]"
        Output: false

        # Explanation of Example 3 (not in the output)
        The current question requires the documents to be grouped by [Entity] before we can find the group with the highest percentage related to [Entity]. So the answer is false.
        
        
        
        Example 4:
        
        Current Original Question: "Count the number of documents that satisfy rlated to database and also satisfy related to AI."
        Current Parsed Question: "Count the number of documents that satisfy [Condition] and also satisfy [Condition]."
        Candidate Basic Question: "Count the number of documents that satisfy [Condition]"
        Output: false

        # Explanation of Example 4 (not in the output)
        The result of this basic question is a number, and it only solves one condition of the question, leaving the other condition not solved. So it should not use this basic question now. Two conditions have to be solved one first, so the answer is No. 



        Example 5:
        
        Current Original Question: "Count the number of documents that satisfy related to database and also satisfy related to AI."
        Current Parsed Question: "Count the number of documents that satisfy [Condition] and also satisfy [Condition]."
        Candidate Basic Question: "Documents satisfy [Condition]"
        Output: true
        
        # Explanation of Example 5 (not in the output)
        The basic question can be applied to the current question for filtering some documents. This does not rely on any prerequisites,  so the answer is true.



    Now, for the current input:

        Current Original Question: "{original_question}"
        Current Parsed Question: "{parsed_question}"
        Candidate Basic Question: "{bq['Question']}"

        Please output like above examples (do not explain).
    """
    return prompt