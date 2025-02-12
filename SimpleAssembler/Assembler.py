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


def get_instruction_type(instr):
    #Checks which type the instruction belongs to
    if instr in riscv_r_type:
        return "R"
    elif instr in riscv_i_type:
        return "I"
    elif instr in riscv_s_type:
        return "S"
    elif instr in riscv_b_type:
        return "B"
    elif instr in riscv_u_type:
        return "U"
    elif instr in riscv_j_type:
        return "J"
    else:
        return "UNKNOWN"

riscv_registers = {
    "x0":  "00000", "x1":  "00001", "x2":  "00010", "x3":  "00011",
    "x4":  "00100", "x5":  "00101", "x6":  "00110", "x7":  "00111",
    "x8":  "01000", "x9":  "01001", "x10": "01010", "x11": "01011",
    "x12": "01100", "x13": "01101", "x14": "01110", "x15": "01111",
    "x16": "10000", "x17": "10001", "x18": "10010", "x19": "10011",
    "x20": "10100", "x21": "10101", "x22": "10110", "x23": "10111",
    "x24": "11000", "x25": "11001", "x26": "11010", "x27": "11011",
    "x28": "11100", "x29": "11101", "x30": "11110", "x31": "11111"
}


def extract(file_name,riscv_instructions):
    main={} # general structure to be {operation:{rd:"",rs1:"",rs2:""}}
    f = open(file_name,"r")
    for line in f:
        operation = line.split(" ")[0].strip()
        main[operation] = {}
        right = line.split(" ")[1].strip()
        if (riscv_instructions[operation.upper()]['func7'] =="" and riscv_instructions[operation.upper()]['func3'] ==""):
            #something
        elif (riscv_instructions[operation.upper()]['func7'] ==""):
            #something
        else:
            #something

        rd = right.split(",")[0].strip()
        rs1 = right.split(",")[1].strip()
        rs2 = right.split(",")[2].strip()
        main[operation]["rd"] = rd
        main[operation]["rs1"] = rs1
        main[operation]["rs2"] = rs2
    for i,j in main.items():
        print(i,j)
    f.close()
    return main

extract("instruction.txt",riscv_instructions)

#main logic of the code, loop it around for every operation and we're done
main = {'instruction':['rd','rs1','rs2']}

PC = ''
PC += riscv_instructions['instruction'][2]
#add rs2
#add rs1
PC += riscv_instructions['instruction'][1]
#add rd
PC += riscv_instructions['instruction'][0]
print(PC)