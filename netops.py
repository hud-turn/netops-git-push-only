import paramiko, requests, json, os, csv, datetime
from dotenv import load_dotenv
from github import Github
load_dotenv()

#Directory Operations
directory_path = os.getcwd()
subdirectory_name = "configs_dir"
subdirectory_path = os.path.join(directory_path, subdirectory_name)
if not os.path.exists(subdirectory_path):
    os.makedirs(subdirectory_path)

##constructors
def write_list_to_file(lst, filename):
    file_path = os.path.join(subdirectory_path,filename)
    with open(file_path, 'w') as f:
        for item in lst:
            f.write("%s\n" % item.strip())

#Importing Paramiko
ssh = paramiko.SSHClient()

#Defining SSH commands
cmd0 = "terminal length 0"
cmd1 = "show running-config"

with open('targets.csv', newline='') as csvfile:
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
        #Importing Credentials and Information
        g = Github(os.getenv('GITHUBACCESSTOKEN'))
        user = g.get_user()
        repo = user.get_repo(os.getenv('GITHUBREPO'))
        dir_path = subdirectory_path
        commit_message = datetime.date.now().strftime("%I:%M%p on %B %d, %Y")
        # Loop through all files in the current directory:
        for filename in os.listdir(dir_path):
            # Open the file:
            with open(os.path.join(dir_path, filename), 'r') as file:
                content = file.read()
            # Create a new file in the repository:
                repo.create_file(filename, commit_message, content)
    except:
        print("Unable to connect to Github")
    