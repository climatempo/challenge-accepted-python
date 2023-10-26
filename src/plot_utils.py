import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_2_graphs(df, y_col = "observed", pred_col = "predicted", error_col = "error"):
    plt.figure(figsize=(14, 6))

    # Graph 1: Plotting the observed and forecasted values over time
    plt.subplot(1, 2, 1)
    plt.plot(df.index, df[y_col], label='Temperature Observed', marker='o')
    plt.plot(df.index, df[pred_col], label='Temperature Forecasted', marker='o')
    plt.xlabel('Time')
    plt.ylabel('Temperature (K)')
    plt.title('Observed and Forecasted Temperature Over Time')
    plt.legend()

    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=18))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    # Graph 2: RSME over time
    plt.subplot(1, 2, 2)
    plt.plot(df.index, df[error_col], label='Root Squared error', marker='o', color='r')
    plt.xlabel('Time')
    plt.ylabel('RSME Values')
    plt.title('Graph of Root Squared Error Over Time')

    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=18))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    plt.show()

if __name__ == "__main__":
    from netcdf_utils import read_netcdf_to_dataframe
    from data_utils import time_to_datetime, celsius_to_kelvin, rse
    file_name = 'data/observation.nc'
    city_coordinates = (8,26)
    observed = read_netcdf_to_dataframe(file_name, city_coordinates)
    observed["time"] = time_to_datetime(observed["time"])
    observed["temperature"] = observed["temperature"].apply(celsius_to_kelvin)
    observed["observed"] = observed["temperature"]
    observed.drop(columns=["temperature"], inplace=True)
    print(observed.head())

    # Using the read_netcdf_to_dataframe function to the "forecast.nc" file
    file_name = 'data/forecast.nc'
    city_coordinates = (8,26)
    predicted = read_netcdf_to_dataframe(file_name, city_coordinates)
    predicted["time"] = time_to_datetime(predicted["time"])
    predicted["predicted"] = predicted["temperature"]
    predicted.drop(columns=["temperature"], inplace=True)
    print(predicted.head())

    # merge dataframes
    df = observed.merge(predicted, on=["time"])
    
    # calculate rmse
    df["error"] = rse(df,"observed","predicted")

    df.set_index("time", inplace=True)
    # Plot the graphs
    plot_2_graphs(df)
