import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

from utils import auth_functions
from utils.visualize_data import load_csv_files

auth_functions.check_authentication()

# Dataloader page content
st.title("Dataloader")
st.header("Load and Visualize CSV Files")

# Folder selection input
folder_path = st.text_input("Enter the folder path containing CSV files:")

# Placeholder for data storage
if 'dataframes' not in st.session_state:
    st.session_state.dataframes = {}

# Load and visualize data
if st.button("Load CSV Files"):
    if not folder_path or not os.path.isdir(folder_path):
        st.error("Please enter a valid folder path.")
    else:
        # Load CSV files and store them in session state
        st.session_state.dataframes = load_csv_files(folder_path)
        st.success(f"Loaded {len(st.session_state.dataframes)} files.")

# Visualization options
if st.session_state.dataframes:
    st.header("Visualization Options")

    # File selection
    file_selection = st.multiselect(
        "Select CSV files to visualize:",
        options=list(st.session_state.dataframes.keys()),
        default=list(st.session_state.dataframes.keys())  # Default to all files
    )

    # Grouping Option (Dropdown)
    group_count = st.selectbox("Number of Groups for Plotting", [1, 2, 3], index=0)

    groups = []
    chart_types = []  # Store chart type selection for each group
    for i in range(group_count):
        group_files = st.multiselect(f"Select files for Group {i+1}:", options=file_selection)
        groups.append(group_files)

        # Allow users to select chart type for each group
        chart_type = st.radio(f"Select Chart Type for Group {i+1}:", options=["Candlestick", "Line Chart"], index=0)
        chart_types.append(chart_type)

    # Plot the selected data
    if file_selection:
        # Plotting each group separately
        for group_index, group in enumerate(groups):
            if group:
                st.subheader(f"Group {group_index + 1} Chart")
                fig = go.Figure()
                for filename in group:
                    df = st.session_state.dataframes[filename]
                    # Ensure 'time' column is datetime
                    df['time'] = pd.to_datetime(df['time'])
                    if chart_types[group_index] == "Candlestick":
                        fig.add_trace(
                            go.Candlestick(
                                x=df['time'],
                                open=df['open'],
                                high=df['high'],
                                low=df['low'],
                                close=df['close'],
                                name=filename
                            )
                        )
                    elif chart_types[group_index] == "Line Chart":
                        fig.add_trace(
                            go.Scatter(
                                x=df['time'],
                                y=df['close'],
                                mode='lines',
                                name=filename
                            )
                        )
                fig.update_layout(
                    title=f"Group {group_index + 1} Chart",
                    xaxis_title="Time",
                    yaxis_title="Price",
                    xaxis_rangeslider_visible=False if chart_types[group_index] == "Candlestick" else True,
                    template="plotly_dark",
                )
                st.plotly_chart(fig)
