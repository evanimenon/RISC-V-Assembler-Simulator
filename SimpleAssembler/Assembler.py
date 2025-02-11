
def extract(file_name):
    f = open(file_name,"r")
    for line in f:
        operation = line.split(" ")[0].strip()
        right = line.split(" ")[1].strip()
        print(operation," ",right)
    f.close()

extract("Ex_test_5")
