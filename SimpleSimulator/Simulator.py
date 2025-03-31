import os
import sys

# Initialize registers (32 registers, initially all zeros)
registers = [0] * 32 #Initialize them all has binary with value 0
memory = {}  # Dictionary for memory (key = address, value = 32-bit data as string)
for i in range(65536,65661,4):
    memory[f"{i & 0xFFFFFFFF:08x}"] = '0b' + '0'*32   #Memory initialization with given range

print(memory)
PC = 4  # Program Counter starts at 4

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
                Address = registers[rs1] + imm
                Address = f"{Address & 0xFFFFFFFF:08x}"
                Address = Address.upper()
                Address = '0x' + Address
            if Address in memory:
                registers[rd] = int(memory[Address][2:],2)
            else:
                registers[rd] = 0
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
    rs1 = int(instr[12:17],2)
    rs2 = int(instr[7:12],2)
    
    if func == '000':    #BEQ
        if registers[rs1] == registers[rs2]:
            PC += imm
            return
    elif func == '001':       #BNE
        if registers[rs1] != registers[rs2]:
            PC += imm
            return
    PC += 4


def j_type(instr): # JAL
    global PC
    imm = sign_extend(int(instr[0] + instr[12:20] + instr[11] + instr[1:11] + "0", 2), 21)
    # opcode = instr[25:32]
    rd = int(instr[20:25],2)
    registers[rd] = PC + 4
    #PC = (PC + imm) & ~1
    PC += imm
    
    
    
def decode_execute(instr, output_lines):
    """ Decodes the binary instruction and executes it. """
    global PC
    opcode = instr[-7:]

    if opcode == "0010011" or opcode == "0000011" or opcode == "1100111":  # I-Type Instructions
        i_type(instr)
        PC += 4

    elif opcode == "0110011":  # R-Type Instructions
        r_type(instr)
        PC += 4

    elif opcode == "0100011":  # SW (Store Word)
        rs1 = int(instr[12:17],2)
        rs2 = int(instr[7:12],2)
        imm = instr[:7] + instr[20:25]
        imm = sign_extend(int(imm,2),12)


        Address = registers[rs1] + imm
        Address = f"{Address & 0xFFFFFFFF:08x}"
        Address = Address.upper()
        Address = '0x' + Address
        if Address in memory:
            memory[Address] = f"0b{registers[rs2] & 0xFFFFFFFF:032b}"
        PC += 4

    elif opcode == "1100011":  # Branch Instructions beq and bne
        b_type(instr)

    elif opcode == "1101111":  # JAL
        j_type(instr)
    
    else:
        output_lines.append(f"Unknown instruction: {instr}")

    register_state = " ".join(
    f"{registers[i] & 0xFFFFFFFF:032b}" if registers[i] >= 0 else f"{(registers[i] + (1 << 32)) & 0xFFFFFFFF:032b}" for i in range(32))

    output_lines.append(f"{PC:032b} {register_state}")
    print("PC after instr: ",PC)




if __name__ == "__main__":
    file_name = "SimpleSimulator/simple/simple_3.txt"
    instructions = load_instructions(file_name)

    if instructions:
        prev_PC = 0
        Halt_Check = 0
        output_lines = []
        # for instr in instructions:
        #     decode_execute(instr, output_lines)
        while PC < 4*len(instructions):
            print("Running instruction at address:",PC)
            prev_PC = PC
            decode_execute(instructions[PC//4 - 1],output_lines)
            print(" ".join(f"{registers[i]}" for i in range(32)))
            if prev_PC == PC:
                print("Program HALTED")
                break

        with open("out.txt", "w") as outfile:
            outfile.write("\n".join(output_lines))
            for Address in memory:
                outfile.write('\n')
                outfile.write('0x' + Address + ':' + memory[Address])


        #output written to out.txt
    
