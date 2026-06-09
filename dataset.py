import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# 1. Dashboard Header & Initial Input Elements
# st.image('Header.png') # Uncomment if you have your header image file ready!

st.date_input("Select a date")

st.title(
    """Welcome to my Dashboard
This is my first time using streamlit."""
)

# 2. Data Acquisition
# To make it dynamic, we use file_uploader like your reference script commented out. 
# It falls back to reading "gaming_academic.csv" locally if no file is uploaded.
upload_file = st.file_uploader("Please upload your CSV file here:", type="csv")

if upload_file is not None:
    df = pd.read_csv(upload_file)
else:
    try:
        df = pd.read_csv("gaming_academic.csv")
    except FileNotFoundError:
        st.warning("Please upload a file or place 'gaming_academic.csv' in the directory to continue.")
        st.stop()

# 3. Data Preparation & Cleaning Pipeline (From your Notebook)
df.columns = [col.capitalize() for col in df.columns]
df.fillna(0, inplace=True)
df.drop_duplicates(inplace=True)

df["Gaming_hours"] = df["Gaming_hours"].astype("int")
df["Study_hours"] = df["Study_hours"].astype("int")
df["Sleep_hours"] = df["Sleep_hours"].astype("int")
df = df.rename(columns={"Reaction_time_ms": "Reaction_time"})

# Feature Engineering
df["Total_activity_hours"] = (
    df["Gaming_hours"] + df["Study_hours"] + df["Sleep_hours"]
)
df["Activity_percentage"] = ((df["Total_activity_hours"] / 24) * 100).round(1)
df["Grades"] = df["Grades"].round(2)

# Grade Categorization 
grade_categories = []
for grade in df["Grades"]:
    if grade > 80:
        grade_categories.append("A")
    elif grade >= 50:
        grade_categories.append("Pass")
    else:
        grade_categories.append("Fail")
df["Grade_category"] = grade_categories


# 4. Display Cleaned Data Summary
st.subheader("Cleaned Dataset Summary")
st.write(df)


# 5. Interactive Analysis Section (From your Reference Script)
st.markdown("---")
st.header("🔍 Interactive Exploratory Charts")

# Histogram Tool
st.subheader("Dynamic Histogram")
column = st.selectbox("Choose a column for the histogram", df.columns)
fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
df[column].plot(kind="hist", ax=ax_hist, color="blue", edgecolor="black")
st.pyplot(fig_hist)

# Scatter Chart Tool
st.subheader("Dynamic Scatter Chart")
x_column = st.selectbox("Choose x-axis column", df.columns, index=0)
y_column = st.selectbox("Choose y-axis column", df.columns, index=1)
fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
ax_scatter.scatter(df[x_column], df[y_column], color="purple", alpha=0.7)
ax_scatter.set_xlabel(x_column)
ax_scatter.set_ylabel(y_column)
ax_scatter.set_title(f"Scatter plot of {x_column} vs {y_column}")
st.pyplot(fig_scatter)


# 6. Specific Project Visualizations Section (From your Notebook)
st.markdown("---")
st.header("📊 Main Analytical Findings")

# Graph 1: Average Grades Trend by Gaming Hours
st.subheader("1. Average Grades Trend by Gaming Hours")
gaming_grades = df.groupby("Gaming_hours")["Grades"].mean()
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(
    gaming_grades.index,
    gaming_grades.values,
    marker="o",
    linestyle="-",
    color="y",
)
ax1.set_title("Average Grades Trend by Gaming Hours")
ax1.set_xlabel("Gaming hours")
ax1.set_ylabel("Average Grades")
ax1.grid(True)
st.pyplot(fig1)

# Graph 2: Average Stress Level Based on Device Usage
st.subheader("2. Average Stress Level Based on Device Usage")
stress_level = df.groupby("Stress_level")["Device_usage"].mean().round(2)
fig2, ax2 = plt.subplots(figsize=(10, 6))
stress_level.plot(kind="bar", color="skyblue", ax=ax2)
ax2.set_title("Average Stress Level Based on Device Usage")
ax2.set_xlabel("Stress level")
ax2.set_ylabel("Device usage")
ax2.tick_params(axis="x", rotation=45)
ax2.grid(axis="y", linestyle="--", alpha=0.7)
fig2.tight_layout()
st.pyplot(fig2)

# Graph 3: Reaction Time Share by Gaming Genre
st.subheader("3. Distribution of Reaction Time by Gaming Genre")
colors = ["purple", "green", "red", "orange", "blue"]
explode = tuple([0.05] * len(df["Gaming_genre"].unique()))

fig3, ax3 = plt.subplots(figsize=(8, 8))
df.groupby(["Gaming_genre"]).sum().plot(
    kind="pie",
    y="Reaction_time",
    autopct="%1.0f%%",
    colors=colors[: len(df["Gaming_genre"].unique())],
    explode=explode,
    ax=ax3,
)
ax3.set_ylabel("")  # Clear out automatic 'Reaction_time' text on the y-axis side
st.pyplot(fig3)