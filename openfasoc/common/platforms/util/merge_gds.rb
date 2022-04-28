# Ruby Script for merging gds files
# Please run the script within Klayout

layout = RBA::Layout.new

# list all input gds files here
files = Dir["./*.gds"]

load_layout_options = RBA::LoadLayoutOptions.new

files.each do |file_name|
  if !File.directory? file_name
    puts file_name

    # read the second file which basically performs the merge
    lmap = layout.read(file_name, load_layout_options)
    load_layout_options.set_layer_map(lmap, true)
  end
end

# specify output gds file
layout.write("./out/out.gds")
