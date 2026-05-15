import streamlit as st
import matplotlib.pyplot as plt
from beam_engine import beam_analysis

# ---------------------------
# TITLE
# ---------------------------
st.title("Advanced Beam Analysis System")

# ---------------------------
# INPUTS
# ---------------------------

beam_length = st.number_input("Beam Length (m)", value=10.0)

# ---------------------------
# SUPPORTS
# ---------------------------

supports = []

st.subheader("Supports (2 required for stability)")

for i in range(2):

    col1, col2 = st.columns(2)

    with col1:
        s_type = st.selectbox(
            f"Support Type {i+1}",
            ["pin", "roller", "fixed", "hinge", "spring"],
            key=f"type_{i}"
        )

    with col2:
        pos = st.number_input(
            f"Position {i+1}",
            value=float(i*5),
            key=f"pos_{i}"
        )

    supports.append({"type": s_type, "position": pos})

# ---------------------------
# LOADS
# ---------------------------

num_loads = st.number_input("Number of Loads", value=1, step=1)

loads = []

for i in range(int(num_loads)):

    st.subheader(f"Load {i+1}")

    load_type = st.selectbox(
        "Type",
        ["point", "udl", "moment"],
        key=f"load_{i}"
    )

    if load_type == "point":
        P = st.number_input("Force (kN)", key=f"P{i}")
        a = st.number_input("Position (m)", key=f"a{i}")
        loads.append({"type": "point", "P": P, "a": a})

    elif load_type == "udl":
        w = st.number_input("Intensity (kN/m)", key=f"w{i}")
        start = st.number_input("Start", key=f"s{i}")
        end = st.number_input("End", key=f"e{i}")
        loads.append({"type": "udl", "w": w, "start": start, "end": end})

    elif load_type == "moment":
        M = st.number_input("Moment (kN-m)", key=f"M{i}")
        a = st.number_input("Position", key=f"ma{i}")
        loads.append({"type": "moment", "M": M, "a": a})

# ---------------------------
# RUN ANALYSIS
# ---------------------------

if st.button("Run Analysis"):

    x, V, M, RA, RB = beam_analysis(beam_length, supports, loads)

    st.success("Analysis Complete")

    st.write(f"Reaction A: {RA:.2f} kN")
    st.write(f"Reaction B: {RB:.2f} kN")

    fig, ax = plt.subplots(2, 1, figsize=(8, 6))

    ax[0].plot(x, V)
    ax[0].set_title("Shear Force Diagram")

    ax[1].plot(x, M)
    ax[1].set_title("Bending Moment Diagram")

    st.pyplot(fig)
