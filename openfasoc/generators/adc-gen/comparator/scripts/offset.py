################Description############################
#                                                     # 
# This scripts is to draw the high output possability #
# versus input offset. The plot will give you a clear #
# understanding of the offset range                   #
#                                                     #
#######################################################
import numpy as np
import re
import matplotlib.pyplot as plt

def Str2Value(s):
    data = re.split('  | ',s)
    vip = float(data[2])
    vin = float(data[3])
    vout = float(data[4])
    return vip, vin, vout

############## Double-Tail Latch-Type ##########################

f = open("../output/comparator.out","r")
lines = f.read().splitlines()
f.close()

#print(lines)
#print(Str2Value(lines[11]))

dict = {}
num = {}

for i in range(1,len(lines)):
    vip, vin, vout = Str2Value(lines[i])
    vid = float(np.round(vip - vin, 4))
    if(dict.get(vid) == None):
        num[vid] = 1
        if(vout > 3):
            dict[vid] = 1
        else:
            dict[vid] = 0
    else:
        num[vid] = num[vid] + 1
        if(vout > 3):
            dict[vid]  = dict[vid] + 1
print("# of high: ", dict)
print("total #: ", num)

x = []
y = []
for key in dict:
    x.append(key*1000)
    y.append(np.round(float(dict[key])/num[key],4))

print("x: ", x)
print("y: ", y)

plt.plot(x,y,marker='o',color='r',label='Double-Tail')


#################### self-calibrating ###############


# f = open("../output/comparator_self.out","r")
# lines = f.read().splitlines()
# f.close()


# dict = {}
# num = {}

# for i in range(1,len(lines)):
#     vip, vin, vout = Str2Value(lines[i])
#     vid = float(np.round(vip - vin, 4))
#     if(dict.get(vid) == None):
#         num[vid] = 1
#         if(vout > 3):
#             dict[vid] = 1
#         else:
#             dict[vid] = 0
#     else:
#         num[vid] = num[vid] + 1
#         if(vout > 3):
#             dict[vid]  = dict[vid] + 1
# print("# of high: ", dict)
# print("total #: ", num)

# x = []
# y = []
# for key in dict:
#     x.append(key*1000)
#     y.append(np.round(float(dict[key])/num[key],4))
    
# print("x: ", x)
# print("y: ", y)

# plt.plot(x,y,marker='o',color='g',label='Self-Calibrating')



#################### StrongArm ###############


f = open("../output/comparator_strongarm.out","r")
lines = f.read().splitlines()
f.close()


dict = {}
num = {}

for i in range(1,len(lines)):
    vip, vin, vout = Str2Value(lines[i])
    vid = float(np.round(vip - vin, 4))
    if(dict.get(vid) == None):
        num[vid] = 1
        if(vout > 3):
            dict[vid] = 1
        else:
            dict[vid] = 0
    else:
        num[vid] = num[vid] + 1
        if(vout > 3):
            dict[vid]  = dict[vid] + 1
print("# of high: ", dict)
print("total #: ", num)

x = []
y = []
for key in dict:
    x.append(key*1000)
    y.append(np.round(float(dict[key])/num[key],4))
    
print("x: ", x)
print("y: ", y)

plt.plot(x,y,marker='o',color='y',label='StrongARM')





# #####################complete the plot##########################



plt.xlabel("vip - vin [mV]")
plt.ylabel("possibility(output=HIGH) [%]")
plt.legend()
plt.show()
