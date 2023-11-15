import requests
import json
import base64
import sys
import pandas as pd
import os
from IPython.display import display

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
org_teams_url = f"https://dev.azure.com/{ORG}/_apis/teams?api-version=7.1-preview.3"

try:
  org_teams_response = requests.get(org_teams_url, headers=headers)
except requests.exceptions.RequestException as e:
  print(f"An error occurred while getting the list of teams in the organization: {e}")
  sys.exit(2)

data = []

# Iterate over each team in the organization
for team in org_teams_response.json()['value']:
  # Initialize the JSON object to store the team membership info
  team_info = {
    'Team Name': team['name'],
    'Project Name': team['projectName'],
    'Team ID': team['id'],
    'Project ID': team['projectId']
  }

  # Get the members of the team
  team_members_url = f"https://dev.azure.com/{ORG}/_apis/projects/{team['projectId']}/teams/{team['id']}/members?api-version=7.1-preview.2"
  try:
    team_members_response = requests.get(team_members_url, headers=headers, timeout=10)
  except requests.exceptions.RequestException as e:
    print(f"An error occurred while getting the members of the team {team['name']}: {e}")
    continue
  
  for member in team_members_response.json()['value']:
    row = team_info.copy()
    # If the unique name contains vsts:/// then it is a group and not a user. Do a nested call to get all user memberships
    if 'vstfs:' in member['identity']['uniqueName']:
      group_membership_url = f"https://vsaex.dev.azure.com/{ORG}/_apis/GroupEntitlements/{member['identity']['id']}/members?api-version=7.1-preview.1"
      try:
        group_members_response = requests.get(group_membership_url, headers=headers, timeout=10)
      except requests.exceptions.RequestException as e:
        print(f"An error occurred while getting the members of the group {member['identity']['uniqueName']}: {e}")
        continue
      
      # For each of the group members, add them as a row to the dataframe
      for group_member in group_members_response.json()['members']:
        row.update({
          'Group Display Name': member['identity']['displayName'],
          'Group Unique Name': member['identity']['uniqueName'],
          'Group ID': member['identity']['id'],
          'User Display Name': group_member['user']['displayName'],
          'User Unique Name': group_member['user']['principalName'],
          'User Origin': group_member['user']['origin'],
          'User ID': group_member['user']['originId']
        })
    else:
      # If the unique name does not contain vsts:/// then it is a user. Add them as a row to the dataframe
      row.update({
        'User Origin': 'ado',
        'User Display Name': member['identity']['displayName'],
        'User Unique Name': member['identity']['uniqueName'],
        'User ID': member['identity']['id']
      })
    data.append(row)

df = pd.DataFrame(data)
df = df[['Project Name', 'Project ID', 'Team Name', 'Team ID', 'User Display Name', 'User Unique Name', 'User ID', 'User Origin', 'Group Display Name', 'Group Unique Name', 'Group ID']]
# display(df.to_markdown()) # To debug dataframe output locally

print(df)
