import sys
import os

def extract(file_name):
    output_file = "out.txt" 
    try:
        if not os.path.exists(file_name):
            print(f"Error: {file_name} not found.")
            return
        
        with open(file_name, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                binary_instr = line.strip() 
                if binary_instr:
                    outfile.write(binary_instr + '\n')

        print(f"Binary instructions written to {os.path.abspath(output_file)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    file_name = "simple/simple_1.txt"  
    extract(file_name)
