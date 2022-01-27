# Ruby Script for merging gds file together
# Please run the script within Klayout

layout = RBA::Layout.new

files = Dir["/home/elonjia/OpenFASOC/common/platforms/sky130osu15Ths/gds/*.gds"]

load_layout_options = RBA::LoadLayoutOptions.new
    
files.each do |file_name|
  if !File.directory? file_name
    puts file_name
	
    # read the second file which basically performs the merge
    lmap = layout.read(file_name, load_layout_options)
    load_layout_options.set_layer_map(lmap, true)
  end
end


layout.write("/home/elonjia/OpenFASOC/common/platforms/sky130osu15Ths/gds/sky130_osu_sc_15T_hs.gds")
