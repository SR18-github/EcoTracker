import pandas as pd
import streamlit as st

# Carbon footprint factors (kg CO2e per kg of waste)
CARBON_FACTORS = {
    'Paper': 0.9,
    'Plastic': 2.5,
    'Glass': 0.6,
    'Metal': 2.7,
    'Organic': 0.8,
    'Electronics': 20.0,
    'Other': 1.5
}

def calculate_carbon_footprint(waste_data):
    """Calculate carbon footprint from waste data"""
    if waste_data.empty:
        return {
            'total_footprint': 0.0,
            'by_category': pd.Series(dtype='float64'),
            'savings_from_recycling': 0.0
        }
    
    # Calculate footprint by category
    footprint_by_category = waste_data.apply(
        lambda row: row['weight'] * CARBON_FACTORS[row['category']] * (0.4 if row['recycled'] else 1.0),
        axis=1
    )
    
    # Calculate savings from recycling
    potential_footprint = waste_data['weight'].mul(waste_data['category'].map(CARBON_FACTORS)).sum()
    actual_footprint = footprint_by_category.sum()
    recycling_savings = potential_footprint - actual_footprint
    
    return {
        'total_footprint': actual_footprint,
        'by_category': waste_data.groupby('category')['weight'].sum().mul(pd.Series(CARBON_FACTORS)),
        'savings_from_recycling': recycling_savings
    }

def get_reduction_recommendations(carbon_data):
    """Generate personalized recommendations based on carbon footprint data"""
    recommendations = []
    
    if carbon_data['by_category'].empty:
        return [
            "Start tracking your waste to get personalized recommendations",
            "Consider recycling to reduce your carbon footprint",
            "Minimize single-use items in your daily routine"
        ]
    
    # Sort categories by impact
    high_impact_categories = carbon_data['by_category'].sort_values(ascending=False)
    
    for category, impact in high_impact_categories.items():
        if category == 'Plastic':
            recommendations.append("Reduce plastic usage by choosing reusable alternatives")
        elif category == 'Electronics':
            recommendations.append("Extend device lifespan through proper maintenance")
        elif category == 'Paper':
            recommendations.append("Switch to digital alternatives when possible")
        elif category == 'Organic':
            recommendations.append("Consider composting organic waste")
    
    return recommendations[:3]  # Return top 3 most relevant recommendations
