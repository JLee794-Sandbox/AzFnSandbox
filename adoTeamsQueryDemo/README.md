# Project Title

This project is a Python script that retrieves the list of teams in an Azure DevOps organization and their members.

**NOTE: This is not production-grade by any means, use at your own risk.**

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. You also need the following Python packages:

- `requests`
- `json`
- `base64`
- `sys`
- `pandas`
- `os`
- `dotenv`

You can install these packages using pip:

```bash
pip install requests json base64 sys pandas os python-dotenv

# Or, use the requirements.txt file
pip install -r requirements.txt
```

### Installing

Clone the repository to your local machine:

```bash
git clone https://github.com/JLee794-Sandbox/AzFnSandbox.git
```

Navigate to the adoTeamsQuery project directory:

```bash
cd AzFnSandbox # Navigate into the project directory
cd adoTeamsQuery # Navigate to the adoTeamsQuery Python script directory
```

### Usage

#### Run within PowerBI

Since within PowerBI you cannot use .env file, follow the commented instructions in the main.py file to set your PAT and ORG variables. Then, you can simply copy and paste the script into the PowerBI Python Data source and execute.

```python
import requests
import json
import base64
import sys
import pandas as pd
import os
# Comment out the below lines until ---- if you are running this in PowerBI
from dotenv import load_dotenv
load_dotenv()
# ----- Comment to here

# Update the below variables with your ADO organization name and PAT for PowerBI, as you will not be able to use the .env file
PAT = os.getenv('PAT') # For PowerBI, PAT = 'YOUR_PAT'
ORG = os.getenv('ORG') # fOR PowerBI, ORG = 'YOUR_ORG'
```


#### Run locally with Python
Before running the script, you need to set up your environment variables. Create a `.env`` file in the project root and add your Azure DevOps Personal Access Token (PAT) and organization name:

```bash
# Inside your .env file
PAT=your_pat
ORG=your_org
```

Then, you can run the script:

```bash
python main.py
```

The script will retrieve the list of teams in your Azure DevOps organization and their members, and print the information to the console.

