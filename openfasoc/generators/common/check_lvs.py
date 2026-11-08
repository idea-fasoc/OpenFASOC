"""
Reads a netgen LVS report and decides whether LVS passed.

netgen ends every `lvs` run with a "Final result:" block. LVS is clean only when that block says
"Circuits match uniquely." and reports no property errors and no failed subcells or pins. Any other
final result ("Netlists do not match.", "Top level cell failed pin matching.", ...) or a report
without a final result is a failure.

Returns:
    (clean, summary): clean is True only for a unique match; summary is the "Final result:" block on one line
"""


def lvs_result(lvs_filename):
    with open(lvs_filename) as f:
        report = f.read()
    pos = report.rfind("Final result:")
    if pos < 0:
        return False, "no 'Final result:' line in " + lvs_filename
    final = report[pos + len("Final result:"):].strip()
    clean = (
        final.startswith("Circuits match uniquely.")
        and "property error" not in final.lower()
        and "failed" not in final
        and "do not match" not in final
    )
    summary = " ".join(l.strip() for l in final.splitlines() if l.strip() not in ("", "."))
    return clean, summary
