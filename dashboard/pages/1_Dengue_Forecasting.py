"""
Streamlit Page: Dengue Forecasting & Impact Analysis

This page shows historical data, future predictions, and the projected
impact of different intervention strategies on future dengue cases.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import sys
import json

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.config as config
from src.model_pipeline import load_model, make_predictions

st.set_page_config(page_title="Dengue Forecasting", page_icon="📈", layout="wide")

st.title("📈 Dengue Forecasting & Impact Analysis")
st.markdown("Explore historical patterns, future predictions, and intervention impacts.")

@st.cache_data
def load_data_and_model():
    """Loads the processed data and the trained model."""
    processed_data_path = config.PROCESSED_DATA_DIR / config.PROCESSED_DATA_FILE
    model_path = config.OUTPUT_DIR / config.MODEL_FILE
    metrics_path = config.OUTPUT_DIR / f"{Path(config.MODEL_FILE).stem}_metrics.json"

    # Check if files exist
    missing_files = []
    if not processed_data_path.exists():
        missing_files.append(f"Processed data: {processed_data_path}")
    if not model_path.exists():
        missing_files.append(f"Model file: {model_path}")
    
    if missing_files:
        st.error("Required files not found:")
        for file in missing_files:
            st.error(f"  • {file}")
        return None, None, None

    # Load data and model
    df = pd.read_csv(processed_data_path, parse_dates=[config.DATE_COLUMN])
    model = load_model(model_path)
    
    # Load metrics if available
    metrics = None
    if metrics_path.exists():
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
    
    return df, model, metrics

# Load data
df, model, metrics = load_data_and_model()

if df is not None and model is not None:
    
    # Create tabs for different analyses
    tab1, tab2 = st.tabs(["📊 Historical Data & Forecasting", "🎯 Intervention Impact Projections"])
    
    with tab1:
        # Sidebar controls
        st.sidebar.header("Forecast Settings")
        forecast_periods = st.sidebar.slider("Forecast Horizon (weeks)", 
                                            min_value=4, max_value=52, 
                                            value=config.FORECAST_HORIZON)
        
        show_components = st.sidebar.checkbox("Show Forecast Components", value=True)
        show_metrics = st.sidebar.checkbox("Show Model Performance", value=True)
        
        # Make predictions
        forecast = make_predictions(model, forecast_periods)
        
        # Data overview
        st.subheader("📊 Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        with col2:
            st.metric("Date Range", f"{df[config.DATE_COLUMN].dt.year.min()}-{df[config.DATE_COLUMN].dt.year.max()}")
        with col3:
            st.metric("Avg Weekly Cases", f"{df[config.TARGET_VARIABLE].mean():.1f}")
        with col4:
            st.metric("2020 Total Cases", f"{df[df[config.DATE_COLUMN].dt.year == 2020][config.TARGET_VARIABLE].sum():,.0f}")
        
        # Main forecast plot
        st.subheader("🔮 Dengue Cases Forecast")
        
        # Create interactive plot
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=df[config.DATE_COLUMN],
            y=df[config.TARGET_VARIABLE],
            mode='lines',
            name='Historical Cases',
            line=dict(color='blue', width=2)
        ))
        
        # Future predictions
        future_data = forecast.tail(forecast_periods)
        fig.add_trace(go.Scatter(
            x=future_data['ds'],
            y=future_data['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='red', dash='dash', width=2)
        ))
        
        # Confidence intervals
        fig.add_trace(go.Scatter(
            x=future_data['ds'],
            y=future_data['yhat_upper'],
            mode='lines',
            name='Upper Bound',
            line=dict(color='lightcoral', width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=future_data['ds'],
            y=future_data['yhat_lower'],
            mode='lines',
            name='Lower Bound',
            line=dict(color='lightcoral', width=0),
            fill='tonexty',
            fillcolor='rgba(255, 182, 193, 0.2)',
            showlegend=False
        ))
        
        fig.update_layout(
            title="Historical Dengue Cases and Future Forecast",
            xaxis_title="Date",
            yaxis_title="Weekly Cases",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast summary
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Recent data table
            st.subheader("📋 Recent Data & Predictions")
    
            # Show recent historical (always 4)
            recent_historical = df.tail(4)[[config.DATE_COLUMN, config.TARGET_VARIABLE]].copy()
            recent_historical['Type'] = 'Historical'
            recent_historical.columns = ['Date', 'Cases', 'Type']
            
            # Show ALL future predictions - FULLY RESPONSIVE
            future_predictions = future_data[['ds', 'yhat']].copy()  # Remove .head(4)!
            future_predictions['Type'] = 'Predicted'
            future_predictions.columns = ['Date', 'Cases', 'Type']
            
            combined_data = pd.concat([recent_historical, future_predictions])
            combined_data['Cases'] = combined_data['Cases'].round(0)
            combined_data['Date'] = combined_data['Date'].dt.strftime('%Y-%m-%d')
            
            st.info(f"📊 Showing {len(recent_historical)} historical + {len(future_predictions)} forecasted weeks")
            
            # Use height parameter to make table scrollable for long forecasts
            st.dataframe(combined_data, use_container_width=True, height=400)
        
        with col2:
            # Summary statistics
            st.subheader("🎯 Forecast Summary")
            avg_prediction = future_data['yhat'].mean()
            max_prediction = future_data['yhat'].max()
            min_prediction = future_data['yhat'].min()
            
            st.metric("Avg Predicted Cases", f"{avg_prediction:.0f}")
            st.metric("Peak Prediction", f"{max_prediction:.0f}")
            st.metric("Lowest Prediction", f"{min_prediction:.0f}")
            
            # Trend analysis
            recent_trend = forecast['trend'].tail(4).mean() - forecast['trend'].tail(8).head(4).mean()
            trend_direction = "📈 Increasing" if recent_trend > 0 else "📉 Decreasing"
            st.metric("Trend Direction", trend_direction)
        
        # Model performance
        if show_metrics and metrics:
            st.subheader("📊 Model Performance")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Training MAPE", f"{metrics.get('mape', 0):.1f}%")
            with col2:
                st.metric("Holdout MAPE", f"{metrics.get('holdout_mape', 0):.1f}%")
            with col3:
                st.metric("Training MAE", f"{metrics.get('mae', 0):.1f}")
            with col4:
                st.metric("Training RMSE", f"{metrics.get('rmse', 0):.1f}")
            
            # Performance interpretation
            holdout_mape = metrics.get('holdout_mape', 0)
            if holdout_mape < 10:
                performance_level = "🟢 Excellent"
            elif holdout_mape < 20:
                performance_level = "🟡 Good"
            elif holdout_mape < 30:
                performance_level = "🟠 Fair"
            else:
                performance_level = "🔴 Poor"
            
            st.info(f"**Model Performance Rating:** {performance_level} (Holdout MAPE: {holdout_mape:.1f}%)")
        
        # Forecast components
        if show_components:
            st.subheader("📈 Forecast Components")
            fig2 = model.plot_components(forecast)
            st.pyplot(fig2)
    
    with tab2:
        st.header("🎯 Intervention Impact on Future Cases")
        st.markdown("See how different interventions would affect the forecasted dengue cases.")
        
        # Intervention controls
        col1, col2 = st.columns(2)
        
        with col1:
            intervention_type = st.selectbox(
                "Select Intervention",
                ["None", "Wolbachia", "Dengvaxia", "Combined Strategy"]
            )
        
        with col2:
            implementation_week = st.slider(
                "Implementation Start (weeks from now)",
                min_value=1, max_value=min(26, forecast_periods-4),
                value=4
            )
        
        # Efficacy controls
        if intervention_type in ["Wolbachia", "Combined Strategy"]:
            wolbachia_efficacy = st.slider(
                "Wolbachia Efficacy (%)",
                min_value=50, max_value=90,
                value=int(config.WOLBACHIA_EFFICACY * 100)
            ) / 100
        else:
            wolbachia_efficacy = 0
        
        if intervention_type in ["Dengvaxia", "Combined Strategy"]:
            dengvaxia_efficacy = st.slider(
                "Dengvaxia Efficacy (%)",
                min_value=60, max_value=95,
                value=int(config.DENGVAXIA_EFFICACY * 100)
            ) / 100
        else:
            dengvaxia_efficacy = 0
        
        # Calculate intervention impact
        baseline_forecast = forecast.copy()
        intervention_forecast = forecast.copy()
        
        # Apply intervention effect after implementation week
        if intervention_type != "None":
            intervention_start_idx = len(df) + implementation_week
            
            if intervention_type == "Wolbachia":
                efficacy = wolbachia_efficacy
            elif intervention_type == "Dengvaxia":
                efficacy = dengvaxia_efficacy
            elif intervention_type == "Combined Strategy":
                efficacy = 1 - ((1 - wolbachia_efficacy) * (1 - dengvaxia_efficacy))
            
            # Apply gradual implementation (ramp up over 4 weeks)
            for i in range(intervention_start_idx, len(intervention_forecast)):
                weeks_since_start = i - intervention_start_idx
                if weeks_since_start < 4:
                    # Gradual ramp-up
                    gradual_efficacy = efficacy * (weeks_since_start + 1) / 4
                else:
                    # Full efficacy
                    gradual_efficacy = efficacy
                
                intervention_forecast.loc[i, 'yhat'] *= (1 - gradual_efficacy)
                intervention_forecast.loc[i, 'yhat_lower'] *= (1 - gradual_efficacy)
                intervention_forecast.loc[i, 'yhat_upper'] *= (1 - gradual_efficacy)
        
        # Plot comparison
        st.subheader(f"📊 Impact of {intervention_type} Intervention")

        fig_intervention = go.Figure()

        # Historical data
        fig_intervention.add_trace(go.Scatter(
            x=df[config.DATE_COLUMN],
            y=df[config.TARGET_VARIABLE],
            mode='lines',
            name='Historical Cases',
            line=dict(color='blue', width=2)
        ))

        # Baseline forecast
        future_baseline = baseline_forecast.tail(forecast_periods)
        fig_intervention.add_trace(go.Scatter(
            x=future_baseline['ds'],
            y=future_baseline['yhat'],
            mode='lines',
            name='Baseline Forecast',
            line=dict(color='red', dash='dash', width=2)
        ))

        # Intervention forecast
        if intervention_type != "None":
            future_intervention = intervention_forecast.tail(forecast_periods)
            fig_intervention.add_trace(go.Scatter(
                x=future_intervention['ds'],
                y=future_intervention['yhat'],
                mode='lines',
                name=f'With {intervention_type}',
                line=dict(color='green', width=2)
            ))
            
            # Add intervention start line - FIXED
            intervention_start_date = future_baseline['ds'].iloc[implementation_week-1]
            
            fig_intervention.add_shape(
                type="line",
                x0=intervention_start_date, x1=intervention_start_date,
                y0=0, y1=1,
                yref="paper",
                line=dict(color="orange", width=2, dash="dot"),
            )
            
            fig_intervention.add_annotation(
                x=intervention_start_date,
                y=0.9,
                yref="paper",
                text=f"{intervention_type} Implementation",
                showarrow=True,
                arrowhead=2,
                arrowcolor="orange"
            )

        fig_intervention.update_layout(
            title=f"Dengue Cases: Baseline vs {intervention_type} Intervention",
            xaxis_title="Date",
            yaxis_title="Weekly Cases",
            hovermode='x unified',
            height=500
        )

        st.plotly_chart(fig_intervention, use_container_width=True)
        
        # Impact summary
        if intervention_type != "None":
            total_baseline = future_baseline['yhat'].sum()
            total_intervention = future_intervention['yhat'].sum()
            cases_prevented = total_baseline - total_intervention
            percent_reduction = (cases_prevented / total_baseline) * 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Baseline Total Cases", f"{total_baseline:.0f}")
            with col2:
                st.metric("With Intervention", f"{total_intervention:.0f}")
            with col3:
                st.metric("Cases Prevented", f"{cases_prevented:.0f}", f"{percent_reduction:.1f}% reduction")
            
            # Intervention details
            if intervention_type == "Combined Strategy":
                st.info(f"🔗 **Combined Efficacy**: {efficacy:.1%} "
                        f"(Wolbachia: {wolbachia_efficacy:.1%} + Dengvaxia: {dengvaxia_efficacy:.1%})")
            
            st.success(f"🎯 **{intervention_type}** could prevent **{cases_prevented:.0f} cases** "
                      f"({percent_reduction:.1f}% reduction) over the next {forecast_periods} weeks.")

else:
    st.warning("Please run the data preprocessing and model training pipelines before using this page.")
    st.code("""
    python scripts/run_preprocessing.py
    python scripts/run_training.py
    """)