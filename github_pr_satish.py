"""
Author: AJ Sathishkumar
Email: ajsatix@gmail.com

This script retrieves the summary of opened, closed, and merged pull requests
in the last week for the Kubernetes repository on GitHub and generates an email-like report.
"""


import requests
import datetime

# GitHub API endpoint for pull requests
api_url = "https://api.github.com/repos/kubernetes/kubernetes/pulls"

# Parameters for the API request
params = {
    "state": "all",  # all pull requests (opened, closed, and merged)
    "sort": "created",  # sort by creation date
    "direction": "desc",  # sort in descending order
}

# Retrieve the pull requests from the last week
last_week = datetime.datetime.now() - datetime.timedelta(days=7)
params["since"] = last_week.isoformat()

# Send GET request to GitHub API
response = requests.get(api_url, params=params)

# Check the response status
if response.status_code == 200:
    pull_requests = response.json()
    
    # Variables for storing PR summary
    opened_prs = []
    closed_prs = []
    merged_prs = []

    # Process each pull request
    for pr in pull_requests:
        pr_number = pr["number"]
        pr_title = pr["title"]
        pr_state = pr["state"]
        
        # Categorize the pull request based on its state
        if pr_state == "open":
            opened_prs.append((pr_number, pr_title))
        elif pr_state == "closed":
            if pr.get("merged", False):
                merged_prs.append((pr_number, pr_title))
            else:
                closed_prs.append((pr_number, pr_title))

    # Generate the email summary report
    report = "From: AJ Sathishkumar <ajsatix@gmail.com>\n"
    report += "To: Scrum master - xyz@abc.com\n"
    report += "Subject: Summary of PRs for last 7 days\n"
    report += "Content-Type: text/plain; charset=utf-8\n\n"

    report += "Pull Request Summary for the Kubernetes Repository\n\n"
    report += "Last Week's Pull Requests:\n\n"
    
    report += f"Opened Pull Requests ({len(opened_prs)}):\n"
    for pr_number, pr_title in opened_prs:
        report += f"- #{pr_number}: {pr_title}\n"
    report += "\n"
    
    report += f"Closed Pull Requests ({len(closed_prs)}):\n"
    for pr_number, pr_title in closed_prs:
        report += f"- #{pr_number}: {pr_title}\n"
    report += "\n"
    
    report += f"Merged Pull Requests ({len(merged_prs)}):\n"
    for pr_number, pr_title in merged_prs:
        report += f"- #{pr_number}: {pr_title}\n"
    
    # Print or send the report via email
    print(report)

else:
    print("Failed to retrieve pull requests. Status code:", response.status_code)
