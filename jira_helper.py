import os
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

jira = JIRA(server=JIRA_URL, basic_auth=(JIRA_USER, JIRA_API_TOKEN))

def create_jira_ticket(project_key, summary, priority, issue_type):
    issue_dict = {
        "project": {"key": project_key},
        "summary": summary,
        "description": summary,
        "issuetype": {"name": issue_type},
        "priority": {"name": priority},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    return new_issue.key
