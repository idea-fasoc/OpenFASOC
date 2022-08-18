#!/bin/python3 -f

import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulation input")
    parser.add_argument("--filename", help="inputs spice file", required=True)
    parser.add_argument(
        "--mostype", help="Mosfet Type", required=True, nargs="+", default=[]
    )
    # Model Name
    run_dict = {
        "pfet_lvt": {  # lmin    lmax    wmin     wmax
            "sky130_fd_pr__pfet_01v8_lvt__model.0": [2.0e-05, 1.0e-04, 7e-06, 1.0e-4],
            "sky130_fd_pr__pfet_01v8_lvt__model.1": [8e-06, 2.0e-05, 7e-06, 1.0e-4],
            "sky130_fd_pr__pfet_01v8_lvt__model.2": [4e-06, 8e-06, 7e-06, 1.0e-4],
            "sky130_fd_pr__pfet_01v8_lvt__model.3": [2e-06, 4e-06, 7e-06, 1.0e-4],
            "sky130_fd_pr__pfet_01v8_lvt__model.4": [1.5e-06, 2e-06, 7e-06, 1.0e-4],
            "sky130_fd_pr__pfet_01v8_lvt__model.5": [1e-06, 1.5e-06, 7e-06, 1.0e-4],
            "sky130_fd_pr__pfet_01v8_lvt__model.6": [5e-07, 1e-06, 7e-06, 1.0e-4],
            "sky130_fd_pr__pfet_01v8_lvt__model.7": [3.5e-07, 5e-07, 7e-06, 1.0e-4],
            "sky130_fd_pr__pfet_01v8_lvt__model.8": [2.0e-05, 1.0e-04, 5.0e-06, 7.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.9": [8e-06, 2.0e-05, 5.0e-06, 7.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.10": [4e-06, 8e-06, 5.0e-06, 7.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.11": [2e-06, 4e-06, 5.0e-06, 7.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.12": [1.5e-06, 2e-06, 5.0e-06, 7.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.13": [1e-06, 1.5e-06, 5.0e-06, 7.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.14": [5e-07, 1e-06, 5.0e-06, 7.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.15": [3.5e-07, 5e-07, 5.0e-06, 7.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.16": [
                2.0e-05,
                1.0e-04,
                3.0e-06,
                5.0e-6,
            ],
            "sky130_fd_pr__pfet_01v8_lvt__model.17": [8e-06, 2.0e-05, 3.0e-06, 5.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.18": [4e-06, 8e-06, 3.0e-06, 5.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.19": [2e-06, 4e-06, 3.0e-06, 5.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.20": [1.5e-06, 2e-06, 3.0e-06, 5.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.21": [1e-06, 1.5e-06, 3.0e-06, 5.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.22": [5e-07, 1e-06, 3.0e-06, 5.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.23": [3.5e-07, 5e-07, 3.0e-06, 5.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.24": [2.0e-05, 1.0e-04, 1e-06, 3.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.25": [8e-06, 2.0e-05, 1e-06, 3.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.26": [4e-06, 8e-06, 1e-06, 3.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.27": [2e-06, 4e-06, 1e-06, 3.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.28": [1.5e-06, 2e-06, 1e-06, 3.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.29": [1e-06, 1.5e-06, 1e-06, 3.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.30": [5e-07, 1e-06, 1e-06, 3.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.31": [3.5e-07, 5e-07, 1e-06, 3.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.32": [
                2.0e-05,
                1.0e-04,
                5.5e-07,
                1.0e-6,
            ],
            "sky130_fd_pr__pfet_01v8_lvt__model.33": [8e-06, 2.0e-05, 5.5e-07, 1.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.34": [4e-06, 8e-06, 5.5e-07, 1.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.35": [2e-06, 4e-06, 5.5e-07, 1.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.36": [1.5e-06, 2e-06, 5.5e-07, 1.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.37": [1e-06, 1.5e-06, 5.5e-07, 1.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.38": [5e-07, 1e-06, 5.5e-07, 1.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.39": [3.5e-07, 5e-07, 5.5e-07, 1.0e-6],
            "sky130_fd_pr__pfet_01v8_lvt__model.40": [
                2.0e-05,
                1.0e-04,
                4.2e-07,
                5.5e-7,
            ],
            "sky130_fd_pr__pfet_01v8_lvt__model.41": [8e-06, 2.0e-05, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__pfet_01v8_lvt__model.42": [4e-06, 8e-06, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__pfet_01v8_lvt__model.43": [2e-06, 4e-06, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__pfet_01v8_lvt__model.44": [1.5e-06, 2e-06, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__pfet_01v8_lvt__model.45": [1e-06, 1.5e-06, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__pfet_01v8_lvt__model.46": [5e-07, 1e-06, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__pfet_01v8_lvt__model.47": [3.5e-07, 5e-07, 4.2e-07, 5.5e-7],
        },
        "nfet_lvt": {
            "sky130_fd_pr__nfet_01v8_lvt__model.0": [8e-06, 1.0e-04, 7e-06, 1.0e-4],
            "sky130_fd_pr__nfet_01v8_lvt__model.1": [4e-06, 8e-06, 7e-06, 1.0e-4],
            "sky130_fd_pr__nfet_01v8_lvt__model.2": [2e-06, 4e-06, 7e-06, 1.0e-4],
            "sky130_fd_pr__nfet_01v8_lvt__model.3": [1e-06, 2e-06, 7e-06, 1.0e-4],
            "sky130_fd_pr__nfet_01v8_lvt__model.4": [5e-07, 1e-06, 7e-06, 1.0e-4],
            "sky130_fd_pr__nfet_01v8_lvt__model.5": [2.5e-07, 5e-07, 7e-06, 1.0e-4],
            "sky130_fd_pr__nfet_01v8_lvt__model.6": [1.8e-07, 2.5e-07, 7e-06, 1.0e-4],
            "sky130_fd_pr__nfet_01v8_lvt__model.7": [1.5e-07, 1.8e-07, 7e-06, 1.0e-4],
            "sky130_fd_pr__nfet_01v8_lvt__model.8": [8e-06, 1.0e-04, 5.05e-06, 7.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.9": [4e-06, 8e-06, 5.05e-06, 7.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.10": [2e-06, 4e-06, 5.05e-06, 7.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.11": [1e-06, 2e-06, 5.05e-06, 7.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.12": [5e-07, 1e-06, 5.05e-06, 7.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.13": [2.5e-07, 5e-07, 5.05e-06, 7.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.14": [
                1.8e-07,
                2.5e-07,
                5.05e-06,
                7.0e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.15": [
                1.5e-07,
                1.8e-07,
                5.05e-06,
                7.0e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.16": [8e-06, 1.0e-04, 5.0e-06, 5.05e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.17": [4e-06, 8e-06, 5.0e-06, 5.05e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.18": [2e-06, 4e-06, 5.0e-06, 5.05e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.19": [1e-06, 2e-06, 5.0e-06, 5.05e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.20": [5e-07, 1e-06, 5.0e-06, 5.05e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.21": [2.5e-07, 5e-07, 5.0e-06, 5.05e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.22": [
                1.8e-07,
                2.5e-07,
                5.0e-06,
                5.05e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.23": [
                1.5e-07,
                1.8e-07,
                5.0e-06,
                5.05e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.24": [8e-06, 1.0e-04, 3.01e-06, 5.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.25": [4e-06, 8e-06, 3.01e-06, 5.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.26": [2e-06, 4e-06, 3.01e-06, 5.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.27": [1e-06, 2e-06, 3.01e-06, 5.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.28": [5e-07, 1e-06, 3.01e-06, 5.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.29": [2.5e-07, 5e-07, 3.01e-06, 5.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.30": [
                1.8e-07,
                2.5e-07,
                3.01e-06,
                5.0e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.31": [
                1.5e-07,
                1.8e-07,
                3.01e-06,
                5.0e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.32": [8e-06, 1.0e-04, 3.0e-06, 3.01e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.33": [4e-06, 8e-06, 3.0e-06, 3.01e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.34": [2e-06, 4e-06, 3.0e-06, 3.01e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.35": [1e-06, 2e-06, 3.0e-06, 3.01e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.36": [5e-07, 1e-06, 3.0e-06, 3.01e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.37": [2.5e-07, 5e-07, 3.0e-06, 3.01e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.38": [
                1.8e-07,
                2.5e-07,
                3.0e-06,
                3.01e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.39": [
                1.5e-07,
                1.8e-07,
                3.0e-06,
                3.01e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.40": [8e-06, 1.0e-04, 1.65e-06, 3.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.41": [4e-06, 8e-06, 1.65e-06, 3.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.42": [2e-06, 4e-06, 1.65e-06, 3.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.43": [1e-06, 2e-06, 1.65e-06, 3.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.44": [5e-07, 1e-06, 1.65e-06, 3.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.45": [2.5e-07, 5e-07, 1.65e-06, 3.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.46": [
                1.8e-07,
                2.5e-07,
                1.65e-06,
                3.0e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.47": [
                1.5e-07,
                1.8e-07,
                1.65e-06,
                3.0e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.48": [8e-06, 1.0e-04, 1e-06, 1.65e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.49": [4e-06, 8e-06, 1e-06, 1.65e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.50": [2e-06, 4e-06, 1e-06, 1.65e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.51": [1e-06, 2e-06, 1e-06, 1.65e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.52": [5e-07, 1e-06, 1e-06, 1.65e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.53": [2.5e-07, 5e-07, 1e-06, 1.65e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.54": [1.8e-07, 2.5e-07, 1e-06, 1.65e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.55": [1.5e-07, 1.8e-07, 1e-06, 1.65e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.56": [8e-06, 1.0e-04, 8.4e-07, 1.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.57": [4e-06, 8e-06, 8.4e-07, 1.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.58": [2e-06, 4e-06, 8.4e-07, 1.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.59": [1e-06, 2e-06, 8.4e-07, 1.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.60": [5e-07, 1e-06, 8.4e-07, 1.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.61": [2.5e-07, 5e-07, 8.4e-07, 1.0e-6],
            "sky130_fd_pr__nfet_01v8_lvt__model.62": [
                1.8e-07,
                2.5e-07,
                8.4e-07,
                1.0e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.63": [
                1.5e-07,
                1.8e-07,
                8.4e-07,
                1.0e-6,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.64": [8e-06, 1.0e-04, 6.4e-07, 8.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.65": [4e-06, 8e-06, 6.4e-07, 8.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.66": [2e-06, 4e-06, 6.4e-07, 8.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.67": [1e-06, 2e-06, 6.4e-07, 8.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.68": [5e-07, 1e-06, 6.4e-07, 8.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.69": [2.5e-07, 5e-07, 6.4e-07, 8.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.70": [
                1.8e-07,
                2.5e-07,
                6.4e-07,
                8.4e-7,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.71": [
                1.5e-07,
                1.8e-07,
                6.4e-07,
                8.4e-7,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.72": [8e-06, 1.0e-04, 5.5e-07, 6.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.73": [4e-06, 8e-06, 5.5e-07, 6.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.74": [2e-06, 4e-06, 5.5e-07, 6.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.75": [1e-06, 2e-06, 5.5e-07, 6.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.76": [5e-07, 1e-06, 5.5e-07, 6.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.77": [2.5e-07, 5e-07, 5.5e-07, 6.4e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.78": [
                1.8e-07,
                2.5e-07,
                5.5e-07,
                6.4e-7,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.79": [
                1.5e-07,
                1.8e-07,
                5.5e-07,
                6.4e-7,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.80": [8e-06, 1.0e-04, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.81": [4e-06, 8e-06, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.82": [2e-06, 4e-06, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.83": [1e-06, 2e-06, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.84": [5e-07, 1e-06, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.85": [2.5e-07, 5e-07, 4.2e-07, 5.5e-7],
            "sky130_fd_pr__nfet_01v8_lvt__model.86": [
                1.8e-07,
                2.5e-07,
                4.2e-07,
                5.5e-7,
            ],
            "sky130_fd_pr__nfet_01v8_lvt__model.87": [
                1.5e-07,
                1.8e-07,
                4.2e-07,
                5.5e-7,
            ],
        },
        "nfet_3v3": {
            "sky130_fd_pr__nfet_03v3_nvt__model.0": [
                4.95e-07,
                5.05e-07,
                9.995e-06,
                1.0005e-5,
            ],
            "sky130_fd_pr__nfet_03v3_nvt__model.1": [
                4.95e-07,
                5.05e-07,
                9.95e-07,
                1.005e-6,
            ],
            "sky130_fd_pr__nfet_03v3_nvt__model.2": [
                5.95e-07,
                6.05e-07,
                9.95e-07,
                1.005e-6,
            ],
            "sky130_fd_pr__nfet_03v3_nvt__model.3": [
                4.95e-07,
                5.05e-07,
                3.995e-06,
                4.005e-6,
            ],
            "sky130_fd_pr__nfet_03v3_nvt__model.4": [
                4.95e-07,
                5.05e-07,
                4.15e-07,
                4.25e-7,
            ],
            "sky130_fd_pr__nfet_03v3_nvt__model.5": [
                5.95e-07,
                6.05e-07,
                4.15e-07,
                4.25e-7,
            ],
            "sky130_fd_pr__nfet_03v3_nvt__model.6": [
                7.95e-07,
                8.05e-07,
                4.15e-07,
                4.25e-7,
            ],
            "sky130_fd_pr__nfet_03v3_nvt__model.7": [
                4.95e-07,
                5.05e-07,
                6.95e-07,
                7.05e-7,
            ],
            "sky130_fd_pr__nfet_03v3_nvt__model.8": [
                5.95e-07,
                6.05e-07,
                6.95e-07,
                7.05e-7,
            ],
        },
    }
    args = parser.parse_args()
    fileh = open(args.filename)
    spfile = fileh.read()
    for mostype in args.mostype:
        os.system(f"mkdir -p {mostype}")
        for binname, binval in run_dict[mostype].items():
            if mostype == "pfet_lvt":
                print("Type", mostype, binname)
                Lnew = 1e6 * (binval[0] + binval[1]) / 2
                Wnew = 1e6 * (binval[2] + binval[3]) / 2
                newspfile = spfile.replace(
                    "L=0.15 W=0.42", f"L={Lnew} W={Wnew}"
                ).replace("*XM3", "XM3")
            elif mostype == "nfet_lvt":
                print("Type", mostype, binname)
                Lnew = 1e6 * (binval[0] + binval[1]) / 2
                Wnew = 1e6 * (binval[2] + binval[3]) / 2
                newspfile = spfile.replace(
                    "L=0.15 W=0.42", f"L={Lnew} W={0.42}"
                ).replace("*XM1", "XM1")
            elif mostype == "nfet_3v3":
                print("Type", mostype, binname)
                Lnew = 1e6 * (binval[0] + binval[1]) / 2
                Wnew = 1e6 * (binval[2] + binval[3]) / 2
                newspfile = spfile.replace(
                    "L=0.15 W=0.42", f"L={Lnew} W={Wnew}"
                ).replace("*XM6", "XM6")
            filen = open(f"{mostype}/{binname}", mode="w")
            filen.write(newspfile)
            filen.close()
            # Run Xyce
            print(f"Running Xyce with Lnew:{Lnew} and Wnew:{Wnew}")
            os.system(
                f"~/Tools/XyceSerial/bin/Xyce {mostype}/{binname} -l {mostype}/{binname}.log"
            )
