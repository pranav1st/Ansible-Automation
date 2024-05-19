import requests
import json
import os

# def playbook_to_template(playbook):
#     # Define the URL and payload
#     url = 'http://localhost:3000/api/project/1/templates'
#     payload = {
#         "type": "",
#         "name": playbook,
#         "description": '',
#         "playbook": playbook+".yaml",
#         "inventory_id": 9,
#         "repository_id": 1,
#         "environment_id": 1,
#         "vault_key_id": None,
#         "project_id": 1
#     }

#     # Define headers
#     headers = {
#         "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
#         "Accept": "application/json, text/plain, */*",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Content-Type": "application/json",
#         "Origin": "http://localhost:3000",
#         "Connection": "keep-alive",
#         "Referer": "http://localhost:3000/project/1/templates",
#         "Cookie": "semaphore=MTcxNTA3MTA3OHw1Ym9ueXRzTUY3ZXotMHNka19UMlRSTEc0UzVsQWVsVXBOSml2aWVxSGo0QmtVSUZvWXB3M1VDMS1GeEptQ2c4MHNETGQyYjNxWlA5T3ZQWkJqLXJKQT09fEXTmskmaNBswP5mIzNwOot-n0RpCnT1uGM3QJCysGkw",
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin"
#     }

#     # Convert payload to JSON
#     payload_json = json.dumps(payload)

#     # Send the POST request
#     response = requests.post(url, data=payload_json, headers=headers)

#     # Print response
#     print("Response status code:", response.status_code)
#     print("Response content:", response.text)

def playbook_to_template(playbook, owner, repo, access_token):
    # Define the URL for the GitHub repository contents endpoint
    url_repo = f"https://api.github.com/repos/{owner}/{repo}/contents/{playbook}.yaml"

    # Define headers with the access token
    headers_repo = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Send a GET request to download the YAML file from the GitHub repository
    response_repo = requests.get(url_repo, headers=headers_repo)

    # Check if the request was successful (status code 200)
    if response_repo.status_code == 200:
        # Write the downloaded YAML file to a local directory
        with open(f"{playbook}.yaml", "wb") as f:
            f.write(response_repo.content)

        # Define the URL for the Semaphore API endpoint
        url_api_template = 'http://localhost:3000/api/project/1/templates'

        # Define the payload to add the playbook to the template
        payload_template = {
            "type": "",
            "name": playbook,
            "description": '',
            "playbook": playbook + ".yaml",
            "inventory_id": 9,
            "repository_id": 1,
            "environment_id": 1,
            "vault_key_id": None,
            "project_id": 1
        }

        # Define headers for the POST request to add playbook to template
        headers_api_template = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "http://localhost:3000",
            "Connection": "keep-alive",
            "Referer": "http://localhost:3000/project/1/templates",
            "Cookie": "semaphore=MTcxNTA3MTA3OHw1Ym9ueXRzTUY3ZXotMHNka19UMlRSTEc0UzVsQWVsVXBOSml2aWVxSGo0QmtVSUZvWXB3M1VDMS1GeEptQ2c4MHNETGQyYjNxWlA5T3ZQWkJqLXJKQT09fEXTmskmaNBswP5mIzNwOot-n0RpCnT1uGM3QJCysGkw",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        # Send a POST request to add the playbook to the template
        response_api_template = requests.post(url_api_template, json=payload_template, headers=headers_api_template)

        print("Status code:", response_api_template.status_code)
        print("Response:", response_api_template.text)

        print("Playbook added to template successfully.")

        # Extract the template ID from the response
        template_id = response_api_template.json()["id"]

        # Define the URL for the Semaphore API endpoint to add tasks
        url_api_tasks = 'http://localhost:3000/api/project/1/tasks'

        # Define the payload to add tasks
        payload_tasks = {
            "template_id": template_id,
            "environment": "{}",
            "project_id": 1
        }

        # Define headers for the POST request to add tasks
        headers_api_tasks = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "http://localhost:3000",
            "Connection": "keep-alive",
            "Referer": f"http://localhost:3000/project/1/templates/{template_id}",
            "Cookie": "semaphore=MTcxNTA3MTA3OHw1Ym9ueXRzTUY3ZXotMHNka19UMlRSTEc0UzVsQWVsVXBOSml2aWVxSGo0QmtVSUZvWXB3M1VDMS1GeEptQ2c4MHNETGQyYjNxWlA5T3ZQWkJqLXJKQT09fEXTmskmaNBswP5mIzNwOot-n0RpCnT1uGM3QJCysGkw",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        # Send a POST request to add tasks
        response_api_tasks = requests.post(url_api_tasks, json=payload_tasks, headers=headers_api_tasks)

        # Check if the request was successful (status code 200)
        if response_api_tasks.status_code == 200:
            print("Tasks added successfully.")
        else:
            print("Failed to add tasks.")
            print("Status code:", response_api_tasks.status_code)
            print("Response:", response_api_tasks.text)

            

        # Delete the locally stored YAML file
        os.remove(f"{playbook}.yaml")
    else:
        print("Failed to download YAML file from repository.")
        print("Status code:", response_repo.status_code)


def fetch_from_templates():
    url = 'http://localhost:3000/api/project/1/templates'

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "http://localhost:3000/project/1/templates",
        "Cookie": "semaphore=MTcxNTA3MTA3OHw1Ym9ueXRzTUY3ZXotMHNka19UMlRSTEc0UzVsQWVsVXBOSml2aWVxSGo0QmtVSUZvWXB3M1VDMS1GeEptQ2c4MHNETGQyYjNxWlA5T3ZQWkJqLXJKQT09fEXTmskmaNBswP5mIzNwOot-n0RpCnT1uGM3QJCysGkw",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Extract the "name" values from the response JSON
        names = [template["name"] for template in response.json()]
        return names
    else:
        print("Failed to get response. Status code:", response.status_code)
        return []

def get_yaml_files_from_repo(owner, repo, access_token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()

        yaml_files = [file["name"] for file in response_json if file["name"].endswith('.yaml') or file["name"].endswith('.yml')]
        yaml_files = [file[:-5] if file.endswith('.yaml') else file[:-4] for file in yaml_files]

        return yaml_files
    else:
        print(f"Failed to get repository contents. Status code: {response.status_code}")
        return []
    
def del_from_repo(file_path):
    def get_file_sha(owner, repo, file_path, access_token):
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            return response_json["sha"]
        else:
            print(f"Failed to get file details. Status code: {response.status_code}")
            print(response.text)
            return None
    
    def remove_file_from_repository(owner, repo, file_path, commit_message, access_token):
        file_sha = get_file_sha(owner, repo, file_path, access_token)
        if file_sha is None:
            return

        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        payload = {
            "message": commit_message,
            "sha": file_sha,  # Set SHA to the SHA hash of the file
            "branch": "main"
        }

        # Send a DELETE request to remove the file
        response = requests.delete(url, headers=headers, json=payload)

        if response.status_code == 200:
            print("File removed successfully.")
        else:
            print(f"Failed to remove file. Status code: {response.status_code}")
            print(response.text)

    owner = "pranav1st"
    repo = "Ansible-automation"

    commit_message = "Remove file from repository"

    access_token = "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"

    remove_file_from_repository(owner, repo, file_path, commit_message, access_token)


owner = "pranav1st"
repo = "Ansible-automation"

access_token = "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"

playbooks = fetch_from_templates()

yaml_files = get_yaml_files_from_repo(owner, repo, access_token)

for playbook in playbooks:
    if playbook not in yaml_files:
        print(f"Playbook '{playbook}' not found in the repository.")
        print("Calling playbook_to_template: ")
        #playbook_to_template(playbook)
        #trigger (not possible)

for yaml_file in yaml_files:
    if yaml_file not in playbooks:
        print(f"YAML file '{yaml_file}' not associated with any playbook.")
        print("Calling playbook_to_template: ")
        playbook_to_template(yaml_file, owner, repo, access_token)
