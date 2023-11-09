import requests
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

PAT = os.getenv('PAT')
ORG = os.getenv('ORG')

# Construct the HTTP Auth Header for ADO
b64PAT=base64.urlsafe_b64encode(f"`:{PAT}".encode('UTF-8')).decode('utf-8')
headers = {
    'Authorization': 'Basic ' + b64PAT
}

# Retrieve the list of teams in the organization
# GET https://dev.azure.com/{organization}/_apis/teams?api-version=7.1-preview.3
try:
  org_teams_url = f"https://dev.azure.com/{ORG}/_apis/teams?api-version=7.1-preview.3"
  org_teams_response = requests.get(org_teams_url, headers=headers)
  teams_info = []

  # Iterate over each team in the organization
  for team in org_teams_response.json()['value']:
    # Initialize the JSON object to store the team membership info
    team_info = {
      'teamName': team['name'],
      'projectName': team['projectName'],
      'teamID': team['id'],
      'projectID': team['projectId'],
      'members': []
    }
    
    # Get the members of the team
    # GET https://dev.azure.com/{organization}/_apis/projects/{projectId}/teams/{teamId}/members?api-version=7.1-preview.2
    team_members_url = f"https://dev.azure.com/{ORG}/_apis/projects/{team['projectId']}/teams/{team['id']}/members?api-version=7.1-preview.2"
    team_members_response = requests.get(team_members_url, headers=headers, timeout=10)

    try:
      for member in team_members_response.json()['value']:
        member_info = {
          'displayName': member['identity']['displayName'],
          'uniqueName': member['identity']['uniqueName'] 
        }
        team_info['members'].append(member_info)
    except requests.exceptions.RequestException as e:
      print(f"An error occurred while getting the members of the team {team['name']}: {e}")
      continue
    teams_info.append(team_info)
  
  teams_info_json = json.dumps(teams_info)
  print(json.dumps(teams_info, indent=2))    
except requests.exceptions.RequestException as e:
  print(f"An error occurred while getting the list of teams in the organization: {e}")
  exit
