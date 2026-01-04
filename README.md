# SoC_estimation

# Li-ion State of Charge (SoC) Estimation – Model-Based Demo

This repository presents a **model-based Li-ion battery State of Charge (SoC) estimation demo**, implemented as a Python script.

The core estimation logic is derived from a **continuous-time mathematical battery model originally developed in MATLAB/Simulink**.  
The algorithm was subsequently **manually refactored and simplified into Python** to create a **public-safe, portable demonstration** independent of proprietary toolchains.

---

## Overview

The demo implements:
- Coulomb counting–based SoC estimation
- Open-Circuit Voltage (OCV) estimation using a **published Li-ion OCV–SoC lookup table**
- Pack-level voltage estimation via series cell scaling
- Offline execution with a synthetic current profile (no hardware required)

All numerical parameters are **generic demonstration values** and do not represent any specific commercial battery pack or vehicle.

---

## Key Characteristics

- **SoC state** (`SoC_est`)
- Model-based structure consistent with embedded implementations
- Explicit current sign convention (configurable)
- Hardware-independent offline execution
- Realtime CAN integration intentionally left as a commented template

---

## Running the Demo

```bash
python SoC_comp.py
