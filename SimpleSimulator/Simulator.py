import os
import sys

# Initialize registers (32 registers, initially all zeros)
registers = ['0b' + '0'*32] * 32 #Initialize them all has binary with value 0
memory = {}  # Dictionary for memory (key = address, value = 32-bit data as string)
PC = 0  # Program Counter starts at 0

def load_instructions(file_name):
    """ Reads binary instructions from file into a list. """
    instructions = []
    try:
        if not os.path.exists(file_name):
            print(f"Error: {file_name} not found.")
            return []
        
        with open(file_name, 'r') as infile:
            for line in infile:
                binary_instr = line.strip()
                if binary_instr:
                    instructions.append(binary_instr)
        
        print(f"Loaded {len(instructions)} instructions.")
        return instructions

    except Exception as e:
        print(f"Error: {e}")
        return []

def sign_extend(value, bits):
    """ Sign-extends value from bits to 32-bit. 
    checks if MSB is positive or negative"""
    if value & (1 << (bits - 1)):  # Check sign bit
        value -= (1 << bits)  # Convert to negative
    return value


def r_type(instr):
    funct7 = instr[:7]
    rs2 = int(instr[7:12], 2)
    rs1 = int(instr[12:17], 2)
    funct3 = instr[17:20]
    rd = int(instr[20:25], 2)
    opcode = instr[25:32] # Last 7 bits (opcode)

    if funct3 == "000":
        if funct7 == "0000000":  # ADD
            registers[rd] = registers[rs1] + registers[rs2]
        elif funct7 == "0100000":  # SUB
            registers[rd] = registers[rs1] - registers[rs2]
        else:
            print("Error")
    elif funct3 == "010":  # SLT
        if funct7=="0000000":
            registers[rd] = 1 if registers[rs1] < registers[rs2] else 0
        else:
            print("Error")
    elif funct3 == "101":
        if funct7 == "0000000":  # SRL
            registers[rd] = registers[rs1] >> (registers[rs2] & 0x1F)
        else:
            print("Error")
    elif funct3 == "110":  # OR
        if funct7=="0000000":
            registers[rd] = registers[rs1] | registers[rs2]
        else:
            print("Error")
    elif funct3 == "111":  # AND
        if funct7=="0000000":
            registers[rd] = registers[rs1] & registers[rs2]
        else:
            print("Error")
    else:
        print("Error")


def i_type(instr):
    global PC
    imm = sign_extend(int(instr[:12], 2), 12)
    rs1 = int(instr[12:17], 2)
    funct3 = instr[17:20]
    rd = int(instr[20:25], 2)
    opcode = instr[25:32]  # Last 7 bits (opcode)
    
    if funct3=="010":
        if opcode=="0000011": # LW
            if instr[-7:] == '0000011':
                imm = instr[:12]
                imm = sign_extend(int(imm,2),12)
                print(imm)
                Address = int(registers[rs1][2:],2) + imm
                Address = f"{Address & 0xFFFFFFFF:08x}"
                Address = Address.upper()
                Address = '0x' + Address
            if Address in memory:
                registers[rd] = memory[Address][2:]
            else:
                memory[Address] = '0b00000000000000000000000000000000'
                registers[rd] = '0'*32
        else:
            print("Error")


    elif funct3=="000": 
        if opcode=="0010011":  # ADDI
            registers[rd] = registers[rs1] + imm
        elif opcode=="1100111": # JALR
            registers[rd] = PC + 4
            PC = (registers[rs1] + imm) & ~1 # last part makes LSB 0 by making it even 
        else:
            print("Error")
    else:
        print("Error")


def b_type(instr):
    global PC
    imm = instr[0] + instr[24] + instr[1:7] + instr[20:24]+ "0"
    imm = sign_extend(int(imm, 2), 13)
    func = instr[17:20]
    rs1 = instr[12:17]
    rs2 = instr[7:12]
    
    if func == '000':    #BEQ
        if registers[rs1] == registers[rs2]:
            PC = PC + imm
            return
    elif func == '001':       #BNE
        if registers[rs1] != registers[rs2]:
            PC = PC + imm
            return
    
    PC+=4


def j_type(instr): # JAL
    global PC
    imm = sign_extend(int(instr[0] + instr[12:20] + instr[11] + instr[1:11] + "0", 2), 21)
    # opcode = instr[25:32]
    rd = int(instr[20:25],2)
    registers[rd] = PC + 4
    PC = (PC + imm) & ~1
    
    
    
def decode_execute(instr, output_lines):
    """ Decodes the binary instruction and executes it. """
    global PC
    opcode = instr[-7:]

    if opcode == "0010011" | opcode == "0000011" | opcode == "1100111":  # I-Type Instructions
        i_type(instr)

    elif opcode == "0110011":  # R-Type Instructions
        r_type(instr)

    elif opcode == "0100011":  # SW (Store Word)
        rs1 = int(instr[12:17],2)
        rs2 = int(instr[7:12],2)
        imm = instr[:7] + instr[20:25]
        imm = sign_extend(int(imm,2),12)


        Address = int(registers[rs1][2:],2) + imm
        Address = f"{Address & 0xFFFFFFFF:08x}"
        Address = Address.upper()
        Address = '0x' + Address
        memory[Address] = registers[rs2]

    elif opcode == "1100011":  # Branch Instructions beq and bne
        b_type(instr)

    elif opcode == "1101111":  # JAL
        j_type(instr)
    
    else:
        output_lines.append(f"Unknown instruction: {instr}")

    register_state = " ".join(f"{registers[i]:032b}" for i in range(32))
    output_lines.append(f"PC: {PC:08x} {register_state}")
    PC += 4



if __name__ == "__main__":
    file_name = "SimpleSimulator/simple/simple_1.txt"
    instructions = load_instructions(file_name)
    
    if instructions:
        output_lines = []
        for instr in instructions:
            decode_execute(instr, output_lines)

        with open("out.txt", "w") as outfile:
            outfile.write("\n".join(output_lines))

        #output written to out.txt
