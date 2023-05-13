import paramiko, requests, os, csv, requests, sys
from dotenv import load_dotenv
from datetime import datetime
from requests.auth import HTTPBasicAuth


#Directory Operations
directory_path = os.getcwd()
subdirectory_name = "configs_dir"
subdirectory_path = os.path.join(directory_path, subdirectory_name)
if not os.path.exists(subdirectory_path):
    os.makedirs(subdirectory_path)

##constructors
def write_list_to_file(lst, filename):
    file_path = os.path.join(subdirectory_path,filename)
    with open(file_path, 'w' , encoding = "utf-8") as f:
        for item in lst:
            f.write("%s\n" % item.strip())

#Importing Paramiko
ssh = paramiko.SSHClient()

#Loading envs
load_dotenv()

#Defining SSH commands
cmd1 = "show running-config"

with open('targets.csv', newline='', encoding = "utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        for ipaddress in row:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("Attempting to establish SSH connection with " + ipaddress)
            try:
                #Trying to connect to the SSH server
                ssh.connect(ipaddress, username = os.getenv('CISCOUSERNAME'), password = os.getenv('CISCOPASSWORD'))
                #Executing commands
                ##stdin, stdout, stderr = ssh.exec_command(cmd0)
                stdin, stdout, stderr = ssh.exec_command(cmd1)
                output = stdout.readlines()
                #Creating a .conf file
                write_list_to_file(output, ipaddress + ".config")
                ssh.close()
            except:
                print("Unable to establish SSH connection with " + ipaddress)
        try:
            # Replace the directory path with the path to your directory
            directory_path = subdirectory_path
            # Replace the repository owner with your username or organization name
            repository_owner = os.getenv('GITHUBREPOOWNER')
            # Replace the repository name with your repository name
            repository_name = os.getenv('GITHUBREPONAME')
            # Replace the branch name with your branch name
            branch_name = os.getenv('BRANCH')
            # Replace the commit message with your commit message
            now =datetime.now()
            commit_message = now.strftime("%I:%M%p on %B %d, %Y")
            # Replace the GitHub username with your username
            github_username = os.getenv('GITHUBUSERNAME')
            # Replace the GitHub personal access token with your personal access token
            github_token = os.getenv('GITHUBACCESSTOKEN')
            # Get the SHA of the latest commit on the branch
            url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/git/refs/heads/{branch_name}"
            response = requests.get(url, auth=HTTPBasicAuth(github_username, github_token))
            sha = response.json()["object"]["sha"]
            # Create a new tree object with the files in the directory
            tree_url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/git/trees"
            tree_data = {
                "base_tree": sha,
                "tree": []
            }
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        file_content = f.read()
                        file_content_utf8 = file_content.decode("utf-8")
                        tree_data["tree"].append({
                        "path": os.path.relpath(file_path, directory_path),
                        "mode": "100644",
                        "type": "blob",
                        "content": file_content_utf8
                    })
            response = requests.post(tree_url, json=tree_data, auth=HTTPBasicAuth(github_username, github_token))
            tree_sha = response.json()["sha"]
            # Create a new commit object with the new tree object
            commit_url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/git/commits"
            commit_data = {
                "message": commit_message,
                "parents": [sha],
                "tree": tree_sha
            }
            response = requests.post(commit_url, json=commit_data, auth=HTTPBasicAuth(github_username, github_token))
            commit_sha = response.json()["sha"]
            # Update the branch reference to point to the new commit object
            ref_url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/git/refs/heads/{branch_name}"
            ref_data = {
                "sha": commit_sha,
                "force": True
            }
            response = requests.patch(ref_url, json=ref_data, auth=HTTPBasicAuth(github_username, github_token))
            print("Files pushed to GitHub successfully!")
        except:
            print("Push to Github was unsuccessful")
sys.exit(0)    