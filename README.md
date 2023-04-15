# netops-git-push-only

## Requirements
1. In order to use this repo you will need to create two separate files.
   + You will need to create an .env that stores the credentials used to connect to a Cisco SSH instance.  
   + You will also want to to add the credentials used to connect and push configuration files to an online git repository.  
2. The second file that is required is a targets.csv file, as it currently stands you will need to delineate your SSH targets.  
   + The targets.csv file must contain a list of ip addresses delimited by a comma without a space (for example "192.168.1.1,192.168.1.2"). 
 
### Environmental File Contents
1. You will likely want to start off with a unique Cisco Username and Password for this project. Preferably a credential that has read access only to prevent damage if the system that this script is running on is compromised in some form or fashion.
   + You can either use a AAA server like RADIUS to help disseminate the credentials.
   + You can also create a local account on the Cisco appliance which also works if you don't want to go through the hassle of setting up a AAA server.
   
```
CISCOUSERNAME = "{your admin account}"
CISCOPASSWORD = "{your admin account password}"

GITHUBREPOOWNER = "{The username that is listed in the GitHub URL}"
GITHUBREPONAME = "{the repo you want to push to}"
BRANCH = "{the branch you want to push to}"
GITHUBUSERNAME = "{the GitHub account that will be pushing code}"
GITHUBACCESSTOKEN = "{You will need to generate a GitHub access token to insert here}"
```
