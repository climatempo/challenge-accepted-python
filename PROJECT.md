# São Paulo Weather Forecast RSME From netCDF File


## Table of Contents

1. [Overview](#overview)
2. [Challenge](#challenge)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Contact](#contact)
7. [License](#license)

## Overview

**Disclaimer**
This repository is part of the technical interview for StormGeo Jr. Data Engineer position. 



## Challenge
The challenge includes: 
  - read two files NetCDF with temperature data, forecasted and observed
  - calculate Root Mean Square Error (RSME) for each 6 hour interval
  - plot 2D maps (x: index of the period, y: time series values)
  - create this file describing installation and usage
  - write the results in a NetCDF file 

## Requirements

Python version:

- Python (version 3.11.5)

Depedencies:

- pandas (version 2.1.1)
- numpy (version 1.26.0)
- netCDF4 (version 1.6.2)
- matplotlib (version 3.7.2)


## Installation

### For Windows:

1. **Clone the repository:**
   - You can use the Git Bash tool to execute the following command:
     ```sh
     git clone https://github.com/luizamfsantos/challenge-accepted-python.git
     ```

2. **Navigate to the project directory:**
   - Open Command Prompt (CMD) and use the following command:
     ```sh
     cd challenge-accepted-python
     ```

3. **Create and activate a conda virtual environment:**
   - In the CMD, use the following commands:
     ```sh
     conda create --name your_env_name
     conda activate your_env_name
     ```

4. **Install the required dependencies:**
   - Use Command Prompt (CMD) to execute the following command:
     ```sh
     pip install -r requirements.txt
     ```

### For MacOS and Linux:

1. **Clone the repository:**
   - Open the terminal and use the following command:
     ```sh
     git clone https://github.com/luizamfsantos/challenge-accepted-python.git
     ```

2. **Navigate to the project directory:**
   - In the terminal, use the following command:
     ```sh
     cd challenge-accepted-python
     ```

3. **Create and activate a conda virtual environment:**
   - In the terminal, use the following commands:
     ```sh
     conda create --name your_env_name
     conda activate your_env_name
     ```

4. **Install the required dependencies:**
   - In the terminal, use the following command:
     ```sh
     pip install -r requirements.txt
     ```

**More information about Conda environments:**
   - For more information about Conda and creating virtual environments, you can visit [the official Conda website](https://conda.io/miniconda.html).

## Usage

To run the project, follow these simple steps:

1. **Ensure you have followed the [**installation steps**](#installation) above.**
2. **Open a terminal or command prompt**.
3. **Navigate to the project directory**.
   ```sh
   cd challenge-accepted-python
   ```
4. **Run the following command**:
  ```sh
  python main.py
  ```
Running this command will execute the main script. Please ensure that you have the necessary dependencies installed before running the script.

During execution, you'll see the Root Mean Square Error (RMSE) for every 6 hours displayed in the terminal. Additionally, two time series graphs will be generated, showing the observed temperature versus predicted temperature, as well as the forecast error over time. These visualizations will provide insights into the performance of the forecasting model.

## Contact

For any inquiries or feedback regarding this project, please feel free to reach out to me:

**Luiza Santos**
- [**Email**](mailto:luiza.marques_@hotmail.com)
- [**GitHub**](http://github.com/luizamfsantos)
- [**LinkedIn**](https://www.linkedin.com/in/santosluiza/)

You can also open an issue on the [project's GitHub repository](https://github.com/luizamfsantos/challenge-accepted-python/issues) for any bug reports, feature requests, or general discussions related to the project.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
