# Heat Exchanger Design Project

A project for heat exchanger design. It makes use of the cell method/matrix approach to calculate the resulting temperatures of the heat exchanger. Further information can be seen in [examples/theorie.pdf](examples/theorie.pdf).


## Navigation

- [How to install](#how-to-install)
- [Project structure](#project-structure)
- [Units systems](#units-systems)
- [List of properties](#list-of-properties)
    - TODO
- [List of methods](#list-of-methods)
    - TODO
- [Examples](#examples)
    - TODO

## How to install

1. Clone the repository to your local machine:

```shell
git clone <repository_url>
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
### TODO
* `examples/`
  - `heatexchanger_networks.ipynb`: Jupyter Notebook with examples for using the heat exchanger simulator.
  - `komplex_heatexchanger_network/`: Directory with more complex heat exchanger network definitions.
  - `simple_heatexchanger/`: Directory with simpler heat exchanger network definitions.
  - `theorie.pdf`: Theoretical documentation in PDF format.

* `exchanger/`
  - `__init__.py`: Marks the directory as a Python package.
  - `exchanger.py`: Implementation of the heat exchanger.
  - `exchanger_creator.py`: File for creating heat exchangers.
  - `exchanger_types.py`: Definitions of different types of heat exchangers.
  - `matrix_converter.py`: File for matrix conversion.
  - `network.py`: Contains network definitions.
  - `parts.py`: Definitions of various parts of the heat exchanger.
  - `stream.py`: Deals with the flow behavior in the heat exchanger.
  - `utils.py`: Helper functions for the heat exchanger.

* `tests/`
  - `__init__.py`: Marks the directory as a Python package.
  - `some_unittest_files`: Files with unit tests for the project.

* `pyfluids.json`: Configuration file for pyfluids in JSON format.

* `README.md`: This file.

* `requirements.txt`: File listing the project dependencies.



## Units systems

Calculations are performed in SI system, and temperature results are provided in K or °C. 


## Exchanger Library

The `Exchanger` library provides classes for modeling heat exchangers. It consists of the following files and classes:

### `exchanger.py` File

#### `HeatExchanger` Class

The `HeatExchanger` class represents a heat exchanger, which facilitates the exchange of heat between two fluid flows (hot and cold sides). It consists of the following properties and methods:

##### Properties:

- `name` (`str`): The name of the heat exchanger.
- `hot_side` (`Flow`): The hot side flow, an instance of the `Flow` class.
- `cold_side` (`Flow`): The cold side flow, an instance of the `Flow` class.
- `heat_transfer_rate` (`float`): The heat transfer rate in Watts (W).
- `heat_exchange_area` (`float`): The heat exchange area in square meters (m^2).

##### Methods:

- `heat_transfer_rate_str()`: Returns a formatted string for the heat transfer rate.
- `clone()`: Creates a new `HeatExchanger` object with the same properties.

##### Additional Information:

- The heat transfer rate is calculated based on the temperature difference between the hot and cold sides and the heat exchange area.

### `exchanger_creator.py` File

The `exchanger_creator.py` file provides a set of functions to create instances of heat exchangers with predefined configurations. It consists of the following functions:

#### `create_simple_heat_exchanger(name, hot_fluid, cold_fluid)`

Creates a simple heat exchanger with the given name, hot fluid, and cold fluid.

- Parameters:
  - `name` (`str`): The name of the heat exchanger.
  - `hot_fluid` (`Fluid`): The hot side fluid.
  - `cold_fluid` (`Fluid`): The cold side fluid.

- Returns:
  - `HeatExchanger`: The created heat exchanger.

#### `create_advanced_heat_exchanger(name, hot_fluid, cold_fluid, custom_property)`

Creates an advanced heat exchanger with additional custom properties.

- Parameters:
  - `name` (`str`): The name of the heat exchanger.
  - `hot_fluid` (`Fluid`): The hot side fluid.
  - `cold_fluid` (`Fluid`): The cold side fluid.
  - `custom_property` (`float`): An additional custom property.

- Returns:
  - `HeatExchanger`: The created heat exchanger.

### `exchanger_types.py` File

The `exchanger_types.py` file defines a set of classes representing different types of heat exchangers. It includes the following classes:

#### `ParallelFlowExchanger`

Represents a parallel-flow heat exchanger.

- Methods:
  - `__init__(self, name, hot_fluid, cold_fluid)`: Initializes a parallel-flow heat exchanger.
  - `simulate(self, duration)`: Simulates the heat exchange process for the specified duration.

#### `CounterFlowExchanger`

Represents a counter-flow heat exchanger.

- Methods:
  - `__init__(self, name, hot_fluid, cold_fluid)`: Initializes a counter-flow heat exchanger.
  - `simulate(self, duration)`: Simulates the heat exchange process for the specified duration.

#### `CrossFlowExchanger`

Represents a cross-flow heat exchanger.

- Methods:
  - `__init__(self, name, hot_fluid, cold_fluid)`: Initializes a cross-flow heat exchanger.
  - `simulate(self, duration)`: Simulates the heat exchange process for the specified duration.

### `matrix_converter.py` File

The `matrix_converter.py` file provides functions for converting data between matrices and other representations. It includes the following functions:

#### `list_to_matrix`

Converts a list of lists to a matrix (2D NumPy array).

- Parameters:
  - `data (list[list[float]]):` The input data in the form of a list of lists.

- Returns:
  - `numpy.ndarray:` The converted matrix.

#### `matrix_to_list`

Converts a matrix (2D NumPy array) to a list of lists.

- Parameters:
  - `matrix (numpy.ndarray):` The input matrix.

- Returns:
  - `list[list[float]]:` The converted list of lists.

### `network.py` File

The `network.py` file provides a class `Network` for creating and managing network structures. Here is an overview of the properties and methods within the file:

#### Class: `Network`

Represents a network structure with nodes and connections.

- **Properties:**
  - `nodes (List[Node]):` List of Node objects representing network nodes.
  - `connections (List[Connection]):` List of Connection objects representing connections between nodes.

- **Methods:**
  - `add_node(node: Node):` Adds a node to the network.
  - `add_connection(connection: Connection):` Adds a connection between nodes in the network.
  - `get_node_by_id(node_id: str):` Retrieves a node from the network based on its ID.
  - `get_connection_by_ids(start_id: str, end_id: str):` Retrieves a connection based on the IDs of its start and end nodes.
  - `remove_node(node_id: str):` Removes a node from the network based on its ID.
  - `remove_connection(start_id: str, end_id: str):` Removes a connection between nodes based on their IDs.
  - `get_node_ids():` Returns a list of IDs of all nodes in the network.
  - `get_connection_ids():` Returns a list of tuples representing the IDs of connected nodes.
  - `clear():` Clears the network by removing all nodes and connections.

TODO parts.py

### `stream.py` File

#### `Fluid` Class

##### Properties:

- `title` (`str`): The name of the fluid.
- `instance` (`str`): The type of fluid instance.
- `fluid` (`pyfluids.Fluid`): The fluid object associated with the instance.
- `pressure` (`float`): The pressure of the fluid in Pascals (Pa).
- `temperature` (`float`): The temperature of the fluid in Kelvin (K).

##### Methods:

- `ntp_state()`: Set the fluid properties to standard conditions (NTP).
- `clone()`: Create a new `Fluid` object by cloning the current one.

##### Additional Information:

- The `pyfluids` library must be installed to use this class.
- The unit system is initialized to the International System of Units (SI).

#### `Flow` Class

##### Properties:

- `in_fluid` (`Fluid`): The input fluid.
- `out_fluid` (`Fluid`): The output fluid.
- `volume_flow` (`float`): The volume flow rate in m^3/s.
- `pressure_loss` (`float`): The pressure loss in Pascals (Pa).
- `out_temperature` (`float`): The output temperature in Kelvin (K).
- `phase_change` (`bool`): Indicates if a phase change occurs in the flow.
- `mass_flow` (`float`): The mass flow rate in kg/s.
- `heat_capacity_flow` (`float`): The heat capacity flow rate in Watts per Kelvin (W/K).
- `heat_flow` (`float`): The heat flow rate in Watts (W).

##### Methods:

- `mass_flow_str()`: Returns a formatted string for mass flow rate.
- `heat_capacity_flow_str()`: Returns a formatted string for heat capacity flow rate.
- `heat_flow_str()`: Returns a formatted string for heat flow rate.
- `clone()`: Creates a new `Flow` object with the same properties.
- `clone_by_fluid(clone_fluid='in')`: Creates a new `Flow` object by cloning and using the specified input or output fluid.

##### Additional Information:

- Assumes incompressible flow.
- Warning: Phase changes in the flow may lead to issues.

### `utils.py` File

#### Functions:

#### `get_available_class_names`

**Purpose:** Get a list of class names defined in a module.

**Parameters:**
- `module` (`module`): The Python module to search for class names.
- `base_class` (optional): The base class to filter the results. Default is `None`.

**Returns:** A list of class names defined in the module.

#### `get_def_or_calc_value`

**Purpose:** Get a value based on defined and calculated values.

**Parameters:**
- `defined_value` (Any): The defined value.
- `calc_value` (Any): The calculated value.
- `default` (optional): The criteria for selecting the value ('defined', 'calculated', or 'default'). Default is 'defined'.
- `default_value` (optional): The default value to use if 'default' criteria is chosen. Default is `NotImplemented`.

**Returns:** The selected value based on the criteria.

## Examples

The use of the class to calculate a heat exchanger and necessary steps to get a result are shown in the example Jupyter notebooks in [examples](examples).
### `heatexchanger_network.ipynb`
