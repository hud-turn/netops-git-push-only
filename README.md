# netops-git-push-only

In order to use this repo you will need to create two separate files.
The first one is a .env that stores the credentials used to connect to a Cisco SSH instance and eventually the credentials used to connect and push configuration files to an online git repository.
The second filt that is required is a targets.csv file.
The targets.csv file must contain a list of ip addresses delimited by a comma without a space (for example "192.168.1.1,192.168.1.2").
