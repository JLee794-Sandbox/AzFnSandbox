import requests
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

PAT = os.getenv('PAT')
ORG = os.getenv('ORG')

b64PAT=base64.urlsafe_b64encode(f"`:{PAT}".encode('UTF-8')).decode('utf-8')

# GET https://dev.azure.com/{organization}/_apis/teams?api-version=7.1-preview.3

org_teams_url = f"https://dev.azure.com/{ORG}/_apis/teams?api-version=7.1-preview.3"
headers = {
    'Authorization': 'Basic ' + b64PAT
}
org_teams_response = requests.get(org_teams_url, headers=headers)
teams_info = []

if org_teams_response:
  # print(f"Response Code: {org_teams_response.status_code}")
  # print(f"Response Content: {org_teams_response.content}")

  # Iterate over each item in the response and print the name of the team
  for team in org_teams_response.json()['value']:
    team_info = {
      'teamName': team['name'],
      'projectName': team['projectName'],
      'teamID': team['id'],
      'projectID': team['projectId'],
      'members': []
    }
    # print(f"Team Name: {team['name']}\n\t| ID: {team['id']}\n\t| Project Name: {team['projectName']}\n\t| Project ID: {team['projectId']}")
    
    # Get the members of the team
    # GET https://dev.azure.com/{organization}/_apis/projects/{projectId}/teams/{teamId}/members?api-version=7.1-preview.2
    team_members_url = f"https://dev.azure.com/{ORG}/_apis/projects/{team['projectId']}/teams/{team['id']}/members?api-version=7.1-preview.2"
    team_members_response = requests.get(team_members_url, headers=headers, timeout=10)

    if team_members_response:
      for member in team_members_response.json()['value']:
        member_info = {
          'displayName': member['identity']['displayName'],
          'uniqueName': member['identity']['uniqueName'] 
        }
        team_info['members'].append(member_info)

    teams_info.append(team_info)

teams_info_json = json.dumps(teams_info)
# print(teams_info_json)

print(json.dumps(teams_info, indent=2))