def get_op_literals(condition):
    # get the prompt to get the target keyword requirement in the condition
    PROMPT = f"""
                You are given a condition. Your task is to extract the operator and literal from the condition, separated by ,. 
                The operator should be chosen from >, <, =.
                

                # Example 1
                ## Condition: "greater than 5"
                ## Output: >, 5

                # Example 2
                ## Condition: "larger than 13"
                ## Output: >, 13


                # Example 3
                ## Condition: "less than 50"
                ## Output: <, 50
                
                
                # Example 4
                ## Condition: "smaller than 9"
                ## Output: <, 9
                
                # Example 5
                ## Condition: "equals to 14"
                ## Output: =, 14

                # Example 6
                ## Condition: "greater than 10,000"
                ## Output: =, 10000

                Please note that there should be no commas in the middle of the returned numbers
                and the output should be in the format of "operator, literal" without any other text.
                
                Now please solve the following query like above examples. 

                ## Condition: "{condition}"

                Please provide the output without any other output.
        """

    return PROMPT


def get_attribute_prompt(condition, text):
    PROMPT = f"""
                You are given a condition and a text paragraph. Your task is to extract the attribute described in the condition from the text. 

                # Example 1
                ## Condition: "sports"
                ## Text: "Michael Fred Phelps II OLY (born June 30, 1985) is an American former competitive swimmer. He is the most successful and most decorated Olympian of all time with a total of 28 medals. Phelps also holds the all-time records for Olympic gold medals"
                ## Output: swimming

                # Example 2
                ## Condition: "ML model"
                ## Text: "A decision tree is a decision support recursive partitioning structure that uses a tree-like model of decisions and their possible consequences, including chance event outcomes, resource costs, and utility. It is one way to display an algorithm that only contains conditional control statements."
                ## Output: decision tree
            
            
                # Example 3
                ## Condition: "role"
                ## Text: "Sir Christopher Edward Nolan (born 30 July 1970) is a British and American filmmaker. Known for his Hollywood blockbusters with complex storytelling, he is considered a leading filmmaker of the 21st century"
                ## Output: film maker
            


                Now please solve the following query like above examples. 

                ## Condition: "{condition}"
                ## Text: "{text}"

                Please provide the output without any other output.
        """

    return PROMPT