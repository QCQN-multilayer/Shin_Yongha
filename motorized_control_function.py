import serial
import time

hex_table = {
    "0": "30", "1": "31", "2": "32", "3": "33", "4": "34", "5": "35", "6": "36", "7": "37", "8": "38", "9": "39",
    "A": "41", "B": "42", "C": "43", "D": "44", "E": "45", "F": "46",
    "G": "47", "H": "48", "I": "49", "J": "4A", "K": "4B", "L": "4C", "M": "4D", "N": "4E", "O": "4F",
    "P": "50", "Q": "51", "R": "52", "S": "53", "T": "54", "U": "55", "V": "56", "W": "57", "X": "58", "Y": "59", "Z": "5A",
    "+": "2B", "-": "2D", ".": "2E", "/": "2F", "?": "3F",
    "STX": "02", "Tab": "09", "LF": "0A", "CR": "0D"
}

# Function to convert a string into hexadecimal codes    
def string_to_hex(input_string):
    hex_result = []
    for char in input_string:
        if char in hex_table:
            hex_result.append(hex_table[char])
        else:
            raise ValueError(f"Character '{char}' not found in hex table.")
    return " ".join(hex_result)

def send_command(axes, baud_rate, timeout, command, expected_bytes=4):
    if axes=="x" or axes=="y":
        port = "COM4"
    else:
        port = "COM3"
    try:
        # Open the serial port
        with serial.Serial(port, baudrate=baud_rate, timeout=timeout) as ser:
            print(f"Connected to {port}")
            
            # Send the hex command
            ser.write(command)  
            print(f"Sent: {command.hex()}")
            
            # Read the response
            response = b""
            start_time = time.time()

            while True:
                # Read available data in chunks
                chunk = ser.read(ser.in_waiting or 1)  # Read all available or 1 byte at a time
                response += chunk

                # Break when the response is complete
                if len(response) >= expected_bytes:
                    break
                
                # Timeout to avoid infinite loop
                if time.time() - start_time > timeout:
                    print("Timeout waiting for response.")
                    break
            
            # Display the received response
            if response:
                print(f"Received (hex): {response.hex()}")
                print(f"Received (ASCII): {response.decode(errors='ignore')}")  # Optional: ASCII interpretation
            else:
                print("No response received.")
    except serial.SerialException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        
def motor_control(axes, speed, position):
    # Configure the serial port
    # Change this if you're using a different port
    baud_rate = 115200  # Match the baud rate of your device
    timeout = 10  # Timeout in seconds
    commands = {
        "y": bytes.fromhex("02 "+string_to_hex("APS1/")+" "+string_to_hex(str(speed))+" "+string_to_hex("/")+" "+string_to_hex(str(position))+" "+string_to_hex("/0")+" "+"0D 0A"),
        "x": bytes.fromhex("02 "+string_to_hex("APS2/")+" "+string_to_hex(str(speed))+" "+string_to_hex("/")+" "+string_to_hex(str(position))+" "+string_to_hex("/0")+" "+"0D 0A"),
        "z": bytes.fromhex("02 "+string_to_hex("APS1/")+" "+string_to_hex(str(speed))+" "+string_to_hex("/")+" "+string_to_hex(str(position))+" "+string_to_hex("/0")+" "+"0D 0A")
    }
    send_command(axes,baud_rate,timeout,commands[axes])
    
def initialize_all():
    baud_rate = 115200  # Match the baud rate of your device
    timeout = 10  # Timeout in seconds

    # Hex commands
    commands = {
        "y": bytes.fromhex("02 4F 52 47 31 2F 34 2F 30 0D 0A"),
        "x": bytes.fromhex("02 4F 52 47 32 2F 34 2F 30 0D 0A"),
        "z": bytes.fromhex("02 4F 52 47 31 2F 34 2F 30 0D 0A")
    }

    # Send commands for each port
    for axes, command in commands.items():
        send_command(axes, baud_rate, timeout, command)
        
def setting_ORG():
    baud_rate = 115200  # Match the baud rate of your device
    timeout = 10  # Timeout in seconds
    
    commands = {
        "y": bytes.fromhex("02 57 53 59 31 2F 32 2F 34 0D 0A"),
        "x": bytes.fromhex("02 57 53 59 32 2F 32 2F 34 0D 0A"),
        "z": bytes.fromhex("02 57 53 59 31 2F 32 2F 34 0D 0A")
    }

    # Send commands for each port
    for axes, command in commands.items():
        send_command(axes, baud_rate, timeout, command)
    