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
