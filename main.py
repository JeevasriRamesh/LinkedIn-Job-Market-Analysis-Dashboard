import pandas as pd

# Load raw data
df = pd.read_csv("sample_jobs.csv")


# BASIC CLEANING

df = df.drop_duplicates()

# Remove rows where description is missing
df = df.dropna(subset=['description'])

# Fill missing company names
df['company_name'] = df['company_name'].fillna("Unknown")

# Fix location
df['location'] = df['location'].fillna("Unknown")
df['location'] = df['location'].str.lower().str.strip()

# Standardize locations
df['location'] = df['location'].replace({
    'united states': 'usa',
    'us': 'usa',
    'new york, ny': 'new york',
    'san francisco, ca': 'san francisco'
})

# Remove useless unknown rows (optional)
df = df[df['location'] != 'unknown']

# Convert title to lowercase
df['title'] = df['title'].str.lower()


# FEATURE ENGINEERING

df['python'] = df['description'].str.contains('python', case=False, na=False).astype(int)
df['sql_skill'] = df['description'].str.contains('sql', case=False, na=False).astype(int)
df['excel'] = df['description'].str.contains('excel', case=False, na=False).astype(int)
df['power_bi'] = df['description'].str.contains('power bi', case=False, na=False).astype(int)

# Experience extraction
# Experience extraction (Improved)
df['experience'] = df['formatted_experience_level'].str.extract(r'(\d+)')

# Convert to numeric
df['experience'] = pd.to_numeric(df['experience'], errors='coerce')

# Fill missing based on text levels
df.loc[df['formatted_experience_level'].str.contains('entry', case=False, na=False), 'experience'] = 0
df.loc[df['formatted_experience_level'].str.contains('associate', case=False, na=False), 'experience'] = 2
df.loc[df['formatted_experience_level'].str.contains('mid', case=False, na=False), 'experience'] = 4
df.loc[df['formatted_experience_level'].str.contains('senior', case=False, na=False), 'experience'] = 6
df.loc[df['formatted_experience_level'].str.contains('director', case=False, na=False), 'experience'] = 10


# SALARY CLEANING

df = df[df['normalized_salary'].notnull()]
df = df[(df['normalized_salary'] > 10000) & (df['normalized_salary'] < 300000)]


# SELECT IMPORTANT COLUMNS

df = df[[
    'job_id',
    'company_name',
    'title',
    'description',
    'location',
    'normalized_salary',
    'python',
    'sql_skill',
    'excel',
    'power_bi',
    'experience'
]]


# SAVE CLEANED DATA

df.to_csv("output/cleaned_jobs.csv", index=False)
print("✅ Data cleaned and saved successfully!")