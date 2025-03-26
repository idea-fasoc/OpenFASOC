from decimal import Decimal
from typing import Literal, Optional, Union

from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
# Imports for tap ring
from gdsfactory.components.rectangular_ring import rectangular_ring
from gdsfactory.functions import transformed
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.util.comp_utils import (
    add_ports_perimeter,
    align_comp_to_port,
    evaluate_bbox,
    prec_ref_center,
    to_decimal,
    to_float,
)
from glayout.flow.pdk.util.port_utils import (
    rename_ports_by_list,
    rename_ports_by_orientation,
)
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from glayout.flow.primitives.fet import multiplier
from glayout.flow.primitives.via_gen import via_array, via_stack
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.straight_route import straight_route


def macro_two_transistor_placement_Onchip(
    pdk: MappedPDK,
    deviceA_and_B: Literal["nfet", "pfet"],
    with_substrate_tap: bool = False,
    with_tie: bool = True,
    width1: float = 1,
    width2: float = 1,
    length1: float = None,
    length2: float = None,
    fingers1: int = 3,
    fingers2: int = 3,
    matriz: list = [[0,2,1,1,2,0],[0,1,2,2,1,0],[0,2,1,1,2,0],[0,1,2,2,1,0]],
    with_lvt_layer = False,
    **kwargs
) -> Component:
    #Codigo realizado por Sebastian Suarez y Jose Felix, estudiantes de ingeniería electronica UIS
    # crear fila de dummys arriba y abajo
    row_dumys = list()
    for i in range(len(matriz[0])):
        row_dumys.append(0)
    matriz.insert(len(matriz),row_dumys)
    matriz.insert(0,row_dumys)
    #matriz transpuesta
    matrizT = [list(fila) for fila in zip(*matriz)]
    # sobreescribe los kwargs para las opciones necesitadas
    #Extensión de source y drain con el transistor
    kwargs["sd_route_extension"] = 0
    #Extensión de gate con el transistor
    kwargs["gate_route_extension"] = 0

    kwargs["sdlayer"] = "n+s/d" if deviceA_and_B == "nfet" else "p+s/d"
    kwargs["pdk"] = pdk
    kwargs["dummy"] = (False,False)

    #crear el transistor B con menor longitud de extensión sd y gate
    center_devB = multiplier(width=width2, length=length2, fingers=fingers2, **kwargs)

    #aumentar longitud de extensión sd y gate para el segundo transistor (A)
    devA_sd_extension = pdk.util_max_metal_seperation() + 0.6*abs(center_devB.ports["drain_N"].center[1]-center_devB.ports["diff_N"].center[1])+0.14
    devA_gate_extension = pdk.util_max_metal_seperation() + 0.6*abs(center_devB.ports["row0_col0_gate_S"].center[1]-center_devB.ports["gate_S"].center[1])
    kwargs["sd_route_extension"] = pdk.snap_to_2xgrid(devA_sd_extension)
    kwargs["gate_route_extension"] = pdk.snap_to_2xgrid(devA_gate_extension)
    #crear el segundo transistor con la extensión antes definida
    center_devA = multiplier(width=width1, length=length1, fingers=fingers1, **kwargs)

    #aumentar longitud de extensión sd y gate para los dummys
    dummy_sd_extension = 2*(pdk.util_max_metal_seperation() + 0.6*abs(center_devB.ports["drain_N"].center[1]-center_devB.ports["diff_N"].center[1]))+0.14
    dummy_gate_extension = 2*(pdk.util_max_metal_seperation() + 0.6*abs(center_devB.ports["row0_col0_gate_S"].center[1]-center_devB.ports["gate_S"].center[1]))
    kwargs["sd_route_extension"] = pdk.snap_to_2xgrid(dummy_sd_extension)
    kwargs["gate_route_extension"] = pdk.snap_to_2xgrid(dummy_gate_extension)
    #crear los dummys con la extensiones antes
    dumm_mos = multiplier(width=width1, length=length1, fingers=fingers1, **kwargs)

    # place devices
    idplace = Component()
    dims = [evaluate_bbox(center_devA), evaluate_bbox(center_devB)]
    #separación de los dispositivos A
    xdispA = pdk.snap_to_2xgrid(dims[0][0] + 2*pdk.get_grule("active_diff")["min_separation"] + 9.4*pdk.get_grule("met5")["min_width"])
    ydispA = pdk.snap_to_2xgrid(dims[0][1] + 2*pdk.get_grule("active_diff")["min_separation"] + 5*pdk.get_grule("met5")["min_width"])
    #separación de los dispositivos B
    xdispB = pdk.snap_to_2xgrid(dims[1][0] + 2*pdk.get_grule("active_diff")["min_separation"] + 9.4*pdk.get_grule("met5")["min_width"])
    ydispB = pdk.snap_to_2xgrid(dims[1][1] + 2*pdk.get_grule("active_diff")["min_separation"] + 5*pdk.get_grule("met5")["min_width"])
    #separación desde la primera fila de dummys
    ydispA1 = pdk.snap_to_2xgrid(dims[0][1] + 2*pdk.get_grule("active_diff")["min_separation"] + 2*pdk.get_grule("met5")["min_width"])
    ydispB1 = pdk.snap_to_2xgrid(dims[1][1] + 2*pdk.get_grule("active_diff")["min_separation"] + 2*pdk.get_grule("met5")["min_width"])

    #ubicación y adición de los transistores en el componente
    refs = list()
    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
        #Ubicación transistores A
        if matriz[i][j] == 1:
          refs.append(idplace << center_devA)
          devletter = "A"
        #Ubicación transistores B
        elif matriz[i][j] == 2:
          refs.append(idplace << center_devB)
          devletter = "B"
        else:
          #Ubicación transistores Dummys
          #los transistores dummys de la primera y ultima fila tienen separación ds y gate diferente
          if i==0 or i==len(matriz)-1:
            kwargs["sd_route_extension"] = 0
            kwargs["gate_route_extension"] = 0
            dumm_mos1 = multiplier(width=width1, length=length1, fingers=fingers1, **kwargs)
            refs.append(idplace << dumm_mos1)
            devletter = "D"
          #Separación sd y gate del resto de transistores dumys
          else:
            refs.append(idplace << dumm_mos)
            devletter = "D"
        #separación de la primera fila de dummys (fila 0)
        if i==0:
          refs[-1].movex(j*(xdispA + xdispB)/2)
        #separación de los dispositivos de la fila 1
        elif i==1:
          refs[-1].movex(j*(xdispA + xdispB)/2)
          refs[-1].movey((-i*(ydispA1 + ydispB1)/2)-0.14)
          disref = (-i*(ydispA1 + ydispB1)/2)
        #separación de la ultima fila de dummys
        elif i==len(matriz)-1:
          refs[-1].movex(j*(xdispA + xdispB)/2)
          refs[-1].movey((((-2*(ydispA + ydispB)/2)-0.14)+((i-2)*((-2*(ydispA + ydispB)/2)-disref))+2*devA_sd_extension)-0.14)
        #separación del resto de filas
        else:
          refs[-1].movex(j*(xdispA + xdispB)/2)
          refs[-1].movey(((-2*(ydispA + ydispB)/2)-0.14)+((i-2)*((-2*(ydispA + ydispB)/2)-disref)))

        #Adición de los puertos de los transistores
        prefix=devletter+""+str(int(i))+""+str(int(j))+"_"
        idplace.add_ports(refs[-1].get_ports_list(), prefix=prefix)

    #rutear por filas
    #listas que guardan todas la posiciones de los transistores A,B y dummys
    pos_transA = list()
    pos_transB = list()
    pos_transDummy = list()
    #listas que guardan unicamente la primera y ultima vez que aparecen los transistores A,B y dummys
    pos_transA_FL = list()
    pos_transB_FL = list()
    pos_transDummy_FL = list()
    #listas que guardan solo la ultima vez que aparecen por filas los transistores A y B
    pos_transAL = list()
    pos_transBL = list()
    #contador que identifica las posiciones de los transistores en el placement
    cont=0
    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
        if matriz[i][j]==1:
          pos_transA.append(cont)
          cont+=1
        elif matriz[i][j]==2:
          pos_transB.append(cont)
          cont+=1
        else:
          pos_transDummy.append(cont)
          cont+=1
      #Guarda las ultima posición de los transistores A y B, de no haber guarda un 0
      if len(pos_transA)>0:
        pos_transAL.append(max(pos_transA))
      else:
        pos_transAL.append(0)
      if len(pos_transB):
        pos_transBL.append(max(pos_transB))
      else:
        pos_transBL.append(0)

      if i!=0 and i!=len(matriz)-1:
        if len(pos_transA)>0:
          pos_transA_FL.append(min(pos_transA))
          pos_transA_FL.append(max(pos_transA))
        if len(pos_transB)>0:
          pos_transB_FL.append(min(pos_transB))
          pos_transB_FL.append(max(pos_transB))
        #ruteo por fila de cada tipo de transistor
        if len(pos_transA)>0:
          A_src_h = idplace << rename_ports_by_orientation(rename_ports_by_list(straight_route(pdk, refs[pos_transA_FL[0]].ports["source_W"], refs[pos_transA_FL[1]].ports["source_E"]), [("route_","_")]))
          A_drain_h = idplace << rename_ports_by_orientation(rename_ports_by_list(straight_route(pdk, refs[pos_transA_FL[0]].ports["drain_W"], refs[pos_transA_FL[1]].ports["drain_E"]), [("route_","_")]))
          A_gate_h = idplace << rename_ports_by_orientation(rename_ports_by_list(straight_route(pdk, refs[pos_transA_FL[0]].ports["gate_W"], refs[pos_transA_FL[1]].ports["gate_E"]), [("route_","_")]))
          idplace.add_ports(A_src_h.get_ports_list(), prefix="A_src_h_"+str(i)+str(j))
          idplace.add_ports(A_drain_h.get_ports_list(), prefix="A_drain_h_"+str(i)+str(j))
          idplace.add_ports(A_gate_h.get_ports_list(), prefix="A_gate_h_"+str(i)+str(j))
        if len(pos_transB)>0:
          B_src_h = idplace << rename_ports_by_orientation(rename_ports_by_list(straight_route(pdk, refs[pos_transB_FL[0]].ports["source_W"], refs[pos_transB_FL[1]].ports["source_E"]), [("route_","_")]))
          B_drain_h = idplace << rename_ports_by_orientation(rename_ports_by_list(straight_route(pdk, refs[pos_transB_FL[0]].ports["drain_W"], refs[pos_transB_FL[1]].ports["drain_E"]), [("route_","_")]))
          B_gate_h = idplace << rename_ports_by_orientation(rename_ports_by_list(straight_route(pdk, refs[pos_transB_FL[0]].ports["gate_W"], refs[pos_transB_FL[1]].ports["gate_E"]), [("route_","_")]))
          idplace.add_ports(B_src_h.get_ports_list(), prefix="B_src_h_"+str(i)+str(j))
          idplace.add_ports(B_drain_h.get_ports_list(), prefix="B_drain_h_"+str(i)+str(j))
          idplace.add_ports(B_gate_h.get_ports_list(), prefix="B_gate_h_"+str(i)+str(j))
        pos_transA = list()
        pos_transA = list()
        pos_transB = list()
        pos_transA_FL = list()
        pos_transB_FL = list()
      pos_transDummy_FL.append(min(pos_transDummy))
      pos_transDummy_FL.append(max(pos_transDummy))
      #ruteo por fila para las dos filas de dummys
      Dummy_src = idplace << rename_ports_by_orientation(rename_ports_by_list(straight_route(pdk, refs[pos_transDummy_FL[0]].ports["source_W"], refs[pos_transDummy_FL[1]].ports["source_E"]), [("route_","_")]))
      Dummy_drain = idplace << rename_ports_by_orientation(rename_ports_by_list(straight_route(pdk, refs[pos_transDummy_FL[0]].ports["drain_W"], refs[pos_transDummy_FL[1]].ports["drain_E"]), [("route_","_")]))
      Dummy_gate = idplace << rename_ports_by_orientation(rename_ports_by_list(straight_route(pdk, refs[pos_transDummy_FL[0]].ports["gate_W"], refs[pos_transDummy_FL[1]].ports["gate_E"]), [("route_","_")]))
      pos_transDummy = list()
      pos_transDummy_FL = list()

    #rutear por columnas
    #contador general
    cont=0
    #control de ruteo primera vez de A,B y Dummys
    contRdummy=0
    contRA=0
    contRB=0
    #posiciones en fila de cada transistor
    listaJA=list()
    listaJB=list()
    listaJDummy=list()
    #posiciones de cada transistor ruteado
    listaJAR=list()
    listaJBR=list()
    for i in range(len(matrizT)):
      for j in range(len(matrizT[i])):
        if matrizT[i][j]==1:
          pos_transA.append(cont)
          listaJA.append(j)
          cont=cont+len(matriz[0])
        elif matrizT[i][j]==2:
          pos_transB.append(cont)
          listaJB.append(j)
          cont=cont+len(matriz[0])
        else:
          pos_transDummy.append(cont)
          listaJDummy.append(j)
          if j==0:
            cont=i+len(matriz[0])
          elif j==len(matrizT[i])-1:
            cont=i+1
          else:
            cont=cont+len(matriz[0])
      source_extensionB = to_decimal(0.38) + to_decimal(pdk.get_grule("met4")["min_separation"])
      drain_extensionB = to_decimal(0.97) + to_decimal(pdk.get_grule("met4")["min_separation"])
      gate_extensionA = (to_decimal(1.87) + to_decimal(pdk.get_grule("met4")["min_separation"]))
      source_extensionA = (to_decimal(2.15) + to_decimal(pdk.get_grule("met4")["min_separation"]))
      drain_extensionA = (to_decimal(2.74) + to_decimal(pdk.get_grule("met4")["min_separation"]))
      gate_extension_Dummy = to_decimal(0.6) + 2*to_decimal(pdk.get_grule("met4")["min_separation"])
      #determino si no se han ruteado los dummys y realizo su ruteo
      if contRdummy==0:
        if len(pos_transDummy)>1:
          for i in range(len(pos_transDummy)-1):
            Dummy_src = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transDummy[i]].ports["source_W"], refs[pos_transDummy[i+1]].ports["source_W"], viaoffset=(True,False), cglayer="met1"), [("route_","_")]))
            Dummy_drain = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transDummy[i]+len(matriz[0])-1].ports["drain_E"], refs[pos_transDummy[i+1]].ports["drain_E"], viaoffset=(True,False), cglayer="met1"), [("route_","_")]))
            Dummy_gate = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transDummy[i]].ports["gate_W"], refs[pos_transDummy[i+1]].ports["gate_W"], viaoffset=(True,False), extension=to_float(gate_extension_Dummy), cglayer="met1"), [("route_","_")]))
            contRdummy+=1
      # Verifico que aún no se haya ruteado los transistores A para hacer el primer ruteo
      if contRA==0:
        if len(pos_transA)>1:
          for i in range(len(pos_transA)-1):
            A_src1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]].ports["source_W"], refs[pos_transA[i+1]].ports["source_W"],viaoffset=(True,False),extension=to_float(source_extensionA), cglayer="met1"), [("route_","_")]))
            A_src2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["source_E"], refs[pos_transA[i+1]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["source_E"],viaoffset=(True,False),extension=to_float(source_extensionA), cglayer="met1"), [("route_","_")]))
            A_drain1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]].ports["drain_W"], refs[pos_transA[i+1]].ports["drain_W"], viaoffset=(False,True), extension=to_float(drain_extensionA), cglayer="met1"), [("route_","_")]))
            A_drain2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["drain_E"], refs[pos_transA[i+1]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["drain_E"], viaoffset=(False,True), extension=to_float(drain_extensionA), cglayer="met1"), [("route_","_")]))
            A_gate1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]].ports["gate_W"], refs[pos_transA[i+1]].ports["gate_W"], viaoffset=(True,False), extension=to_float(gate_extensionA), cglayer="met1"), [("route_","_")]))
            A_gate2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["gate_E"], refs[pos_transA[i+1]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["gate_E"], viaoffset=(True,False), extension=to_float(gate_extensionA), cglayer="met1"), [("route_","_")]))
            contRA+=1
          listaJAR+=listaJA
      #Condiciones de ruteo en caso de no ser la primera vez que se rutea un transistor A
      if contRA!=0:
        if len(pos_transA)>1:
          #Determino si ya se rutearon los transistores de dicha columna
          for i in range(len(listaJA)):
            if listaJA[i] in listaJAR:
              pass
            else:
              for i in range(len(pos_transA)-1):
                A_src1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]].ports["source_W"], refs[pos_transA[i+1]].ports["source_W"],viaoffset=(True,False),extension=to_float(source_extensionA), cglayer="met1"), [("route_","_")]))
                A_src2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["source_E"], refs[pos_transA[i+1]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["source_E"],viaoffset=(True,False),extension=to_float(source_extensionA), cglayer="met1"), [("route_","_")]))
                A_drain1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]].ports["drain_W"], refs[pos_transA[i+1]].ports["drain_W"], viaoffset=(False,True), extension=to_float(drain_extensionA), cglayer="met1"), [("route_","_")]))
                A_drain2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["drain_E"], refs[pos_transA[i+1]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["drain_E"], viaoffset=(False,True), extension=to_float(drain_extensionA), cglayer="met1"), [("route_","_")]))
                A_gate1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]].ports["gate_W"], refs[pos_transA[i+1]].ports["gate_W"], viaoffset=(True,False), extension=to_float(gate_extensionA), cglayer="met1"), [("route_","_")]))
                A_gate2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transA[i]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["gate_E"], refs[pos_transA[i+1]+(pos_transAL[listaJA[0]]-pos_transA[0])].ports["gate_E"], viaoffset=(True,False), extension=to_float(gate_extensionA), cglayer="met1"), [("route_","_")]))
                contRA+=1
              listaJAR+=listaJA
      # Verifico que aún no se haya ruteado los transistores B para hacer el primer ruteo
      if contRB==0:
        if len(pos_transB)>1:
          for i in range(len(pos_transB)-1):
            B_src1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]].ports["source_W"], refs[pos_transB[i+1]].ports["source_W"], viaoffset=(True,False), extension=to_float(source_extensionB), cglayer="met1"), [("route_","_")]))
            B_src2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["source_E"], refs[pos_transB[i+1]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["source_E"], viaoffset=(True,False), extension=to_float(source_extensionB), cglayer="met1"), [("route_","_")]))
            B_drain1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]].ports["drain_W"], refs[pos_transB[i+1]].ports["drain_W"], viaoffset=(False,True), extension=to_float(drain_extensionB), cglayer="met1"), [("route_","_")]))
            B_drain2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["drain_E"], refs[pos_transB[i+1]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["drain_E"], viaoffset=(False,True), extension=to_float(drain_extensionB), cglayer="met1"), [("route_","_")]))
            B_gate1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]].ports["gate_W"], refs[pos_transB[i+1]].ports["gate_W"], viaoffset=(True,False), cglayer="met1"), [("route_","_")]))
            B_gate2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["gate_E"], refs[pos_transB[i+1]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["gate_E"], viaoffset=(True,False), cglayer="met1"), [("route_","_")]))
            contRB+=1
          listaJBR+=listaJB
      #Condiciones de ruteo en caso de no ser la primera vez que se rutea un transistor B
      if contRB!=0:
        if len(pos_transB)>1:
          #Determino si ya se rutearon los transistores de dicha columna
          for i in range(len(listaJB)):
            if listaJB[i] in listaJBR:
              pass
            else:
              for i in range(len(pos_transB)-1):
                B_src1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]].ports["source_W"], refs[pos_transB[i+1]].ports["source_W"], viaoffset=(True,False), extension=to_float(source_extensionB), cglayer="met1"), [("route_","_")]))
                B_src2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["source_E"], refs[pos_transB[i+1]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["source_E"], viaoffset=(True,False), extension=to_float(source_extensionB), cglayer="met1"), [("route_","_")]))
                B_drain1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]].ports["drain_W"], refs[pos_transB[i+1]].ports["drain_W"], viaoffset=(False,True), extension=to_float(drain_extensionB), cglayer="met1"), [("route_","_")]))
                B_drain2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["drain_E"], refs[pos_transB[i+1]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["drain_E"], viaoffset=(False,True), extension=to_float(drain_extensionB), cglayer="met1"), [("route_","_")]))
                B_gate1 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]].ports["gate_W"], refs[pos_transB[i+1]].ports["gate_W"], viaoffset=(True,False), cglayer="met1"), [("route_","_")]))
                B_gate2 = idplace << rename_ports_by_orientation(rename_ports_by_list(c_route(pdk, refs[pos_transB[i]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["gate_E"], refs[pos_transB[i+1]+(pos_transBL[listaJB[0]]-pos_transB[0])].ports["gate_E"], viaoffset=(True,False), cglayer="met1"), [("route_","_")]))
                contRB+=1
              listaJBR+=listaJB
      pos_transA=list()
      listaJA=list()
      pos_transB=list()
      listaJB=list()
      pos_transDummy=list()
      listaJDummy=list()

    #centro todo el componente
    idplace = transformed(prec_ref_center(idplace))
    idplace.unlock()

    base_multiplier = idplace
    #met3 == met2 Klayout
    #met1 == li Klayout
    #met2 == met1 Klayout
    #Defino si el transistor es Nmos o Pmos para agregar el pwell y el substrate tap
    if deviceA_and_B=="nfet":
      # add tie if tie
      if with_tie:
        tie_layers = ["met2","met1"]
        tap_separation = max(
            pdk.util_max_metal_seperation(),
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
        tap_separation += pdk.get_grule("p+s/d", "active_tap")["min_enclosure"]
        tap_encloses = (
            2 * (tap_separation + idplace.xmax),
            2 * (tap_separation + idplace.ymax),
        )
        tiering_ref = idplace << create_tapring_onchip(
            pdk,
            enclosed_rectangle=tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer=tie_layers[0],
            vertical_glayer=tie_layers[1],
            with_lvt_layer = with_lvt_layer,
        )
        idplace.add_ports(tiering_ref.get_ports_list(), prefix="tie_")

      # add pwell
      base_multiplier.add_padding(
        layers=(pdk.get_glayer("pwell"),),
        default=pdk.get_grule("pwell", "active_tap")["min_enclosure"],
      )

      # add substrate tap
      base_multiplier = add_ports_perimeter(base_multiplier,layer=pdk.get_glayer("pwell"),prefix="well_")
      # add substrate tap if with_substrate_tap
      if with_substrate_tap:
        pass
    else:
      # add tie if tie
      if with_tie:
        tie_layers = ["met2","met1"]
        tap_separation = max(
            pdk.get_grule("met2")["min_separation"],
            pdk.get_grule("met1")["min_separation"],
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
        tap_separation += pdk.get_grule("n+s/d", "active_tap")["min_enclosure"]
        tap_encloses = (
            2 * (tap_separation + idplace.xmax),
            2 * (tap_separation + idplace.ymax),
        )
        tapring_ref = idplace << create_tapring_onchip(
            pdk,
            enclosed_rectangle=tap_encloses,
            sdlayer="n+s/d",
            horizontal_glayer=tie_layers[0],
            vertical_glayer=tie_layers[1],
            with_lvt_layer=with_lvt_layer,
        )
        idplace.add_ports(tapring_ref.get_ports_list(),prefix="tie_")

      # add pwell
      base_multiplier.add_padding(
        layers=(pdk.get_glayer("nwell"),),
        default=pdk.get_grule("nwell", "active_tap")["min_enclosure"],
      )
      # add substrate tap
      base_multiplier = add_ports_perimeter(base_multiplier,layer=pdk.get_glayer("nwell"),prefix="well_")
      # add substrate tap if with_substrate_tap

      if with_substrate_tap:
        substrate_tap_separation = pdk.get_grule("dnwell", "active_tap")[
            "min_separation"
        ]
        substrate_tap_encloses = (
            2 * (substrate_tap_separation + base_multiplier.xmax),
            2 * (substrate_tap_separation + base_multiplier.ymax),
        )
        ringtoadd = create_tapring_onchip(
            pdk,
            enclosed_rectangle=substrate_tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer="met2",
            vertical_glayer="met1",
            with_lvt_layer = False,
        )
        tapring_ref = base_multiplier << ringtoadd
        base_multiplier.add_ports(tapring_ref.get_ports_list(),prefix="substratetap_")
      base_multiplier.info["route_genid"] = "two_transistor_interdigitized"

    #ports
    size_idplace_x = evaluate_bbox(idplace.flatten())[0]
    size_idplace_y = evaluate_bbox(idplace.flatten())[1]
    pos_ports_y = size_idplace_y/4
    pos_ports_x = size_idplace_x/4
    width_port = 0.5

    #Posiciones de ruteo
    puerto_GA = []
    puerto_GB = []
    puerto_DA = []
    puerto_DB = []
    puerto_SA = []
    puerto_SB = []
    puerto_VDDSS1= [str(int(0))+str(int(len(matriz[0])/2))]
    puerto_VDDSS2= [str(int(len(matriz)-1))+str(int(len(matriz[0])/2))]

    #find mosfet to connect GA and SA
    for i in range(len(matriz)):
      for j in range(len(matriz[i])):
        if matriz[i][j] == 1:
          puerto_GA.append(str(i)+str(j))
          puerto_SA.append(str(i)+str(j))
          break
    #find mosfet to connect GB
    for i in range(len(matriz)):
      for j in range(len(matriz[i])-1,-1,-1):
        if matriz[i][j] == 2:
          puerto_GB.append(str(i)+str(j))
          break
    #find mosfet to connect DA
    for i in range(len(matriz)):
      for j in range(len(matriz[i])-1,-1,-1):
        if matriz[i][j] == 1:
          puerto_DA.append(str(i)+str(j))
          break
    #find mosfet to connect SB
    for i in range(len(matriz)-1,-1,-1):
      for j in range(len(matriz[i])):
        if matriz[i][j] == 2:
          puerto_SB.append(str(i)+str(j))
          break
    #find mosfet to connect DB
    for i in range(len(matriz)-1,-1,-1):
      for j in range(len(matriz[i])-1,-1,-1):
        if matriz[i][j] == 2:
          puerto_DB.append(str(i)+str(j))
          break

    #Creacion de ports
    #GA
    GA_port = idplace.ports['A'+puerto_GA[0]+'_gate_S']
    via_GA = via_stack(pdk, 'met1', 'met3') #Porque met1, met3? no noto cambio
    via_GA_ref = align_comp_to_port(via_GA, GA_port, alignment=('c','t'))
    via_GA_port = via_GA_ref.ports["top_met_N"] #Porque top_metN?
    port_rectangle_met3 = rectangle((width_port,width_port), layer=pdk.get_glayer("met3"))
    GA = align_comp_to_port(port_rectangle_met3.copy(), via_GA_port, alignment=(None,'c'))
    idplace.add(GA)
    pl = GA.bbox
    offset = -pl[0]
    GA.move(destination=offset) #como es esto?
    GA.movex(pdk.snap_to_2xgrid(-1.0543*size_idplace_x/2))
    idplace.add_ports(GA.get_ports_list(),prefix='GA_')

    #GB
    GB_port = idplace.ports['B'+puerto_GB[0]+'_gate_S']
    via_GB = via_stack(pdk, 'met1', 'met3')
    via_GB_ref = align_comp_to_port(via_GB, GB_port, alignment=('c','t'))
    via_GB_port = via_GB_ref.ports["top_met_N"]
    GB = align_comp_to_port(port_rectangle_met3.copy(), via_GB_port, alignment=(None,'c'))
    idplace.add(GB)
    pl = GB.bbox
    offset = -pl[0]
    GB.move(destination=offset)
    GB.movex(pdk.snap_to_2xgrid(1.0271*size_idplace_x/2))
    idplace.add_ports(GB.get_ports_list(),prefix='GB_')

    #DA
    DA_port = idplace.ports['A'+puerto_DA[0]+'_drain_S']
    via_DA = via_stack(pdk, 'met1', 'met2')
    via_DA_ref = align_comp_to_port(via_DA, DA_port, alignment=('c','t'))
    via_DA_port = via_DA_ref.ports["top_met_N"]
    port_rectangle_met4 = rectangle((width_port,width_port), layer=pdk.get_glayer("met2"))
    DA = align_comp_to_port(port_rectangle_met3.copy(), via_DA_port, alignment=(None,'c'))
    idplace.add(DA)
    pl = DA.bbox
    offset = -pl[0]
    DA.move(destination=offset)
    DA.movex(pdk.snap_to_2xgrid(-1.1590*size_idplace_x/2)).movey(size_idplace_y*0.1)
    idplace.add_ports(DA.get_ports_list(),prefix='DA_')

    #DB
    DB_port = idplace.ports['B'+puerto_DB[0]+'_drain_S']
    via_DB = via_stack(pdk, 'met1', 'met2')
    via_DB_ref = align_comp_to_port(via_DB, DB_port, alignment=('c','t'))
    via_DB_port = via_DB_ref.ports["top_met_N"]
    DB = align_comp_to_port(port_rectangle_met3.copy(), via_DB_port, alignment=(None,'c'))
    idplace.add(DB)
    pl = DB.bbox
    offset = -pl[0]
    DB.move(destination=offset)
    DB.movex(pdk.snap_to_2xgrid(1.1318*size_idplace_x/2)).movey(size_idplace_y*0.1)
    idplace.add_ports(DB.get_ports_list(),prefix='DB_')

    #SA
    SA_port = idplace.ports['A'+puerto_SA[0]+'_source_S']
    via_SA = via_stack(pdk, 'met1', 'met2')
    via_SA_ref = align_comp_to_port(via_SA, SA_port, alignment=('c','t'))
    via_SA_port = via_SA_ref.ports["top_met_N"]
    SA = align_comp_to_port(port_rectangle_met3.copy(), via_SA_port, alignment=(None,'c'))
    idplace.add(SA)
    pl = SA.bbox
    offset = -pl[0]
    SA.move(destination=offset)
    SA.movex(pdk.snap_to_2xgrid(-1.2637*size_idplace_x/2)).movey(-size_idplace_y*0.1)
    idplace.add_ports(SA.get_ports_list(),prefix='SA_')

    #SB
    SB_port = idplace.ports['B'+puerto_SB[0]+'_source_S']
    via_SB = via_stack(pdk, 'met1', 'met2')
    via_SB_ref = align_comp_to_port(via_SB, SB_port, alignment=('c','t'))
    via_SB_port = via_SB_ref.ports["top_met_N"]
    SB = align_comp_to_port(port_rectangle_met3.copy(), via_SB_port, alignment=(None,'c'))
    idplace.add(SB)
    pl = SB.bbox
    offset = -pl[0]
    SB.move(destination=offset)
    SB.movex(pdk.snap_to_2xgrid(1.2366*size_idplace_x/2)).movey(-size_idplace_y*0.1)
    idplace.add_ports(SB.get_ports_list(),prefix='SB_')

    port_rectangle_met3 = rectangle((width_port,width_port), layer=pdk.get_glayer("met2"))
    #VDD1/VSS1
    VDD1_VSS1_port = idplace.ports['D'+puerto_VDDSS1[0]+'_gate_S']
    via_VDD1_VSS1 = via_stack(pdk, 'met1', 'met3')
    via_VDD1_VSS1_ref = align_comp_to_port(via_VDD1_VSS1, VDD1_VSS1_port, alignment=('c','t'))
    via_VDD1_VSS1_port = via_VDD1_VSS1_ref.ports["top_met_N"]
    VDD1_VSS1 = align_comp_to_port(port_rectangle_met3.copy(), via_VDD1_VSS1_port, alignment=(None,'c'))
    idplace.add(VDD1_VSS1)
    VDD1_VSS1.movey(pdk.snap_to_2xgrid(4.145*pdk.get_grule('nwell')["min_separation"]))
    idplace.add_ports(VDD1_VSS1.get_ports_list(),prefix='VDD1_VSS1_')

    #VDD2/VSS2
    VDD2_VSS2_port = idplace.ports['D'+puerto_VDDSS2[0]+'_gate_S']
    via_VDD2_VSS2 = via_stack(pdk, 'met1', 'met3')
    via_VDD2_VSS2_ref = align_comp_to_port(via_VDD2_VSS2, VDD2_VSS2_port, alignment=('c','t'))
    via_VDD2_VSS2_port = via_VDD2_VSS2_ref.ports["top_met_N"]
    VDD2_VSS2 = align_comp_to_port(port_rectangle_met3.copy(), via_VDD2_VSS2_port, alignment=(None,'c'))
    idplace.add(VDD2_VSS2)
    VDD2_VSS2.movey(pdk.snap_to_2xgrid(-2.525*pdk.get_grule('nwell')["min_separation"]))
    idplace.add_ports(VDD2_VSS2.get_ports_list(),prefix='VDD2_VSS2_')

    nombres_puertos_tie_s = [name for name in idplace.ports if "tie_S" in name and 'top_met_S' in name]
    nombres_puertos_tie_n = [name for name in idplace.ports if "tie_N" in name and 'top_met_N' in name]
    nombres_puertos_tie_s_W = [name for name in idplace.ports if "tie_S" in name and 'top_met_W' in name]
    nombres_puertos_tie_n_W = [name for name in idplace.ports if "tie_N" in name and 'top_met_W' in name]
    nombres_puertos_tap_s = [name for name in idplace.ports if 'substratetap_S' in name and 'top_met_S' in name]
    nombres_puertos_tap_n = [name for name in idplace.ports if 'substratetap_N' in name and 'top_met_N' in name]
    pos_tie_center_s = int(len(nombres_puertos_tie_s)/2)

    if with_substrate_tap and deviceA_and_B=='pfet':
      substrate_tap_port1 = idplace.ports[nombres_puertos_tap_s[0]]
      via_substrate_tap1 = via_stack(pdk, 'met1', 'met3')
      via_substrate_tap_port_ref1 = align_comp_to_port(via_substrate_tap1, substrate_tap_port1, alignment=('c','t'))
      via_substrate_tap_port1 = via_substrate_tap_port_ref1.ports["top_met_N"]
      substrate_tap1 = align_comp_to_port(port_rectangle_met3.copy(), via_substrate_tap_port1, alignment=(None,'c'))
      idplace.add(substrate_tap1)
      substrate_tap1.movey(-3.1*pdk.get_grule('nwell')["min_separation"]).movex(pdk.snap_to_2xgrid(-pos_ports_x))
      idplace.add_ports(substrate_tap1.get_ports_list(),prefix='substratetap1_')

      substrate_tap_port2 = idplace.ports[nombres_puertos_tap_n[0]]
      via_substrate_tap2 = via_stack(pdk, 'met1', 'met3')
      via_substrate_tap_port_ref2 = align_comp_to_port(via_substrate_tap2, substrate_tap_port2, alignment=('c','t'))
      via_substrate_tap_port2 = via_substrate_tap_port_ref2.ports["top_met_N"]
      substrate_tap2 = align_comp_to_port(port_rectangle_met3.copy(), via_substrate_tap_port2, alignment=(None,'c'))
      idplace.add(substrate_tap2)
      substrate_tap2.movey(2.5*pdk.get_grule('nwell')["min_separation"]).movex(pdk.snap_to_2xgrid(-pos_ports_x))
      idplace.add_ports(substrate_tap2.get_ports_list(),prefix='substratetap2_')

    rename_ports_by_orientation(idplace) #Linea necesaria para que los puertos se creen con las direcciones N, S, W y E en el nombre

    #Ruteo de ports
    rename_ports_by_orientation(idplace)
    #Adicion vias de la mitad
    viamet1_2 = via_stack(pdk, 'met1', 'met2')
    #Elementos de buscqueda (ports de las rutas horizontales)
    busqueda = [[-1.475,'A_src_h'], [-0.885,'A_gate_h'], [-0.295,'A_drain_h'], [0.295,'B_src_h'], [0.885,'B_gate_h'], [1.475,'B_drain_h']]
    vias = []
    for offset, puerto in busqueda:
      #Permite encontrar los ports que contengan las palabras de busqueda (puerto en el for) y que se conecten a la direccion W
      puertos_W = [name for name in idplace.ports if puerto in name and "W" in name]
      #Permite encontrar los ports que contengan las palabras de busqueda (puerto en el for) y que se conecten a la direccion N
      puertos_N = [name for name in idplace.ports if puerto in name and "N" in name]
      width = []
      pos = []
      for encontrados in puertos_W:
        #Guarda la información del ancho de los puertos encontrados
        width.append(idplace.ports[encontrados].width)
      vias.append(len(width)-1)
      for encontrados in puertos_N:
        #Guarda la información de la posicion de los puertos encontrados
        pos.append(list(idplace.ports[encontrados].center))
      #Agrega todas las vias en las posiciones encontradas por los puertos
      for i in range(len(width)):
        via_i = idplace << viamet1_2
        via_i.movex(offset+pos[i][0]).movey(pos[i][1] - width[i]/2)
        idplace.add_ports(via_i.get_ports_list(), prefix='Via_center_'+str(i)+'_'+puerto)
      #Rutea las vias creadas
      idplace << straight_route(pdk, idplace.ports['Via_center_0_'+puerto+'bottom_met_S'], idplace.ports['Via_center_'+str(len(width)-1)+'_'+puerto+'bottom_met_N'])

    rename_ports_by_orientation(idplace)

    #Ruteo de los ports de salida
    #GA
    #Con las vias creadas en el centro se conectan a los puertos de salida de forma simetrica (la primera y ultima)
    idplace << c_route(pdk, idplace.ports['Via_center_0_A_gate_htop_met_W'], idplace.ports['GA_W'], width1=0.33, viaoffset=(False,False))
    idplace << c_route(pdk, idplace.ports['Via_center_'+str(vias[1])+'_A_gate_htop_met_W'], idplace.ports['GA_W'], width1=0.33, viaoffset=(False,False))
    #GB
    idplace << c_route(pdk, idplace.ports['Via_center_0_B_gate_htop_met_E'], idplace.ports['GB_E'], width1=0.33, viaoffset=(False,False))
    idplace << c_route(pdk, idplace.ports['Via_center_'+str(vias[4])+'_B_gate_htop_met_E'], idplace.ports['GB_E'], width1=0.33, viaoffset=(False,False))
    #DA
    idplace << c_route(pdk, idplace.ports['Via_center_0_A_drain_htop_met_W'], idplace.ports['DA_W'], viaoffset=(False,False))
    idplace << c_route(pdk, idplace.ports['Via_center_'+str(vias[2])+'_A_drain_htop_met_W'], idplace.ports['DA_W'], viaoffset=(False,False))
    #DB
    idplace << c_route(pdk, idplace.ports['Via_center_0_B_drain_htop_met_E'], idplace.ports['DB_E'], viaoffset=(False,False))
    idplace << c_route(pdk, idplace.ports['Via_center_'+str(vias[5])+'_B_drain_htop_met_E'], idplace.ports['DB_E'], viaoffset=(False,False))
    #SA
    idplace << c_route(pdk, idplace.ports['Via_center_0_A_src_htop_met_W'], idplace.ports['SA_W'], viaoffset=(False,False))
    idplace << c_route(pdk, idplace.ports['Via_center_'+str(vias[0])+'_A_src_htop_met_W'], idplace.ports['SA_W'], viaoffset=(False,False))
    #SB
    idplace << c_route(pdk, idplace.ports['Via_center_0_B_src_htop_met_E'], idplace.ports['SB_E'], viaoffset=(False,False))
    idplace << c_route(pdk, idplace.ports['Via_center_'+str(vias[3])+'_B_src_htop_met_E'], idplace.ports['SB_E'], viaoffset=(False,False))

    if with_tie:
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS2[0]+'_gate_W'], idplace.ports[nombres_puertos_tie_s[pos_tie_center_s-2]])
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS2[0]+'_source_W'], idplace.ports[nombres_puertos_tie_s[pos_tie_center_s-2]])
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS2[0]+'_drain_W'], idplace.ports[nombres_puertos_tie_s[pos_tie_center_s-2]])
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS1[0]+'_gate_W'], idplace.ports[nombres_puertos_tie_n[pos_tie_center_s+1]])
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS1[0]+'_source_W'], idplace.ports[nombres_puertos_tie_n[pos_tie_center_s+1]])
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS1[0]+'_drain_W'], idplace.ports[nombres_puertos_tie_n[pos_tie_center_s+1]])
      if with_substrate_tap and deviceA_and_B=='pfet':
        idplace << c_route(pdk, idplace.ports[nombres_puertos_tie_s_W[pos_tie_center_s]], idplace.ports['VDD2_VSS2_W'], cglayer='met3', extension=0.4)
        idplace << c_route(pdk, idplace.ports[nombres_puertos_tie_n_W[pos_tie_center_s]], idplace.ports['VDD1_VSS1_W'], cglayer='met3', extension=0.4, viaoffset=(False,False))
        idplace << L_route(pdk, idplace.ports[nombres_puertos_tap_s[-1]], idplace.ports['substratetap1_E'], vglayer="met1")
        idplace << L_route(pdk, idplace.ports[nombres_puertos_tap_n[0]], idplace.ports['substratetap2_E'], vglayer="met1")
      else:
        idplace << L_route(pdk, idplace.ports[nombres_puertos_tie_n[pos_tie_center_s+1]], idplace.ports['VDD1_VSS1_W'])
        idplace << L_route(pdk, idplace.ports[nombres_puertos_tie_s[pos_tie_center_s-2]], idplace.ports['VDD2_VSS2_W'])
    else:
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS1[0]+'_gate_E'], idplace.ports['VDD1_VSS1_N'])
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS1[0]+'_source_E'], idplace.ports['VDD1_VSS1_N'])
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS1[0]+'_drain_E'], idplace.ports['VDD1_VSS1_N'])
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS2[0]+'_gate_E'], idplace.ports['VDD2_VSS2_S'])
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS2[0]+'_source_E'], idplace.ports['VDD2_VSS2_S'])
      idplace << L_route(pdk, idplace.ports['D'+puerto_VDDSS2[0]+'_drain_E'], idplace.ports['VDD2_VSS2_S'])
      if with_substrate_tap and deviceA_and_B=='pfet':
        idplace << L_route(pdk, idplace.ports[nombres_puertos_tap_s[-1]], idplace.ports['substratetap1_W'], vglayer="met1")
        idplace << L_route(pdk, idplace.ports[nombres_puertos_tap_n[0]], idplace.ports['substratetap2_W'], vglayer="met1")

    component = rename_ports_by_orientation(idplace).flatten()
    return component


def create_tapring_onchip(
    pdk: MappedPDK,
    enclosed_rectangle=(2.0, 4.0),
    sdlayer: str = "p+s/d",
    horizontal_glayer: str = "met2",
    vertical_glayer: str = "met1",
    sides: tuple[bool,bool,bool,bool] = (True,True,True,True),
    with_lvt_layer = False
) -> Component:
    """ptapring produce a p substrate / pwell tap rectanglular ring
    This ring will legally enclose a rectangular shape
    args:
    pdk: MappedPDK is the pdk to use
    enclosed_rectangle: tuple is the (width, hieght) of the area to enclose
    ****NOTE: the enclosed_rectangle will be the enclosed dimensions of active_tap
    horizontal_glayer: string=met2, layer used over the ring horizontally
    vertical_glayer: string=met1, layer used over the ring vertically
    sides: instead of creating the ring on all sides, only create it on the specified sides (W,N,E,S)
    ports:
    Narr_... all ports in top via array
    Sarr_... all ports in bottom via array
    Earr_... all ports in right via array
    Warr_... all ports in left via array
    bl_corner_...all ports in bottom left L route
    """
    #"pwell": (64,44),
    well_ring = "pwell" if sdlayer == 'p+s/d' else 'nwell'

    enclosed_rectangle = pdk.snap_to_2xgrid(enclosed_rectangle,return_type="float")
    # check layers, activate pdk, create top cell
    pdk.has_required_glayers(
        [sdlayer, "active_tap", "mcon", horizontal_glayer, vertical_glayer]
    )
    pdk.activate()
    ptapring = Component()
    if not "met" in horizontal_glayer or not "met" in vertical_glayer:
        raise ValueError("both horizontal and vertical glayers should be metals")
    # check that ring is not too small
    min_gap_tap = pdk.get_grule("active_tap")["min_separation"]
    if enclosed_rectangle[0] < min_gap_tap:
        raise ValueError("ptapring must be larger than " + str(min_gap_tap))
    # create active tap
    tap_width = max(
        pdk.get_grule("active_tap")["min_width"],
        2 * pdk.get_grule("active_tap", "mcon")["min_enclosure"]
        + pdk.get_grule("mcon")["width"],
    )
    ptapring << rectangular_ring(
        enclosed_size=enclosed_rectangle,
        width=tap_width,
        centered=True,
        layer=pdk.get_glayer("active_tap"),
    )
    # create p plus area
    pp_enclosure = pdk.get_grule("active_tap", sdlayer)["min_enclosure"]
    pp_width = 2 * pp_enclosure + tap_width
    pp_enclosed_rectangle = [dim - 2 * pp_enclosure for dim in enclosed_rectangle]
    ptapring << rectangular_ring(
        enclosed_size=pp_enclosed_rectangle,
        width=pp_width,
        centered=True,
        layer=pdk.get_glayer(sdlayer),
    )
    # create 65/44 area
    con = (65,44)
    ptapring << rectangular_ring(
        enclosed_size = enclosed_rectangle,
        width = tap_width,
        centered = True,
        layer = con,
    )
    if with_lvt_layer:
      # create lvt area
      lvt_layer = (125,44)
      ptapring << rectangle(
        size = enclosed_rectangle, 
        centered = True,
        layer = lvt_layer,
      )

    # create via arrs
    via_width_horizontal = evaluate_bbox(via_stack(pdk, "active_tap", horizontal_glayer))[0]
    arr_size_horizontal = enclosed_rectangle[0]
    horizontal_arr = via_array(
        pdk,
        "active_tap",
        horizontal_glayer,
        (arr_size_horizontal, via_width_horizontal),
        minus1=True,
        lay_every_layer=True
    )
    # Create via vertical
    via_width_vertical = evaluate_bbox(via_stack(pdk, "active_tap", vertical_glayer))[1]
    arr_size_vertical = enclosed_rectangle[1]
    vertical_arr = via_array(
        pdk,
        "active_tap",
        vertical_glayer,
        (via_width_vertical, arr_size_vertical),
        minus1=True,
        lay_every_layer=True
    )

    # add via arrs
    refs_prefixes = list()
    if sides[1]:
        metal_ref_n = ptapring << horizontal_arr
        metal_ref_n.movey(round(0.5 * (enclosed_rectangle[1] + tap_width),4))
        refs_prefixes.append((metal_ref_n,"N_"))
    if sides[2]:
        metal_ref_e = ptapring << vertical_arr
        metal_ref_e.movex(round(0.5 * (enclosed_rectangle[0] + tap_width),4))
        refs_prefixes.append((metal_ref_e,"E_"))
    if sides[3]:
        metal_ref_s = ptapring << horizontal_arr
        metal_ref_s.movey(round(-0.5 * (enclosed_rectangle[1] + tap_width),4))
        refs_prefixes.append((metal_ref_s,"S_"))
    if sides[0]:
        metal_ref_w = ptapring << vertical_arr
        metal_ref_w.movex(round(-0.5 * (enclosed_rectangle[0] + tap_width),4))
        refs_prefixes.append((metal_ref_w,"W_"))
    # connect vertices
    if sides[1] and sides[0]:
        tlvia = ptapring << L_route(pdk, metal_ref_n.ports["top_met_W"], metal_ref_w.ports["top_met_N"])
        refs_prefixes += [(tlvia,"tl_")]
    if sides[1] and sides[2]:
        trvia = ptapring << L_route(pdk, metal_ref_n.ports["top_met_E"], metal_ref_e.ports["top_met_N"])
        refs_prefixes += [(trvia,"tr_")]
    if sides[3] and sides[0]:
        blvia = ptapring << L_route(pdk, metal_ref_s.ports["top_met_W"], metal_ref_w.ports["top_met_S"])
        refs_prefixes += [(blvia,"bl_")]
    if sides[3] and sides[2]:
        brvia = ptapring << L_route(pdk, metal_ref_s.ports["top_met_E"], metal_ref_e.ports["top_met_S"])
        refs_prefixes += [(brvia,"br_")]
    # add ports, flatten and return
    for ref_, prefix in refs_prefixes:
        ptapring.add_ports(ref_.get_ports_list(),prefix=prefix)
    return component_snap_to_grid(ptapring)