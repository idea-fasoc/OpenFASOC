import gdsfactory as gf
import warnings
from gdsfactory.generic_tech import get_generic_pdk
warnings.filterwarnings('ignore')
import layers
import subcon

def nfet_03p3(width,length):
    comp = gf.Component("nfet")
    contact_no = round((width-0.07)/(0.22+0.28))
    nfet_contactl = [0]*(contact_no);
    nfet_contactr = [0]*(contact_no);
    if (width >= 0.4):
        nfet_nplus = comp << layers.nplus(0.44*2+length+0.16*2,width+(0.22*2)+0.02,32)
        nfet_diffr = comp << layers.diff(0.44,width,22)
        nfet_diffl = comp << layers.diff(0.44,width,22)
        nfet_diffm = comp << layers.diff(length,width,22)
        nfet_poly  = comp << layers.poly(length,width+(0.22*2),30)
        nfet_metal1_le  = comp << layers.metal1(0.38,width+0.02,34)
        nfet_metal1_ri  = comp << layers.metal1(0.38,width+0.02,34)
        nfet_sub_contact = comp << subcon.sub_contact(width)   
        nfet_sub_contact.movex(-(0.44+0.26))
        if (contact_no >=1):
            for i in range(contact_no):
                nfet_contactl[i] = comp << layers.contact(0.22,0.22,33)
                nfet_contactr[i] = comp << layers.contact(0.22,0.22,33)
                nfet_contactl[i].movex(0.16+0.07).movey((0.22+0.01+0.07)+i*(0.5))
                nfet_contactr[i].movex(0.16+0.44+length+0.15).movey(0.22+0.01+0.07+i*(0.5))
        else:
            nfet_contactle = comp << layers.contact(0.22,0.22,33)
            nfet_contactri = comp << layers.contact(0.22,0.22,33)
            nfet_contactle.movex(0.16+0.07).movey(0.22+0.01+0.07)
            nfet_contactri.movex(0.16+0.44+length+0.15).movey(0.22+0.01+0.07)
    
        nfet_diffl.movex(0.16).movey(0.22+0.01)
        nfet_diffr.movex(0.16+(0.44+length)).movey(0.22+0.01)
        nfet_diffm.movex(0.16+0.44).movey(0.22+0.01)
        nfet_poly.movex(0.16+0.44).movey(0.01)
        nfet_metal1_le.movex(0.16-0.01).movey(0.22)
        nfet_metal1_ri.movex(0.16+(0.44+length+0.07)).movey(0.22)
            
    else:
        nfet_nplus = comp << layers.nplus(0.46*2+length+0.16*2,width+(0.22*2)+0.02,32)
        nfet_diffr = comp << layers.diff(0.36,width+0.14,22)
        nfet_diffl = comp << layers.diff(0.36,width+0.14,22)
        nfet_diffm = comp << layers.diff(length+0.2,width,22)
        nfet_poly  = comp << layers.poly(length,width+(0.22*2),30)
        nfet_contactle = comp << layers.contact(0.22,0.22,33)
        nfet_contactri= comp << layers.contact(0.22,0.22,33) 
        nfet_metal1_le  = comp << layers.metal1(0.38,width+0.14+0.02,34)
        nfet_metal1_ri  = comp << layers.metal1(0.38,width+0.14+0.02,34)
        nfet_sub_contact = comp << subcon.sub_contact(width)   
        nfet_sub_contact.movex(-(0.44+0.26))

        nfet_diffl.movex(0.16).movey(0.22+0.01-0.07)
        nfet_diffr.movex(0.16+(0.46+length+0.1)).movey(0.22+0.01-0.07)
        nfet_diffm.movex(0.16+0.36).movey(0.22+0.01)
        nfet_poly.movex(0.16+0.46).movey(0.01)
        nfet_contactle.movex(0.16+0.07).movey(0.22+0.01)
        nfet_contactri.movex(0.16+0.46+length+0.17).movey(0.22+0.01)
        nfet_metal1_le.movex(0.16-0.01).movey(0.22-0.07)
        nfet_metal1_ri.movex(0.16+(0.46+length+0.09)).movey(0.22-0.07)
         
    
    return comp
    
pc3 = nfet_03p3(1,1)
#pc1.show()