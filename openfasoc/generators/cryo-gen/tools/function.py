################ modules for HSPICE sim ######################
##############################################################
#########   varmap definition             ####################
##############################################################
### This class is to make combinations of given variables ####
### mostly used for testbench generation     #################
### EX: varmap1=HSPICE_varmap.varmap(4) %%num of var=4 #######
###     varmap1.get_var('vdd',1.5,1.8,0.2) %%vdd=1.5:0.2:1.8##
###     varmap1.get_var('abc', ........ %%do this for 4 var ##
###     varmap1.cal_nbigcy()             %%end of var input###
###     varmap1.combinate  %%returns variable comb 1 by 1 ####
##############################################################


class varmap:
    # def __init__(self,num_var):
    # 	self.n_smlcycle=1
    # 	self.last=0
    # 	self.smlcy=1
    # 	self.bigcy=0
    # 	self.vv=0
    # 	self.vf=1
    # 	self.size=num_var
    # 	self.map=[None]*self.size
    # 	self.comblist=[None]*self.size
    # 	self.nvar=0
    def __init__(self) -> None:
        self.n_smlcycle = 1
        self.last = 0
        self.smlcy = 1
        self.bigcy = 0
        self.vv = 0
        self.vf = 1
        # self.map=[None]
        # self.comblist=[None]
        self.nvar = 0

    def get_var(self, name, start, end, step) -> None:
        if self.nvar == 0:
            self.map = [None]
            self.comblist = [None]
        else:
            self.map.append(None)
            self.comblist.append(None)
        self.map[self.nvar] = list([name])
        self.comblist[self.nvar] = list([name])
        self.nswp = (end - start) // step + 1
        for i in range(1, self.nswp + 1):
            self.map[self.nvar].append(start + step * (i - 1))
        self.nvar += 1

    def cal_nbigcy(self) -> None:
        self.bias = [1] * (len(self.map))
        for j in range(1, len(self.map) + 1):
            self.n_smlcycle = self.n_smlcycle * (len(self.map[j - 1]) - 1)
        self.n_smlcycle = self.n_smlcycle * len(self.map)

    def increm(self, inc) -> None:  # increment bias
        self.bias[inc] += 1
        if self.bias[inc] > len(self.map[inc]) - 1:
            self.bias[inc] % len(self.map[inc]) - 1

    def check_end(
        self, vf
    ) -> int:  # When this is called, it's already last stage of self.map[vf]
        self.bias[vf] = 1
        # 		if vf==0 and self.bias[0]==len(self.map[0])-1:
        # 			return 0
        if (
            self.bias[vf - 1] == len(self.map[vf - 1]) - 1
        ):  # if previous column is last element
            self.check_end(vf - 1)
        else:
            self.bias[vf - 1] += 1
            return 1

    def combinate(self) -> None:
        # 		print self.map[self.vv][self.bias[self.vv]]
        self.smlcy += 1
        if self.vv == len(self.map) - 1:  # last variable
            self.bigcy += 1
            for vprint in range(0, len(self.map)):
                self.comblist[vprint].append(self.map[vprint][self.bias[vprint]])
                # print self.map[vprint][self.bias[vprint]]
            if self.bias[self.vv] == len(self.map[self.vv]) - 1:  # last element
                if self.smlcy < self.n_smlcycle:
                    self.check_end(self.vv)
                    self.vv = (self.vv + 1) % len(self.map)
                    self.combinate()
                else:
                    pass
            else:
                self.bias[self.vv] += 1
                self.vv = (self.vv + 1) % len(self.map)
                self.combinate()
        else:
            self.vv = (self.vv + 1) % len(self.map)
            self.combinate()


##############################################################
#########   netmap                    ########################
##############################################################
### This class is used for replacing lines    ################
### detects @@ for line and @ for nets #######################
##############################################################
# --------   EXAMPLE   ---------------------------------------#
### netmap1=netmap(2) %input num_var #########################
### netmap1.get_var('ab','NN',1,4,1) %flag MUST be 2 char ####
## netmap2.get_var('bc','DD',2,5,1) %length of var must match#
# !!caution: do get_var in order, except for lateral prints ##
### which is using @W => varibales here, do get_var at last ##
### for line in r_file.readlines():###########################
###     netmap1.printline(line,w_file) #######################
##############################################################


class netmap:
    # def __init__(self,num_var):
    # 	self.size=num_var
    # 	self.map=[None]*self.size
    # 	self.flag=[None]*self.size
    # 	self.name=[None]*self.size
    # 	self.nnet=[None]*self.size
    # 	self.nn=0
    # 	self.pvar=1
    # 	self.cnta=0
    # 	self.line_nvar=0      # index of last variable for this line
    # 	self.nxtl_var=0      # index of variable of next line
    # 	self.ci_at=100
    def __init__(self) -> None:
        self.nn = 0
        self.pvar = 1
        self.cnta = 0
        self.line_nvar = 0  # index of last variable for this line
        self.nxtl_var = 0  # index of variable of next line
        self.ci_at = -5

    def get_net(
        self, flag, netname, start, end, step
    ) -> None:  # if start==None: want to repeat without incrementation(usually for tab) (end)x(step) is the num of repetition
        if self.nn == 0:
            self.map = [None]
            self.flag = [None]
            self.name = [None]
            self.nnet = [None]
        else:
            self.map.append(None)
            self.name.append(None)
            self.flag.append(None)
            self.nnet.append(None)
        if netname == None:
            self.name[self.nn] = 0
        else:
            self.name[self.nn] = 1
        self.map[self.nn] = list([netname])
        self.flag[self.nn] = flag
        if start != None and start != "d2o":
            self.nnet[self.nn] = int((end - start + step / 10) // step + 1)
            if self.name[self.nn] == 1:
                for i in range(1, self.nnet[self.nn] + 1):
                    self.map[self.nn].append("")
            else:
                for i in range(1, self.nnet[self.nn] + 1):
                    self.map[self.nn].append(start + step * (i - 1))
        elif start == "d2o":
            for i in range(0, end):
                if step - i > 0:
                    self.map[self.nn].append(1)
                else:
                    self.map[self.nn].append(0)
                i += 1
        else:
            self.map[self.nn] = list([netname])
            for i in range(1, step + 1):
                self.map[self.nn].append(end)
        # 			self.map[self.nn]=[None]*step
        # 			for i in range(1,self.nnet[self.nn]+1):
        # 				self.map[self.nn][i]=None
        self.nn += 1
        # print self.map

    def add_val(self, flag, netname, start, end, step) -> None:
        varidx = self.flag.index(flag)
        if start != None:
            nval = int((end - start + step / 10) // step + 1)
            for i in range(1, nval + 1):
                self.map[varidx].append(start + step * (i - 1))
        else:
            for i in range(1, step + 1):
                self.map[varidx].append(end)

    def printline(self, line, wrfile) -> None:
        if line[0:2] == "@@":
            # print('self.ci_at=%d'%(self.ci_at))
            self.nline = line[3 : len(line)]
            self.clist = list(self.nline)  # character list
            # print(self.clist,self.nxtl_var)
            for iv in range(1, len(self.map[self.nxtl_var])):
                for ci in range(0, len(self.clist)):
                    if (ci == self.ci_at + 1 or ci == self.ci_at + 2) and ci != len(
                        self.clist
                    ) - 1:
                        pass
                    elif self.clist[ci] == "@":
                        # print self.cnta
                        self.cnta += 1
                        self.line_nvar += 1
                        varidx = self.flag.index(
                            self.clist[ci + 1] + self.clist[ci + 2]
                        )
                        if self.name[varidx]:
                            wrfile.write(self.map[varidx][0])
                        # 	print(self.map[varidx])
                        if type(self.map[varidx][self.pvar]) == float:
                            wrfile.write(
                                "%e" % (self.map[varidx][self.pvar])
                            )  # modify here!!!!
                        elif type(self.map[varidx][self.pvar]) == int:
                            wrfile.write("%d" % (self.map[varidx][self.pvar]))
                        self.ci_at = ci
                    elif ci == len(self.clist) - 1:  # end of the line
                        if (
                            self.pvar
                            == len(self.map[self.nxtl_var + self.line_nvar - 1]) - 1
                        ):  # last element
                            self.pvar = 1
                            self.nxtl_var = self.nxtl_var + self.line_nvar
                            self.line_nvar = 0
                            self.cnta = 0
                            self.ci_at = -6
                            # print('printed all var for this line, %d'%(ci))
                        else:
                            self.pvar += 1
                            # self.line_nvar=self.cnta
                            self.line_nvar = 0
                            # print ('line_nvar= %d'%(self.line_nvar))
                            self.cnta = 0
                        wrfile.write(self.clist[ci])
                    else:
                        wrfile.write(self.clist[ci])
        elif line[0:2] == "@W":
            # print('found word line')
            self.nline = line[3 : len(line)]
            self.clist = list(self.nline)
            for ci in range(0, len(self.clist)):
                if ci == self.ci_at + 1 or ci == self.ci_at + 2:
                    pass
                elif self.clist[ci] == "@":
                    varidx = self.flag.index(self.clist[ci + 1] + self.clist[ci + 2])
                    for iv in range(1, len(self.map[varidx])):
                        if self.name[varidx]:
                            wrfile.write(self.map[varidx][0])
                        wrfile.write("%d	" % (self.map[varidx][iv]))
                        print(
                            "n is %d, varidx=%d, iv=%d"
                            % (self.map[varidx][iv], varidx, iv)
                        )
                    self.ci_at = ci
                else:
                    wrfile.write(self.clist[ci])
            self.ci_at = -5
        else:
            wrfile.write(line)


##############################################################
#########   resmap                    ########################
##############################################################
### This class is used to deal with results   ################
### detects @@ for line and @ for nets #######################
##############################################################
# --------   EXAMPLE   ---------------------------------------#
### netmap1=netmap(2) %input num_var #########################
### netmap1.get_var('ab','NN',1,4,1) %flag MUST be 2 char ####
## netmap2.get_var('bc','DD',2,5,1) %length of var must match#
### for line in r_file.readlines():###########################
###     netmap1.printline(line,w_file) #######################
###### self.tb[x][y][env[]]###############################
##############################################################


class resmap:
    def __init__(self, num_tb, num_words, index) -> None:  # num_words includes index
        self.tb = [None] * num_tb
        self.tbi = [None] * num_tb
        self.vl = [None] * num_tb
        self.vlinit = [None] * num_tb
        self.svar = [None] * num_tb
        self.index = index
        self.nenv = 0
        self.num_words = num_words
        self.vr = [None] * (num_words + index)  # one set of variables per plot
        self.vidx = [None] * (num_words + index)
        self.env = [None] * (num_words + index)
        # 		self.vl=[None]*(num_words+index)             #one set of variables per plot
        for itb in range(0, len(self.tb)):
            # 	self.tb[itb].vr=[None]*(num_words+index)
            self.tbi[itb] = 0  # index for counting vars within tb
            self.vl[itb] = [None] * (num_words + index)
            self.vlinit[itb] = [0] * (num_words + index)

    def get_var(self, ntb, var) -> None:
        self.vr[self.tbi[ntb]] = var
        # 		self.vl[ntb][self.tbi[ntb]]=list([None])
        self.tbi[ntb] += 1
        if self.tbi[ntb] == len(self.vr):  # ????????
            self.tbi[ntb] = 0

    def add(self, ntb, value) -> None:
        if self.vlinit[ntb][self.tbi[ntb]] == 0:  # initialization
            self.vl[ntb][self.tbi[ntb]] = [value]
            self.vlinit[ntb][self.tbi[ntb]] += 1
        else:
            self.vl[ntb][self.tbi[ntb]].append(value)
        self.tbi[ntb] = (self.tbi[ntb] + 1) % len(self.vr)

    def plot_env(
        self, ntb, start, step, xvar, xval
    ) -> None:  # setting plot environment: if ntb=='all': x axis is in terms of testbench
        if ntb == "all":
            self.nenv += 1
            self.xaxis = [None] * len(self.tb)
            for i in range(0, len(self.tb)):
                self.xaxis[i] = start + i * step
            self.vidx[self.nenv] = self.vr.index(xvar)
            # print self.vl[0][self.vidx[self.nenv]]
            print("", self.vl[0][self.vidx[self.nenv]])
            self.env[self.nenv] = [
                i
                for (i, x) in enumerate(self.vl[0][self.vidx[self.nenv]])
                if x == "%s" % (xval)
            ]
        else:
            self.nenv += 1
            self.xaxis = [None]  # one output
            self.xaxis = [start]
            self.vidx[self.nenv] = self.vr.index(xvar)
            self.env[self.nenv] = [
                i
                for (i, x) in enumerate(self.vl[0][self.vidx[self.nenv]])
                if x == "%s" % (xval)
            ]

    def rst_env(self) -> None:
        self.vidx[self.nenv] = None
        self.env[self.nenv] = 0
        self.nenv = 0
        # print self.vl[0][self.vidx[self.nenv]]

    def plot_y(self, yvar) -> None:
        self.yidx = self.vr.index(yvar)
        print("yidx=%d" % (self.yidx))
        # print self.vl[0][self.yidx][self.env[self.nenv][0]]
        print("", self.vl[0][self.yidx][self.env[self.nenv][0]])
        self.yaxis = [None] * len(self.xaxis)
        for xx in range(0, len(self.xaxis)):
            self.yaxis[xx] = self.vl[xx][self.yidx][self.env[self.nenv][0]]
        # plt.plot(self.xaxis,self.yaxis)
        # plt.ylabel(self.vr[self.yidx])

    def sort(self, var) -> None:
        varidx = self.vr.index(var)
        for k in range(len(self.vl)):  # all testbenches
            self.svar[k] = {}  # define dict
            for i in range(len(self.vl[0][0])):  # all values
                self.svar[k][self.vl[k][varidx][i]] = []
                for j in range(len(self.vr)):  # all variables
                    if j != varidx:
                        self.svar[k][self.vl[k][varidx][i]].append(self.vl[k][j][i])
                # 	if k==0:
                # 		print self.svar[k]
