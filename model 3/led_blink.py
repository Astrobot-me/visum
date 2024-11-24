import serial
import random
import time

# Define the serial port and baud rate

ser = serial.Serial('COM3', 9600) 

    #  Change 'COM3' to the appropriate port

while True:
 
    state = random.randint(1, 3)  # Generate a random state (1, 2, or 3)
    ser.write(str(state).encode())  # Send the state to Arduino
    print(f'Sent state {state} to Arduino')
    time.sleep(3) 
    

        # Wait for 8 sq