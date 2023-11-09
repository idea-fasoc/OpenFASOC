"""read rule deck we have saved in google sheets into a better format for writing to python:
this is the google sheets format
https://docs.google.com/spreadsheets/d/172P-CW_dGQU5icyUQAasLVq7Jlz51R5lB1rJ4JyvfIc/edit?usp=sharing

directions
1) go to the google sheets and download as .csv
2) run this program with the csv input
"""

import csv
from pathlib import Path
from pydantic import validate_arguments


def split_rule(rule: str) -> tuple:
    """Accepts a rule in the expected format and splits into rule name and float value"""
    if (rule != "") and (not "," in rule):
        raise ValueError("rule may be formatted wrong " + rule)
    rule = rule.replace(" ", "").split(",", maxsplit=1)[-1]
    rtr = rule.split("=")
    if len(rtr) != 2:
        rtr.append("*****FIXTHIS!!!MANUALLY!*****")
    elif "," in rtr[1]:
        strlist = rtr[1].replace("(", "").replace(")", "").split(",")
        rtr[1] = tuple([int(layint) for layint in strlist])
    else:
        rtr[1] = float(rtr[1])
    return tuple(rtr)


def __str_rules(groupdata: tuple, group: list, glayers: list) -> str:
    """appends the rules in groupdata to output"""
    group_rules = str()
    for edgenum, edge in enumerate(groupdata):
        group_rules += 'grulesobj["' + group[1] + '"]'
        group_rules += '["' + glayers[edgenum] + '"] = ' + str(edge)
        group_rules += "\n"
    return group_rules


def create_ruledeck_python_dictionary_definition(csvtoread: Path):
    if not csvtoread.is_file():
        raise RuntimeError("csv to read must be a file")
    output = str()
    glayers = list()
    groupdata = []  # list of dictionary
    group = [0, "none"]
    # int,string -> current group
    with open(csvtoread, newline="") as csvfile:
        myreader = csv.reader(csvfile, delimiter=",")
        for rownum, row in enumerate(myreader):
            # deal with header and ignore label rows
            if rownum == 0:
                glayers = row
                glayers.pop(0)
            elif rownum < 3:
                continue
            # processing logic
            # the google sheets csv format is in rows of 3
            # we use group and groupdata to track all rules in a row then update output
            else:
                if group[0] == 0:  # first in group
                    groupdata.clear()
                    group[1] = row[0]
                    for colnum, col in enumerate(row):
                        if colnum == 0:
                            continue
                        groupdata.append(dict())
                for colnum, col in enumerate(row):
                    if colnum == 0:
                        continue
                    if col == "":
                        continue
                    key_val_pair = split_rule(col)
                    groupdata[colnum - 1][key_val_pair[0]] = key_val_pair[1]
                # finished with the group
                if group[0] == 2:  # last in group
                    output += __str_rules(groupdata, group, glayers)
                # update group index
                group[0] = (group[0] + 1) % 3
        # incase missed last group print one more time
        last_grp_rules = __str_rules(groupdata, group, glayers)
        output += "\n" if last_grp_rules in output else last_grp_rules
    return output


@validate_arguments
def visualize_ruleset(ruleset: dict):
    """use networkx to print a visual of the ruleset graph
    nodes are glayers (strings)
    edges are rules (tuple[name:value])
    """
    import pygraphviz as pgv
    ruleGraph = pgv.AGraph(strict=False, directed=False, multigraph=True)
    ruleGraph.add_nodes_from(ruleset.keys())
    for glayer1 in ruleset.keys():
        for glayer2 in ruleset[glayer1].keys():
            for rule, value in ruleset[glayer1][glayer2].items():
                color="black"
                if "min_separ" in rule:
                    color="red"
                elif "min_enclos" in rule:
                    color = "blue"
                elif "width" in rule:
                    color = "orange"
                #ruleGraph.add_edge(glayer1,glayer2,label=value,color=color,key=rule)
                ruleGraph.add_edge(glayer1,glayer2,color=color,key=rule)
    ruleGraph.draw("test.png",format="png",prog="dot")


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        prog="print rules", description="read rule deck we have saved in google sheets"
    )
    parser.add_argument("-f", "--file", help="path of csv file to read")
    parser.add_argument(
        "-c",
        "--code",
        action="store_true",
        help="true/false write python file to current dir",
    )
    args = parser.parse_args()
    csvtoread = Path(args.file).resolve()
    output = create_ruledeck_python_dictionary_definition(csvtoread)
    print(output)
    if args.code:
        append_front = """from pdk.mappedpdk import MappedPDK\n
grulesobj = dict()
for glayer in MappedPDK.valid_glayers:
    grulesobj[glayer] = dict((x, None) for x in MappedPDK.valid_glayers)\n
"""
        output = append_front + output
        with open("grules.py", "w") as outputpy:
            outputpy.write(output)
