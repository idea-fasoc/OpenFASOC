from decimal import Decimal
from typing import Literal, Optional, Union

# Import custom functions
from custom_functions import macro_two_transistor_placement_Onchip
#from glayout.flow.primitives.fet import nmos, pmos, multiplier
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from gdsfactory.functions import transformed
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
#from glayout.flow.primitives.guardring import tapring
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
#from gdsfactory.functions import transformed
from glayout.flow.primitives.via_gen import via_stack
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.straight_route import straight_route


def create_differential_pair(pdk: MappedPDK) -> Component:

  # Define Differential Pair dimentions
  m1 = {'type':'nfet', 'name':'M1', 'width':1, 'length':1, 'multipliers':1, 'fingers':1, 'with_substrate_tap':False}
  m2 = m1 
  matriz = [
      [0, 1, 2, 2, 1, 1, 2, 2, 1, 0],  # Fila 1:    ABBA ABBA 
      [0, 2, 1, 1, 2, 2, 1, 1, 2, 0],  # Fila 2:    BAAB BAAB 
      [0, 1, 2, 2, 1, 1, 2, 2, 1, 0],  # Fila 3:    ABBA ABBA 
      [0, 2, 1, 1, 2, 2, 1, 1, 2, 0],  # Fila 4:    BAAB BAAB 
      [0, 1, 2, 2, 1, 1, 2, 2, 1, 0],  # Fila 5:    ABBA ABBA 
  ] 
  devices_info = [m1,m2]


  Diff_PairComp = Component()
  Diff_Pair_matrix = macro_two_transistor_placement_Onchip(pdk=pdk, deviceA_and_B=devices_info[0]['type'], with_substrate_tap=devices_info[0]['with_substrate_tap'],
                                                              width1=devices_info[0]['width'], width2=devices_info[1]['width'], length1=devices_info[0]['length'],
                                                              length2=devices_info[1]['length'], fingers1=devices_info[0]['fingers'], fingers2=devices_info[1]['fingers'],
                                                              matriz=matriz)

  Diff_Pair_matrix_dimentions = evaluate_bbox(Diff_Pair_matrix)
  Diff_Pair_ref = Diff_PairComp << Diff_Pair_matrix
  #Diff_PairComp << c_route(pdk, Diff_Pair_matrix.ports['SA_N'], Diff_Pair_matrix.ports['SB_N'], cglayer="met3")
  route_sources_ref = Diff_PairComp << c_route(pdk, Diff_Pair_ref.ports['SA_S'], Diff_Pair_ref.ports['SB_S'], cglayer="met2", extension=0.85*Diff_Pair_matrix_dimentions[1]/2)
  route_bulks_ref = Diff_PairComp << c_route(pdk, Diff_Pair_ref.ports['VDD2_VSS2_W'], Diff_Pair_ref.ports['VDD1_VSS1_W'], cglayer="met3", extension=1.05*Diff_Pair_matrix_dimentions[0]/2)


  # Share the ports 
  Diff_PairComp.add_ports(route_sources_ref.get_ports_list(), prefix='Diff_Pair_route_source_')
  Diff_PairComp.add_ports(route_bulks_ref.get_ports_list(), prefix='Diff_Pair_route_bulk_')
  Diff_PairComp.add_ports(Diff_Pair_matrix.get_ports_list(), prefix='Diff_Pair_')


  # Name ports properly
  Diff_PairComp = rename_ports_by_orientation(Diff_PairComp).flatten()


  return Diff_PairComp












def create_tail_transistor(pdk: MappedPDK) -> Component:

  # Define the parameters to force using placement onchip function
  m0 = {'type':'nfet', 'name':'M1', 'width':0.5, 'length':6.5, 'multipliers':5, 'fingers':1, 'with_substrate_tap':False} 
  m0B = {'type':'nfet', 'name':'M1', 'width':0.5, 'length':6.5, 'multipliers':5, 'fingers':1, 'with_substrate_tap':False}
  matriz = [
      [0, 1, 2, 2, 1, 0],  # Fila 1:   AB
      [0, 2, 1, 1, 2, 0],  # Fila 2:   BA   
      [0, 1, 2, 2, 1, 0],  # Fila 3:   AB  
  ]
  devices_info = [m0, m0B]

  tail_comp = Component()

  tail_matrix = macro_two_transistor_placement_Onchip(pdk=pdk, deviceA_and_B=devices_info[0]['type'], with_substrate_tap=devices_info[0]['with_substrate_tap'],
                                                              width1=devices_info[0]['width'], width2=devices_info[1]['width'], length1=devices_info[0]['length'],
                                                              length2=devices_info[1]['length'], fingers1=devices_info[0]['fingers'], fingers2=devices_info[1]['fingers'],
                                                              matriz=matriz)

  tail_matrix_dimentions = evaluate_bbox(tail_matrix)
  tail_matrix_ref = tail_comp << tail_matrix  

  route_sources_ref = tail_comp << c_route(pdk, tail_matrix_ref.ports['SA_S'], tail_matrix_ref.ports['SB_S'], cglayer="met2", extension=0.4*tail_matrix_dimentions[1])
  tail_comp << c_route(pdk, tail_matrix_ref.ports['GA_S'], tail_matrix_ref.ports['GB_S'], cglayer="met2", extension=(0.5*tail_matrix_dimentions[1]) + 2*pdk.util_max_metal_seperation() )
  #route_drains_ref = tail_comp << c_route(pdk, tail_matrix_ref.ports['DA_N'], tail_matrix_ref.ports['DB_N'], cglayer="met2", extension=0.45*tail_matrix_dimentions[1] )

  #tail_comp.add_ports(route_drains_ref.get_ports_list(), prefix='Tail_route_drains_')
  tail_comp.add_ports(route_sources_ref.get_ports_list(), prefix='Tail_route_sources_')
  tail_comp.add_ports(tail_matrix_ref.get_ports_list(), prefix='Tail_')

  # Name ports properly
  tail_comp = rename_ports_by_orientation(tail_comp).flatten()

  return tail_comp












def create_nLoad(pdk: MappedPDK) -> Component:
  
  m1 = {'name':'M1', 'width':0.84, 'length':3, 'multipliers':1, 'fingers':1, 'type':'nfet'}
  m2 = {'name':'M2', 'width':0.84, 'length':3, 'multipliers':1, 'fingers':1, 'type':'nfet'}
  m3 = {'name':'M3', 'width':0.42, 'length':6.5, 'multipliers':1, 'fingers':1, 'type':'nfet'}
  m4 = {'name':'M4', 'width':0.42, 'length':6.5, 'multipliers':1, 'fingers':1, 'type':'nfet'}
  matriz1 = [[0,1,2,1,1,2,1,0],
             [0,2,1,2,2,1,2,0]] #0 dummy, 1 mos A, 2 mos B
  matriz2 = [[0,1,2,1,1,2,1,0],
             [0,2,1,2,2,1,2,0]] #0 dummy, 1 mos A, 2 mos B 
  devices_info = [m1, m2, m3, m4]


  # TODO: error checking
  pdk.activate()
  nLoad = Component()
  # Create Interdigitized

  if devices_info[0]['type']!=devices_info[1]['type']:
    raise ValueError('M1 and M2 must be same type')

  if devices_info[2]['type']!=devices_info[3]['type']:
    raise ValueError('M3 and M4 must be same type')

  Placement1 = macro_two_transistor_placement_Onchip(pdk, deviceA_and_B=devices_info[0]['type'], width1=devices_info[0]['width'], length1=devices_info[0]['length'],
                                                     fingers1=devices_info[0]['fingers'], width2=devices_info[1]['width'], length2=devices_info[1]['length'],
                                                     fingers2=devices_info[1]['fingers'], matriz = matriz1.copy(), with_substrate_tap=True)

  Placement2 = macro_two_transistor_placement_Onchip(pdk, deviceA_and_B=devices_info[2]['type'], width1=devices_info[2]['width'], length1=devices_info[2]['length'],
                                                     fingers1=devices_info[2]['fingers'], width2=devices_info[3]['width'], length2=devices_info[3]['length'],
                                                     fingers2=devices_info[3]['fingers'], matriz = matriz2.copy(), with_substrate_tap=True)

  size_1 = evaluate_bbox(Placement1.flatten())
  size_2 = evaluate_bbox(Placement2.flatten())

  M3M4 = nLoad << Placement1
  M9M10 = nLoad << Placement2

  M3M4.movex(1.05*size_1[0]/2)
  M9M10.movex(-1.05*size_2[0]/2)

  #Ruteo del componenete
  Ruta_G3G4 = nLoad << c_route(pdk, M3M4.ports['GA_N'], M3M4.ports['GB_N'], viaoffset=(True,False), extension=to_float(1.1*size_1[1]/2), cglayer='met2')
  Ruta_G9G10 = nLoad << c_route(pdk, M9M10.ports['GA_N'], M9M10.ports['GB_N'], viaoffset=(True,False), extension=to_float(1.1*size_2[1]/2), cglayer='met2', cwidth=1)
  nLoad.add_ports(Ruta_G3G4.get_ports_list(), prefix='G3G4_')
  nLoad.add_ports(Ruta_G9G10.get_ports_list(), prefix='G9G10_')

  #Ruteo source - drain
  if size_1[1] >= size_2[1]:
    Ruta_S3D9 = nLoad << c_route(pdk, M3M4.ports['SA_N'], M9M10.ports['DB_N'], viaoffset=(True,True), cglayer='met2', extension=size_1[1]/2)
    Ruta_S4D10 = nLoad << c_route(pdk, M3M4.ports['SB_N'], M9M10.ports['DA_N'], viaoffset=(True,True), cglayer='met2', extension=1.05*size_1[1]/2)
  else:
    Ruta_S4D10 = nLoad << c_route(pdk, M3M4.ports['SB_N'], M9M10.ports['DA_N'], viaoffset=(True,True), cglayer='met2', extension=1.05*size_2[1]/2)
    Ruta_S3D9 = nLoad << c_route(pdk, M3M4.ports['SA_N'], M9M10.ports['DB_N'], viaoffset=(True,True), cglayer='met2', extension=size_2[1]/2)
  nLoad.add_ports(Ruta_S3D9.get_ports_list(), prefix='S3D9_')
  nLoad.add_ports(Ruta_S4D10.get_ports_list(), prefix='S4D10_')

  #Ruteo source M9 y M10
  Ruta_S9S10 = nLoad << c_route(pdk, M9M10.ports['SA_S'], M9M10.ports['SB_S'], viaoffset=(True,True), cglayer='met4',extension=to_float(1.15*size_2[1]/2))
  nLoad.add_ports(Ruta_S9S10.get_ports_list(), prefix='S9S10_')

  #Ruteo Bulks VDD1 Top VDD2 Bot
  if size_1[1] > size_2[1]:
    Ruta_Bulks_1 = nLoad << L_route(pdk, M9M10.ports['VDD1_VSS1_N'], M3M4.ports['VDD1_VSS1_W'])
    Ruta_Bulks_2 = nLoad << L_route(pdk, M9M10.ports['VDD2_VSS2_S'], M3M4.ports['VDD2_VSS2_W'])
  else:
    Ruta_Bulks_1 = nLoad << L_route(pdk, M3M4.ports['VDD1_VSS1_N'], M9M10.ports['VDD1_VSS1_E'])
    Ruta_Bulks_2 = nLoad << L_route(pdk, M3M4.ports['VDD2_VSS2_S'], M9M10.ports['VDD2_VSS2_E'])
  nLoad.add_ports(Ruta_Bulks_1.get_ports_list(), prefix='Bulks_1_')
  nLoad.add_ports(Ruta_Bulks_2.get_ports_list(), prefix='Bulks_2_')

  #Falta el ruteo de los Bulks a GND
  Ruta_Bulk_Top_GND_1 = nLoad << c_route(pdk, M3M4.ports['VDD1_VSS1_E'], nLoad.ports['S9S10_con_E'], cglayer='met3', e2glayer='met2',viaoffset=(True,True), extension=size_1[0]*0.65, cwidth=0.5)
  Ruta_Bulk_Bot_GND_1 = nLoad << c_route(pdk, M3M4.ports['VDD2_VSS2_E'], nLoad.ports['S9S10_con_E'], cglayer='met3', e2glayer='met2',viaoffset=(True,True), extension=size_1[0]*0.65, cwidth=0.5)
  Ruta_Bulk_Top_GND_2 = nLoad << c_route(pdk, M9M10.ports['VDD1_VSS1_W'], nLoad.ports['S9S10_con_W'], cglayer='met3', viaoffset=(True,True), cwidth=0.5) #, extension=size_2[0]*0.15
  Ruta_Bulk_Bot_GND_2 = nLoad << c_route(pdk, M9M10.ports['VDD2_VSS2_W'], nLoad.ports['S9S10_con_W'], cglayer='met3', viaoffset=(True,True), cwidth=0.5) #, extension=size_2[0]*0.15

  #Creación de ports para conexión con otros componenetes
  #Lista de ports necesarios
  #Vout
  #VSS
  #Vcomn source de M4 y Drain de M10

  #Port VSS
  #Busco el puerto S9S10
  busqueda = [['S9S10', 'VSS', 70], ['S4D10_', 'Vcomn', 68]]
  for puerto, label, layer in busqueda:
    #Busco los puertos que contengan la palabra de busqueda y contengan W para solo tener puertos de dirección W
    puertos_W = [name for name in nLoad.ports if puerto in name and "W" in name]
    #Busco los puertos que contengan la palabra de busqueda y contengan con porque los ruteos en C solo generan los puertos de la ruta intermedia y se identifican con con
    puertos_con = [name for name in nLoad.ports if puerto in name and "con" in name]
    #Descomentar por si los quiere ver
    width = []
    pos = []
    for encontrados in puertos_W:
      #guardo el ancho de cada puerto encontrado con W
      width.append(nLoad.ports[encontrados].width)
    for encontrados in puertos_con:
      #guardo la posicion en la que se ubican los puerto de con
      pos.append(list(nLoad.ports[encontrados].center))

    #Calculo el largo del rectangulo de la capa pin
    Len = pos[1][0]-pos[0][0]
    #calculo la posicion del centro para ubicar el rectangulo de la capa pin
    center = [pos[0][0], pos[0][1]-width[0]/2]
    #Calculo la posicion del label
    center_label= [pos[0][0]/2+pos[1][0], pos[0][1]]
    #Creo el rectangulo de la capa pin para metal 2 de tupla de layer (70,16)
    pin_Met4 = rectangle(size=(Len,width[0]), layer=(layer,16))
    #Agrego y centro el rectangulo
    pin_1 = nLoad << pin_Met4
    pl = pin_1.bbox
    offset = -pl[0]
    pin_1.move(destination=offset)
    #Lo muevo a la direccion del centro calculada
    pin_1.movey(center[1]).movex(center[0])
    #Agrego el label en la posicion calculada y en la layer (70, 5) para labels de metal 2
    nLoad.add_label(label, position=center_label,  layer=(layer, 5))
    #Guardo sus ports
    nLoad.add_ports(pin_1.get_ports_list(), prefix=label+'_')

  nLoad.add_ports(M3M4.get_ports_list(), prefix='M3M4_')
  nLoad.add_ports(M9M10.get_ports_list(), prefix='M9M10_')

  #Creacion de port VOUT
  port_rectangle_met4 = rectangle((2,2), layer=pdk.get_glayer("met4"))
  VOUT_port = M3M4.ports['DB_N']
  via_VOUT = via_stack(pdk, 'met3','met4')
  via_VOUT_ref = align_comp_to_port(via_VOUT, VOUT_port, alignment=('c','t'))
  via_VOUT_port = via_VOUT_ref.ports["top_met_N"]
  VOUT = align_comp_to_port(port_rectangle_met4.copy(), via_VOUT_port, alignment=(None,'c'))
  nLoad.add(VOUT)
  VOUT_via = nLoad << via_VOUT
  pl = VOUT.bbox
  offset = -pl[0]
  VOUT.move(destination=offset)
  VOUT.movex(pdk.snap_to_2xgrid(1.1*size_1[0])).movey(pdk.snap_to_2xgrid(0.8*size_1[1]))
  VOUT_via.movex(pdk.snap_to_2xgrid(1.1*size_1[0]+1)).movey(pdk.snap_to_2xgrid(0.8*size_1[1]+1))
  nLoad.add_ports(VOUT.get_ports_list(), prefix='VOUT_Rect')
  nLoad.add_ports(VOUT_via.get_ports_list(), prefix='VOUT_via_')
  rename_ports_by_orientation(nLoad)

  #Rutear a VOUT
  ruta_D4VOUT = nLoad << c_route(pdk, M3M4.ports['DB_S'], nLoad.ports['VOUT_via_bottom_met_S'], cglayer='met2')
  nLoad.add_ports(ruta_D4VOUT.get_ports_list(), prefix='D4VOUT_')

  busqueda =  [['VOUT', 'VOUT']]
  for puerto, label in busqueda:
    #Obtengo el ancho del port en dirección W
    width = [nLoad.ports[puerto+'_W'].width]
    #Obtengo la posicion del port en dirección N (para estar centrado)
    pos = [list(nLoad.ports[puerto+'_N'].center)]
    #Calculo el centro del rectangulo de pin a agregar (se le resta el ancho para que quede en el centro y no sobre el borde N)
    center = [pos[0][0]-width[0]/2, pos[0][1]-width[0]]
    #Creo el rectangulo para pines en metal 3, layer (69,16)
    pin_Met3 = rectangle(size=(width[0],width[0]), layer=(70,16))
    #Agrego el pin y lo centro
    pin_1 = nLoad << pin_Met3
    pl = pin_1.bbox
    offset = -pl[0]
    pin_1.move(destination=offset)
    #Lo ubico a la posicion final calculada
    pin_1.movey(center[1]).movex(center[0])
    #Agrego el label para los metales 3, layer (69,5)
    nLoad.add_label(label, position=pos[0],  layer=(70, 5))
    #Agrego los ports al componente
    nLoad.add_ports(pin_1.get_ports_list(), prefix=label+'_')

  #centro todo el componente
  nLoad = transformed(prec_ref_center(nLoad))
  nLoad.unlock()
  nLoad =  rename_ports_by_orientation(nLoad).flatten()

  #nLoad.info['netlist'] = nLoad_netlist(fet3, fet4, fet9, fet10)

  return nLoad










  
def create_lvt_pcascode(pdk: MappedPDK) -> Component:

  m7 = {'name':'M7', 'width':1, 'length':3, 'multipliers':6, 'fingers':1, 'type':'pfet'}
  m8 = {'name':'M8', 'width':1, 'length':3, 'multipliers':6, 'fingers':1, 'type':'pfet'}
  m5 = {'name':'M5', 'width':1, 'length':1.5, 'multipliers':10, 'fingers':1, 'type':'pfet'}
  m6 = {'name':'M6', 'width':1, 'length':1.5, 'multipliers':10, 'fingers':1, 'type':'pfet'}

  matriz1 = [[0,1,2,1,1,2,1,0],
             [0,2,1,2,2,1,2,0]] #0 dummy, 1 mos A, 2 mos B
  matriz2 = [[0,1,2,1,1,2,1,0],
             [0,2,1,2,2,1,2,0],
             [0,1,2,1,1,2,1,0]] #0 dummy, 1 mos A, 2 mos B
  devices_info = [m7, m8, m5, m6] 

  # TODO: error checking
  pdk.activate()
  Pcascode = Component()
  # Create Interdigitized #(Interdigitation for the PCascode)

  if devices_info[0]['type']!=devices_info[1]['type']:
    raise ValueError('M1 and M2 must be same type')

  if devices_info[2]['type']!=devices_info[3]['type']:
    raise ValueError('M3 and M4 must be same type')

  Placement1 = macro_two_transistor_placement_Onchip(pdk, deviceA_and_B=devices_info[0]['type'], width1=devices_info[0]['width'], length1=devices_info[0]['length'],
                                                     fingers1=devices_info[0]['fingers'], width2=devices_info[1]['width'], length2=devices_info[1]['length'],
                                                     fingers2=devices_info[1]['fingers'], matriz = matriz1.copy(), with_substrate_tap=True, with_lvt_layer=True)

  Placement2 = macro_two_transistor_placement_Onchip(pdk, deviceA_and_B=devices_info[2]['type'], width1=devices_info[2]['width'], length1=devices_info[2]['length'],
                                                     fingers1=devices_info[2]['fingers'], width2=devices_info[3]['width'], length2=devices_info[3]['length'],
                                                     fingers2=devices_info[3]['fingers'], matriz = matriz2.copy(), with_substrate_tap=True, with_lvt_layer=True)


  size_1 = evaluate_bbox(Placement1.flatten()) # We find the size of every interdigitation block
  size_2 = evaluate_bbox(Placement2.flatten())



  M7M8 = Pcascode << Placement1 # We place the interdigitation on the top
  M5M6 = Pcascode << Placement2

  M7M8.movex(-1.1*size_1[0]/2) # We separate the interdigitation of M7M8 from M5M6 <---> through opposite movement
  M5M6.movex(1.1*size_2[0]/2)

  #Component routing (Gate routing)
  Route_G5G6 = Pcascode << c_route(pdk, M5M6.ports['GA_S'], M5M6.ports['GB_S'], viaoffset=(True,False), extension=to_float(1.25*size_1[1]/2), cglayer='met2')
  Route_G7G8 = Pcascode << c_route(pdk, M7M8.ports['GA_S'], M7M8.ports['GB_S'], viaoffset=(True,False), extension=to_float(1.1*size_2[1]/2), cglayer='met2', cwidth=1)
  Pcascode.add_ports(Route_G5G6.get_ports_list(), prefix='G5G6_')
  Pcascode.add_ports(Route_G7G8.get_ports_list(), prefix='G9G10_')

  #Source - drain routing
  if size_1[1] > size_2[1]:
    Route_D8S6 = Pcascode << c_route(pdk, M5M6.ports['SB_S'], M7M8.ports['DA_S'], viaoffset=(True,True), cglayer='met2', extension=1.05*size_1[1]/2)
    Route_D7S5 = Pcascode << c_route(pdk, M5M6.ports['SA_S'], M7M8.ports['DB_S'], viaoffset=(True,True), cglayer='met2', extension=0.7*size_1[1]/2)
  else:
    Route_D7S5 = Pcascode << c_route(pdk, M5M6.ports['SA_S'], M7M8.ports['DB_S'], viaoffset=(True,True), cglayer='met2', extension=0.7*size_1[1]/2)
    Route_D8S6 = Pcascode << c_route(pdk, M5M6.ports['SB_S'], M7M8.ports['DA_S'], viaoffset=(True,True), cglayer='met2', extension=1.05*size_2[1]/2)
  Pcascode.add_ports(Route_D7S5.get_ports_list(), prefix='D7S5_')
  Pcascode.add_ports(Route_D8S6.get_ports_list(), prefix='D8S6_')

  #VDD Routing
  Route_S7S8 = Pcascode << c_route(pdk, M7M8.ports['SA_N'], M7M8.ports['SB_N'], viaoffset=(True,True), extension=to_float(1.16*size_2[1]/2), cglayer='met2')
  Pcascode.add_ports(Route_S7S8.get_ports_list(), prefix='S7S8_')

  #Active load routing
  Route_D5G7 = Pcascode << c_route(pdk, M5M6.ports['GA_S'], M7M8.ports['DA_S'], viaoffset=(True,True), cglayer='met2', extension=1.28*size_2[1]/2)
  Pcascode.add_ports(Route_D5G7.get_ports_list(), prefix='D5G7_')

  #Creating via
  via_met2_3 = via_stack(pdk, 'met2', 'met3')
  Via_VDD_1 = Pcascode << via_met2_3
  Via_VDD_2 = Pcascode << via_met2_3
  Via_VDD_3 = Pcascode << via_met2_3
  Via_VDD_4 = Pcascode << via_met2_3
  pos_VDD_objetivo_M7M8_N = M7M8.ports['VDD1_VSS1_N'].center
  pos_VDD_objetivo_M5M6_N = M5M6.ports['VDD1_VSS1_N'].center
  pos_VDD_objetivo_M7M8_S = M7M8.ports['VDD2_VSS2_S'].center
  pos_VDD_objetivo_M5M6_S = M5M6.ports['VDD2_VSS2_S'].center
  Via_VDD_1.movex(pos_VDD_objetivo_M7M8_N[0]).movey(pos_VDD_objetivo_M7M8_N[1]-0.25)
  Via_VDD_2.movex(pos_VDD_objetivo_M5M6_N[0]).movey(pos_VDD_objetivo_M5M6_N[1]-0.25)
  Via_VDD_3.movex(pos_VDD_objetivo_M7M8_S[0]).movey(pos_VDD_objetivo_M7M8_S[1]+0.25)
  Via_VDD_4.movex(pos_VDD_objetivo_M5M6_S[0]).movey(pos_VDD_objetivo_M5M6_S[1]+0.25)
  Pcascode.add_ports(Via_VDD_1.get_ports_list(), prefix='Via_VDD_1_')
  Pcascode.add_ports(Via_VDD_2.get_ports_list(), prefix='Via_VDD_2_')
  Pcascode.add_ports(Via_VDD_3.get_ports_list(), prefix='Via_VDD_3_')
  Pcascode.add_ports(Via_VDD_4.get_ports_list(), prefix='Via_VDD_4_')
  rename_ports_by_orientation(Pcascode)


  #Ruteo Bulks VDD1 Top VDD2 Bot
  if size_1[1] < size_2[1]:
    Route_Bulks_1 = Pcascode << c_route(pdk, M7M8.ports['VDD1_VSS1_N'], M5M6.ports['VDD1_VSS1_N'], cglayer='met2',e1glayer='met3',e2glayer='met3')
    Route_Bulks_2 = Pcascode << c_route(pdk, M7M8.ports['VDD2_VSS2_S'], M5M6.ports['VDD2_VSS2_S'], cglayer='met2',e1glayer='met3',e2glayer='met3')
  else:
    Route_Bulks_1 = Pcascode << c_route(pdk, M5M6.ports['VDD1_VSS1_N'], M7M8.ports['VDD1_VSS1_N'], cglayer='met2',e1glayer='met3',e2glayer='met3')
    Route_Bulks_2 = Pcascode << c_route(pdk, M5M6.ports['VDD2_VSS2_S'], M7M8.ports['VDD2_VSS2_S'], cglayer='met2',e1glayer='met3',e2glayer='met3')
  Pcascode.add_ports(Route_Bulks_1.get_ports_list(), prefix='Bulks_1_')
  Pcascode.add_ports(Route_Bulks_2.get_ports_list(), prefix='Bulks_2_')

  #Falta el ruteo de los Bulks a VDD
  #Ruta_Bulk_Top_VDD_1 = Pcascode << c_route(pdk, M5M6.ports['VDD1_VSS1_E'], Pcascode.ports['S7S8_con_E'], cglayer='met3', e1glayer='met4', e2glayer='met4', viaoffset=(True,True), extension=size_1[0]*0.45)
  #Ruta_Bulk_Bot_VDD_1 = Pcascode << c_route(pdk, M5M6.ports['VDD2_VSS2_E'], Pcascode.ports['S7S8_con_E'], cglayer='met3', e1glayer='met4', e2glayer='met4', viaoffset=(True,True), extension=size_1[0]*0.45)
  #Ruta_Bulk_Top_VDD_2 = Pcascode << c_route(pdk, M7M8.ports['VDD1_VSS1_W'], Pcascode.ports['S7S8_con_W'], cglayer='met3', e1glayer='met4', e2glayer='met4', viaoffset=(True,True)) #, extension=size_2[0]*0.15
  #Ruta_Bulk_Bot_VDD_2 = Pcascode << c_route(pdk, M7M8.ports['VDD2_VSS2_W'], Pcascode.ports['S7S8_con_W'], cglayer='met3', e1glayer='met4', e2glayer='met4', viaoffset=(True,True)) #, extension=size_2[0]*0.15
  #Port VDD
  # We look after the S7S8 port
  busqueda = [['S7S8','VDD']]
  #Busco los puertos que contengan la palabra de busqueda y contengan W para solo tener puertos de dirección W
  puertos_W = [name for name in Pcascode.ports if busqueda[0][0] in name and "W" in name]
  #Busco los puertos que contengan la palabra de busqueda y contengan con porque los ruteos en C solo generan los puertos de la ruta intermedia y se identifican con con
  puertos_con = [name for name in Pcascode.ports if busqueda[0][0] in name and "con" in name]
  #Descomentar por si los quiere ver
  #print(puertos_con)
  width = []
  pos = []
  for encontrados in puertos_W:
    #guardo el ancho de cada puerto encontrado con W
    width.append(Pcascode.ports[encontrados].width)
  for encontrados in puertos_con:
    #guardo la posicion en la que se ubican los puerto de con
    pos.append(list(Pcascode.ports[encontrados].center))

  #Calculo el largo del rectangulo de la capa pin
  Len = pos[1][0]-pos[0][0]
  #calculo la posicion del centro para ubicar el rectangulo de la capa pin
  center = [pos[0][0], pos[0][1]-width[0]/2]
  #Calculo la posicion del label
  center_label= [pos[0][0]/2+pos[1][0], pos[0][1]]
  #Creo el rectangulo de la capa pin para metal 4 de tupla de layer (70,16)
  pin_Met4 = rectangle(size=(Len,width[0]), layer=(70,16))
  #Agrego y centro el rectangulo
  pin_1 = Pcascode << pin_Met4
  pl = pin_1.bbox
  offset = -pl[0]
  pin_1.move(destination=offset)
  #Lo muevo a la direccion del centro calculada
  pin_1.movey(center[1]).movex(center[0])
  #Agrego el label en la posicion calculada y en la layer (70, 5) para labels de metal 4
  Pcascode.add_label(busqueda[0][1], position=center_label,  layer=(70, 5))
  #Guardo sus ports
  Pcascode.add_ports(pin_1.get_ports_list(), prefix=busqueda[0][1]+'_')

  rename_ports_by_orientation(Pcascode)

  ruta_bulk_vdd = Pcascode << straight_route(pdk, M7M8.ports['VDD1_VSS1_N'], Pcascode.ports['VDD_S'], glayer2='met2')

  Pcascode.add_ports(M5M6.get_ports_list(), prefix='M5M6_')
  Pcascode.add_ports(M7M8.get_ports_list(), prefix='M7M8_')

  #centro todo el componente
  Pcascode = transformed(prec_ref_center(Pcascode))
  Pcascode.unlock()
  Pcascode =  rename_ports_by_orientation(Pcascode).flatten()

  #Pcascode.info['netlist'] = nLoad_netlist(fet3, fet4, fet9, fet10)

  return Pcascode