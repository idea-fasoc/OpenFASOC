# Flipped Voltage Follower (fvf)
fvf_params = {
    "type": {
        "values": ["nmos", "pmos"],
        "count": 1
    },
    "width": {
        "min": 0.5, "max": 10.0, "step": 0.25,
        "count": 2    # two devices
    },
    "length": {
        "min": 0.15, "max": 4.0, "step": 0.2,
        "count": 2
    },
    "fingers": {
        "min": 1, "max": 5, "step": 1,
        "count": 2
    },
    "multipliers": {
        "min": 1, "max": 2, "step": 1,
        "count": 2
    },
    "placement": {
        "values": ["horizontal", "vertical"],
        "count": 1
    }
}

# Transmission Gate
txgate_params = {
    "width": {
        "min": 0.5, "max": 10.0, "step": 0.25,
        "count": 2
    },
    "length": {
        "min": 0.15, "max": 4.0, "step": 0.2,
        "count": 2
    },
    "fingers": {
        "min": 1, "max": 5, "step": 1,
        "count": 2
    },
    "multipliers": {
        "min": 1, "max": 2, "step": 1,
        "count": 2
    }
}

# Current Mirror
cm_params = {
    "type": {
        "values": ["nmos", "pmos"],
        "count": 1
    },
    "numcols": {
        "min": 1, "max": 5, "step": 1,
        "count": 1
    },
    "width": {
        "min": 0.5, "max": 20.0, "step": 0.25,
        "count": 1
    },
    "length": {
        "min": 0.15, "max": 4.0, "step": 0.2,
        "count": 1
    }
}

# Differential Pair
diffpair_params = {
    "type": {
        "values": ["nmos", "pmos"],
        "count": 1
    },
    "width": {
        "min": 0.5, "max": 20.0, "step": 0.25,
        "count": 1
    },
    "length": {
        "min": 0.15, "max": 4.0, "step": 0.2,
        "count": 1
    },
    "fingers": {
        "min": 1, "max": 5, "step": 1,
        "count": 1
    },
    "short_source": {
        "values": [True, False],
        "count": 1
    }
}
