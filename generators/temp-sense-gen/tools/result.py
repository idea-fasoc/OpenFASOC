
import sys

##### get result file name from cmd
file_name = sys.argv[1]

##### open mt0 file
r_mt0 = open(file_name)
mt0_lines=r_mt0.readlines()

##### mt0 parse & data organizing
##### actual data starts from line 4
data_start_line = 4
result = list()
result = mt0_lines[data_start_line-1].split()

##### print to output file
#print("%s	%s        %s"%(result[3], result[1], result[2]))
print("%s	%s        %s"%(result[4], result[1], result[2]), file=open("code_result", "a"))

