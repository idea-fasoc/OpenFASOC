import gdsfactory as gf
import warnings
from gdsfactory.generic_tech import get_generic_pdk
warnings.filterwarnings('ignore')
import layers

@gf.cell
def sub_contact(width):
    comp = gf.Component("sub_contact")
    con_no = round((width-0.13)/(0.22+0.28))
    con = [0]*(con_no);
    pplus_con = comp << layers.pplus(0.44+(0.13*2),width+(0.22*2)+0.02,31)
    diff_con = comp << layers.diff(0.44,width,22)
    diff_con.movex(0.13).movey(0.22)
    if (con_no >=1):
        for k in range(con_no):
            con[k] = comp << layers.contact(0.22,0.22,33)
            con[k].movex(0.11+0.13).movey(0.13+0.16+k*0.5)
    else:
        subcon = comp << layers.contact(0.22,0.22,33)
        subcon.movex(0.11+0.13).movey(0.13+0.22)
    metal_con = comp << layers.metal1(0.44,width+0.02,34)
    metal_con.movex(0.13).movey(0.21)
    return comp

pc3 = sub_contact(2)
pc3.show()
