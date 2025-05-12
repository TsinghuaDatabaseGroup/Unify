
def get_scan_prompt(condition, content):
    """
        Prompt for the scan operator.
        :param condition: The condition to be satisfied by the documents.
        :param content: The content of the document.
    """

    PROMPT = f"""
                You are given a document and a condition. Your task is to determine if the document satisfies the condition. Please answer 'Yes' if the document satisfies the condition, and 'No' otherwise. 
                Here are some examples.


                # Example 1
                ## Condition "talks about computer science"
                ## Document: "Database is an important area in computer science research"
                ## Output: "Yes"


                # Example 2
                ## Condition "related to computer science"
                ## Document: "Basketball is a team sport in which two teams, most commonly of five players each, opposing one another on a rectangular court, compete with the primary objective of shooting a basketball (approximately 9.4 inches (24 cm) in diameter) through the defender's hoop (a basket 18 inches (46 cm) in diameter mounted 10 feet (3.048 m) high to a backboard at each end of the court), while preventing the opposing team from shooting through their own hoop."
                ## Output: "No"


                # Example 3
                ## Condition "about swimming"
                ## Document: "Breaststroke is a swimming style in which the swimmer is on their chest and the torso does not rotate. It is the most popular recreational style due to the swimmer's head being out of the water a large portion of the time, and that it can be swum comfortably at slow speeds. "
                ## Output: "Yes"

                Now please solve the following query like above examples. 

                ## Condition: "{condition}"
                ## Document: "{content}"

                Please answer 'Yes' if the document satisfies the condition, and 'No' otherwise.
        """
    return PROMPT


def get_check_if_semantic_prompt(condition):
    """
        Prompt for the checking if the condition needs to use semantic (LLM).
        :param condition: The condition to be checked.
    """
    PROMPT = f"""
                You are given a condition. Your task is to determine if the condition requires semantic understanding to evaluate. 
                Please answer 'Yes' if the condition requires semantic understanding, and 'No' otherwise. 
                Here are some examples.


                # Example 1
                ## Condition: "talks about computer science"
                ## Output: "Yes"


                # Example 2
                ## Condition: "related to computer science"
                ## Output: "Yes"


                # Example 3
                ## Condition: "explicitly containint swimming"
                ## Output: "No"
                
                
                # Example 4
                ## Condition: "contains the keyword running"
                ## Output: "No"

                # Example 5
                ## Condition: "longer than 100 words"
                ## Output: "No"

                # Example 6
                ## Condition: "with a length greater than 100"
                ## Output: "No"

                # Example 7
                ## Condition: "contains the keyword running"
                ## Output: "No"


                Now please solve the following query like above examples. 

                ## Condition: "{condition}"

                Please answer 'Yes' if the condition requires semantic understanding, and 'No' otherwise.
        """

    return PROMPT



def get_keyword_prompt(condition):
    # get the prompt to get the target keyword requirement in the condition
    PROMPT = f"""
                You are given a condition. Your task is to extract the target keyword from the condition. 
                The target keyword is the most important keyword that is necessary to evaluate the condition. 
                Please provide the target keyword based on the following examples.


                # Example 1
                ## Condition "explicitly contains computer science"
                ## Target Keyword: "computer science"


                # Example 2
                ## Condition "contains the keyword swim"
                ## Target Keyword: "swim"


                # Example 3
                ## Condition "about basketball"
                ## Target Keyword: "basketball"


                Now please solve the following query like above examples. 

                ## Condition: "{condition}"

                Please provide the target keyword without any other output.
        """

    return PROMPT