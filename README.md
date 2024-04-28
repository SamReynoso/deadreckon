# Deadreckon
It took several hours, but I prompted it out of ChatGPT.

## Maritime Navigation Simulation

This document provides an overview of a Python program designed to simulate 
and visualize maritime navigation processes.

### Functionality Overview

1. **CSV Data Handling**: The program reads and writes data from CSV files 
containing information about coordinates, instrument readings (e.g., wind 
speed and direction, water current speed and direction), and other relevant 
data for navigation.

2. **Navigation Simulation**: It simulates a navigation process using dead 
reckoning, estimating the current position based on a previously determined 
position and adjusting for factors like wind and water currents. The program 
calculates vectors representing wind, water, and craft movement to determine 
the craft's new position.

3. **CLI Interface**: The program provides a command-line interface (CLI) for 
user interaction. Users can set parameters such as craft speed and journey 
limit, view status updates during the simulation, and make adjustments as 
needed.

4. **Visualization**: It includes functionality for visualizing the navigation 
process using matplotlib, a Python plotting library. The program plots the 
craft's path, target destination, and other relevant vectors to provide a 
visual representation of the navigation simulation.

Overall, the code serves as a tool for simulating and visualizing maritime 
navigation processes, particularly focusing on dead reckoning techniques.

