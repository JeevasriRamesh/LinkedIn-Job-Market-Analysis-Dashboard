import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("sample_jobs.csv")

# Page setup
st.set_page_config(page_title="Job Dashboard", layout="wide")

st.title("📊 LinkedIn Job Market Analysis")


# SIDEBAR FILTERS

st.sidebar.header("🔍 Filters")

location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + sorted(df['location'].unique())
)

min_salary = st.sidebar.slider(
    "Minimum Salary",
    int(df['normalized_salary'].min()),
    int(df['normalized_salary'].max()),
    int(df['normalized_salary'].min())
)

# Apply filters
filtered_df = df.copy()

if location != "All":
    filtered_df = filtered_df[filtered_df['location'] == location]

filtered_df = filtered_df[
    filtered_df['normalized_salary'] >= min_salary
]


# KPIs

col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(filtered_df))
col2.metric("Avg Salary", int(filtered_df['normalized_salary'].mean()))
col3.metric("Max Salary", int(filtered_df['normalized_salary'].max()))

# SKILL DEMAND

st.subheader("💻 Skill Demand")

skills = ['python', 'sql_skill', 'excel', 'power_bi']
counts = [filtered_df[s].sum() if s in filtered_df.columns else 0 for s in skills]

fig, ax = plt.subplots()
ax.bar(skills, counts)
st.pyplot(fig)


# SALARY DISTRIBUTION

st.subheader("💰 Salary Distribution")

fig, ax = plt.subplots()
ax.hist(filtered_df['normalized_salary'], bins=30)
st.pyplot(fig)


# TOP LOCATIONS

st.subheader("📍 Top Job Locations")

top_locations = filtered_df['location'].value_counts().head(10)

fig, ax = plt.subplots()
top_locations.plot(kind='bar', ax=ax)
st.pyplot(fig)


# TOP COMPANIES (NEW 🔥)

st.subheader("🏢 Top Companies")

top_companies = filtered_df['company_name'].value_counts().head(10)

fig, ax = plt.subplots()
top_companies.plot(kind='bar', ax=ax)
st.pyplot(fig)


# DATA TABLE

st.subheader("📄 Job Data")
st.dataframe(filtered_df.head(50))