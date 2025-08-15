import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import time
from datetime import datetime

st.set_page_config(page_title="IoT Normal Distribution Analyzer", layout="wide")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["timestamp", "temperature"])
if "running" not in st.session_state:
    st.session_state.running = False

# Function to simulate one temperature reading
def generate_temperature():
    base_temp = 22  # average room temperature
    variation = np.random.normal(0, 0.5)  # noise
    return round(base_temp + variation, 2)

st.title("IoT Temperature Distribution with Empirical Rule")

# Controls
col1, col2 = st.columns(2)
if col1.button("Start Simulation"):
    st.session_state.running = True
if col2.button("Stop Simulation"):
    st.session_state.running = False

# Live update loop
if st.session_state.running:
    new_row = {
        "timestamp": datetime.now(),
        "temperature": generate_temperature()
    }
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])],
        ignore_index=True
    )
    time.sleep(1)
    st.rerun()

# Show latest reading
if not st.session_state.data.empty:
    latest_temp = st.session_state.data.iloc[-1]
    st.metric("Latest Temperature (°C)", latest_temp["temperature"])

# Mean and std dev from actual data
if len(st.session_state.data) >= 2:
    mean = st.session_state.data["temperature"].mean()
    std_dev = st.session_state.data["temperature"].std()

    # Prepare normal curve
    x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
    y = norm.pdf(x, mean, std_dev)

    # Plot
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(x, y, color='black', linewidth=2, label='Normal Distribution')

    # Shade 95% empirical rule region
    lower_bound = mean - 2*std_dev
    upper_bound = mean + 2*std_dev
    x_fill = np.linspace(lower_bound, upper_bound, 500)
    ax.fill_between(x_fill, norm.pdf(x_fill, mean, std_dev), alpha=0.3, color='lightgreen', label='95% range')

    # Plot actual data points on curve
    temps = st.session_state.data["temperature"].values
    y_points = norm.pdf(temps, mean, std_dev)
    ax.scatter(temps, y_points, color='red', zorder=5, label='Data points')

    # Labels
    ax.set_title("IoT Temperature Distribution", fontsize=16)
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Probability Density")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# Show table of last readings
st.dataframe(st.session_state.data.tail(20))

# Download option
if not st.session_state.data.empty:
    csv = st.session_state.data.to_csv(index=False)
    st.download_button("Download Data as CSV", data=csv, file_name="temperature_data.csv", mime="text/csv")
