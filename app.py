import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

st.set_page_config(page_title="Normal Distribution Empirical Rule", layout="centered")

st.title("Normal Distribution with Empirical Rule")

# Sidebar controls
mean = st.sidebar.number_input("Mean (μ)", value=0.0, step=0.1)
std_dev = st.sidebar.number_input("Standard Deviation (σ)", value=1.0, step=0.1, min_value=0.1)

# Generate curve data
x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
y = norm.pdf(x, mean, std_dev)

# Create figure
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(x, y, color='black', linewidth=2)

# Shade 68% region (μ ± 1σ)
x_fill = np.linspace(mean - std_dev, mean + std_dev, 500)
ax.fill_between(x_fill, norm.pdf(x_fill, mean, std_dev), alpha=0.3, color='skyblue', label='68% of data')

# Shade 95% region (μ ± 2σ)
x_fill = np.linspace(mean - 2*std_dev, mean + 2*std_dev, 500)
ax.fill_between(x_fill, norm.pdf(x_fill, mean, std_dev), alpha=0.3, color='lightgreen', label='95% of data')

# Shade 99.7% region (μ ± 3σ)
x_fill = np.linspace(mean - 3*std_dev, mean + 3*std_dev, 500)
ax.fill_between(x_fill, norm.pdf(x_fill, mean, std_dev), alpha=0.3, color='lightcoral', label='99.7% of data')

# Lines for mean and ±σ
ax.axvline(mean, color='black', linestyle='--', label='Mean')
for i in range(1, 4):
    ax.axvline(mean - i*std_dev, color='gray', linestyle='--')
    ax.axvline(mean + i*std_dev, color='gray', linestyle='--')

# Labels
ax.set_title("Normal Distribution with Empirical Rule", fontsize=16)
ax.set_xlabel("Value")
ax.set_ylabel("Probability Density")
ax.legend()
ax.grid(True)

# Display in Streamlit
st.pyplot(fig)

