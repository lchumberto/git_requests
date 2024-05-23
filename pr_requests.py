import os
import requests
from datetime import datetime, timedelta


def get_pull_requests(repo_owner, repo_name, one_week_ago):
    # Construct the GitHub API URL for fetching pull requests
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls'
    
    # Set up the request headers
    headers = {
        'Accept': 'application/vnd.github.v3+json'  
    }
    
    # Set up the request parameters to filter pull requests
    params = {
        'state': 'all',  
        'sort': 'updated',  
        'direction': 'desc',  
        'since': one_week_ago  
    }
    
    # Make the request to the GitHub API
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Return the list of pull requests as JSON
        return response.json()
    else:
        # Raise an exception if the request failed
        raise Exception(f'Failed to retrieve pull requests: {response.text}')

def generate_summary(repo_owner, repo_name, pull_requests, one_week_ago):
    # Initialize lists to categorize pull requests
    opened = []
    in_progress = []
    closed = []
    
    # Loop through each pull request to classify it and check its timestamp
    for pr in pull_requests:
        pr_created_at = datetime.strptime(pr['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        pr_updated_at = datetime.strptime(pr['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
        pr_closed_at = pr['closed_at'] and datetime.strptime(pr['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
        
        if pr['state'] == 'open' and pr_created_at >= one_week_ago:
            opened.append(pr)
        elif pr['state'] == 'open' and pr_updated_at >= one_week_ago:
            in_progress.append(pr)
        elif pr['state'] == 'closed' and pr_closed_at and pr_closed_at >= one_week_ago:
            closed.append(pr)
    
    # Build the summary string
    summary = f"Summary of Pull Requests for {repo_owner}/{repo_name}:\n"
    summary += f"From: {one_week_ago.strftime('%Y-%m-%d %H:%M:%S')} until today {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary += f"Total Opened: {len(opened)}\n"
    summary += "Titles of Open Pull Requests:\n"
    for pr in opened:
        summary += f"- {pr['title']} (Created at: {pr['created_at']})\n"
    summary += "\n"
    summary += f"Total In Progress: {len(in_progress)}\n"
    summary += "Titles of In Progress Pull Requests:\n"
    for pr in in_progress:
        summary += f"- {pr['title']} (Updated at: {pr['updated_at']})\n"
    summary += "\n"
    summary += f"Total Closed: {len(closed)}\n"
    summary += "Titles of Closed Pull Requests:\n"
    for pr in closed:
        summary += f"- {pr['title']} (Closed at: {pr['closed_at']})\n"
    
    return summary

def main():
    # Retrieve configuration from environment variables
    repo_owner = os.getenv('REPO_OWNER', 'octocat')
    repo_name = os.getenv('REPO_NAME', 'Hello-World')
    
    # Calculate the datetime for one week ago from now
    one_week_ago = datetime.now() - timedelta(days=7)
    one_week_ago_iso = one_week_ago.isoformat()

    # Retrieve pull requests from the GitHub API
    pull_requests = get_pull_requests(repo_owner, repo_name, one_week_ago_iso)
    
    # Generate the summary of pull requests
    summary = generate_summary(repo_owner, repo_name, pull_requests, one_week_ago)
    
    # Email details
    email_from = "your-email@example.com"
    email_to = "manager@example.com"
    email_subject = f"Weekly Pull Request Summary"
    email_body = summary
    
    # Print the email details to the console
    print(f"From: {email_from}")
    print(f"To: {email_to}")
    print(f"Subject: {email_subject}")
    print()
    print(email_body)

main()