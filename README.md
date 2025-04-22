# 🧠 Forecasting Dengue Cases & Evaluating Public Health Interventions in Singapore
> Predicting outbreaks and assessing the cost-effectiveness of Wolbachia vs. Dengvaxia®

---

## 🧠 Problem Statement
This project addresses two interlinked public health goals:

- **📊 Forecasting:** Develop a time series model to predict weekly dengue cases in Singapore up to **16 weeks ahead**.
- **📈 Intervention Analysis:** Compare cost-effectiveness of two control strategies:
  - **Wolbachia** mosquito deployment
  - **Dengvaxia®** population-level vaccination

---

## ✅ Success Criteria

- **Forecasting Objective:** Minimize **Mean Absolute Percentage Error (MAPE)** on the test set (16-week forecast horizon).
- **Cost-Effectiveness:** Identify the intervention with the **lowest cost per DALY averted** (in 2020 USD).

---

## 📁 Project Structure

| Component | Description |
|----------|-------------|
| `project_4_cleaning_eda_modeling.ipynb` | Full pipeline: cleaning, EDA, modeling, evaluation |
| `README.md` Sections | Data, Approach, Modeling, Conclusions, Recommendations, References |

---

## 📊 Data Overview

| Feature               | Type    | Source CSV                         | Description                                                                                      |
|-----------------------|---------|------------------------------------|--------------------------------------------------------------------------------------------------|
| `dengue_cases`        | int64   | Weekly Infectious Disease          | Weekly count of dengue cases reported                                                           |
| `temp`, `tempmax`, `tempmin` | float64 | Daily Weather Data                | Aggregated to weekly averages (mean, max, min temperature)                                      |
| `humidity`, `precip`, `precipcover` | float64 | Daily Weather Data        | Weekly means of humidity and precipitation-related metrics                                       |
| `number_of_searches` | int64   | Monthly Google Trends              | Weekly proxy derived from monthly search interest on dengue                                     |
| `total_population`    | float64 | Yearly Population                  | Weekly values backfilled from annual data assuming intra-year constancy                         |

**Final dataset:** `dengue_df` with **574 weekly entries** from **2012-01-01 to 2022-12-25**.

---

## 🔍 Methodology

### ✔️ Data Cleaning Summary
All datasets underwent:
- Duplicate and null check
- Datetime parsing & reindexing
- Frequency conversion to weekly granularity
- Forward/backward fill depending on temporal assumptions
- Renaming and harmonizing of column labels

### ⚖️ Statistical Tests

| Test         | Result     | Interpretation                     |
|--------------|------------|------------------------------------|
| ADF Test     | p = 0.0037 | Stationary                         |
| KPSS Test    | p = 0.10   | Non-stationary trend component     |
| FS Test      | FS = 0.5678| No seasonal differencing required  |

### 🌐 Transformations Applied
- Log transformation
- First-order differencing to stabilize variance
- No seasonal differencing needed

---

## 🤖 Modeling & Cost-Benefit Analysis

### 🔢 Forecasting Model Performance (MAPE Scores)

| Model         | Train MAPE | Test MAPE |
|---------------|------------|-----------|
| ARIMA         | 3.59       | 0.68      |
| SARIMA        | 3.59       | 0.68      |
| SARIMAX       | 3.08       | 0.66      |
| Holt-Winters  | 3.90       | 0.36      |
| BATS          | 2.99       | 0.50      |
| TBATS         | 2.47       | 0.43      |
| **Prophet**   | **1.19**   | **0.095** |

> ⬆️ **Prophet** achieved the **lowest test MAPE** (0.0952), outperforming all other models.

### ⚖️ Cost-Effectiveness of Interventions

#### Wolbachia Deployment (International Benchmarks)

| Location   | Cost/year (USD) | Benefit/year (USD) | BCR  | Cost/DALY (USD) | WHO Threshold (0.5x GDP) |
|------------|------------------|---------------------|------|------------------|----------------------------|
| Vietnam    | 17.13M           | 15.95M              | 1.86 | 1,048            | 1,760                      |
| Jakarta    | 13.73M           | 27.90M              | 4.06 | 1,100            | 4,487                      |
| Singapore  | 27.00M           | 78.40M              | 2.90 | 60,039           | 30,364                     |

#### Dengvaxia® Vaccination (Singapore)

| Metric                                  | Value             |
|-----------------------------------------|--------------------|
| Population (2022 est.)                  | 5,637,022          |
| 3-dose cost per person                  | 391 USD            |
| 10-year vaccination cost (80% efficacy) | 220.7M USD         |
| DALYs averted                           | 611.6              |
| Cost per DALY averted                   | 360,876 USD        |
| WHO Threshold (3x GNI)                  | 166,255 USD        |

> ❌ **Dengvaxia® is not cost-effective**, with a cost per DALY averted **6x higher** than Wolbachia.

---

## 📌 Conclusion

- **Forecasting:** Prophet is the best model to support **16-week dengue forecasting**, enabling earlier deployment of vector control strategies.
- **Cost-Benefit:** **Wolbachia is significantly more cost-effective** than Dengvaxia®.
- **Policy Implication:** Singapore's low dengue seroprevalence (7% in youth) renders **population-wide Dengvaxia® vaccination impractical** without screening.

---

## ✅ Recommendations

1. **Operationalize Prophet forecasts** to guide annual pre-emptive Wolbachia deployment and public awareness campaigns.
2. **Fine-tune Prophet** to reduce overfitting (train vs. test MAPE gap).
3. **Scale Wolbachia deployment**, prioritizing high-risk zones and adjusting for seasonal forecasts.
4. **Monitor vaccine pipeline**: Consider Takeda's TAK-003 upon approval as a safer alternative to Dengvaxia®.
5. **Avoid indiscriminate vaccination**: Current low seroprevalence makes mass Dengvaxia® rollout unsafe without prior testing.

---

## 📄 References

1. https://www.visualcrossing.com/weather/weather-data-services/Singapore/metric/
2. https://trends.google.com/trends/explore?date=today%205-y&geo=SG&q=%2Fm%2F09wsg
3. https://tablebuilder.singstat.gov.sg/table/TS/M810001#!
4. https://beta.data.gov.sg/datasets/508/view
5. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9968779
6. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6085773/
7. https://journals.plos.org/plosntds/article/file?id=10.1371/journal.pntd.0011400&type=printable
8. https://www.ncid.sg/Health-Professionals/Articles/Pages/Rise-in-dengue-cases-underscores-need-for-constant-vigilance.asp
9. https://www.straitstimes.com/multimedia/graphics/2022/06/singapore-dengue-cases/index.html?shell
10. https://academic.oup.com/jid/article/223/3/399/5916376
11. https://www.nature.com/articles/s41597-022-01666-y
12. https://www.ncid.sg/Health-Professionals/Articles/Pages/Epidemic-Dengue-in-Singapore-During-COVID-19-Pandemic.aspx
13. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7798931/
14. https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0001426
15. https://www.who.int/data/gho/indicator-metadata-registry/imr-details/158
16. https://www.channelnewsasia.com/singapore/nea-dengue-cases-wolbachia-mosquito-production-3441776
17. https://www.nea.gov.sg/corporate-functions/resources/research/wolbachia-aedes-mosquito-suppression-strategy/wolbachia-aedes-release-schedule
18. https://www.straitstimes.com/singapore/health/about-200m-wolbachia-aedes-mosquitoes-released-from-mosquito-factory-nea
19. https://www.nea.gov.sg/corporate-functions/resources/research/wolbachia-aedes-mosquito-suppression-strategy
20. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10021432/
21. https://www.sciencedaily.com/releases/2021/10/211013152142.htm
22. https://www.channelnewsasia.com/singapore/dengue-death-2023-infection-cases-clusters-nea-3652756
23. https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0011356
24. https://bmcmedicine.biomedcentral.com/articles/10.1186/s12916-020-01638-2#Tab1
25. https://www.cdc.gov/dengue/vaccine/parents/eligibility/faq.html
26. https://ehp.niehs.nih.gov/doi/10.1289/ehp.1509981
27. https://github.com/docligot/aedesproject
28. https://towardsdatascience.com/time-series-from-scratch-decomposing-time-series-data-7b7ad0c30fe7
29. https://towardsdatascience.com/interpreting-acf-and-pacf-plots-for-time-series-forecasting-af0d6db4061c
30. https://www.straitstimes.com/singapore/health/singapore-records-first-2-deaths-from-dengue-for-2023
31. https://timeseriesreasoning.com/contents/holt-winters-exponential-smoothing/
32. https://towardsdatascience.com/time-series-in-python-exponential-smoothing-and-arima-processes-2c67f2a52788
33. https://facebook.github.io/prophet/
34. https://towardsdatascience.com/how-to-forecast-time-series-with-multiple-seasonalities-23c77152347e
35. https://towardsdatascience.com/3-types-of-seasonality-and-how-to-detect-them-4e03f548d167
36. https://www.statsmodels.org/stable/examples/notebooks/generated/stationarity_detrending_adf_kpss.html
37. https://www.moh.gov.sg/news-highlights/details/development-of-dengue-vaccines-or-drugs-that-may-become-viable-for-public-consumption
38. https://www.moh.gov.sg/news-highlights/details/subsidies-for-dengue-vaccine

---

**Author:** Wes Lee  
🔗 [LinkedIn](https://www.linkedin.com/in/wes-lee)  · 💻 Portfolio available upon request  
📝 License: MIT

---
