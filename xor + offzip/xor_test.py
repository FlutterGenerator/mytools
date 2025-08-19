import os
import subprocess

def file_xor(file_path, xor_key):
    """XOR operation for the file with the given key"""
    with open(file_path, "rb") as f:
        data = f.read()

    # XOR each byte with the key
    result = bytearray([byte ^ xor_key for byte in data])

    return result

def save_decrypted_file(output_path, decrypted_data):
    """Save the decrypted file data"""
    with open(output_path, "wb") as f:
        f.write(decrypted_data)

def unpack_pak(file_path):
    """Unpack .pak files using offzip.exe"""
    if os.path.exists("offzip.exe"):
        try:
            output_dir = os.path.splitext(file_path)[0]  # Create folder with same name as file
            os.makedirs(output_dir, exist_ok=True)
            command = f"offzip.exe -a {file_path} {output_dir}"
            subprocess.run(command, shell=True, check=True)
            print(f"Unpacked {file_path} to {output_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Error while unpacking {file_path}: {e}")
    else:
        print("offzip.exe not found! Please make sure it's in the current directory.")

def log_message(message):
    """Log message to the console (print)"""
    print(message)

def process_file(input_file):
    """Process the file with XOR decryption for all keys from 0x00 to 0xFF"""
    for xor_key in range(0x00, 0x100):  # Loop through all XOR keys from 0x00 to 0xFF
        # XOR the file data
        decrypted_data = file_xor(input_file, xor_key)

        # Log the output file name
        output_file = f"decrypt_map_xor{xor_key:02X}.pak"
        log_message(f"Decrypting file using XOR key 0x{xor_key:02X}...")
        
        # Save the decrypted file
        save_decrypted_file(output_file, decrypted_data)

        log_message(f"Decrypted file saved as {output_file}")

        # Unpack the decrypted file
        unpack_pak(output_file)

def main():
    """Main function to handle file decryption process"""
    input_file = "pakchunk02-Table-Android_ASTC.pak"  # Replace with the actual file path game_patch_3.8.1.19939.pak

    # Check if the file exists
    if not os.path.exists(input_file):
        log_message(f"Error: File '{input_file}' not found!")
        return

    log_message(f"Starting decryption for {input_file}...")

    # Process the file for all XOR keys from 0x00 to 0xFF
    process_file(input_file)
    
    log_message("Decryption process completed!")

if __name__ == "__main__":
    main()
