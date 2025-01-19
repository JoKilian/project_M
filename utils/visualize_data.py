import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

def load_csv_files(folder_path):
    """Load all CSV files from a given folder and its subdirectories."""
    csv_files = list(Path(folder_path).rglob("*.csv"))
    dataframes = {}
    for file in csv_files:
        try:
            # Load CSV into a DataFrame
            df = pd.read_csv(file)
            # Store DataFrame in dictionary with filename as the key
            dataframes[file.name] = df
        except Exception as e:
            st.error(f"Error loading {file.name}: {e}")
    return dataframes
