
import os
import subprocess
import time

file_path = "input_csv.csv"

main_flag = True

while main_flag:
    print('Restarting Loop')
    time.sleep(3)
    try: 
        # Check if the file exists
        if os.path.exists(file_path):

            # Run pkt_xmt.py as a separate process
            pkt_xmt_process = subprocess.Popen(["python3", "pkt_xmt.py"])
            
            # Wait for 6 seconds - let pkt_xmt.py run - IF you change this, change sleep in pktxmt too
            print('pkt_xmt.py is running...')
            time.sleep(6)
            
            # Terminate pkt_xmt.py process
            print('Waiting for pkt_xmt.py to terminate...')
            pkt_xmt_process.terminate()

        else:
            print(f"File {file_path} does not exist.")
    except: 
        print(f"File {file_path} does not exist. Except")
