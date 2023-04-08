import gdsfactory as gf
import warnings
from gdsfactory.generic_tech import get_generic_pdk
warnings.filterwarnings('ignore')
import layers
import subcon
import nwellcon

@gf.cell
def pfet_03p3(width,length):
    comp = gf.Component("pfet")
    contact_no = round((width-0.07)/(0.22+0.28))
    pfet_contactl = [0]*(contact_no);
    pfet_contactr = [0]*(contact_no);
    if (width >= 0.4):
        pfet_pplus = comp << layers.pplus(0.44*2+length+0.16*2,width+(0.22*2)+0.02,31)
        pfet_nwell = comp << layers.nwell((0.44*2+length+0.16*2)+(0.27*2),(width+(0.22*2)+0.02)+(0.27*2),21)
        pfet_diffr = comp << layers.diff(0.44,width,22)
        pfet_diffl = comp << layers.diff(0.44,width,22)
        pfet_diffm = comp << layers.diff(length,width,22)
        pfet_poly  = comp << layers.poly(length,width+(0.22*2),30)
        pfet_metal1_le  = comp << layers.metal1(0.38,width+0.02,34)
        pfet_metal1_ri  = comp << layers.metal1(0.38,width+0.02,34)
        pfet_nwell_contact = comp << nwellcon.nwell_contact(width)   
        pfet_nwell_contact.movex(-(0.44+0.26+0.27))
        if (contact_no >=1):
            for i in range(contact_no):
                pfet_contactl[i] = comp << layers.contact(0.22,0.22,33)
                pfet_contactr[i] = comp << layers.contact(0.22,0.22,33)
                pfet_contactl[i].movex(0.16+0.07).movey((0.22+0.01+0.07)+i*(0.5))
                pfet_contactr[i].movex(0.16+0.44+length+0.15).movey(0.22+0.01+0.07+i*(0.5))
        else:
            pfet_contactle = comp << layers.contact(0.22,0.22,33)
            pfet_contactri = comp << layers.contact(0.22,0.22,33)
            pfet_contactle.movex(0.16+0.07).movey(0.22+0.01+0.07)
            pfet_contactri.movex(0.16+0.44+length+0.15).movey(0.22+0.01+0.07)
    
        pfet_nwell.movex(-0.27).movey(-0.27)
        pfet_diffl.movex(0.16).movey(0.22+0.01)
        pfet_diffr.movex(0.16+(0.44+length)).movey(0.22+0.01)
        pfet_diffm.movex(0.16+0.44).movey(0.22+0.01)
        pfet_poly.movex(0.16+0.44).movey(0.01)
        pfet_metal1_le.movex(0.16-0.01).movey(0.22)
        pfet_metal1_ri.movex(0.16+(0.44+length+0.07)).movey(0.22)
            
    else:
        pfet_pplus = comp << layers.pplus(0.46*2+length+0.16*2,width+(0.22*2)+0.02,32)
        pfet_nwell = comp << layers.nwell((0.46*2+length+0.16*2)+(0.27*2),(width+(0.22*2)+0.02)+(0.27*2),21)
        pfet_diffr = comp << layers.diff(0.36,width+0.14,22)
        pfet_diffl = comp << layers.diff(0.36,width+0.14,22)
        pfet_diffm = comp << layers.diff(length+0.2,width,22)
        pfet_poly  = comp << layers.poly(length,width+(0.22*2),30)
        pfet_contactle = comp << layers.contact(0.22,0.22,33)
        pfet_contactri= comp << layers.contact(0.22,0.22,33) 
        pfet_metal1_le  = comp << layers.metal1(0.38,width+0.14+0.02,34)
        pfet_metal1_ri  = comp << layers.metal1(0.38,width+0.14+0.02,34)
        pfet_nwell_contact = comp << nwellcon.nwell_contact(width)   
        pfet_nwell_contact.movex(-(0.44+0.26+0.27))

        pfet_nwell.movex(-0.27).movey(-0.27)
        pfet_diffl.movex(0.16).movey(0.22+0.01-0.07)
        pfet_diffr.movex(0.16+(0.46+length+0.1)).movey(0.22+0.01-0.07)
        pfet_diffm.movex(0.16+0.36).movey(0.22+0.01)
        pfet_poly.movex(0.16+0.46).movey(0.01)
        pfet_contactle.movex(0.16+0.07).movey(0.22+0.01)
        pfet_contactri.movex(0.16+0.46+length+0.17).movey(0.22+0.01)
        pfet_metal1_le.movex(0.16-0.01).movey(0.22-0.07)
        pfet_metal1_ri.movex(0.16+(0.46+length+0.09)).movey(0.22-0.07)
            
    
    return comp
pc4 = pfet_03p3(2,4)
pc4
