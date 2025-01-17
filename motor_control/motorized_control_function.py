import serial
import time
from datetime import datetime

hex_table = {
    "0": "30", "1": "31", "2": "32", "3": "33", "4": "34", "5": "35", "6": "36", "7": "37", "8": "38", "9": "39",
    "A": "41", "B": "42", "C": "43", "D": "44", "E": "45", "F": "46",
    "G": "47", "H": "48", "I": "49", "J": "4A", "K": "4B", "L": "4C", "M": "4D", "N": "4E", "O": "4F",
    "P": "50", "Q": "51", "R": "52", "S": "53", "T": "54", "U": "55", "V": "56", "W": "57", "X": "58", "Y": "59", "Z": "5A",
    "+": "2B", "-": "2D", ".": "2E", "/": "2F", "?": "3F",
    "STX": "02", "Tab": "09", "LF": "0A", "CR": "0D"
}

def log_to_file(file_name, command, response):
    """
    Append the command and response to a log file with a timestamp.

    Args:
        file_name (str): Name of the log file.
        command (bytes): The command sent to the device.
        response (bytes): The response received from the device.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current time
    with open(file_name, "a") as file:
        file.write(f"Time: {current_time}\n")
        file.write(f"Command Sent (hex): {command.hex()}\n")
        file.write(f"Command Sent (ASCII): {command.decode(errors='ignore')}\n")
        file.write(f"Response Received (hex): {response.hex()}\n")
        file.write(f"Response Received (ASCII): {response.decode(errors='ignore')}\n")
        file.write("-" * 40 + "\n")

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
    if axes == "x" or axes == "y":
        port = "COM3"
    else:
        port = "COM4"
    
    log_file = "command_response_log.txt"  # Log file name

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
            
            # Log command and response to the file
            log_to_file(log_file, command, response)
    except serial.SerialException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        
def motor_control(axes, speed, position):
    # Configure the serial port
    # Change this if you're using a different port
    baud_rate = 115200  # Match the baud rate of your device
    timeout = 10  # Timeout in seconds
    # Define position limits for each axis
    position_limits = {
        "x": {"min": 0, "max": 1000},  # Example limits for x-axis
        "y": {"min": 0, "max": 1000},  # Example limits for y-axis
        "z": {"min": 0, "max": 1000},  # Example limits for z-axis
    }
    
    # Check if the position is within the allowed range
    if axes not in position_limits:
        print(f"Error: Invalid axis '{axes}' specified.")
        return
    
    if position < position_limits[axes]["min"] or position > position_limits[axes]["max"]:
        print(f"Error: Position {position} for axis '{axes}' is out of bounds. "
              f"Allowed range: {position_limits[axes]['min']} - {position_limits[axes]['max']}.")
        return
    commands = {
        "y": bytes.fromhex("02 "+string_to_hex("APS1/")+" "+string_to_hex(str(speed))+" "+string_to_hex("/")+" "+string_to_hex(str(position))+" "+string_to_hex("/0")+" "+"0D 0A"),
        "x": bytes.fromhex("02 "+string_to_hex("APS2/")+" "+string_to_hex(str(speed))+" "+string_to_hex("/")+" "+string_to_hex(str(position))+" "+string_to_hex("/0")+" "+"0D 0A"),
        "z": bytes.fromhex("02 "+string_to_hex("APS1/")+" "+string_to_hex(str(speed))+" "+string_to_hex("/")+" "+string_to_hex(str(position))+" "+string_to_hex("/0")+" "+"0D 0A")
    }
    send_command(axes,baud_rate,timeout,commands[axes])
#ORG is not recommanded
def initialize_all():
    motor_control("x", 4, 0)
    motor_control("y", 4, 0)
    motor_control("z", 4, 0)

def read_system_setting(system_num):
    #RSY
    baud_rate=115200
    timeout=10
    commands = {
        "y": bytes.fromhex("02 "+string_to_hex("RSY1/")+string_to_hex(str(system_num))+" 0D 0A"),
        "x": bytes.fromhex("02 "+string_to_hex("RSY2/")+string_to_hex(str(system_num))+" 0D 0A"),
        "z": bytes.fromhex("02 "+string_to_hex("RSY1/")+string_to_hex(str(system_num))+" 0D 0A")
    }

    # Send commands for each port
    for axes, command in commands.items():
        send_command(axes, baud_rate, timeout, command)

def write_microstep(micro_step):
    baud_rate = 115200  # Match the baud rate of your device
    timeout = 10  # Timeout in seconds
    '''
    commands_dc = {
        "y": bytes.fromhex("02 "+string_to_hex("WSY1/")),
        "x": bytes.fromhex("02 "+string_to_hex("WSY2/")),
        "z": bytes.fromhex("02 "+string_to_hex("WSY1/"))
    }

    for axes, command in commands_dc.items():
    send_command(axes, baud_rate, timeout, command)
    '''

    commands_ms = {
        "y": bytes.fromhex("02 "+string_to_hex("WSY1/66/")+string_to_hex(str(micro_step))+" 0D 0A"),
        "x": bytes.fromhex("02 "+string_to_hex("WSY2/66/")+string_to_hex(str(micro_step))+" 0D 0A"),
        "z": bytes.fromhex("02 "+string_to_hex("WSY1/66/")+string_to_hex(str(micro_step))+" 0D 0A")
    }

    # Send commands for each port
    for axes, command in commands_ms.items():
        send_command(axes, baud_rate, timeout, command)

def read_position(axes):
    baud_rate=115200
    timeout=10
    if axes=="x":
        axis_num=2
    elif axes=="y":
        axis_num=1
    else:
        axis_num=1
    #RDP
    command=bytes.fromhex("02 "+string_to_hex("RDP")+" "+string_to_hex(str(axis_num))+" 0D 0A")
    send_command(axes,baud_rate,timeout,command)

'''
def device_information():
    #IDN, RSY, STR
    baud_rate=115200
    timeout=10
    command=bytes.fromhex("02 "+string_to_hex("IDN")+" 0D 0A")
    send_command("x",baud_rate,timeout,command)
    send_command("z",baud_rate,timeout,command)
'''

def quit_motor():
    baud_rate=115200
    timeout=10
    #RST
    command=bytes.fromhex("02 "+string_to_hex("RST")+" 0D 0A")
    send_command("x",baud_rate,timeout,command)
    send_command("z",baud_rate,timeout,command)