import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from utils import (
    create_progress_chart, create_waste_composition_chart,
    create_trend_chart, ECO_TIPS, WASTE_CATEGORIES
)
from data import (
    initialize_session_state, add_waste_entry,
    get_weekly_stats, get_impact_metrics
)
from community import (
    initialize_community_state, share_progress,
    get_community_stats
)
import random
from carbon_calculator import calculate_carbon_footprint, get_reduction_recommendations

# Page configuration
st.set_page_config(
    page_title="EcoTracker - Waste Reduction & Recycling",
    page_icon="♻️",
    layout="wide"
)

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session states
initialize_session_state()
initialize_community_state()

# Header
st.markdown("<h1 class='main-header'>EcoTracker</h1>", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Waste Tracking Dashboard")

    # Input form
    with st.form("waste_entry"):
        category = st.selectbox("Waste Category", WASTE_CATEGORIES)
        weight = st.number_input("Weight (kg)", min_value=0.1, max_value=100.0, value=1.0)
        recycled = st.checkbox("Recycled")
        submitted = st.form_submit_button("Log Waste")

        if submitted:
            add_waste_entry(category, weight, recycled)
            st.success("Entry logged successfully!")

    # Weekly statistics
    total_waste, recycled_waste, recycling_rate = get_weekly_stats()

    st.subheader("📈 Weekly Progress")
    stats_col1, stats_col2, stats_col3 = st.columns(3)

    with stats_col1:
        st.metric("Total Waste", f"{total_waste:.1f} kg")
    with stats_col2:
        st.metric("Recycled", f"{recycled_waste:.1f} kg")
    with stats_col3:
        st.metric("Recycling Rate", f"{recycling_rate:.1f}%")

    # Progress chart
    progress_chart = create_progress_chart(recycled_waste, st.session_state.goals['weekly_recycling'])
    st.plotly_chart(progress_chart, use_container_width=True)

    # Waste composition
    st.subheader("🗑️ Waste Composition")
    composition_chart = create_waste_composition_chart(st.session_state.waste_data)
    if composition_chart:
        st.plotly_chart(composition_chart, use_container_width=True)

    # Community Section
    st.subheader("🌟 Community")
    # Share progress button
    if st.button("Share My Progress"):
        share_progress(total_waste, recycled_waste, recycling_rate)
        st.success("Progress shared with the community!")

    # Community stats
    community_stats = get_community_stats()
    comm_col1, comm_col2 = st.columns(2)

    with comm_col1:
        st.metric(
            "Community Average",
            f"{community_stats['avg_recycling_rate']:.1f}%",
            f"{recycling_rate - community_stats['avg_recycling_rate']:.1f}%"
        )
        if community_stats['community_rank'] > 0:
            st.info(f"Your rank in the community: #{community_stats['community_rank']}")

    with comm_col2:
        st.write("🏆 Top Recyclers This Week")
        if not community_stats['top_recyclers'].empty:
            for _, recycler in community_stats['top_recyclers'].iterrows():
                st.markdown(
                    f"**{recycler['user_id']}**: {recycler['recycling_rate']:.1f}%"
                )

with col2:
    st.subheader("🌍 Environmental Impact")

    # Calculate carbon footprint
    carbon_data = calculate_carbon_footprint(st.session_state.waste_data)

    # Display carbon metrics
    st.markdown("### 🏭 Carbon Footprint")
    carbon_col1, carbon_col2 = st.columns(2)

    with carbon_col1:
        st.metric(
            "Total CO₂ Impact",
            f"{carbon_data['total_footprint']:.1f} kg",
            f"-{carbon_data['savings_from_recycling']:.1f} kg"
        )

    with carbon_col2:
        st.metric(
            "Recycling Savings",
            f"{carbon_data['savings_from_recycling']:.1f} kg CO₂"
        )

    # Display category breakdown if data exists
    if not carbon_data['by_category'].empty:
        st.markdown("### 📊 Impact by Category")
        fig = px.bar(
            x=carbon_data['by_category'].index,
            y=carbon_data['by_category'].values,
            labels={'x': 'Category', 'y': 'CO₂ Impact (kg)'},
            color=carbon_data['by_category'].values,
            color_continuous_scale='Greens'
        )
        fig.update_layout(height=200)
        st.plotly_chart(fig, use_container_width=True)

    # Display recommendations
    st.markdown("### 💡 Reduction Tips")
    recommendations = get_reduction_recommendations(carbon_data)
    for rec in recommendations:
        st.markdown(f"- {rec}")

    trees, co2, water = get_impact_metrics()

    impact_col1, impact_col2, impact_col3 = st.columns(3)
    with impact_col1:
        st.markdown(f"### 🌳\n{trees:.1f}\ntrees saved")
    with impact_col2:
        st.markdown(f"### 🌡️\n{co2:.1f} kg\nCO₂ reduced")
    with impact_col3:
        st.markdown(f"### 💧\n{water:.1f} L\nwater saved")

    # Educational tip
    st.subheader("💡 Eco Tip of the Day")
    st.markdown(f"<div class='eco-tip'>{random.choice(ECO_TIPS)}</div>", unsafe_allow_html=True)

    # Achievement badges
    st.subheader("🏆 Achievements")
    if recycling_rate >= 50:
        st.markdown("<div class='achievement-badge'>50% Recycling Rate</div>", unsafe_allow_html=True)
    if trees >= 1:
        st.markdown("<div class='achievement-badge'>Tree Saver</div>", unsafe_allow_html=True)
    if water >= 100:
        st.markdown("<div class='achievement-badge'>Water Guardian</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        EcoTracker helps you monitor your waste reduction journey and environmental impact.
        Together, we can make a difference! 🌱
    </div>
    """,
    unsafe_allow_html=True
)