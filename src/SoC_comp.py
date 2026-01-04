#!/usr/bin/env python3
"""
SoC (SoC_est only) offline demo.

"""

import time
import random
from dataclasses import dataclass
from typing import List

# =========================
# Configuration
# =========================

TS = 0.1  # [s] demo sample time
CAPACITY_AH = 60.0  # demo capacity (Ah)
AH_TO_COULOMB = CAPACITY_AH * 3600.0
FULL_RANGE_KM = 25.0  # demo full-range (km)

CURRENT_POSITIVE_IS_CHARGE = True  # set False if your system uses +I as discharge

# Convention (set to match your system):
# current > 0  => CHARGE     => SoC increases
# current < 0  => DISCHARGE  => SoC decreases

# =========================
# Public OCV(SOC) LUT (cell)
# NOTE: LUT uses SOC in percent (0..100). Values are from a published Li-ion cell OCV table
# and are used here for demonstration only.
# =========================

SOC_PCT_LUT = [
    0.0, 2.36, 4.73, 7.09, 9.45, 12.38, 15.30, 24.17,
    33.03, 46.44, 59.85, 73.91, 87.98, 91.99, 95.99, 100.0
]

OCV_CELL_V_LUT = [
    2.6929, 3.1683, 3.3177, 3.3668, 3.3923, 3.4225, 3.4561, 3.5478,
    3.6094, 3.7059, 3.8368, 3.9740, 4.0759, 4.1018, 4.1315, 4.1710
]

N_SERIES = 12  # demo pack series count (e.g., 12s)

def interp1(x_table, y_table, x):
    if x <= x_table[0]:
        return y_table[0]
    if x >= x_table[-1]:
        return y_table[-1]
    for i in range(len(x_table) - 1):
        if x_table[i] <= x <= x_table[i + 1]:
            t = (x - x_table[i]) / (x_table[i + 1] - x_table[i])
            return y_table[i] + t * (y_table[i + 1] - y_table[i])
    return y_table[-1]

def soc_to_voltage_est(soc_pct):
    ocv_pack = [v * N_SERIES for v in OCV_CELL_V_LUT]
    return interp1(SOC_PCT_LUT, ocv_pack, soc_pct)

# =========================
# Estimator
# =========================

class BatterySoCEstimator:
    def __init__(self, ts=TS):
        self.ts = ts
        self.state = 0.7  # demo initial SoC (70%)
        self.soc_est = 70.0
        self.voltage_est = soc_to_voltage_est(self.soc_est)
        self.range_km = FULL_RANGE_KM * self.state

    def step(self, current_a):
        # Coulomb counting (discharge positive)
        sign = 1.0 if CURRENT_POSITIVE_IS_CHARGE else -1.0
        delta = (sign) * current_a / AH_TO_COULOMB * self.ts  # current sign convention
        self.state += delta
        self.state = max(0.0, min(1.0, self.state))

        self.soc_est = 100.0 * self.state
        self.voltage_est = soc_to_voltage_est(self.soc_est)
        self.range_km = FULL_RANGE_KM * self.state

# =========================
# Offline demo
# =========================

def generate_current_profile(duration_s=30.0):
    steps = int(duration_s / TS)
    profile = []
    for k in range(steps):
        t = k * TS
        if t < 10.0:
            i = 20.0     # +I charge (demo)
        elif t < 15.0:
            i = 0.0
        else:
            i = -10.0    # -I discharge (demo)
        profile.append(i)
    return profile

def main():
    est = BatterySoCEstimator(ts=TS)
    currents = generate_current_profile(30.0)

    print("Running offline SoC_est demo...\n")
    print(" t [s] | Current [A] | SoC_est [%] | V_est [V] | Range [km]")
    print("------------------------------------------------------------")

    step_print = int(0.5 / TS)

    for k, iA in enumerate(currents):
        est.step(iA)
        if k % step_print == 0:
            t = k * TS
            print(
                f"{t:6.2f} | {iA:11.2f} | {est.soc_est:10.2f} | "
                f"{est.voltage_est:9.2f} | {est.range_km:9.2f}"
            )

    print("\nDone. (Single SoC_est only)")

# =========================
# Realtime CAN template (commented)
# =========================

def realtime_can_template():
    """
    Example (COMMENTED):

        import can
        bus = can.Bus(interface="pcan", channel="PCAN_USBBUS1")

        while True:
            msg = bus.recv()
            if msg.arbitration_id == 0x100:
                current_a = ...
                est.step(current_a)
    """
    pass

if __name__ == "__main__":
    main()
