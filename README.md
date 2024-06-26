# Heat Exchanger Design Tool

An object-oriented design tool to design any heat exchanger using the cell method/matrix approach to calculate the resulting temperatures of the heat exchanger. Further information about the solving algorithm can be seen in [examples/theorie.pdf](examples/theorie.pdf).
Any configuration of heat exchanger can be calculated utilizing the fluid data of pyfluids. The different configurations of various designs can either be calculated analytically by formulas (partly already implemented as a separate class) or by individual configurations using the cell method. More information can be found in the [examples](#examples).

## Navigation

- [How to install](#how-to-install)
- [Project structure](#project-structure)
- [Units system](#units-systems)
- [Examples](#examples)
    - [standard_heatexchangers.ipynb](#standard_heatexchangersipynb)
    - [heatexchanger_twoflows.ipynb](#heatexchanger_twoflowsipynb)
    - [complex_heatexchanger_networks.ipynb](#complex_heatexchanger_networksipynb)

## How to install

1. Clone the repository to your local machine:

```shell
git clone https://github.com/chris00Code/Heat-exchanger-design-tool.git
```

2. Navigate to the project directory:

```shell
cd <project_directory>
```

3. Install the required dependencies using the following command:

```shell
pip install -r requirements.txt
```


## Project structure
* `examples/`
  - `heatexchanger_networks.ipynb`: Jupyter Notebook with examples for using the heat exchanger simulator.
  - `komplex_heatexchanger_network/`: Directory with more complex heat exchanger network definitions.
  - `simple_heatexchanger/`: Directory with simpler heat exchanger network definitions.
  - `theorie.pdf`: Theoretical documentation in PDF format.

* `exchanger/`
  - `exchanger.py`: classes - implementation of heat exchangers with dimensionless parameters, as well predefined types.
  - `exchanger_creator.py`: function - to create a heat exchanger with 2 flows and equal cell properties
  - `exchanger_types.py`: classes - heat exchangers with 2 flows
  - `matrix_converter.py`: functions - to process info from matrices
  - `network.py`: class - implementation of solving a heat exchanger network with the cell methode
  - `parts.py`: classes - implementation of constructive parts of a heat exchanger 
  - `stream.py`: classes - implementation of fluids and flows 
  - `utils.py`: helper functions

* `tests/` files with unit tests

* `pyfluids.json`: Configuration file for pyfluids in JSON format.

* `README.md`: This file.

* `requirements.txt`: File listing the project dependencies.



## Units systems

Calculations are performed in SI system, and temperature results are provided in K or °C. 


## Examples

The use of the class to calculate a heat exchanger and necessary steps to get a result are shown in the example Jupyter notebooks in [examples](examples).

### [`standard_heatexchangers.ipynb`](examples/standard_heatexchangers.ipynb)
This notebook provides examples how to calculate the properties, in particular dimensionless parameters and fluid temperatures, of heat exchangers with predefined characteristics.  

### [`heatexchanger_twoflows.ipynb`](examples/heatexchanger_twoflows.ipynb)
The examples show in particular the application for a shell and tube heat exchanger with two fluid flows and without phase transition.
In particular, the use of the classes and functions provided is shown and these can be used to design simple shell-and-tube heat exchangers very quickly.

### [`complex_heatexchanger_networks.ipynb`](examples/complex_heatexchanger_networks.ipynb)
This notebook shows how to calculate more complex heat transfer networks. This requires the manual provision of structural matrices etc.
