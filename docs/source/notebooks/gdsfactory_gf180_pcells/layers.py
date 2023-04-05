import gdsfactory as gf
import warnings
from gdsfactory.generic_tech import get_generic_pdk
warnings.filterwarnings('ignore')
@gf.cell
def nplus(width,height,layerno):
    comp = gf.Component("nplus")
    nplus = gf.components.rectangle(size=(width,height),layer=layerno)
    nplus=comp << nplus
    return comp
@gf.cell
def pplus(width,height,layerno):
    comp = gf.Component("pplus")
    nplus = gf.components.rectangle(size=(width,height),layer=layerno)
    nplus=comp << nplus
    return comp
@gf.cell
def nwell(width,height,layerno):
    comp = gf.Component("nwell")
    nwell = gf.components.rectangle(size=(width,height),layer=layerno)
    nwell=comp << nwell
    return comp
@gf.cell
def diff(width,height,layerno):
    comp = gf.Component("diff")
    diff = gf.components.rectangle(size=(width,height),layer=layerno)
    diff=comp << diff
    return comp
@gf.cell
def poly(width,height,layerno):
    comp = gf.Component("poly")
    poly = gf.components.rectangle(size=(width,height),layer=layerno)
    poly=comp << poly
    return comp
@gf.cell
def contact(width,height,layerno):
    comp = gf.Component("contact")
    contact = gf.components.rectangle(size=(width,height),layer=layerno)
    contact=comp << contact
    return comp
@gf.cell
def metal1(width,height,layerno):
    comp = gf.Component("rect")
    metal1 = gf.components.rectangle(size=(width,height),layer=layerno)
    metal1=comp << metal1
    return comp
@gf.cell
def sab(width,height,layerno):
    comp = gf.Component("sab")
    sab = gf.components.rectangle(size=(width,height),layer=layerno)
    sab=comp << sab
    return comp

