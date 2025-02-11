
def extract(file_name):
    main={}
    f = open(file_name,"r")
    for line in f:
        operation = line.split(" ")[0].strip()
        right = line.split(" ")[1].strip()
        rd = right.split(",")[0].strip()
        rs1 = right.split(",")[1].strip()
        #rs2 = right.split(",")[2].strip()
        main[operation] = {}
        main[operation]["rd"] = rd
        main[operation]["rs1"] = rs1
        #main[operation]["rs2"] = rs2
    for i,j in main.items():
        print(i,j)
    f.close()
    return main

extract("Ex_test_5.txt")

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