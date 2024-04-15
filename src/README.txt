There is a complex environment set up to run these files successfully. Inside of each folder will be an additional README file for setting up that individual component.

Here is a brief overview:

1. Flask Display
	- type "flask run --debug" in the location that contains 'out.csv' and the rest of the files inside of this folder.
	- Requires 'pos.csv' to be created. Upon launch, remove and create a new 'pos.csv' file. The first GPS location gathered from the SPOT Gen4 will mark the initial position of the payload.
	- 'out.csv' is generated from the parser.
	- click the link that pops up in terminal to visualize data.
	- all entries are tabulated and specific ones are viewed graphically.

2. Gnu Radio Receiver
	- on the ground station, after installing the correct version of gnu radio, run 'gnuradio-companion' from terminal. 
	- navigate to this file and hit play to start the ground station. 
	- saves a file 'output_csv.csv' that contains all data received.
	- saves a file 'complex.dat' to external hard drive that contains raw data.

3. Gnu Radio Transmission
	- Follow instructions exactly. These files exist on the Raspberry Pi with PlutoSDR and mech team sensors connected.
	- Connect to terminal via SSH (rPi is configured as an access point with static IP 10.3.141.1)
	- navigate to 'docker_link'. This folder is a mounted drive that can be accessed within docker.
	- run 'nohup python3 full_go.py > output_sensor.log 2>&1 &'. This runs mech sensor file in background.
	- open another terminal window and SSH in again
	- Enter these commands in terminal (Start docker, navigate to file, run masterscript2)
		- docker start gr385
		- docker exec -it gr385 /bin/bash
		- cd home/shared
		- nohup python3 master_script2.py > output_tx.log 2>&1 &
	- master_script2.py controls the flow of transmission (on for 55 sec, off for 5) from csv files.
	- full_go.py reads sensor data and saved to file 'input_csv.csv' and 'backup.csv'
	- input_csv.csv is filled with sensor data, transmitted, then deleted. backup.csv stores all sensor entries.
	- disconnect from terminal
	- ** in the future, properly configure full_go.py to run in background using systemd. 
	- ** experiment with altering master_script2.py for mission requirements.

4. Mech Team Files
	- These files contain the libraries and dependencies for the mech team. They need to be there but our team was not responsible for their creation.

5. Parser
	- on the ground station, 'parser_final.py' reads through and removes erroneous or duplicate entries in 'output_csv.csv
	- saves cleaned entries to 'out.csv' which is used for display.
	- bug found on launch day, sensitive to errors in date/time caused crash.