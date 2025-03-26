import os
import sys

"""note to rest of group
so far ive done file extraction (load_instructions), and most of opcode handling for all instruction typees, 
(ive just made the outline for evert opcode)
so now we just have to do the execute part

"""

# Initialize registers (32 registers, initially all zeros)
registers = [0] * 32
memory = {}  # Dictionary for memory (key = address, value = 32-bit data)
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

def decode_execute(instr, output_lines):
    """ Decodes the binary instruction and executes it. """
    global PC

    opcode = instr[-7:]  # Last 7 bits (opcode)
    rd = int(instr[20:25], 2)  # Destination register
    funct3 = instr[17:20]  # Function code
    rs1 = int(instr[12:17], 2)  # First source register
    rs2 = int(instr[7:12], 2)  # Second source register (for R-type)
    imm = sign_extend(int(instr[:12], 2), 12)  # Immediate for I-type

    if opcode == "0010011":  # I-Type Instructions
        if funct3 == "000":  # ADDI
            a=0
    
    elif opcode == "0110011":  # R-Type Instructions
        funct7 = instr[:7]
        if funct3 == "000":
            if funct7 == "0000000":  # ADD
                registers[rd] = registers[rs1] + registers[rs2]
            elif funct7 == "0100000":  # SUB
                registers[rd] = registers[rs1] - registers[rs2]
        elif funct3 == "010":  # SLT
            registers[rd] = 1 if registers[rs1] < registers[rs2] else 0
        elif funct3 == "101":
            if funct7 == "0000000":  # SRL
                registers[rd] = registers[rs1] >> (registers[rs2] & 0x1F)
        elif funct3 == "110":  # OR
            registers[rd] = registers[rs1] | registers[rs2]
        elif funct3 == "111":  # AND
            registers[rd] = registers[rs1] & registers[rs2]

    elif opcode == "0000011":  # LW (Load Word)
        address = registers[rs1] + imm
        registers[rd] = memory.get(address, 0)  # Load from memory

    elif opcode == "0100011":  # SW (Store Word)
        imm_s = sign_extend(int(instr[:7] + instr[20:25], 2), 12)  # Split S-type immediate
        address = registers[rs1] + imm_s
        memory[address] = registers[rs2]  # Store to memory

    elif opcode == "1100011":  # Branch Instructions beq and bne and blt
        a=0

    elif opcode == "1100111":  # JALR
        registers[rd] = PC + 4
        PC = (registers[rs1] + imm) & ~1
        
    elif opcode == "1101111":  # JAL
        imm_j = sign_extend(int(instr[0] + instr[12:20] + instr[11] + instr[1:11] + "0", 2), 21)
        registers[rd] = PC + 4
        PC += imm_j - 4
    
    # elif opcode == "0010111":  # AUIPC
    #     a=0 not sure if we add this or not?
    
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
