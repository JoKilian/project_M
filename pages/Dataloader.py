import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO
from utils import auth_functions

auth_functions.check_authentication()

# Dataloader page content
st.title("Dataloader")
st.header("Load and Visualize CSV Files")

# File uploader (allow multiple files)
uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

# Placeholder for data storage
if 'dataframes' not in st.session_state:
    st.session_state.dataframes = {}

# Load and store files if any are uploaded
if uploaded_files:
    # Load CSV files into session state
    st.session_state.dataframes = {}
    for uploaded_file in uploaded_files:
        # Read file content and load into DataFrame
        file_name = uploaded_file.name
        file_content = uploaded_file.getvalue().decode("utf-8")
        df = pd.read_csv(StringIO(file_content))
        st.session_state.dataframes[file_name] = df
    
    st.success(f"Loaded {len(uploaded_files)} files.")

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
