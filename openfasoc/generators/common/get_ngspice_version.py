import subprocess
import re

def check_ngspice_version() -> int:
    
    last_known_version = "42"
    result = subprocess.run(["ngspice", "--version"], capture_output=True, text=True)

    if result.returncode == 0:
        data = result.stdout.strip()
        match = re.search(r'ngspice-(\S+)', data)

        if match:
            ngspice_version = match.group(1)
            return ngspice_version == last_known_version
        else:
            print("Error parsing ngspice version.")
    else:
        print("Error getting ngspice version:", result.stderr)
    
    return 0
