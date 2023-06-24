"""read rule deck we have saved in google sheets into a better format for writing to python:
this is the google sheets format
https://docs.google.com/spreadsheets/d/172P-CW_dGQU5icyUQAasLVq7Jlz51R5lB1rJ4JyvfIc/edit?usp=sharing

directions
1) go to the google sheets and download as .csv
2) run this program with the csv input
"""

import csv
from pathlib import Path


def split_rule(rule: str) -> tuple:
    """Accepts a rule in the expected format and splits into rule name and float value"""
    if (rule != "") and (not "," in rule):
        raise ValueError("rule may be formatted wrong " + rule)
    rule = rule.replace(" ", "").split(",")[-1]
    rtr = rule.split("=")
    if len(rtr) != 2:
        rtr.append("*****FIXTHIS!!!MANUALLY!*****")
    else:
        rtr[1] = float(rtr[1])
    return tuple(rtr)


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
                # finished with the group so
                if group[0] == 2:  # last in group
                    for edgenum, edge in enumerate(groupdata):
                        output += (
                            'grulesobj["'
                            + group[1]
                            + '"]["'
                            + glayers[edgenum]
                            + '"] = '
                            + str(edge)
                        ) + "\n"
                # update group index
                group[0] = (group[0] + 1) % 3
        # incase missed last group print one more time
        for edgenum, edge in enumerate(groupdata):
            output += (
                'grulesobj["'
                + group[1]
                + '"]["'
                + glayers[edgenum]
                + '"] = '
                + str(edge)
            ) + "\n"
    return output


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        prog="print rules", description="read rule deck we have saved in google sheets"
    )
    parser.add_argument("-f", "--file")
    args = parser.parse_args()
    csvtoread = Path(args.file).resolve()
    output = create_ruledeck_python_dictionary_definition(csvtoread)
    print(output)
