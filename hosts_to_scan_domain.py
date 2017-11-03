# -*- coding: utf-8 -*-
tmp=""
fp = open("tmp_out.txt", "w")
for line in open("tmp.txt", "r"):
    if line.find("#") == 0:
        continue
    if line.find("#") > 0:
        #pass
        try:
            #tmp = tmp + line.split()[1] + " " +line.split()[2] + "\r\n"
            tmp = tmp + line.split()[1] + "\r\n"
        except:
            pass
    if line.find("#") == -1:
        try:
            tmp = tmp + line.split()[1] + "\r\n"
        except:
            pass

try:
    fp.write(tmp)
finally:
    fp.close()
