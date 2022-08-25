########################################################################################################################
# Copyright 2022 Mabrains Company LLC
#
# Licensed under the LGPL v2.1 License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
########################################################################################################################

import pandas as pd
import pya
import os

#print(os.system('pwd'))
lay_csv_map = os.path.join(os.path.dirname(os.path.realpath(__file__)), "gds_layers.csv")
lay_df = pd.read_csv(lay_csv_map)

# print(lay_df)
nsdm_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "nsdm") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]
psdm_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "psdm") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

diff_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "diff") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]
poly_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "poly") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]
licon_lay_str = lay_df.loc[
    (lay_df["Layer name"] == "licon1") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[0]
npc_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "npc") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]
li_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "li1") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]
mcon_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "mcon") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]
met1_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "met1") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]
tap_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "tap") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

nwell_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "nwell") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

via_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "via") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

met2_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "met2") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

met3_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "met3") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

met4_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "met4") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

met5_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "met5") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

via2_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "via2") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

via3_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "via3") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

via2_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "via2") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

via3_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "via3") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

via4_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "via4") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]
urpm_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "urpm") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]
poly_res_lay_str = \
lay_df.loc[(lay_df["Layer name"] == "poly") & (lay_df["Purpose"].str.contains("resistor")), "GDS layer:datatype"].values[
    0]


# print(diff_lay_str)

diff_lay_num = int(diff_lay_str.split(":")[0])
diff_lay_dt = int(diff_lay_str.split(":")[1])

poly_lay_num = int(poly_lay_str.split(":")[0])
poly_lay_dt = int(poly_lay_str.split(":")[1])

licon_lay_num = int(licon_lay_str.split(":")[0])
licon_lay_dt = int(licon_lay_str.split(":")[1])

nsdm_lay_num = int(nsdm_lay_str.split(":")[0])
nsdm_lay_dt = int(nsdm_lay_str.split(":")[1])

psdm_lay_num = int(psdm_lay_str.split(":")[0])
psdm_lay_dt = int(psdm_lay_str.split(":")[1])

npc_lay_num = int(npc_lay_str.split(":")[0])
npc_lay_dt = int(npc_lay_str.split(":")[1])

li_lay_num = int(li_lay_str.split(":")[0])
li_lay_dt = int(li_lay_str.split(":")[1])

mcon_lay_num = int(mcon_lay_str.split(":")[0])
mcon_lay_dt = int(mcon_lay_str.split(":")[1])

met1_lay_num = int(met1_lay_str.split(":")[0])
met1_lay_dt = int(met1_lay_str.split(":")[1])

tap_lay_num = int(tap_lay_str.split(":")[0])
tap_lay_dt = int(tap_lay_str.split(":")[1])

nwell_lay_num = int(nwell_lay_str.split(":")[0])
nwell_lay_dt = int(nwell_lay_str.split(":")[1])

via_lay_num = int(via_lay_str.split(":")[0])
via_lay_dt = int(via_lay_str.split(":")[1])

met2_lay_num = int(met2_lay_str.split(":")[0])
met2_lay_dt = int(met2_lay_str.split(":")[1])

met3_lay_num = int(met3_lay_str.split(":")[0])
met3_lay_dt = int(met3_lay_str.split(":")[1])

met4_lay_num = int(met4_lay_str.split(":")[0])
met4_lay_dt = int(met4_lay_str.split(":")[1])

met5_lay_num = int(met5_lay_str.split(":")[0])
met5_lay_dt = int(met5_lay_str.split(":")[1])

via2_lay_num = int(via2_lay_str.split(":")[0])
via2_lay_dt = int(via2_lay_str.split(":")[1])

via3_lay_num = int(via3_lay_str.split(":")[0])
via3_lay_dt = int(via3_lay_str.split(":")[1])

via4_lay_num = int(via4_lay_str.split(":")[0])
via4_lay_dt = int(via4_lay_str.split(":")[1])

urpm_lay_num = int(urpm_lay_str.split(":")[0])
urpm_lay_dt = int(urpm_lay_str.split(":")[1])

poly_res_lay_num = int(poly_res_lay_str.split(":")[0])
poly_res_lay_dt = int(poly_res_lay_str.split(":")[1])





# Create layer #'s
# l_diff = layout.layer(diff_lay_num, diff_lay_dt)  # Diffusion
# l_poly = layout.layer(poly_lay_num, poly_lay_dt)  # Poly
# l_nsdm = layout.layer(nsdm_lay_num, nsdm_lay_dt)  # nsdm source drain impalnt
# l_psdm = layout.layer(psdm_lay_num, psdm_lay_dt)  # psdm source drain impaln
# l_licon = layout.layer(licon_lay_num, licon_lay_dt)  # licon local interconnect
# l_npc = layout.layer(npc_lay_num, npc_lay_dt)
# l_li = layout.layer(li_lay_num, li_lay_dt)
# l_mcon = layout.layer(mcon_lay_num, mcon_lay_dt)
# l_met1 = layout.layer(met1_lay_num, met1_lay_dt)
# l_tap = layout.layer(tap_lay_num, tap_lay_dt)
# l_nwell = layout.layer(nwell_lay_num, nwell_lay_dt)
# l_via = layout.layer(via_lay_num, via_lay_dt)



