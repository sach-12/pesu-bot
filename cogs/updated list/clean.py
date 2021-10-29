import time

dat = ''
fp1 = open("batch_list_2021(old).csv", "r")
fp2 = open("batch_list_2021.csv", "a")
for line in fp1:
    x = line.split(',')
    if(len(x) == 10 and x[3] == "Sem-1"):
        if("PG" in x[1]):
            continue
        # print(x)
        dat = f"{x[0]},{x[1]},{x[3]},{x[4]},{x[5]},{x[6]},{x[7]},{x[8]}\n"
        # print(dat)
        # fp2.write(dat)
        # print("NEXT!!!")
    # time.sleep(1)
print("done")

fp1.close()
fp2.close()
fp2 = open("batch_list_2021.csv", "r")
br_list = []
for line in fp2:
    dat = line.split(',')
    role_str = (dat[-2])
    # print(role_str)
    if(role_str not in br_list):
        br_list.append(role_str)
print(br_list)