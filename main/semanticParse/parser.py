import re
import json
from prompts import get_semantic_parse_prompt

def semantic_parse(question, client, chatModel):
    prompt = get_semantic_parse_prompt(question)
    # Set up the messages for the LLM
    past_messages = [{"role": "user", "content": prompt}]
    # Call the LLM
    response = chatModel.create_completion(client, messages = past_messages)

    # Parse the response as JSON
    try:
        parsed_output = json.loads(response)
        # if documents or document is in parsed_output["Entities"], remove it
        if "documents" in parsed_output["Entities"]:
            parsed_output["Entities"].remove("documents")
        if "document" in parsed_output["Entities"]:
            parsed_output["Entities"].remove("document")


    except json.JSONDecodeError:
        print("Failed to parse LLM response as JSON.")
        parsed_output = None

    return parsed_output


def semantic_parse_without_client(question, client, chatModel):
    prompt = get_semantic_parse_prompt(question)
    message = [{"role": "user", "content": prompt}]

    response = chatModel.create_completion(client, max_tokens = 4000, messages = message)

    # Parse the response as JSON
    try:
        parsed_output = json.loads(response)
        # if documents or document is in parsed_output["Entities"], remove it
        if "documents" in parsed_output["Entities"]:
            parsed_output["Entities"].remove("documents")
        if "document" in parsed_output["Entities"]:
            parsed_output["Entities"].remove("document")


    except json.JSONDecodeError:
        print("Failed to parse LLM response as JSON.")
        parsed_output = None

    return parsed_output

def replace_parsed_elements_with_identifiers(question, parsed_result):
    """
    Replace the parsed elements in the question with their respective identifiers.
    """
    if not parsed_result:
        return question  # In case parsing failed, return the original question

    # Replacements for different categories
    replacements = [
        ("Entities", "[Entity]"),
        ("Conditions", "[Condition]"),
    ]
    # Replace the parsed elements in the question with their identifiers
    transformed_question = question
    for category, identifier in replacements:
        if category in parsed_result:
            for element in parsed_result[category]:
                # Escape special regex characters in the entity
                escaped_element = re.escape(element)
                # Replace the element in the question, ignoring case
                transformed_question = re.sub(rf"\b{escaped_element}\b", identifier, transformed_question,
                                                flags=re.IGNORECASE)

    return transformed_question


# Example usage
if __name__ == "__main__":
    question = "Which type of sport is most discussed between sports that require a field and sports that do not require a specific field?"