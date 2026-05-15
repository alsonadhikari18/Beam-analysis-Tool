import numpy as np

def beam_analysis(beam_length, supports, loads):

    support_A = supports[0]["position"]
    support_B = supports[1]["position"]

    span = support_B - support_A

    total_vertical = 0
    total_moment_A = 0

    # ---------------------------
    # REACTIONS CALCULATION
    # ---------------------------

    for load in loads:

        if load["type"] == "point":
            P = load["P"]
            a = load["a"]

            total_vertical += P
            total_moment_A += P * (a - support_A)

        elif load["type"] == "udl":
            w = load["w"]
            start = load["start"]
            end = load["end"]

            length = end - start
            W = w * length
            centroid = (start + end) / 2

            total_vertical += W
            total_moment_A += W * (centroid - support_A)

        elif load["type"] == "moment":
            total_moment_A += load["M"]

    RB = total_moment_A / span
    RA = total_vertical - RB

    # ---------------------------
    # SHEAR & MOMENT
    # ---------------------------

    x = np.linspace(0, beam_length, 500)

    V = []
    M = []

    for xi in x:

        shear = 0
        moment = 0

        if xi >= support_A:
            shear += RA
            moment += RA * (xi - support_A)

        if xi >= support_B:
            shear += RB
            moment += RB * (xi - support_B)

        for load in loads:

            if load["type"] == "point":
                if xi >= load["a"]:
                    shear -= load["P"]
                    moment -= load["P"] * (xi - load["a"])

            elif load["type"] == "udl":
                if xi > load["start"]:
                    eff = min(xi, load["end"]) - load["start"]
                    if eff > 0:
                        W = load["w"] * eff
                        centroid = load["start"] + eff / 2
                        shear -= W
                        moment -= W * (xi - centroid)

            elif load["type"] == "moment":
                if xi >= load["a"]:
                    moment -= load["M"]

        V.append(shear)
        M.append(moment)

    return x, V, M, RA, RB
