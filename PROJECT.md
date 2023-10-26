# São Paulo Weather Forecast RSME From netCDF File


## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Next Steps](#next-steps)
6. [Contact](#contact)
7. [License](#license)

## Overview

**Disclaimer**
*This repository is part of the technical interview for StormGeo Jr. Data Engineer position.* 

The main objective of this project is to assess the accuracy of weather forecasts using netCDF4 files for the time period between April 14, 2018, and April 17, 2018 for the city of Sao Paulo. The project aims to generate time series visualizations of observed temperature and forecasted temperature data and calculate Root Mean Square Error (RSME) values. 

The primary deliverables of this project include detailed graphical representations showcasing the forecasted and observed temperature trends, as well as the calculated RSME values. The project generates two significant output files, namely 'output.nc' and 'output_6hrs.nc,' which capture the errors over time and errors for every 6-hour period, respectively.

This project also presents an opportunity to understand the netCDF4 file structure, which might initially present a learning curve. However, once the structure is comprehended, navigating and extracting relevant information becomes more straightforward. For those unfamiliar with this file type, the project documentation provides insights and recommendations for understanding its unique structure and leveraging it effectively within the project's context.

Additionally, functions that can be found in the src folder are made so that they can easily be adapted for other file sizes and for analysis of other cities. Each function has extensive documentation for ease of use. 

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

## Next Steps

Continuous improvement is key to the success of any project. While this project has made significant strides, there are several areas where enhancements can be made to further refine its capabilities. Some of the immediate next steps include:

- Writing comprehensive unit tests for the netcdf_utils module to ensure robust functionality and stability. In particular, resolving issues related to generating mock data for testing purposes will be a priority. This involves delving deeper into the intricacies of the netCDF4 data format.

- Expanding the scope of data visualization by incorporating additional graphs to facilitate a more comprehensive analysis of forecast errors. This may involve exploring variance analysis and other statistical tools to gain deeper insights into the performance of the forecasting model.


## Contact

For any inquiries or feedback regarding this project, please feel free to reach out to me:

**Luiza Santos**
- [**Email**](mailto:luiza.marques_@hotmail.com)
- [**GitHub**](http://github.com/luizamfsantos)
- [**LinkedIn**](https://www.linkedin.com/in/santosluiza/)

You can also open an issue on the [project's GitHub repository](https://github.com/luizamfsantos/challenge-accepted-python/issues) for any bug reports, feature requests, or general discussions related to the project.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
