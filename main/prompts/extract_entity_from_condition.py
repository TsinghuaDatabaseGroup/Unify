def extract_entity_prompt(condition):
    prompt = f"""Please extract the entities in the conditions input.


            ### Example 1:
            Condition: "related to boxing"
            Output: {{
              "Entities": "boxing"
            }}

            ### Example 2:
            Condition: "involving movings"
            Output: {{
              "Entities": "movies"
            }}


            Now, please process the following condition like above examples. 

            Condition: "{condition}"

            Provide the output in JSON format as:
            {{
              "Entities": ...
            }}

            Please do not output anything except the parsed JSON.
            In addition, "documents" do not need to be parsed as "Entities".
        """
    return prompt