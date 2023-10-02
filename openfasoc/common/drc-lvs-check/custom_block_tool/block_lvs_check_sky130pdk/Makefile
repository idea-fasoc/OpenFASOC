#---------need to be modified by user--------------------------------------------
# the path for your gds file
GDS_FILE_PATH = /home/elonjia/Desktop/tool_package/ALIGN-public/work/DCDC_MUX/DCDC_MUX.gds
#the path for your cdl/ngspice file
CDL_FILE_PATH = /home/elonjia/Desktop/tool_package/ALIGN-public/work/DCDC_MUX/DCDC_MUX.sp
#the name for your block [the name of block in gds & cdl file must be same.]
DesignName = DCDC_MUX
#the path for your PDK file -> to sky130A eg: my sky130A file in the path: /home/elonjia/Desktop/tool_package/open_pdks/sky130/sky130A
export PDK_ROOT=/home/elonjia/Desktop/tool_package/open_pdks/sky130/
#--------------------------------------------------------------------------------
.PHONY: lvs
lvs :
	-mkdir RESULT_LVS
	-mkdir ORIGINAL_CDL
	-mkdir EXTRACT_CDL
	-mkdir EXTRACT_PEX
	-mkdir EXTRACT_SIM
	-mkdir FLATTEN_GDS
	cp $(CDL_FILE_PATH) ./ORIGINAL_CDL/$(DesignName).spice
#do lvs check using netgen
	bash run_lvspex.sh $(GDS_FILE_PATH) $(DesignName) ./RESULT_LVS/$(DesignName)_lvs.rpt
	-rm ./FLATTEN_GDS/*_flat.gds

clean:
	-rm -rf RESULT_LVS
	-rm -rf ORIGINAL_CDL
	-rm -rf EXTRACT_CDL
	-rm -rf EXTRACT_PEX
	-rm -rf EXTRACT_SIM
	-rm -rf FLATTEN_GDS
	-rm *.ext
