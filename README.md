# 🦟 Dengue Case Prediction and Cost-Benefits Analysis Platform

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Prophet](https://img.shields.io/badge/Prophet-095cec.svg)](https://facebook.github.io/prophet/)
[![scikit-time](https://img.shields.io/badge/scikit--time-orange.svg)](https://www.sktime.net/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A production-ready epidemiological forecasting platform that predicts dengue fever outbreaks up to 16 weeks in advance and provides evidence-based cost-benefit analysis of public health interventions for Singapore's National Environment Agency (NEA).

---

## 🎯 Project Overview

This project transforms comprehensive epidemiological research into an operational decision-support platform for public health officials. Built on rigorous time-series analysis of 11 years of Singapore dengue data (2012-2022), the platform addresses critical questions facing health authorities during dengue management.

### 🔬 **Primary Research Objectives**

**1. Predictive Modeling**: Build a time-series model capable of accurately forecasting weekly dengue cases 16 weeks into the future to enable proactive vector control deployment.

**2. Economic Analysis**: Compare the cost-effectiveness of two major intervention strategies:
- **Project Wolbachia**: Island-wide deployment of Wolbachia-infected Aedes mosquitoes
- **Population Vaccination**: Mass immunization program using Dengvaxia®

### 📊 **Key Findings & Impact**

- **🎯 Model Performance**: Prophet model achieves **9.5% MAPE** on 16-week forecasts
- **💰 Cost-Effectiveness**: Wolbachia deployment shows **$60,039 per DALY** vs **$360,876 per DALY** for vaccination
- **📈 Economic Impact**: Analysis of **$1.01-2.27 billion** dengue costs (2010-2020)
- **🚨 Outbreak Prediction**: Successfully models Singapore's record 2020 outbreak (35,068 cases)

---

## 🏗️ System Architecture

### 📊 **Data Pipeline Workflow**

````mermaid
graph TD
    A[Raw Data Sources] --> B[Data Processing]
    B --> C[Feature Engineering]
    C --> D[Model Training]
    D --> E[Predictions]
    E --> F[Cost-Benefit Analysis]
    F --> G[Interactive Dashboard]
    
    A1[Disease Surveillance] --> A
    A2[Weather Data] --> A
    A3[Google Trends] --> A
    A4[Population Statistics] --> A
````

### 🗂️ **Project Structure**

````
Dengue-Case-Prediction-and-Cost-Benefits-Analysis/
│
├── 📂 data/
│   ├── raw/                              # Original datasets
│   │   ├── WeeklyInfectiousDiseaseBulletinCases.csv  # MOH disease surveillance
│   │   ├── Singapore_weather.csv                     # Daily weather (11+ years)
│   │   ├── google_dengue_fever.csv                   # Search trend data
│   │   └── M810001.csv                               # Population statistics
│   ├── processed/                        # Cleaned & merged data
│   │   └── dengue_master_timeseries.csv              # Analysis-ready dataset
│   └── output/                           # Model artifacts & results
│       ├── prophet_model.pkl                         # Trained forecasting model
│       ├── predictions.csv                           # 16-week forecasts
│       ├── forecasting_model_metrics.json            # Model performance
│       └── cost_benefit_analysis.json                # Economic analysis
│
├── 📂 notebooks/
│   └── project_4_cleaning_eda_modeling.ipynb         # Original research notebook
│
├── 📂 src/                               # Core application logic
│   ├── __init__.py
│   ├── config.py                         # Configuration & parameters
│   ├── data_processing.py                # ETL pipeline functions
│   ├── model_pipeline.py                 # ML training & prediction
│   └── cost_benefit_analysis.py          # Economic modeling functions
│
├── 📂 scripts/                           # Execution scripts
│   ├── run_preprocessing.py              # Data preparation pipeline
│   ├── run_training.py                   # Model training workflow
│   ├── run_analysis.py                   # Complete analysis pipeline
│   ├── run_dashboard.py                  # Dashboard launcher
│   └── forecasting.py                    # Prediction generation
│
├── 📂 dashboard/                         # Streamlit web application
│   ├── app.py                           # Main dashboard application
│   └── pages/
│       ├── 1_Dengue_Forecasting.py      # Forecasting interface
│       └── 2_Cost_Benefit_Analysis.py   # Economic analysis interface
│
├── 📄 requirements.txt                   # Python dependencies
├── 📄 environment.yaml                   # Conda environment
└── 📄 README.md                         # Project documentation
````

---

## ⚡ Quick Start Guide

### 🛠️ **Installation & Setup**

**Option 1: pip (Recommended)**
````bash
# Clone repository
git clone https://github.com/yourusername/Dengue-Case-Prediction-and-Cost-Benefits-Analysis.git
cd Dengue-Case-Prediction-and-Cost-Benefits-Analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
````

**Option 2: Conda**
````bash
# Create environment from file
conda env create -f environment.yaml
conda activate dengue-forecasting
````

### 🚀 **Running the Platform**

**Complete Pipeline (Recommended for first run):**
````bash
# Process raw data → train model → generate analysis
python scripts/run_analysis.py
````

**Individual Components:**
````bash
# 1. Data preprocessing only
python scripts/run_preprocessing.py

# 2. Model training only  
python scripts/run_training.py

# 3. Generate new forecasts
python scripts/forecasting.py
````

**Launch Interactive Dashboard:**
````bash
# Start Streamlit application
python scripts/run_dashboard.py
# OR
streamlit run dashboard/app.py
````

🌐 **Access Dashboard**: Open `http://localhost:8501` in your browser

---

## 📈 **Model Performance & Validation**

### 🎯 **Forecasting Accuracy**
- **Prophet Model**: 9.5% MAPE on 16-week holdout test
- **Baseline Comparison**: Outperforms ARIMA, SARIMA, TBATS, Holt-Winters
- **Validation Period**: 2022 data (including dengue resurgence)

### 📊 **Model Features**
- **Temporal Features**: 574 weeks of historical data (2012-2022)
- **Weather Integration**: Temperature, humidity, precipitation patterns  
- **Behavioral Signals**: Google search trends for "dengue fever"
- **Demographic Controls**: Population dynamics and density

### 🔍 **Key Model Insights**
- **Seasonality**: Peak dengue season June-October
- **Trend Analysis**: Multi-year outbreak cycles (2013-2016, 2020, 2022)
- **Weather Impact**: Optimal mosquito conditions at 27.5°C
- **Outbreak Drivers**: Serotype switching and immunity gaps

---

## 💰 **Cost-Benefit Analysis Framework**

### 📋 **Economic Methodology**
- **Disability-Adjusted Life Years (DALYs)**: WHO standard health metric
- **Cost Perspective**: Societal (healthcare + productivity losses)
- **Time Horizon**: 10-year intervention lifecycle
- **Currency**: 2020 USD (inflation-adjusted)

### 🧮 **Intervention Comparison**

| **Metric** | **Wolbachia Deployment** | **Dengvaxia® Vaccination** |
|------------|--------------------------|----------------------------|
| **Efficacy** | 77% case reduction | 82% case reduction |
| **Annual Cost** | $27.0M USD | $220.7M USD |
| **Cost per DALY** | **$60,039** | **$360,876** |
| **Target Population** | Vector suppression | Ages 12-45 (seropositive) |
| **Implementation** | Ongoing releases | 3-dose schedule |

### 🎯 **Policy Recommendations**
✅ **Wolbachia deployment** is **6x more cost-effective** than vaccination  
✅ Meets Singapore's cost-effectiveness threshold ($82,703/DALY for high-HDI countries)  
✅ Provides population-wide protection without individual screening requirements

---

## 🔬 **Scientific Foundation**

### 📚 **Data Sources**
- **Disease Surveillance**: Singapore Ministry of Health weekly bulletins
- **Meteorological Data**: Visual Crossing weather API (4,249 daily records)
- **Search Behavior**: Google Trends "dengue fever" queries
- **Demographics**: Singapore Department of Statistics

### 🧪 **Research Validation**
- **Literature Review**: 12 comprehensive sections on dengue epidemiology
- **Historical Analysis**: 2004-2007, 2013-2016, 2020 outbreak patterns
- **International Benchmarking**: Vietnam, Jakarta cost-effectiveness studies
- **Policy Context**: Singapore's National Environment Agency guidelines

### 📊 **Statistical Rigor**
- **Stationarity Testing**: ADF, KPSS tests for time series properties
- **Model Selection**: Systematic comparison of 7 forecasting algorithms
- **Cross-Validation**: Walk-forward validation on temporal splits
- **Uncertainty Quantification**: Prediction intervals and confidence bounds

---

## 👥 **Stakeholders & Impact**

### 🏛️ **Primary Users**
- **Singapore NEA**: Vector control strategy and resource allocation
- **Ministry of Health**: Surveillance and outbreak preparedness
- **Public Health Researchers**: Epidemiological modeling and intervention analysis

### 🌍 **Broader Applications**  
- **Regional Health Authorities**: Adaptable to other tropical/subtropical regions
- **International Organizations**: WHO, ASEAN health cooperation frameworks
- **Academic Institutions**: Teaching platform for health economics and forecasting

### 📱 **Platform Features**
- **Real-time Forecasting**: Interactive 16-week dengue predictions
- **Scenario Planning**: Adjustable intervention parameters and costs
- **Historical Analysis**: 11-year trend visualization and outbreak detection
- **Export Capabilities**: Download predictions and analysis reports

---

## 🤝 **Contributing & Development**

### 🛠️ **Technical Stack**
- **Core**: Python 3.9+, pandas, numpy
- **Modeling**: Prophet (Meta), scikit-learn, statsmodels
- **Visualization**: Streamlit, Plotly, matplotlib
- **Deployment**: Docker-ready, cloud-compatible

### 📝 **Contributing Guidelines**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Run tests and validate pipeline
4. Submit pull request with detailed description

### 🐛 **Issues & Support**
- Report bugs via GitHub Issues
- Include data, environment, and reproduction steps
- Check existing issues before creating new ones

---

## 📄 **License & Citation**

### 📜 **License**
This project is licensed under the MIT License - see the LICENSE file for details.

### 🎓 **Citation**
If you use this platform in your research, please cite:
````
Singapore Dengue Forecasting Platform (2024)
"Dengue Case Prediction and Cost-Benefits Analysis Platform"
Available at: https://github.com/Adredes-weslee/Dengue-Case-Prediction-and-Cost-Benefits-Analysis
````

### 🔗 **References**
- Original research notebook with comprehensive literature review
- Singapore Ministry of Health dengue surveillance data
- WHO guidelines for health economic evaluation
- Meta Prophet forecasting framework documentation

---

## 🏆 **Acknowledgments**

- **Singapore National Environment Agency**: Vector surveillance data and domain expertise
- **Ministry of Health Singapore**: Disease surveillance infrastructure  
- **Meta AI Research**: Prophet forecasting framework
- **WHO**: DALY methodology and health economic standards

**Built with ❤️ for Singapore's public health community**