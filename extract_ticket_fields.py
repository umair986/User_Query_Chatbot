import re

def extract_ticket_fields(user_input):
    user_input_lower = user_input.lower()
    fields = {}

    # Priority
    if "low" in user_input_lower:
        fields["priority"] = "Low"
    elif "medium" in user_input_lower:
        fields["priority"] = "Medium"
    elif "high" in user_input_lower:
        fields["priority"] = "High"

    # Issue Type
    if "bug" in user_input_lower:
        fields["issue_type"] = "Bug"
    elif "task" in user_input_lower:
        fields["issue_type"] = "Task"
    elif "story" in user_input_lower:
        fields["issue_type"] = "Story"

    # Description
    match = re.search(r"(error|issue|problem|fail(ed)?|bug|unable to|can't|cannot)[^\.!\n]{10,}", user_input_lower)
    if match:
        fields["description"] = match.group(0).capitalize()
    elif len(user_input) < 200:
        fields["description"] = user_input.strip().capitalize()

    return fields
