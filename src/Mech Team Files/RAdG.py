import time
from PiPocketGeiger import RadiationWatch


with RadiationWatch(24, 23) as radiationWatch:
  pass # Do something with the lib.

with RadiationWatch(24, 23) as radiationWatch:
    # Do something with the lib.
    print(radiationWatch.status())

# Create an instance.
radiationWatch = RadiationWatch(24, 23)
# Initialize it (setup GPIOs, interrupts).
radiationWatch.setup()
# Do something with the lib.
print(radiationWatch.status())
# Do not forget to properly close it (free GPIOs, etc.).
radiationWatch.close()

# {'duration': 14.9, 'uSvh': 0.081, 'uSvhError': 0.081, 'cpm': 4.29}

def onRadiation():
    print("Ray appeared!")
def onNoise():
    print("Vibration! Stop moving!")
with RadiationWatch(24, 23) as radiationWatch:
    radiationWatch.register_radiation_callback(onRadiation)
    radiationWatch.register_noise_callback(onNoise)
    while True:
        try:
            # Do something here
            # For example, print the current status
            print(radiationWatch.status())
            # Sleep for 1 second
            time.sleep(1)
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")
            break
        except Exception as e:
            print("An error occurred:", e)
            # Log the error for further analysis
            # You can replace 'error.log' with the path to your log file
            with open('error.log', 'a') as f:
                f.write(f"Error: {e}\n")
            # Optionally, you can raise the error to terminate the program
            # raise