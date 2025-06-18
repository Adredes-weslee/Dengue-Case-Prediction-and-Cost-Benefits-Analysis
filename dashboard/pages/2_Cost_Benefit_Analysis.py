"""
Streamlit Page: Cost-Benefit Analysis

Comprehensive cost-benefit analysis including historical 2020 analysis
and dynamic scenario modeling for intervention strategies.
"""
import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.config as config

st.set_page_config(page_title="Cost-Benefit Analysis", page_icon="💰", layout="wide")

st.title("💰 Cost-Benefit Analysis & Scenario Modeling")
st.markdown("Comprehensive economic analysis of dengue intervention strategies")

@st.cache_data
def load_analysis_results():
    """Loads the cost-benefit analysis results from the JSON file."""
    analysis_path = config.OUTPUT_DIR / config.COST_BENEFIT_FILE
    if not analysis_path.exists():
        return None
    with open(analysis_path, 'r') as f:
        results = json.load(f)
    return results

# Create tabs for different analyses
tab1, tab2 = st.tabs(["📊 2020 Outbreak Analysis", "🔮 Dynamic Scenario Modeling"])

with tab1:
    st.header("📊 2020 Singapore Outbreak Analysis")
    st.markdown("*Analysis based on the actual 35,068 dengue cases recorded in 2020*")
    
    results = load_analysis_results()
    
    if results:
        # Key findings header
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Cases (2020)", f"{results['analysis_metadata']['total_cases_analyzed']:,}")
        with col2:
            st.metric("Population", f"{results['analysis_metadata']['population']:,}")
        with col3:
            cost_ratio = results['dengvaxia']['cost_per_daly_averted_usd'] / results['wolbachia']['cost_per_daly_averted_usd']
            st.metric("Wolbachia Advantage", f"{cost_ratio:.0f}x more cost-effective")
        
        # Side-by-side comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🦟 Wolbachia Deployment")
            wolbachia = results['wolbachia']
            st.metric("Total Program Cost", f"${wolbachia['total_cost_usd']:,.0f}")
            st.metric("Cases Averted", f"{wolbachia['cases_averted']:,.0f}")
            st.metric("DALYs Averted", f"{wolbachia['dalys_averted']:,.1f}")
            st.metric("Cost per DALY", f"${wolbachia['cost_per_daly_averted_usd']:,.0f}")
            
            # Cost-effectiveness status
            cost_per_daly = wolbachia['cost_per_daly_averted_usd']
            if cost_per_daly < 30364:
                status = "🟢 Highly Cost-Effective"
                color = "success"
            elif cost_per_daly < 82703:
                status = "🟡 Cost-Effective"
                color = "info"
            elif cost_per_daly < 166255:
                status = "🟠 Marginally Effective"
                color = "warning"
            else:
                status = "🔴 Not Cost-Effective"
                color = "error"
            
            if color == "success":
                st.success(f"**Status**: {status}")
            elif color == "info":
                st.info(f"**Status**: {status}")
            elif color == "warning":
                st.warning(f"**Status**: {status}")
            else:
                st.error(f"**Status**: {status}")

        with col2:
            st.subheader("💉 Dengvaxia Vaccination")
            dengvaxia = results['dengvaxia']
            st.metric("Total Program Cost", f"${dengvaxia['total_cost_usd']:,.0f}")
            st.metric("Cases Averted", f"{dengvaxia['cases_averted']:,.0f}")
            st.metric("DALYs Averted", f"{dengvaxia['dalys_averted']:,.1f}")
            st.metric("Cost per DALY", f"${dengvaxia['cost_per_daly_averted_usd']:,.0f}")
            
            # Cost-effectiveness status
            cost_per_daly = dengvaxia['cost_per_daly_averted_usd']
            if cost_per_daly < 30364:
                status = "🟢 Highly Cost-Effective"
                color = "success"
            elif cost_per_daly < 82703:
                status = "🟡 Cost-Effective"
                color = "info"
            elif cost_per_daly < 166255:
                status = "🟠 Marginally Effective"
                color = "warning"
            else:
                status = "🔴 Not Cost-Effective"
                color = "error"
            
            if color == "success":
                st.success(f"**Status**: {status}")
            elif color == "info":
                st.info(f"**Status**: {status}")
            elif color == "warning":
                st.warning(f"**Status**: {status}")
            else:
                st.error(f"**Status**: {status}")
        
        # Conclusion
        st.subheader("🏆 Analysis Conclusion")
        if results['analysis_summary']['most_cost_effective_intervention'] == 'Wolbachia':
            st.success("**2020 Outbreak Analysis**: Wolbachia deployment is significantly more cost-effective than Dengvaxia vaccination for Singapore.")
        
        # Comparison visualization
        st.subheader("📊 Cost-Effectiveness Comparison")
        
        # Create comparison chart
        fig = go.Figure()
        
        # Add bars
        interventions = ['Wolbachia', 'Dengvaxia']
        costs = [wolbachia['cost_per_daly_averted_usd'], dengvaxia['cost_per_daly_averted_usd']]
        colors = ['green', 'red']
        
        fig.add_trace(go.Bar(
            x=interventions,
            y=costs,
            marker_color=colors,
            text=[f"${cost:,.0f}" for cost in costs],
            textposition='auto'
        ))
        
        # Add threshold lines
        fig.add_hline(y=30364, line_dash="dash", line_color="green", 
                     annotation_text="Singapore Conservative ($30,364)")
        fig.add_hline(y=82703, line_dash="dash", line_color="orange", 
                     annotation_text="WHO Very High HDI ($82,703)")
        fig.add_hline(y=166255, line_dash="dash", line_color="red", 
                     annotation_text="Not Cost-Effective ($166,255)")
        
        fig.update_layout(
            title="Cost per DALY Averted - 2020 Analysis",
            yaxis_title="Cost per DALY (USD)",
            yaxis_type="log",  # Log scale due to large difference
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary table
        st.subheader("📋 Summary Comparison")
        summary_df = pd.DataFrame({
            "Intervention": ["Wolbachia", "Dengvaxia"],
            "Total Cost (USD)": [f"${wolbachia['total_cost_usd']:,.0f}", f"${dengvaxia['total_cost_usd']:,.0f}"],
            "Cases Averted": [f"{wolbachia['cases_averted']:,.0f}", f"{dengvaxia['cases_averted']:,.0f}"],
            "Cost per DALY (USD)": [f"${wolbachia['cost_per_daly_averted_usd']:,.0f}", f"${dengvaxia['cost_per_daly_averted_usd']:,.0f}"],
            "Cost-Effectiveness": ["✅ Highly Effective", "❌ Not Effective"]
        })
        st.table(summary_df)
    
    else:
        st.error("Analysis results not found. Please run the cost-benefit analysis first.")
        st.code("python scripts/run_analysis.py")

with tab2:
    st.header("🔮 Dynamic Scenario Modeling")
    st.markdown("*Explore different intervention parameters and time horizons*")
    
    # Scenario controls
    col1, col2 = st.columns(2)
    
    with col1:
        intervention = st.selectbox(
            "Select Intervention Strategy",
            ["No Intervention", "Wolbachia", "Dengvaxia", "Combined Strategy"]
        )
    
    with col2:
        years = st.slider("Analysis Period (years)", min_value=1, max_value=10, value=5)
    
    # Efficacy controls
    if intervention in ["Wolbachia", "Combined Strategy"]:
        wolbachia_efficacy = st.slider(
            "Wolbachia Efficacy (%)", 
            min_value=50, max_value=90, 
            value=int(config.WOLBACHIA_EFFICACY * 100)
        ) / 100
    else:
        wolbachia_efficacy = 0
    
    if intervention in ["Dengvaxia", "Combined Strategy"]:
        dengvaxia_efficacy = st.slider(
            "Dengvaxia Efficacy (%)", 
            min_value=60, max_value=95, 
            value=int(config.DENGVAXIA_EFFICACY * 100)
        ) / 100
    else:
        dengvaxia_efficacy = 0
    
    # Additional parameters
    col1, col2 = st.columns(2)
    with col1:
        baseline_cases = st.number_input(
            "Annual Baseline Cases", 
            min_value=1000, max_value=50000, 
            value=35068, step=1000
        )
    with col2:
        population = st.number_input(
            "Population", 
            min_value=1000000, max_value=10000000, 
            value=config.POPULATION_2020, step=100000
        )
    
    # Calculate scenario function
    def calculate_scenario(intervention_type, years, baseline_cases, population):
        """Calculate costs and benefits for different scenarios."""
        if intervention_type == "No Intervention":
            return {
                "total_cost": 0,
                "cases_averted": 0,
                "dalys_averted": 0,
                "cost_per_daly": float('inf')
            }
        
        elif intervention_type == "Wolbachia":
            cases_averted_per_year = baseline_cases * wolbachia_efficacy
            total_cases_averted = cases_averted_per_year * years
            total_cost = config.WOLBACHIA_COST_PER_PERSON * population * years
            dalys_averted = total_cases_averted * config.DALY_PER_CASE
            
            return {
                "total_cost": total_cost,
                "cases_averted": total_cases_averted,
                "dalys_averted": dalys_averted,
                "cost_per_daly": total_cost / dalys_averted if dalys_averted > 0 else float('inf')
            }
        
        elif intervention_type == "Dengvaxia":
            cases_averted_per_year = baseline_cases * dengvaxia_efficacy
            total_cases_averted = cases_averted_per_year * years
            total_cost = config.DENGVAXIA_COST_PER_PERSON * population
            dalys_averted = total_cases_averted * config.DALY_PER_CASE
            
            return {
                "total_cost": total_cost,
                "cases_averted": total_cases_averted,
                "dalys_averted": dalys_averted,
                "cost_per_daly": total_cost / dalys_averted if dalys_averted > 0 else float('inf')
            }
        
        elif intervention_type == "Combined Strategy":
            combined_efficacy = 1 - ((1 - wolbachia_efficacy) * (1 - dengvaxia_efficacy))
            
            cases_averted_per_year = baseline_cases * combined_efficacy
            total_cases_averted = cases_averted_per_year * years
            
            wolbachia_cost = config.WOLBACHIA_COST_PER_PERSON * population * years
            dengvaxia_cost = config.DENGVAXIA_COST_PER_PERSON * population
            total_cost = wolbachia_cost + dengvaxia_cost
            
            dalys_averted = total_cases_averted * config.DALY_PER_CASE
            
            return {
                "total_cost": total_cost,
                "cases_averted": total_cases_averted,
                "dalys_averted": dalys_averted,
                "cost_per_daly": total_cost / dalys_averted if dalys_averted > 0 else float('inf'),
                "combined_efficacy": combined_efficacy
            }
        
        return {
            "total_cost": 0,
            "cases_averted": 0,
            "dalys_averted": 0,
            "cost_per_daly": float('inf')
        }
    
    # Calculate results
    scenario_results = calculate_scenario(intervention, years, baseline_cases, population)
    
    # Display results
    st.subheader("📊 Scenario Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cost", f"${scenario_results['total_cost']:,.0f}")
    with col2:
        st.metric("Cases Averted", f"{scenario_results['cases_averted']:,.0f}")
    with col3:
        st.metric("DALYs Averted", f"{scenario_results['dalys_averted']:,.1f}")
    with col4:
        cost_per_daly = scenario_results['cost_per_daly']
        if cost_per_daly == float('inf'):
            st.metric("Cost per DALY", "N/A")
        else:
            st.metric("Cost per DALY", f"${cost_per_daly:,.0f}")
    
    # Combined strategy info
    if intervention == "Combined Strategy" and 'combined_efficacy' in scenario_results:
        st.info(f"🔗 **Combined Efficacy**: {scenario_results['combined_efficacy']:.1%} "
                f"(Wolbachia: {wolbachia_efficacy:.1%} + Dengvaxia: {dengvaxia_efficacy:.1%})")
    
    # Multi-year projection
    if intervention != "No Intervention":
        st.subheader("📈 Multi-Year Impact Projection")
        
        years_range = list(range(1, years + 1))
        cumulative_cases_averted = [scenario_results['cases_averted'] * y / years for y in years_range]
        cumulative_costs = [scenario_results['total_cost'] * y / years for y in years_range]
        
        fig_projection = go.Figure()
        
        fig_projection.add_trace(go.Scatter(
            x=years_range,
            y=cumulative_cases_averted,
            mode='lines+markers',
            name='Cumulative Cases Averted',
            yaxis='y',
            line=dict(color='blue')
        ))
        
        fig_projection.add_trace(go.Scatter(
            x=years_range,
            y=[cost / 1000000 for cost in cumulative_costs],
            mode='lines+markers',
            name='Cumulative Cost (Million USD)',
            yaxis='y2',
            line=dict(color='red')
        ))
        
        fig_projection.update_layout(
            title=f'{intervention} Strategy: Multi-Year Impact',
            xaxis_title='Years',
            yaxis=dict(title='Cases Averted', side='left'),
            yaxis2=dict(title='Cost (Million USD)', side='right', overlaying='y'),
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_projection, use_container_width=True)
    
    # Cost-effectiveness analysis
    st.subheader("🎯 Cost-Effectiveness Assessment")
    
    if scenario_results['cost_per_daly'] != float('inf'):
        thresholds = {
            "Singapore Conservative": 30364,
            "WHO (Very High HDI)": 82703,
            "Singapore Research Target": 60039,
            "Not Cost-Effective": 166255
        }
        
        cost_per_daly = scenario_results['cost_per_daly']
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            for threshold_name, threshold_value in thresholds.items():
                if cost_per_daly <= threshold_value:
                    status = "✅ Cost-Effective"
                    color = "green"
                else:
                    status = "❌ Not Cost-Effective"
                    color = "red"
                
                st.markdown(f"**{threshold_name}** (${threshold_value:,}/DALY): :{color}[{status}]")
        
        with col2:
            # Overall recommendation
            if cost_per_daly < 30364:
                recommendation = "🟢 **Highly Recommended** - Excellent cost-effectiveness"
                st.success(recommendation)
            elif cost_per_daly < 82703:
                recommendation = "🟡 **Recommended** - Good cost-effectiveness"
                st.info(recommendation)
            elif cost_per_daly < 166255:
                recommendation = "🟠 **Consider** - Marginal cost-effectiveness"
                st.warning(recommendation)
            else:
                recommendation = "🔴 **Not Recommended** - Poor cost-effectiveness"
                st.error(recommendation)
    
    else:
        st.info("💡 Select an intervention strategy to see cost-effectiveness analysis.")