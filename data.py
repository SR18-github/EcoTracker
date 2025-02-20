import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def initialize_session_state():
    print("Initializing session state...")  # Debug log
    if 'waste_data' not in st.session_state:
        st.session_state.waste_data = pd.DataFrame(
            columns=['date', 'category', 'weight', 'recycled']
        )
    if 'goals' not in st.session_state:
        st.session_state.goals = {
            'weekly_recycling': 5.0,
            'waste_reduction': 2.0
        }
    print("Session state initialized successfully")  # Debug log

def add_waste_entry(category, weight, recycled):
    print(f"Adding waste entry: {category}, {weight}kg, recycled={recycled}")  # Debug log
    new_entry = pd.DataFrame({
        'date': [datetime.now()],
        'category': [category],
        'weight': [weight],
        'recycled': [recycled]
    })
    st.session_state.waste_data = pd.concat([st.session_state.waste_data, new_entry], ignore_index=True)
    print("Waste entry added successfully")  # Debug log

def get_weekly_stats():
    print("Calculating weekly stats...")  # Debug log
    if st.session_state.waste_data.empty:
        print("No data available")  # Debug log
        return 0, 0, 0

    week_ago = datetime.now() - timedelta(days=7)
    weekly_data = st.session_state.waste_data[
        st.session_state.waste_data['date'] >= week_ago
    ].copy()  # Use .copy() to avoid SettingWithCopyWarning

    total_waste = weekly_data['weight'].sum()
    recycled = weekly_data[weekly_data['recycled']]['weight'].sum()
    recycling_rate = (recycled / total_waste * 100) if total_waste > 0 else 0

    print(f"Weekly stats calculated: total={total_waste}, recycled={recycled}, rate={recycling_rate}%")  # Debug log
    return total_waste, recycled, recycling_rate

def get_impact_metrics():
    print("Calculating impact metrics...")  # Debug log
    if st.session_state.waste_data.empty:
        print("No data available for impact metrics")  # Debug log
        return 0, 0, 0

    total_recycled = st.session_state.waste_data[
        st.session_state.waste_data['recycled']
    ]['weight'].sum()

    # Approximate environmental impact calculations
    trees_saved = total_recycled * 0.17  # Each kg of recycled paper saves ~0.17 trees
    co2_reduced = total_recycled * 2.5    # Each kg of recycling reduces ~2.5 kg CO2
    water_saved = total_recycled * 3.8    # Each kg of recycling saves ~3.8L of water

    print(f"Impact metrics calculated: trees={trees_saved}, co2={co2_reduced}, water={water_saved}")  # Debug log
    return trees_saved, co2_reduced, water_saved