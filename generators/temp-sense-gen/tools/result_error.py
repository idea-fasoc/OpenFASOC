
import math
import numpy
import os

genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)),"../")

##### read mt0_list, remove \n
r_mt0_list = open(genDir + "./mt0_list", "r")
print(r_mt0_list)
mt0_files = r_mt0_list.readlines()
new_list = list()
for line in mt0_files:
	stripped = line.strip()
	new_list.append(stripped)

mt0_files = new_list
##### get data from mt0_files with column number of 'data_col'
##### generate list with result data [[temp_var0], [temp_var1], [temp_var2], ...]
data0 = list()
data_temp = list()
for mt0_line in mt0_files:
	#print(mt0_line)
	r_file = open(genDir + "./%s"%(mt0_line))
	mt0_data = r_file.readlines()
	data_col = 1
	data_temp.append(mt0_data[3].split())
for line in data_temp:
	data0.append(line[0])



#
#print(data0)
#### calculate T X freq
data1 = list()

i=0
data_temp = list()
for val in data0:
	if val == 'failed':
		val_cal = 'failed'
	else:
		#print(val_cal)
		print(val)
		val_cal = math.log(1/float(val))*((-20+i*20)+273.15)*0.01
	data1.append(val_cal)
	print("postif")
	i=i+1



#
#
#
##### slope correction & row<->col switch
data2 = list()



print("%s    "%(data1))

data_temp0 = list()
slope_f = 80/(data1[len(data1)-2]-data1[1])
#print(slope_f)
data_temp1 = list()
for k in data1:
	if k == 'failed':
		val = 'failed'
		data2.append(val)
	else:
		val = k * slope_f
		data2.append(val)


#### offset correction
data3 = list()

for val in data2:
	offset = data2[1]
	if val == 'failed':
		val = 'failed'
	else:
		val = val - offset
#	data_temp = list()
#	for val in line:
	data3.append(val)
#	data3.append(data_temp)

##### temperature error calculation
data4 = list()
i=0
for val in data3:
	if val == 'failed':
		val = 'failed'
	else:
		val=(-20+i*20)-val
	data4.append(val)
	i=i+1
#print(data4)


r_result_list = open(genDir + "./code_result", "r")
result_lines= r_result_list.readlines()
result_list = list()
result_tmep = list()
i=0
print(os.getcwd())
print('Temp  Frequency Power Error ')
for line in result_lines:
	result_list = result_lines[i].split()
	print('%s %s %s %s'%(result_list[0], result_list[1], result_list[2], data4[i]), file=open("all_result", "a"))
	i=i+1




