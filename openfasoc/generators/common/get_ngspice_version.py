import subprocess
import re

def get_ngspice_version() -> int:
    result = subprocess.run(["ngspice", "--version"], capture_output=True, text=True)

    if result.returncode == 0:
        data = result.stdout.strip()
        match = re.search(r'ngspice-(\S+)', data)

        if match:
            ngspice_version = match.group(1)
            return ngspice_version
        else:
            print("Error parsing ngspice version.")
            return 0
    else:
        print("Error getting ngspice version:", result.stderr)
        return 0