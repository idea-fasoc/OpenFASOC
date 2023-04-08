import gdsfactory as gf
import warnings
from gdsfactory.generic_tech import get_generic_pdk
warnings.filterwarnings('ignore')
import layers
import nfet
import pfet

@gf.cell
def poly_contact():
    comp = gf.Component("poly_contact")
    poly_con = comp << layers.poly(0.36,0.36,30)
    con = comp << layers.contact(0.22,0.22,33)
    metal1_con = comp << layers.metal1(0.36,0.36,34)
    con.movex(0.07).movey(0.07)
    return comp
pc5 = poly_contact()

@gf.cell
def inverter(width,length,strength):
    comp = gf.Component("inverter")
    n_inst = comp << nfet.nfet_03p3(width,length)
    
    p_inst = comp << pfet.pfet_03p3(width*strength,length)  
    p_inst.movey((width+(0.22*2)+0.02)+(0.27*2)+1)
    
    gateext = comp << layers.poly(length,width+(0.22*2)+1,30)
    gateext.movex(0.16+0.44).movey(0.01+width+(0.22*2))
    
    dconn = comp << layers.metal1(0.38,width+(0.22*2)+1.52,34)
    dconn.movex(0.16+(0.44+length+0.07)).movey(0.01+width)
    
    sconn_n = comp << layers.metal1(0.38,1,34)
    sconn_n.movex(0.15).movey(-(1-0.22))
    
    sconn_p = comp << layers.metal1(0.38,1,34)
    sconn_p.movex(0.15).movey((((strength+1)*width)+(0.22*2)+0.02)+(0.27*2)+1+0.22+0.02)
    
    nwell_conn = comp << layers.metal1(1,(0.44*2+length+0.16*2),34)
    nwell_conn.rotate(-90)
    nwell_conn.movey((((strength+1)*width)+(0.22*2)+0.02)+(0.27*2)+1+0.22+0.02+2)
    
    sub_conn = comp << layers.metal1(1,(0.44*2+length+0.16*2),34)
    sub_conn.rotate(-90)
    sub_conn.movey(-(1-0.22))
    
    gateconn = comp << poly_contact()
    gateconn.movex(0.16+0.08).movey(0.01+width+(0.22*2)+0.5)
    
    input_conn = comp << layers.metal1(1,0.36,34)
    input_conn.rotate(180)
    input_conn.movex(0.16+0.08).movey(0.01+width+(0.22*2)+0.5+0.36)
    
    output_conn = comp << layers.metal1(1,0.36,34)
    output_conn.movex(0.16+0.08+length+0.36+0.07).movey(0.01+width+(0.22*2)+0.5)
    
    return comp

