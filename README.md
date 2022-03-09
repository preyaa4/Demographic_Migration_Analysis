# Demographic_Migration_Analysis
Basic analysis of migration patterns as well as their related demographic characteristics. The demographics of focus will be: education, race, sex, population by age, poverty levels, and housing types.

Setup: 
- Install the packages or use conda to setup environment with env.yml file 
- All the scripts are located in src folder 

To Generate Plots:
- Normalized Plots: 
  - ./src/normalized_plots.ipynb
- Age and sex plots:
  - ./src/age_and_sex_plots.py 


Scripts Usage:
- To fetch the data year wise: ./src/MigrationData.py
- Normalized Plots for all categories: ./src/normalized_plots.py
- Geographic map of overal stats: ./src/population_plots.py
- Income related plots: ./src/income_plots.py 
- Race and Education Analysis: ./src/race_and_education_groups.py
- Age and Sex plots: ./src/age_and_sex_plots.py
- Poverty: ./src/poverty_gif_plots.py 
- Normalized Analysis group wise: 
  - ./src/age_group_analysis.py
  - ./src/sex_group_analysis.py
  - ./src/income_group_analysis.py
  - ./src/education_group_analysis.py
  - ./src/race_group_analysis.py
  - ./src/poverty_group_analysis.py
  - ./src/housing_group_analysis.py

## File Structure
```
.
├── README.md
├── data
│   └── migration_data
│       ├── ACSST1Y[2010-2019].S0701_data_with_overlays_[...].csv       --> Year Wise Data 
│       ├── ...
│       └── README.md
├── src
│   ├── MigrationData.py                         --> Main Data class def (functions to fetch data)
│   ├── age_and_sex_plots.py                     --> Age and Sex data analysis
│   ├── population_plots.py                      --> Overall state level migration trend 
│   ├── Poverty_gif_plots.py                     --> Poverty data analysis
│   ├── race_and_education_groups.py             --> Race and Education data analysis 
│   ├── normalized_plots.py                      --> Generate normalized plots for all categories
│   ├── *_group_analysis.py                      --> specific group's normalized analysis script
│   └── README.md
├── Visualization_and_plots
│   └── [...]                                    --> Generated Plots 
├──.gitignore
└── env.yaml                                     --> Package requirements/conda env setup 
```

# Data
- [American Community Survey (in-depth demographic and migration data)](https://data.census.gov/cedsci/table?t=International%20and%20Domestic%20Migration%3APopulation%20Change%20and%20Components&g=0100000US%240400000&tid=ACSST1Y2019.S0701)

## In-depth demographics
- Population
  - 1-18 years old
  - 19-24 years old
  - 25-54 years old
  - 55 years old and above
- Sex
- Race
  - White
  - Black
  - Asian
  - Hispanic
  - Other
- Educational attainment
  - High school and below
  - Some college and associates degree
  - Bachelors degree and above
- Individual income
  - 1-35k
  - 35k-50k
  - 50k-75k
  - 75k+
- Poverty level
  - Below 150%
  - Above 150%
- Housing Tenure
  - Owner occupied
  - Renter occupied

