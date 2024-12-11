def comparison_prompt(old_content: str, new_content: str):
    """
    Function that returns a prompt which compares between the current version
    of a site and the last one that was retrieved by the service.

    Input

    old_content: the last version of the site
    new_content: the current version of the site

    Output

    A string that can be sent to the llm for comparison purposes.
    """
    return f"""
    Your task is to compare between two sites. 
    Evaluate if there is a significant difference between them following this instruction.
    # INSTRUCTION
    Check to see if there's any new information about the subject discussed.
    
    This is the last recorded site:
    {old_content}
    ------------------
    This is the current version of the site:
    {new_content}
    """
