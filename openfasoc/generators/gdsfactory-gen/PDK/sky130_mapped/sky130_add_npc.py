from gdsfactory.component import Component
from gdsfactory.polygon import Polygon
from gdsfactory.geometry.boolean import boolean


def sky130_add_npc(comp: Component) -> Component:
	"""To keep with the generic generator structure,
	we do NOT add nitride poly cut layer in the generic generators (npc is specfic to sky130).
	Because it is easy to add idenpedently, 
	we implement this as a function wrapper to correctly lay npc
	returns the modified component"""
	# extract licon polygons which are over poly (using booleans)
	licon_comp = comp.extract(layers=[(66,44)])
	poly_comp = comp.extract(layers=[(66,20)])
	existing_npc = comp.extract(layers=[(95,20)])
	# TODO: see about an implemtation using gdsfactory component metadata
	if len(licon_comp.get_polygons()) < 2 and len(poly_comp.get_polygons()) < 2:
		return comp
	liconANDpoly = boolean(licon_comp, poly_comp, layer=(1,2), operation="and")
	if len(existing_npc.get_polygons()) > 1:
		liconANDpoly = boolean(liconANDpoly, existing_npc, layer=(1,2), operation="A-B")
	licon_polygons = liconANDpoly.get_polygons(as_array=False)
	# iterate through all licon and create npc (ignore merges for now)
	npc_polygons = list()
	for licon_polygon in licon_polygons:
		bbox = licon_polygon.bounding_box()
		licon_polygonxmin = bbox[0][0]
		licon_polygonymin = bbox[0][1]
		licon_polygonxmax = bbox[1][0]
		licon_polygonymax = bbox[1][1]
		padding_points = [
			[licon_polygonxmin - 0.1, licon_polygonymin - 0.1],
			[licon_polygonxmax + 0.1, licon_polygonymin - 0.1],
			[licon_polygonxmax + 0.1, licon_polygonymax + 0.1],
			[licon_polygonxmin - 0.1, licon_polygonymax + 0.1],
		]
		npc_polygons.append(Polygon(padding_points, layer=(95,20)))
	# determine which npc polygons should be merged 
	# also merge them by adding a polygon over them 
	# naive approach, n^2 complexity
	npc_merged_polygons = list()
	for i, npc_polygon in enumerate(npc_polygons):
		for j, other_polygon in enumerate(npc_polygons):
			# use the fact that all npc polys have the same width (at this point)
			yviolation = abs(npc_polygon.center[1] - other_polygon.center[1]) < 0.64#0.27+0.37
			xviolation = abs(npc_polygon.center[0] - other_polygon.center[0]) < 0.64
			if i==j:#skip same polygon
				continue
			elif (xviolation and yviolation):
				nxmax = max(npc_polygon.xmax, other_polygon.xmax)
				nxmin = min(npc_polygon.xmin, other_polygon.xmin)
				nymax = max(npc_polygon.ymax, other_polygon.ymax)
				nymin = min(npc_polygon.ymin, other_polygon.ymin)
				points = [
					[nxmin,nymin],
					[nxmax,nymin],
					[nxmax,nymax],
					[nxmin,nymax],
				]
				npc_merged_polygons.append(Polygon(points=points,layer=(95,20)))
	# add npc and return
	npc_polygons_to_add = npc_polygons + npc_merged_polygons
	comp.add(npc_polygons_to_add)
	return comp
