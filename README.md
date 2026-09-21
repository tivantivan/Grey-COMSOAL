# Grey COMSOAL for Assembly Line Balancing with Grey Task Times

This repository contains the Python source code and instance datasets for the paper:
> **"Assembly Line Balancing with Grey Task Times: A Grey COMSOAL Heuristic"**  
> *Journal:* Grey Systems: Theory and Application

## Overview
This code implements a heuristic approach based on Grey Systems Theory to solve Assembly Line Balancing Problems (ALBP) where task processing times are uncertain and represented as grey numbers.

## Repository Contents
- `GreyCOMSOAL_48tasks.json`: The 48-task test instance used for scalability and sensitivity analysis.
- Python implementation scripts for the Grey COMSOAL algorithm and regret-based ranking procedure.
- To run the code properly, ensure that all the following files are located in the **same directory (side by side)**:
- `main_app.py` (The main execution script)
- `grey_comparison.py` (Required module for grey comparison and ranking procedures)
- `grey_number_operation.py` (Required module for grey arithmetic)
- `line_balancing.py`((Required module for entering line balancing data)
- `comsol.py` (the main algorithem)
- `GreyCOMSOAL_48tasks.json` (The 48-task test instance used for scalability and sensitivity analysis)


## Usage
1. Before running the algorithm, ensure you have Python installed along with the required libraries.
2. Ensure you have Python installed.
3. Ensure that all Python script files (including main.py, grey_compar.py, and any other helper files) as well as the JSON dataset are placed together in the same folder.
4. Open your terminal or command prompt in that directory.
5. Execute the main script:
6. Load the dataset ( `GreyCOMSOAL_48tasks.json`).
7. Run the model
   
## Manuscript Status
This repository serves as supplemental material to support the manuscript titled:
**"Assembly Line Balancing with Grey Task Times: A Grey COMSOAL Heuristic"**  
*Status:* Currently under peer review at *Grey Systems: Theory and Application*.
