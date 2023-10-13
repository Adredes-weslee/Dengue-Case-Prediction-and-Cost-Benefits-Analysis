**Problem statement:** 

1. Build a time series model that can predict dengue cases up to 16 weeks into the future.

2. Conduct a cost benefit analysis of islandwide Wolbachia deployment vs population level vaccination with Dengvaxia®.

**Acceptance performance metric:**

Minimizes the MAPE score for the test set of up to 16 weeks of number of predicted dengue cases. 
Determine if Wolbachia or Dengvaxia® has the lowest cost per DALY averted in 2020 USD.

**Notebooks**

project_4_cleaning_eda_modeling

**README Overview**

1. Data
2. Approach
3. Models Performance and Cost Benefit Analysis
4. Conclusion
5. Recommendations
6. References

# 1. Data:

4 csv files:
1) Daily Weather data
2) Monthly Google Trends data
3) Yearly Population data
4) Weekly Infectious Diseases data

**Summary of dataframe that is worked on:**

|       Feature      |   Type  |                  Dataset                 |                                                                          Description                                                                          |
|:------------------:|:-------:|:----------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|    dengue_cases    |  int64  | WeeklyInfectiousDiseaseBulletinCases.csv |                                                              Weekly number of dengue fever cases                                                              |
|       tempmax      | float64 |           Singapore_weather.csv          |                                              Aggregated to weekly by taking mean of max daily temperature (in °C)                                             |
|       tempmin      | float64 |           Singapore_weather.csv          |                                              Aggregated to weekly by taking mean of min daily temperature (in °C)                                             |
|        temp        | float64 |           Singapore_weather.csv          |                                              Aggregated to weekly by taking mean of mean daily temperature (in °C)                                            |
|      humidity      | float64 |           Singapore_weather.csv          | Aggregated to weekly by taking mean on the daily amount of water vapor present in the air compared the maximum amount possible for a given temperature (in %) |
|       precip       | float64 |           Singapore_weather.csv          |               Aggregated to weekly by taking mean of daily precipitation that fell or is predicted to fall in the specified time period (in mm)               |
|     precipcover    | float64 |           Singapore_weather.csv          |          Aggregated to weekly by taking mean of daily proportion of time for which measurable precipitation was record during the time period (in %)          |
| number_of_searches |  int64  |          google_dengue_fever.csv         |     Weekly google search index (where 100 is the max) are actually the search index for that month assuming weekly searches are the same as for that month    |
|  total_population  | float64 |                M810001.csv               |         Weekly populations are actually the population for that year assuming population is constant and only increases at the start of the next year         |


# 2. Approach:

**Summary for Data Inspection for Google Trends:**

|          Method          |                          Observation                         | Action Taken |
|:------------------------:|:------------------------------------------------------------:|:------------:|
|        Check Shape       | There are 140 rows and 2 columns, date and our search counts |      ---     |
|   Check for duplicates   |                  There are no duplicate rows                 |      ---     |
| Check for null/na values |                  There are no missing values                 |      ---     |

**Summary for Data Inspection for Population:**

|          Method          |                           Observation                           | Action Taken |
|:------------------------:|:---------------------------------------------------------------:|:------------:|
|        Check Shape       | There are 11 rows and 2 columns, date and our population counts |      ---     |
|   Check for duplicates   |                   There are no duplicate rows                   |      ---     |
| Check for null/na values |                   There are no missing values                   |      ---     |

**Summary for Data Inspection for Weather:**

|          Method          |                                                       Observation                                                       | Action Taken |
|:------------------------:|:-----------------------------------------------------------------------------------------------------------------------:|:------------:|
|        Check Shape       | There are 4249 rows and 7 columns, date, min temp, max temp, mean temp, humidity, precipitation and precipitation cover |      ---     |
|   Check for duplicates   |                                               There are no duplicate rows                                               |      ---     |
| Check for null/na values |                                               There are no missing values                                               |      ---     |

**Summary for Data Inspection for Dengue:**

|                        Method                        |                            Observation                           | Action Taken |
|:----------------------------------------------------:|:----------------------------------------------------------------:|:------------:|
|               Filter for 'Dengue Fever'              |                                ---                               |   As stated  |
| Rename columns from 'no._of_cases' to 'dengue_cases' |                                ---                               |   As stated  |
|                      Check Shape                     | There are 574 rows and 3 columns, date, disease and dengue cases |      ---     |
|                 Check for duplicates                 |                    There are no duplicate rows                   |      ---     |
|               Check for null/na values               |                    There are no missing values                   |      ---     |

**Summary for Data Cleaning for Google Trends:**

|                                                                                                   Action Taken                                                                                                  |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|                                                                                          Convert 'Month' as pd.datetime                                                                                         |
|                                                                                              Set datetime to index                                                                                              |
|                                                                                               Drop 'Month' column                                                                                               |
|                           Convert datetime since it was 'Monthly' asfreq to 'Weekly'. Forward fill in NAs since I assume that the weekly google search interest is the same as monthly                          |
|                                                                            Rename 'Dengue fever: (Singapore)' to 'number_of_searches'                                                                           |
|                                                                                   Slice our data from 2012-01-01 to 2022-12-25                                                                                  |
|                           There are 574 rows which matches the number of rows in our dengue data and 1 column which represents the index (100 is max) of the number of google searches                          |
| There are 536 duplicates but because we are checking for duplicated values for our single column data, we will ignore this since it is possible that the search counts which are integer values can be repeated |
|                                                                                                No missing values                                                                                                |

**Summary for Data Cleaning for Population:**

|                                                                                                                                                                                                Action Taken                                                                                                                                                                                               |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|                                                                                                                                                                        Created NA population row for 2023 for further data cleaning                                                                                                                                                                       |
|                                                                                                                                                                                    Convert 'Data Series' as pd.datetime                                                                                                                                                                                   |
|                                                                                                                                                                                           Set datetime to index                                                                                                                                                                                           |
|                                                                                                                                                                                         Drop 'Data Series' column                                                                                                                                                                                         |
| Convert datetime since it was 'Yearly' asfreq to 'Weekly'. Backward fill in NAs since population data as recorded is as stated for the entire year, I have the make the assumption that the population value is constant for the entire year. Linear interpolation will not give the desired increase since population fell during the Covid-19 outbreak and resumed growing once restrictions were eased |
|                                                                                                                                                           Drop the last NA row since which we do not have dengue data for the first week of 2023                                                                                                                                                          |
|                                                                                                                                                                              Rename 'Total Population ' to 'total_population'                                                                                                                                                                             |
|                                                                                                                                      There are 574 rows which matches the number of rows in our dengue data and 1 column which represents the population of Singapore                                                                                                                                     |
|                                                                                               There are 563 duplicates but because we are checking for duplicated values for our single column data, we will ignore this since population for that year was 'filled in' for all missing values of that year                                                                                               |
|                                                                                                                                                                                             No missing values                                                                                                                                                                                             |

**Summary for Data Cleaning for Weather:**

|                                                            Action Taken                                                            |
|:----------------------------------------------------------------------------------------------------------------------------------:|
|                                                  Convert 'datetime' to pd.datetime                                                 |
|                                                        Set datetime to index                                                       |
|                                          Aggregating daily data to weekly data by the mean                                         |
|                                            Slice our data from 2012-01-01 to 2022-12-25                                            |
| There are 574 rows which matches the number of rows in our dengue data and 6 column which represents the weather data of Singapore |
|                                                     There are no duplicate rows                                                    |
|                                                          No missing values                                            

**Summary for Data Cleaning for Dengue:**

|                                                                                         Action Taken                                                                                        |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|                                                                              Convert 'datetime' to pd.datetime                                                                              |
|                                                                                    Set datetime to index                                                                                    |
|                                                                             Drop 'epi_week' and disease columns                                                                             |
|                                                        Convert datetime asfreq to 'Weekly' to set the datetime index freq to 'W-SUN'                                                        |
|                                                                  There are 574 rows and 1 column which is the dengue count                                                                  |
| There are 220 duplicate values but because we are checking for duplicated values for our single column data, we will ignore this since it is possible that the dengue count can be repeated |
|                                                                                      No missing values                                                                                      |

**Summary for Merging of Dataframes:**

|                                                         Action Taken                                                         |
|:----------------------------------------------------------------------------------------------------------------------------:|
| Individual dengue, weather, google trends and population dataframes were merged into one larger dataframe called 'dengue_df' |
|          There are 574 rows and 9 columns which matches the desired output from merging all 4 individual dataframes          |
|                               Check datatypes to ensure datatypes are in the appropriate format                              |
|                                                  There are no duplicate rows                                                 |
|                                                       No missing values                                                      |
|                                   Save dengue_df dataframe to dengue_df.csv as a checkpoint                                  |

**Statistical Test Results:**

| Test                        | Value  | Action                                                   |
|-----------------------------|--------|----------------------------------------------------------|
| ADF Test                    | 0.0037 | P-value < 0.05, hence Stationary                         |
| KPSS Test                   | 0.1000 | P-value > 0.05, hence Non-Stationary                     |
| Seasonal Strength(FS Test)  | 0.5678 | FS value < 0.64, hence no seasonal differencing required |

**Summary for Exploratory Data Analysis:**

|                                                                                                                                                    Observations                                                                                                                                                   |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|                                                                                      From the seasonal decomposition plots, the seasonality is likely to be multiplicative and the trend is also likely to be multiplicative.                                                                                     |
|                                                                             Furthermore from the plot of dengue cases, the changing periodicity and amplitude of the peaks indicate that the seasonality is stochastic non-stationary.                                                                            |
| Log transformation and 1st differencing of the dengue cases was required to create a graph that had approximately constant mean and variance. Seasonal differencing at a period of 52 weeks did not seem to be necessary as the output did not seem much different from a log transformed 1st differenced series. |
|              The KPSS and ADF test results indicate that only a 1st differencing is necessary for the data to become stationary. The CH and OCSB tests confirm what the transformation and visual plotting of the dengue series data indicate and that is that no seasonal differencing is required.              |
|  The ACF and PACF plots do not allow for a clear indication of a seasonality of 52 weeks and this is likely due to the changing periodicity of the seasonality. The AR and MA components are also not very obvious from the plots, but a value of 3 is likely and a value of 0 for either AR and MA is unlikely.  |
|                                                                        The rolling mean and std for 4, 13 and 52 weeks indicate that the 'shocks' to the data during the outbreaks will require a flexible model for accurate predictions.                                                                        |

# 3. Models Performance and Cost Benefit Analysis:

**Train and Test MAPE for 7 Time Series Models:**

|     Model    | Train MAPE | Test MAPE |
|:------------:|:----------:|:---------:|
|     ARIMA    |   3.5939   |   0.6769  |
|    SARIMA    |   3.5939   |   0.6769  |
|    SARIMAX   |   3.0831   |   0.6625  |
| Holt-Winters |   3.8982   |   0.3575  |
|     BATS     |   2.9868   |   0.4978  |
|     TBATS    |   2.4667   |   0.4336  |
|    Prophet   |   1.1860   |   0.0952  |

**Comparing Wolbachia Deployment in Vietnam, Jakarta and Singapore:**

|                                                       | Vietnam      | Jakarta     | Singapore   |
|-------------------------------------------------------|--------------|-------------|-------------|
| Cost of Wolbachia Deployment per year                 | 17.13 Mn USD | 13.73Mn USD | 27.00Mn USD |
| Benefit of Wolbachia Deployment per year              | 15.95 Mn USD | 27.90Mn USD | 78.40Mn USD |
| Benefit Cost Ratio                                    | 1.86         | 4.06        | 2.90        |
| Cost per disability-adjusted life year (DALY) averted | 1,048 USD    | 1,100 USD   | 60,039 USD  |
| 0.5 x GDP per Capita                                  | 1,760 USD    | 4,487 USD   | 30,364 USD  |

**Comparing Wolbachia Deployment against Dengvaxia® Vaccination in Singapore:**

|                                                                                                                           |                 |
|---------------------------------------------------------------------------------------------------------------------------|-----------------|
| Population (estimated from 2022)                                                                                          | 5,637,022       |
| 3 Doses of Dengvaxia® at Raffles Medical                                                                                  | 391 USD         |
| Cost per year to vaccinate Singapore at a population level assuming vaccine confers immunity for 10 years at 80% efficacy | 220,711,959 USD |
| Disability-adjusted life year (DALY) averted due to vaccination                                                           | 611.6 DALYs     |
| Cost per disability-adjusted life year (DALY) averted                                                                     | 360,876 USD     |
| 3 x GNI per capita                                                                                                        | 166,255 USD     |
| Cost per disability-adjusted life year (DALY) averted using Wolbachia                                                     | 60,039 USD      |

# 4. Conclusion:

The best time series model is Prophet by Facebook (now Meta) with a test MAPE of 0.0953 and a train MAPE of 1.1861. Although the model is overfit to the training data, it exhibits the best performance based on our evaluation metric and hence is deemed suitable to make predictions up to 16 weeks in the future to allow for vector control and suppression efforts to be ramped up in time to 'blunt' or mitigate the worst of the peak dengue season which will minimize both the health and economic cost to society as a whole.

Furthermore, islandwide deployment of Project Wolbachia is deemed to be more cost effective than population level vaccination with Dengvaxia® with a cost per disability-adjusted life year (DALY) averted of 60,039 USD compared to 360,876 USD for population level vaccination with Dengvaxia®. Cost per DALYs averted for islandwide deployment of Project Wolbachia is also less than Singapore's 3x gross national income of 166,255 USD; above which the method is no longer cost effective for Singapore.

# 5. Recommendations

1. Use 16 week predictions of Prophet time series model to inform timing of annual dengue awareness and control campaign and specific site Wolbachia deployment. This makes use of the predictive capability of the best model.
2. Grid Search hyperparameters for Prophet to minimize overfitting on the training data. Ideally, we would like the train and test MAPE to converge to the same values.
3. Continue to expand the capacity of Project Wolbachia and progressively rollout Wolbachia deployment in view of better cost effectiveness compared to population level vaccination with Dengvaxia®
4. Vaccination may become cost effective depending on availability of newer vaccines and [other than Dengvaxia, there are approximately six dengue vaccine candidates in various stages of clinical development, with Takeda’s tetravalent (i.e. targeting all four dengue strains) dengue vaccine (TAK-003) being the most advanced candidate. Takeda has submitted its dengue vaccine candidate for registration in Singapore, and the application is currently being reviewed by HSA.](https://www.moh.gov.sg/news-highlights/details/development-of-dengue-vaccines-or-drugs-that-may-become-viable-for-public-consumption)
5. The other reason why population level vaccination cannot be recommended is that Singapore has a low dengue prevalence at 7% for individuals below 18 years of age.  Among adults age 18 to 74 years, the prevalence is 45%, still below the threshold for population vaccination without screening. [In view of this, the Ministry of Health’s Expert Committee on Immunisation (ECI) has advised that Dengvaxia is not an effective means to control dengue at the population level.](https://www.moh.gov.sg/news-highlights/details/subsidies-for-dengue-vaccine) 

# 6. References

1. https://www.visualcrossing.com/weather/weather-data-services/Singapore/metric/
2. https://trends.google.com/trends/explore?date=today%205-y&geo=SG&q=%2Fm%2F09wsg
3. https://tablebuilder.singstat.gov.sg/table/TS/M810001#!
4. https://beta.data.gov.sg/datasets/508/view
5. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9968779
6. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6085773/
7. https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwja5c2Y9-iAAxV4T2wGHRgWBDcQFnoECDoQAQ&url=https%3A%2F%2Fjournals.plos.org%2Fplosntds%2Farticle%2Ffile%3Fid%3D10.1371%2Fjournal.pntd.0011400%26type%3Dprintable&usg=AOvVaw3qDzs9OpMnvja5UVHkWlGe&opi=89978449
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