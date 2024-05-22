# What is Glayout strictsyntax?
Glayout strictsyntax is a command language for producing analog circuit layout.
## commands and syntax
Below are some example commands
place command: place an genidhere called/named compnamehere with paramshere
route command: route between/from port1 and/to port2 using routetype with paramshere
absolute move command: move compname [by] (x,y)
relative move command: move compname [filler words] direction [filler words] reference_comp [by/with separation]
import command: import comp1, comp2 from mod1, and comp3 from some/path/mod.py
NOTE: imports from glayout only need component name
NOTE: if mod name is not specified, it is assumed to be the component name
create parameter command: create/define [a/an] param_type parameter called/named paramname
create variable: create/define [a/an] var_type variable called/named varname =/equal valorexpr
