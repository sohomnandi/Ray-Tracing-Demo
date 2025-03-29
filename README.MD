# Ray Tracing Shadow Simulation in Python 3.13.2

## Overview

This application demonstrates a real-time ray tracing shadow simulation using Pygame. It accurately models light rays interacting with a movable sphere, casting dynamic shadows. The simulation is designed to illustrate fundamental concepts of optics and ray tracing.

---

## Features

- Real-time light and shadow rendering using ray tracing.
- Interactive movement of the sphere and light source using keyboard controls.
- Realistic shadows and light occlusion.
- Adjustable parameters for more dense or sparse rays.

---

## Prerequisites

Ensure you have the following installed:

- **Python 3.13.2** or higher
- **Pygame 2.5.0** or higher
- **NumPy 1.25.2** or higher

We recommend creating a virtual environment for running the script and installing the dependencies to avoid it interfering with the main system.

To create a Virtual Environment:

```bash
python3 -m venv .
```
Navigate to the folder **Scripts**:

```bash
cd venv/Scripts
```

Activate the Virtual Environment:

For Windows users:
```powershell
.\activate.bat
```
For Linux users:
```bash
source ./activate.sh
```

To deactivate the Virtual Environment:
```bash
deactivate
```

You can install the dependencies using pip:

```bash
pip install pygame numpy
```
or use the requirements.txt

```bash
pip install -r requirements.txt
```

---

## How to Run the Application

1. Clone or download the repository containing the script.
2. Open your terminal or command prompt.
3. Navigate to the script’s directory.
4. Run the script using:

```bash
python -m Ray_Tracing.py
```

---

## Controls

Set the required parameters of the Rays, Light Source and the Sphere and then click **Start Simulation** button to start the simulation. The default values are already filled in for reference.

Use the following keys to move the sphere and light source:

- **Arrow Keys**: Move the sphere in the respective direction.
- **WASD Keys**: Move the Light Source in the respective direction.
- **Close Button**: Exit the simulation.

---

## Expected Behavior

- Light rays are cast from a fixed light source.
- The sphere casts realistic shadows, blocking light rays dynamically.
- When the sphere overlaps the light source, the source is obscured.

---

## Troubleshooting

- Ensure Python 3.13.2 and required packages are installed.
- If the simulation runs slowly, reduce the number of rays in the script.
- If errors occur, verify correct package versions are installed.
- Try using the pre-built **exe** file under releases for simplicity.

---

## Future Enhancements

- Soft shadows using multiple light sources.
- Realistic refraction and reflection effects.
- Eclipse simulation with more accurate optical effects.
