#
### file list
##### a. input_gen.py : input file generation script
##### b. result.py : mt0 parsing/calculation scipt => copied automatically to result directory 'dir_name'
##### c. spice template file

##### 1. input file generation
##### ./> python input_gen.py template_file_name

##### 2. run sim
##### ./dir_name> source run_sim

##### 3. parse mt0 & calculate 
##### ./dir_name> source cal_result



import sys
import os
import shutil
import function
import TEMP_netlist


##### Directory name for result files
dir_name = 'run'


##### Result directory generation
try:
	os.mkdir(dir_name)
except FileExistsError:
	print("Directory ", dir_name , "already exists")

##### get template file name from cmd
file_name = sys.argv[1]
#pex_path = "/afs/eecs.umich.edu/vlsida/projects/FASoC/TSMC_65LP/TEMP/SIM/tsweep_pex/tempsenseInst.pex.netlist"
pex_path = os.path.dirname(os.path.abspath(__file__))
#pex_path = "/afs/eecs.umich.edu/vlsida/projects/FASoC/TSMC_65LP/TEMP/SIM/tsweep_pex/tempsenseInst-skywater.pex.netlist" 


#### need to write No. of stages
stage_start = 6
stage_stop = 8
stage_step = 2

##### need to write No. of header cells start/stop/step
header_start = 9
header_stop = 9
header_step = 2


##### need to write temperature start/stop/step
temp_start = -20
temp_stop = 100
temp_step = 20

##### simulation points calculation
stage_points = int((stage_stop - stage_start) / stage_step)
header_points = int((header_stop - header_start) / header_step)
temp_points = int((temp_stop - temp_start) / temp_step)


##### sweep stage calculation
stage_var=[]
for i in range(0, stage_points+1):
	stage_var.append(stage_start + i*stage_step)
#stage_var = [4]
##### sweep header cell calculation
header_var=[]
for i in range(0, header_points+1):
	header_var.append(header_start + i*header_step)
#header_var = [1]

print(stage_var)
print(header_var)

##### sweep temperature calculation
temp_var=[]
for i in range(0, temp_points+1):
	temp_var.append(temp_start + i*temp_step)


##### template file loading
r_file = open(file_name, "r")
lines = r_file.readlines()

##### hspice input file generation with stage and header
for i in range(0, len(stage_var)):
	for j in range(0, len(header_var)):
		os.mkdir("./%s/inv%d_header%d"%(dir_name, stage_var[i], header_var[j]))
		TEMP_netlist.gen_temp_netlist(dir_name, stage_var[i], header_var[j])
		for t in range(0, len(temp_var)):
			w_file0 = open("./%s/inv%d_header%d/%s_%e.sp"%(dir_name, stage_var[i], header_var[j], file_name, temp_var[t]), "w")
			for line in lines:
				if line[0:2] == '@@':
					nline = line[3:len(line)]
					clist = list(nline)
					for ci in range(0, len(clist)):
						if clist[ci] == '@':
							w_file0.write('%e'%(temp_var[t]))
						elif clist[ci] == '$':
							w_file0.write('%s/run/inv%d_header%d/TEMP_stage%dheader%d.sp'%(pex_path, stage_var[i], header_var[j], stage_var[i], header_var[j]))
						elif clist[ci] == '#':
							w_file0.write('%s_%e.mt0'%(file_name, temp_var[t]))
						else:
							w_file0.write(clist[ci])
				else:
					w_file0.write(line)
		w_file1 = open("./%s/inv%d_header%d/run_sim"%(dir_name,stage_var[i], header_var[j]), "w") ##run_simgeneration
		for k in range(0, len(temp_var)):
			#data = "ngspice -b -o %s_%e.log %s_%e.sp \n"%(file_name, temp_var[k], file_name, temp_var[k])
                	#data = "spectre %s_%e.sp >log &\n"%(file_name, temp_var[k])
			data = "finesim -spice -np 8 %s_%e.sp > %s_%e.log &\n"%(file_name, temp_var[k], file_name, temp_var[k])
			w_file1.write(data)
			#data = "python reshape.py %s_%e\n"%(file_name, temp_var[k])
			#w_file1.write(data)
			#w_file1.write("rm %s_%e.mt0\nmv new_%s_%e.mt0 %s_%e.mt0\n" %(file_name, temp_var[k], file_name, temp_var[k], file_name, temp_var[k]))
		w_file2 = open("./%s/inv%d_header%d/cal_result"%(dir_name, stage_var[i], header_var[j]), "w")
		for m in range(0, len(temp_var)):
			data = "python result.py %s_%e.mt0 >>code_result\n"%(file_name, temp_var[m])
			w_file2.write(data)
		com = "python result_error.py >> code_result_with_error\n"
		w_file2.write(com)
		w_file3 = open("./%s/inv%s_header%s/mt0_list"%(dir_name, stage_var[i], header_var[j]), "w")
		for l in range(0, len(temp_var)):
			data = "%s_%e.mt0\n"%(file_name, temp_var[l])
			w_file3.write(data)

		#shutil.copy2("./reshape.py", '%s/inv%d_header%d'%(dir_name,stage_var[i], header_var[j]))
		shutil.copy2("./result.py", '%s/inv%d_header%d'%(dir_name,stage_var[i], header_var[j]))
		shutil.copy2("./result_error.py", '%s/inv%d_header%d'%(dir_name,stage_var[i], header_var[j]))

#folders = os.listdir("./%s"%(dir_name))
#current = os.getcwd()
#w_file4 = open("./run_sim_top","w")
#for folder in folders:
#	os.chdir("%s/%s/%s"%(current,dir_name,folder))
#	os.system("source run_sim")
	
#	data = "source ./%s/%s/run_sim\n"%(dir_name,folder)
#	w_file4.write(data) 	
