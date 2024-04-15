Gnu Radio Transmission README

*** Docker was used to provide correct version of Gnu Radio for transmission on rPi***
*** Access to the Docker image and the commands to build it are found below***
*** There are two versions of transmission, master_script.py will read the entire CSV file but encounters overflow errors***
*** master_script2.py will not encounter errors but can only send roughly 15 lines in Excel on repeat ***
*** master_script2.py depends on pkt_xmt2.py, and master_script.py depends upon pkt_xmt.py ***

1. packet_format_gr38.py
	- This created and Embedded Python Block which is necessary for running the transmission and packetizing data in the correctly specified format with header information.

2. pkt_xmt.grc / pkt_xmt.py
	- GRC file is used to create pkt_xmt.py. Since the rPi is being run headless, we cannot run pkt_xmt.grc on the rPi
	- to generate while headless, use the command 'grcc pkt_xmt.grc'
	- to control flow inside of pkt_xmt.py, synchronize the time.sleep() command in the main portion with master_script.py

3. pkt_xmt2.grc / pkt_xmt2.py
	-same as above

4. master_script.py / master_script2.py
	- handles the starting and stopping of transmission. Since we were reading from a csv file, this program allows us to delete the csv file, then restart tranmission.
	- must be synchronized with pkt_xmt.py or pkt_xmt2.py, respectively.

DOCKER BUILD

The docker image used comes from a student at FAU (Jose Angel Sanchez). A link to his image can be found here:
https://hub.docker.com/r/joseasanchezviloria/siwn-radio

After installing the image, we build the image using this command. Each argument has a purpose, including mounting the shared drive, linking the display, turning on i2c, and maintaining network capabilities.

sudo docker run --name gr385 -it -e DISPLAY=$DISPLAY -v /home/jonmaz/docker_link:/home/shared -v /dev/net/tun:/dev/net/tun --network host --device /dev/i2c-1 --cap-add=NET_ADMIN joseasanchezviloria/siwn-radio:v1
