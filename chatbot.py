from knowledge_base import search_knowledge_base
from extract_ticket_fields import extract_ticket_fields
from jira_helper import create_jira_ticket

# State to keep track of failed attempts and ticket steps
conversation_state = {
    "failure_count": 0,
    "awaiting_ticket_confirmation": False,
    "awaiting_fields": False,
    "pending_fields": {}
}

def chatbot_response(user_query):
    global conversation_state

    # Greeting message when the chatbot is initialized
    if conversation_state["failure_count"] == 0 and not conversation_state["awaiting_ticket_confirmation"]:
        return "Welcome to the support assistant! How can I help you today?"

    # If waiting for confirmation to raise ticket
    if conversation_state["awaiting_ticket_confirmation"]:
        if "yes" in user_query.lower():
            conversation_state["awaiting_ticket_confirmation"] = False
            conversation_state["awaiting_fields"] = True
            return (
                "Almost there! Please provide:\n"
                "- Brief **description** of the issue\n"
                "- Priority (**Low**, **Medium**, or **High**)\n"
                "- Issue Type (e.g., **Bug**, **Task**, **Story**) "
            )
        else:
            conversation_state["failure_count"] = 0
            conversation_state["awaiting_ticket_confirmation"] = False
            return "Alright, feel free to ask me anything else!"

    # If waiting for ticket fields
    if conversation_state["awaiting_fields"]:
        fields = extract_ticket_fields(user_query)
        conversation_state["pending_fields"].update(fields)

        missing = []
        if "description" not in conversation_state["pending_fields"]:
            missing.append("description")
        if "priority" not in conversation_state["pending_fields"]:
            missing.append("priority")
        if "issue_type" not in conversation_state["pending_fields"]:
            missing.append("issue type")

        if missing:
            return f"Please provide the missing fields: {', '.join(missing)}"
        else:
            # Create the Jira ticket
            try:
                issue = create_jira_ticket(conversation_state["pending_fields"])
                issue_key = issue.key
                # Reset state
                conversation_state = {
                    "failure_count": 0,
                    "awaiting_ticket_confirmation": False,
                    "awaiting_fields": False,
                    "pending_fields": {}
                }
                return f"✅ Your Jira ticket has been created successfully! Issue ID: **{issue_key}**"
            except Exception as e:
                print("❌ Jira Error:", e)
                conversation_state = {
                    "failure_count": 0,
                    "awaiting_ticket_confirmation": False,
                    "awaiting_fields": False,
                    "pending_fields": {}
                }
                return "❌ Sorry, failed to create Jira ticket. Please try again later."

    # Normal KB search flow
    answer = search_knowledge_base(user_query)
    if answer:
        conversation_state["failure_count"] = 0
        return answer
    else:
        conversation_state["failure_count"] += 1
        if conversation_state["failure_count"] >= 2:
            conversation_state["awaiting_ticket_confirmation"] = True
            return "🙁 I couldn't find an answer. Would you like me to raise a Jira ticket for this issue?"
        return "🤔 I couldn't find an answer. Let me try one more time..."
