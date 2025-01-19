import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Check if session state contains dataframes
if 'dataframes' not in st.session_state or not st.session_state.dataframes:
    st.error("No data available. Please upload data in the Dataloader page first.")
else:
    st.title("Marketphase")
    st.header("Analyze US Treasury Yield Curves")

    # Select CSV files for US02Y and US10Y
    st.subheader("Select Files for Analysis")
    us02y_file = st.selectbox("Select US02Y CSV file:", options=st.session_state.dataframes.keys())
    us10y_file = st.selectbox("Select US10Y CSV file:", options=st.session_state.dataframes.keys())

    if us02y_file and us10y_file:
        # Load the selected data
        us02y_data = st.session_state.dataframes[us02y_file]
        us10y_data = st.session_state.dataframes[us10y_file]

        # Ensure 'time' is datetime
        us02y_data['time'] = pd.to_datetime(us02y_data['time'])
        us10y_data['time'] = pd.to_datetime(us10y_data['time'])

        # Filter data to use only overlapping timeframes
        merged_data = pd.merge(us02y_data, us10y_data, on='time', suffixes=('_us02y', '_us10y'))

        # User input for slope calculation window
        slope_window = st.slider("Select the number of points for slope calculation:", min_value=3, max_value=10, value=4)

        # Ensure we have enough data points
        if len(merged_data) < slope_window:
            st.error(f"Not enough overlapping data points to calculate slopes with a window size of {slope_window}.")
        else:
            # Function to calculate slope for a rolling window
            def calculate_slope(series, window):
                """
                Calculate rolling slope for the given series.
                """
                slopes = [None] * (window - 1)  # Fill the initial values with None
                for i in range(window - 1, len(series)):
                    slope = 0
                    for j in range(1, window):
                        slope += (series.iloc[i - (j - 1)] - series.iloc[i - j])
                    slopes.append(slope / (window - 1))
                return pd.Series(slopes)

            # Calculate rolling slopes for US02Y and US10Y
            merged_data['slope_us02y'] = calculate_slope(merged_data['close_us02y'], slope_window)
            merged_data['slope_us10y'] = calculate_slope(merged_data['close_us10y'], slope_window)

            # Determine market phase based on slopes
            def determine_market_phase(row):
                """
                Determine the market phase based on slopes.
                """
                if pd.isna(row['slope_us02y']) or pd.isna(row['slope_us10y']):
                    return None  # Skip rows where slope can't be calculated
                return "US02Y Dominates" if abs(row['slope_us02y']) > abs(row['slope_us10y']) else "US10Y Dominates"

            merged_data['market_phase'] = merged_data.apply(determine_market_phase, axis=1)

            # Display slopes and market phases
            st.write(merged_data[['time', 'slope_us02y', 'slope_us10y', 'market_phase']].dropna())

            # Map phases to colors
            phase_color_map = {"US02Y Dominates": "blue", "US10Y Dominates": "orange"}
            color_list = merged_data['market_phase'].map(phase_color_map).fillna("gray").tolist()

            # Visualize the curves and add a horizontal bar for market phases
            fig = go.Figure()

            # Add US02Y and US10Y curves
            fig.add_trace(go.Scatter(x=merged_data['time'], y=merged_data['close_us02y'],
                                     mode='lines', name='US02Y Yield'))
            fig.add_trace(go.Scatter(x=merged_data['time'], y=merged_data['close_us10y'],
                                     mode='lines', name='US10Y Yield'))

            # Add a horizontal bar for market phases
            fig.add_trace(go.Scatter(
                x=merged_data['time'],
                y=[max(merged_data['close_us02y'].max(), merged_data['close_us10y'].max())] * len(merged_data),
                mode='markers+lines',
                line=dict(width=0),  # No connecting line
                marker=dict(size=10, color=color_list),  # Use the color list for markers
                name='Market Phase'
            ))

            # Configure layout
            fig.update_layout(
                title="US Treasury Yields and Market Phases",
                xaxis_title="Time",
                yaxis_title="Yield",
                template="plotly_white",
                showlegend=True
            )

            # Display the plot
            st.plotly_chart(fig)
