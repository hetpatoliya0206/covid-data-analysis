import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("covid_data.csv")

# -----------------------------
# Data Cleaning
# -----------------------------
df['Date'] = pd.to_datetime(df['Date'])

# Convert important columns to numeric
df['Death'] = pd.to_numeric(df['Death'], errors='coerce')
df['Total Confirmed cases'] = pd.to_numeric(df['Total Confirmed cases'], errors='coerce')

# Fill missing values
df = df.fillna(0)

print("\nDataset Preview:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

# -----------------------------
# Analysis 1: Total Cases by State
# -----------------------------
state_cases = df.groupby("Name of State / UT")["Total Confirmed cases"].max()

print("\nTop States by Cases:")
print(state_cases.sort_values(ascending=False).head(10))

# -----------------------------
# Analysis 2: Daily Cases
# -----------------------------
df['Daily Cases'] = df.groupby("Name of State / UT")["Total Confirmed cases"].diff()

# -----------------------------
# Analysis 3: Death Rate
# -----------------------------
df['Death Rate'] = df['Death'] / df['Total Confirmed cases'].replace(0, 1)

death_rate = df.groupby("Name of State / UT")["Death Rate"].max()

print("\nTop States by Death Rate:")
print(death_rate.sort_values(ascending=False).head(10))

# -----------------------------
# Visualization 1: India Total Cases
# -----------------------------
india_total = df.groupby("Date")["Total Confirmed cases"].sum()

plt.figure()
plt.plot(india_total.index, india_total.values, marker='o')
plt.title("Total COVID-19 Cases in India Over Time")
plt.xlabel("Date")
plt.ylabel("Cases")

plt.savefig("output/india_total_cases.png")
plt.close()

# -----------------------------
# Visualization 2: Top 10 States
# -----------------------------
top10 = state_cases.sort_values(ascending=False).head(10)

plt.figure()
top10.plot(kind='bar')
plt.title("Top 10 States by COVID-19 Cases")
plt.xlabel("State")
plt.ylabel("Cases")

plt.savefig("output/top_states.png")
plt.close()

# -----------------------------
# Visualization 3: Top 5 States Trend
# -----------------------------
top5_states = top10.index[:5]

plt.figure()

for state in top5_states:
    state_data = df[df["Name of State / UT"] == state]
    plt.plot(state_data["Date"], state_data["Total Confirmed cases"], label=state)

plt.legend()
plt.title("Top 5 States COVID-19 Trend Comparison")
plt.xlabel("Date")
plt.ylabel("Cases")

plt.savefig("output/top5_states_trend.png")
plt.close()

print("\nCharts saved in output folder ✅")