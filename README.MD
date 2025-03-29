# Ray Tracing Shadow Simulation in Python 3.13.2

## Overview

This application demonstrates a real-time ray tracing shadow simulation using Pygame. It accurately models light rays interacting with a movable sphere, casting dynamic shadows. The simulation is designed to illustrate fundamental concepts of optics and ray tracing.

---

## Features

- Real-time light and shadow rendering using ray tracing.
- Interactive movement of the sphere using keyboard controls.
- Realistic shadows and light occlusion.
- Adjustable parameters for more dense or sparse rays.

---

## Prerequisites

Ensure you have the following installed:

- **Python 3.13.2** or higher
- **Pygame 2.5.0** or higher
- **NumPy 1.25.2** or higher

You can install the dependencies using pip:

```bash
pip install pygame numpy
```

---

## How to Run the Application

1. Clone or download the repository containing the script.
2. Open your terminal or command prompt.
3. Navigate to the script’s directory.
4. Run the script using:

```bash
python ray_tracing_simulation.py
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

---

## Future Enhancements

- Soft shadows using multiple light sources.
- Realistic refraction and reflection effects.
- Eclipse simulation with more accurate optical effects.
