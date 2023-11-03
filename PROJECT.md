<p align="center">
  <a href="http://www.climatempo.com.br">
      <img src="http://i.imgur.com/Q9lCAMF.png" alt="Climatempo" width="300px"/>
  </a>
</p>

___


## Mirella's Recruiting Process: Data Engineer Jr

I used JupyterLab and python libraries to develop the entire project. The graphs plotted are shown in the .ipynb archive and are saved as .png archives. The rmsefile.nc contains the RMSE values requested by the challenge.

### Steps that have to be followed to execute this project:

#### 1) Install the packages used by me typing this command in the terminal:

```diff
pip install -r requirements.txt
```

The requirements.txt file holds the following packages:

##### - numpy 1.24.1
##### - matplotlib 3.8.1
##### - netCDF4 6.5
##### - seaborn 0.13.0
##### - session_info 1.0.0

##### - IPython 8.9.0
##### - jupyter_client 8.0.2
##### - jupyter_core 5.2.0
##### - jupyterlab 3.5.3
##### - notebook 6.5.2

#### 2) Execute the code:

My entire project, its respective explanation about every step performed, and the results are located in pythonstormgeo.ipynb (JupyterLab).
You will run all the cells by means of going to: Run -> Run All Cells and then, you will be able to see all of the results obtained with the software.

______

### Steps that the Python script goes through:

#### 1) Import libraries

#### 2) Read data from forecast.nc

#### 3) Check if there are missing, invalid, or not written data in forecast.nc file

3.1) To indicate that data values are missing, invalid, or not written, special values are conventionally used. NetCDF data may include variable values that are not written, either on purpose or unintentionally. To detect attempts to later read unwritten data, the netCDF library initializes data with the value of a variable's _FillValue attribute (in the case of this forecast dataset) 

#### 4) Access elements of forecast.nc variables

4.1) Access only the information of t2m variable

4.2) If you try to acess the elements of t2m variable (t2m_forecast = forecast.variables['t2m'][:,:,:]), python will give an error: missing_value not used since it cannot be safely cast to variable data type

4.3) The problem occurs because _FillValue should have the same data type as the variable it describes. The python interface checks for this. If the _FillValue and missing_value don't have the same data type, python interface tries to cast it to that type before using it to create a masked array. The problem is solved by turning off the auto conversion to masked arrays.

4.4) It is possible to check that the fill value nor the missing value are present (not written) in t2m_forecast

#### 5) Read data from observation.nc

#### 6) Check if there are missing, invalid, or not written data values in observation.nc file

#### 7) Access elements of observation.nc variables

#### 8) Nan values in temperatura variable

8.1) There are nan values in the temperatura variable (temperature_observation), so it is necessary to replace them before continuing

8.2) I decided to replace nan values with the mean of the temperature values that are not nan

8.3) Now, the temperatura variable (temperature_observation) doesn't have nan values

8.4) It is possible to check that the fill value nor the missing value aren't present (not written) in temperature_observation

#### 9) Convert temperature from Celsius to Kelvin

9.1) temperature_observation variable has to be converted from Celsius to Kelvin (SI unit). The reason is that t2m_forecast variable is in Kelvin (K) and temperature_observation variable is in Celsius (C).

#### 10) Data from São Paulo 

10.1) Data from São Paulo is obtained using the following coordinates: Latitude=8, Longitude=26 

#### 11) Calculate Root Mean Squared Error (RMSE) of 6-hour time periods

$\text{RMSE}(f, o) = \sqrt{\bar{(f - o)^2}}$

11.1) I computed two sets of values for the RMSE. The first (RMSE_matrix), computes the mean value only in the time dimension. That is, there are RMSE values for each latitude and longitude pair, for each time interval of 6 hours. The second (RMSE_array and RMSE_sp_array), computes the mean in all dimensions. That is, there is only one RMSE value for each 6 hour interval. This approach allows vizualization of the data both in terms of location (first set) and only in terms of the time interval (second set)

#### 12) Date and time of forecast and observation datasets

12.1) It is possible to see, by means of analysing the datasets information, that this data corresponds to: since 04/14/2018 (forecast) and since 04/13/2018 (observation). It will be taken into consideration the following day/month/year: since 04/14/2018, because corresponds to the real observations 

#### 13) Plot the heatmap of RMSE matrix values

13.1) Use Seaborn library to plot the heatmap of RMSE matrix values (RMSE of each 6-hour time period)

<p align="center">
  <a href="https://imgur.com/UZrUi2B">
      <img src="https://i.imgur.com/UZrUi2B.png" alt="Climatempo" width="900px"/>
  </a>
</p>

#### 14) Plot the graph of RMSE array values

14.1)  Use Matplotlib library to plot the graph of RMSE array values (RMSE of 6-hour time periods)

<p align="center">
  <a href="https://imgur.com/AjFxa4B">
      <img src="https://i.imgur.com/AjFxa4B.png" alt="Climatempo" width="700px"/>
  </a>
</p>

#### 15) Plot the graph of RMSE array values for São Paulo

15.1) Use Matplotlib library to plot the graph of RMSE array values (RMSE of 6-hour time periods) for São Paulo 

<p align="center">
  <a href="https://imgur.com/bTgHtTa">
      <img src="https://i.imgur.com/bTgHtTa.png" alt="Climatempo" width="600px"/>
  </a>
</p>

#### 16) Save RMSE values in a NetCDF archive

___

<p align="center">
  <a href="http://www.climatempo.com.br">
      <img src="https://i.imgur.com/n5jf0yD.png" alt="Climatempo" width="300px"/>
  </a>
</p>




