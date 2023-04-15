# netops-git-push-only

## Requirements
1. In order to use this repo you will need to create two separate files.
--- + You will need to create an .env that stores the credentials used to connect to a Cisco SSH instance.-- 
--- + You will also want to to add the credentials used to connect and push configuration files to an online git repository.--
2. The second file that is required is a targets.csv file, as it currently stands you will need to delineate your SSH targets.
--- + The targets.csv file must contain a list of ip addresses delimited by a comma without a space (for example "192.168.1.1,192.168.1.2").--
