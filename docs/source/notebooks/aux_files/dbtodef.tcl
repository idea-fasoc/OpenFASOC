#!/usr/bin/tclsh
# run with openroad -no_init -exit dbtodef.tcl

# read a database file provided the input name set to from_oprd_ in env
read_db $::env(from_oprd_)

# write the database file provided the output name set to to_oprd_ in env
write_def $::env(to_oprd_)
