import sys

riscv_r_type = {  
    "ADD":  {"opcode": "0110011", "func3": "000", "func7": "0000000"},  
    "SUB":  {"opcode": "0110011", "func3": "000", "func7": "0100000"},  
    "AND":  {"opcode": "0110011", "func3": "111", "func7": "0000000"},  
    "OR":   {"opcode": "0110011", "func3": "110", "func7": "0000000"},  
    "XOR":  {"opcode": "0110011", "func3": "100", "func7": "0000000"},  
    "SLL":  {"opcode": "0110011", "func3": "001", "func7": "0000000"},  
    "SRL":  {"opcode": "0110011", "func3": "101", "func7": "0000000"},  
    "SRA":  {"opcode": "0110011", "func3": "101", "func7": "0100000"},  
    "SLT":  {"opcode": "0110011", "func3": "010", "func7": "0000000"},  
    "SLTU": {"opcode": "0110011", "func3": "011", "func7": "0000000"}  
}

riscv_i_type = {  
    "ADDI": {"opcode": "0010011", "func3": "000", "func7": ""},  
    "ANDI": {"opcode": "0010011", "func3": "111", "func7": ""},  
    "ORI":  {"opcode": "0010011", "func3": "110", "func7": ""},  
    "XORI": {"opcode": "0010011", "func3": "100", "func7": ""},  
    "SLLI": {"opcode": "0010011", "func3": "001", "func7": "0000000"},  
    "SRLI": {"opcode": "0010011", "func3": "101", "func7": "0000000"},  
    "SRAI": {"opcode": "0010011", "func3": "101", "func7": "0100000"},  
    "LW":   {"opcode": "0000011", "func3": "010", "func7": ""},  
    "JALR": {"opcode": "1100111", "func3": "000", "func7": ""}  
}

riscv_s_type = {  
    "SW":   {"opcode": "0100011", "func3": "010", "func7": ""},  
    "SB":   {"opcode": "0100011", "func3": "000", "func7": ""},  
    "SH":   {"opcode": "0100011", "func3": "001", "func7": ""}  
}

riscv_b_type = {  
    "BEQ":  {"opcode": "1100011", "func3": "000", "func7": ""},  
    "BNE":  {"opcode": "1100011", "func3": "001", "func7": ""},  
    "BLT":  {"opcode": "1100011", "func3": "100", "func7": ""},  
    "BGE":  {"opcode": "1100011", "func3": "101", "func7": ""},  
    "BLTU": {"opcode": "1100011", "func3": "110", "func7": ""},  
    "BGEU": {"opcode": "1100011", "func3": "111", "func7": ""}  
}

riscv_u_type = {  
    "LUI":   {"opcode": "0110111", "func3": "", "func7": ""},  
    "AUIPC": {"opcode": "0010111", "func3": "", "func7": ""}  
}

riscv_j_type = {  
    "JAL": {"opcode": "1101111", "func3": "", "func7": ""}  
}


def int_to_binary(value, bit_width):
    """
    Convert an integer to its two's complement binary representation.
    
    :param value: The integer value to convert.
    :param bit_width: The number of bits to represent the value.
    :return: A string representing the binary two's complement representation.
    """
    if value < 0:
        value = (2 ** bit_width) + value  # Compute two's complement for negative numbers
    
    binary_representation = format(value & ((2 ** bit_width) - 1), f'0{bit_width}b')
    return binary_representation
    

def get_instruction_type(instr,data):
    PC = ''
    #Checks which type the instruction belongs to
    #note to self: instr and data are both strings
    if instr in riscv_r_type:
        Operands = data.split(',')
        PC += riscv_r_type[instr]['func7'] + riscv_registers[Operands[2]] + riscv_registers[Operands[1]] + riscv_r_type[instr]['func3'] + riscv_registers[Operands[0]] + riscv_r_type[instr]['opcode']
        #Above line is for conversion

    elif instr in riscv_i_type:
        info = data.split(',')
        Operands = [info[0],0,0]
        if instr in "JALRLW":
            Operands[1] = info[1].split('(')[1].strip(')')
            Operands[2] = int_to_binary(int(info[1].split('(')[0]),12)
            PC += Operands[2] + riscv_registers[Operands[1]] + riscv_i_type[instr]['func3'] + riscv_registers[Operands[0]] + riscv_i_type[instr]['opcode']
        else:
            Operands[1] = info[1]
            Operands[2] = int_to_binary(int(info[2]),12)
            PC += Operands[2] + riscv_registers[Operands[1]] + riscv_i_type[instr]['func3'] + riscv_registers[Operands[0]] + riscv_i_type[instr]['opcode']

    elif instr in riscv_s_type:
        rs2, offset_rs1 = data.split(',')
        offset, rs1 = offset_rs1.split('(')
        rs1 = rs1.strip(')')

        imm_bin = int_to_binary(int(offset), 12)
        imm_high, imm_low = imm_bin[:7], imm_bin[7:]

        PC += (imm_high + riscv_registers[rs2] + riscv_registers[rs1] +
               riscv_s_type[instr]['func3'] + imm_low + riscv_s_type[instr]['opcode'])

    elif instr in riscv_b_type:
        rs1, rs2, offset = data.split(',')
        imm_bin = int_to_binary(int(offset), 12)
        imm_high, imm_low = imm_bin[:7], imm_bin[7:]

        PC += (imm_high + riscv_registers[rs2] + riscv_registers[rs1] + 
               riscv_b_type[instr]['func3'] + imm_low + riscv_b_type[instr]['opcode'])

    elif instr in riscv_u_type:
        rd, imm = data.split(',')
        imm_bin = int_to_binary(int(imm), 20)   	
        PC += imm_bin + riscv_registers[rd] + riscv_u_type[instr]['opcode']
        
    elif instr in riscv_j_type:
        rd, imm = data.split(',')
        imm_bin = int_to_binary(int(imm), 21)
        imm_msb  = imm_bin[0]
        imm_high = imm_bin[1:11]
        imm_sep  = imm_bin[11]
        imm_low  = imm_bin[12:20]
        PC += imm_msb + imm_high + imm_sep + imm_low + riscv_registers[rd] + riscv_j_type[instr]['opcode']

    else:
        return "UNKNOWN"
    return PC

riscv_registers = {
    "x0":  "00000", "x1":  "00001", "x2":  "00010", "x3":  "00011",
    "x4":  "00100", "x5":  "00101", "x6":  "00110", "x7":  "00111",
    "x8":  "01000", "x9":  "01001", "x10": "01010", "x11": "01011",
    "x12": "01100", "x13": "01101", "x14": "01110", "x15": "01111",
    "x16": "10000", "x17": "10001", "x18": "10010", "x19": "10011",
    "x20": "10100", "x21": "10101", "x22": "10110", "x23": "10111",
    "x24": "11000", "x25": "11001", "x26": "11010", "x27": "11011",
    "x28": "11100", "x29": "11101", "x30": "11110", "x31": "11111",
    "zero":"00000", "ra":"00001", "sp":"00010", "gp":"00011", "tp":"00100",
    "t0":"00101", "t1":"00110", "t2":"00111", "s0":"01000", "fp":"01000", "s1":"01001", "a0":"01010",
    "a1":"01011", "a2":"01100", "a3":"01101", "a4":"01110", "a5":"01111", "a6":"10000", "a7":"10001", "s2":"10010", "s3":"10011", "s4":"10100",
    "s5":"10101", "s6":"10110", "s7":"10111", "s8":"11000", "s9":"11001", "s10":"11010", "s11":"11011", "t3":"11100", "t4":"11101", "t5":"11110", "t6":"11111"
}

def extract(file_name):
    main={} # general structure to be {operation:data}
    f = open(file_name,"r")
    for line in f:
        operation = line.split(" ")[0].strip()
        data = line.split(" ")[1].strip()
        main[operation.strip().upper()] = data
    f.close()
    return main

def write(main):
    f = open("binary.txt",'w')
    for i,j in main.items():
        bin = get_instruction_type(i,j)
        print(bin)
        f.write(bin) 
        f.write("\n")
    f.close()
    return main


main = extract("Ex_test_1.txt")

count = 1
for i,j in main.items():
    print(i,"-",j)
    count+=1
write(main)