import paramiko, requests, json, os, csv
from dotenv import load_dotenv

def write_list_to_file(lst, filename):
    with open(filename, 'w') as f:
        for item in lst:
            f.write("%s" % item)

cmd0 = "terminal length 0"
cmd1 = "show running-config"
ssh = paramiko.SSHClient()
with open('targets.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        ipaddress = row[0]
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        load_dotenv()
        ssh.connect(ipaddress, username = os.getenv('USERNAME'), password = os.getenv('PASSWORD'))
        stdin, stdout, stderr = ssh.exec_command(cmd1)
        output = stdout.readlines()
        write_list_to_file(output, ipaddress + '.txt')
        ssh.close()