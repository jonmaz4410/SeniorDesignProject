These files are used in the gathering, parsing, and display of data on the receiver side of things.

1. out.csv
	- parsed and cleaned lines used for display in the flask program

2. output_csv.csv
	- all data received from the transmitter

3. pos.csv
	- used in the flask program for controlling pointing information for the yagi antenna. 
	- requires altitude to come from demodulated packets and GPS data from SPOT Gen4
