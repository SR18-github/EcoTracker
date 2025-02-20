import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def initialize_community_state():
    """Initialize community-related session state variables"""
    if 'shared_progress' not in st.session_state:
        st.session_state.shared_progress = pd.DataFrame(
            [], 
            columns=['user_id', 'date', 'total_waste', 'recycled_waste', 'recycling_rate']
        ).astype({
            'user_id': 'str',
            'date': 'datetime64[ns]',
            'total_waste': 'float64',
            'recycled_waste': 'float64',
            'recycling_rate': 'float64'
        })
    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"

def share_progress(total_waste, recycled_waste, recycling_rate):
    """Share user's progress to the community board"""
    try:
        new_entry = pd.DataFrame({
            'user_id': [st.session_state.user_id],
            'date': [datetime.now()],
            'total_waste': [float(total_waste)],
            'recycled_waste': [float(recycled_waste)],
            'recycling_rate': [float(recycling_rate)]
        })

        # Ensure the DataFrame has the correct data types
        new_entry = new_entry.astype({
            'user_id': 'str',
            'date': 'datetime64[ns]',
            'total_waste': 'float64',
            'recycled_waste': 'float64',
            'recycling_rate': 'float64'
        })

        if st.session_state.shared_progress.empty:
            st.session_state.shared_progress = new_entry
        else:
            st.session_state.shared_progress = pd.concat(
                [st.session_state.shared_progress, new_entry],
                ignore_index=True
            ).astype({
                'user_id': 'str',
                'date': 'datetime64[ns]',
                'total_waste': 'float64',
                'recycled_waste': 'float64',
                'recycling_rate': 'float64'
            })

        print(f"Progress shared successfully. DataFrame types: {st.session_state.shared_progress.dtypes}")
    except Exception as e:
        print(f"Error sharing progress: {str(e)}")
        st.error("Failed to share progress. Please try again.")

def get_community_stats():
    """Get community-wide statistics"""
    try:
        if st.session_state.shared_progress.empty:
            return {
                'avg_recycling_rate': 0.0,
                'top_recyclers': pd.DataFrame(),
                'community_rank': 0
            }

        # Calculate average recycling rate
        avg_rate = st.session_state.shared_progress['recycling_rate'].mean()

        # Get top recyclers (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_data = st.session_state.shared_progress[
            st.session_state.shared_progress['date'] >= week_ago
        ].copy()

        top_recyclers = pd.DataFrame()
        if not recent_data.empty:
            top_recyclers = recent_data.nlargest(5, 'recycling_rate')[
                ['user_id', 'recycling_rate']
            ]

        # Calculate user's rank
        community_rank = 0
        if st.session_state.user_id in recent_data['user_id'].values:
            user_rate = recent_data[
                recent_data['user_id'] == st.session_state.user_id
            ]['recycling_rate'].iloc[-1]
            community_rank = (
                recent_data['recycling_rate'] > user_rate
            ).sum() + 1

        print(f"Community stats calculated successfully. Avg rate: {avg_rate}, Rank: {community_rank}")
        return {
            'avg_recycling_rate': float(avg_rate),
            'top_recyclers': top_recyclers,
            'community_rank': int(community_rank)
        }
    except Exception as e:
        print(f"Error calculating community stats: {str(e)}")
        return {
            'avg_recycling_rate': 0.0,
            'top_recyclers': pd.DataFrame(),
            'community_rank': 0
        }