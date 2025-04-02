import os
import sys

# Initialize registers (32 registers, initially all zeros)
registers = [380 if i == 2 else 0 for i in range(32)] #Initialize them all has binary with value 0
memory = {}  # Dictionary for memory (key = address, value = 32-bit data as string)
stack_memory = {}
for i in range(380,251,-4):
    s = f"{i & 0xFFFFFFFF:08x}".upper()
    stack_memory['0x' + s] = '0b' + '0'*32
for i in range(65536,65661,4):
    s = f"{i & 0xFFFFFFFF:08x}".upper()
    memory['0x' + s] = '0b' + '0'*32   #Memory initialization with given range
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
        flag = 0
        if opcode=="0000011": # LW
            imm = instr[:12]
            imm = sign_extend(int(imm,2),12)

            Address = registers[rs1] + imm
            Address = f"{Address & 0xFFFFFFFF:08x}"
            Address = Address.upper()
            Address = '0x' + Address

            if Address in stack_memory:
                registers[rd] = int(stack_memory[Address][2:],2)
            elif Address in memory:
                registers[rd] = int(memory[Address][2:],2)
            else:
                print("SEGMENTATION FAULT(LW)")
                quit()
            PC += 4
        else:
            print("Error")


    elif funct3=="000":
        if opcode=="0010011":  # ADDI
            registers[rd] = registers[rs1] + imm
            PC += 4
        elif opcode=="1100111": # JALR
            if rd:
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
    rd = int(instr[20:25],2)
    if rd:
        registers[rd] = PC + 4
    if imm%4 == 0:
        PC += imm
    else:
        print("INVALID JUMP(JAL)")
        quit()
    
    
    
def decode_execute(instr, output_lines):
    """ Decodes the binary instruction and executes it. """
    global PC
    opcode = instr[-7:]

    if opcode == "0010011" or opcode == "0000011" or opcode == "1100111":  # I-Type Instructions
        i_type(instr)

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
        if Address in stack_memory:
            stack_memory[Address] = f"0b{registers[rs2] & 0xFFFFFFFF:032b}"
        elif Address in memory:
            memory[Address] = f"0b{registers[rs2] & 0xFFFFFFFF:032b}"
        else:
            print("SEGMENTATION FAULT(SW)")
            quit()
        PC += 4

    elif opcode == "1100011":  # Branch Instructions beq and bne
        b_type(instr)

    elif opcode == "1101111":  # JAL
        j_type(instr)
    
    else:
        output_lines.append(f"Unknown instruction: {instr}")

    register_state = " ".join(f"0b{registers[i] & 0xFFFFFFFF:032b}" if registers[i] >= 0 else f"0b{(registers[i] + (1 << 32)) & 0xFFFFFFFF:032b}" for i in range(32))
    PC = (PC//4)*4
    output_lines.append(f"0b{PC:032b} {register_state}")

#bonus part Q3

def rst():
    registers = [0]*32

def mul(instr):
    rs2 = int(instr[7:12], 2)
    rs1 = int(instr[12:17], 2)
    rd = int(instr[20:25], 2)
    registers[rd] = registers[rs1] * registers[rs2]

def halt():
    quit()

def rvrs(instr):
    rs1 = int(instr[12:17],2)
    bin_rs1 = f"{registers[rs1] & 0xFFFFFFFF:08x}"
    bin_rs1 = bin_rs1[::-1]
    rd = int(instr[20:25], 2)
    registers[rd] = int(bin_rs1,2)

if __name__ == "__main__":
    ifile = str(sys.argv[1])
    ofile = str(sys.argv[2])
    instructions = load_instructions(ifile)
    if instructions:
        count1= 0
        prev_PC = 0
        Halt_Check = 0
        output_lines = []
        while PC < 4*len(instructions):
            prev_PC = PC
            decode_execute(instructions[PC//4],output_lines)
            if prev_PC == PC:
                break

        with open(ofile,'w') as outfile:
            outfile.write(" \n".join(output_lines))
            outfile.write(' ')
            i = 65536
            for Address in memory:
                outfile.write('\n')
                outfile.write(Address + ':' + memory[Address])


        #output written to out.txt
    
