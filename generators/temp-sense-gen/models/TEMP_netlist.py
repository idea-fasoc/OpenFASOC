##for HSPICE netlist
import function
import os


def gen_temp_netlist(dir_name, ninv, nhead):
	r_netlist=open("./TEMP_net_template.sp","r")
	lines=list(r_netlist.readlines())
	w_netlist=open("./%s/inv%d_header%d/TEMP_stage%dheader%d.sp"%(dir_name,ninv,nhead,ninv,nhead),"w")


	netmap1=function.netmap() #modify here
	netmap1.get_net('x1',None,1,1,1)
	netmap1.get_net('n0',None,ninv+1,ninv+1,1)
	netmap1.get_net('n1',None,1,1,1)
	netmap1.get_net('x2',None,1,ninv,1)
	netmap1.get_net('n2',None,1,ninv,1)
	netmap1.get_net('n3',None,2,ninv+1,1)
	netmap1.get_net('x3',None,1,1,1)
	netmap1.get_net('n4',None,ninv+1,ninv+1,1)
	netmap1.get_net('x4',None,1,nhead,1)
	for line in lines:
		netmap1.printline(line,w_netlist)

#def gen_temp_makefile(dir_name, folder):
#	r_makefile=open("./Makefile_template","r")
#	lines=list(r_makefile.readlines())
#	w_netlist=open("./Makefile","w")
#	
#	netmap1=function.netmap()
#	netmap1.get_net('n1', folder,1,1,1)
#			
#	for line in lines:
#		netmap1.printline(line,w_netlist)	
