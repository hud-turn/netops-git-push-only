import paramiko, requests, json, os, csv
from dotenv import load_dotenv


ssh = paramiko.SSHClient()
with open('targets.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        ipaddress = row[0]
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        load_dotenv()
        ssh.connect(ipaddress, username= os.getenv('USERNAME'), password= os.getenv('PASSWORD'))
        stdin, stderr = ssh.exec_command('')
        stdin, stderr = ssh.exec_command('en')
        stdin, stderr = ssh.exec_command('terminal length 0')
        stdin, stdout, stderr = ssh.exec_command('show running-config')
        output = stdout.readlines()
        with open(f'{ipaddress}.txt', 'r') as f:
            f.writelines(output)
        ssh.close()