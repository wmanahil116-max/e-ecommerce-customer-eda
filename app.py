
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="E-commerce Customer Analysis",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_customers.csv")

df = load_data()

# Title
st.title("E-commerce Customer Behavior Analysis")
st.write(
    "This dashboard analyzes customer behavior, "
    "website usage, app usage and yearly spending."
)

# Sidebar filters
st.sidebar.header("Customer Filters")

min_membership = float(df["Length of Membership"].min())
max_membership = float(df["Length of Membership"].max())

membership = st.sidebar.slider(
    "Membership Length",
    min_membership,
    max_membership,
    (min_membership, max_membership)
)

min_spend = float(df["Yearly Amount Spent"].min())
max_spend = float(df["Yearly Amount Spent"].max())

spending = st.sidebar.slider(
    "Yearly Spending",
    min_spend,
    max_spend,
    (min_spend, max_spend)
)

# Apply filters
filtered_df = df[
    (df["Length of Membership"].between(*membership)) &
    (df["Yearly Amount Spent"].between(*spending))
]

# Key metrics
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", len(filtered_df))

col2.metric(
    "Average Spending",
    round(filtered_df["Yearly Amount Spent"].mean(), 2)
)

col3.metric(
    "Average Membership",
    round(filtered_df["Length of Membership"].mean(), 2)
)

col4.metric(
    "Highest Spending",
    round(filtered_df["Yearly Amount Spent"].max(), 2)
)

st.divider()

# Graph 1: Spending distribution
st.subheader("1. Yearly Spending Distribution")

fig, ax = plt.subplots()
sns.histplot(
    filtered_df["Yearly Amount Spent"],
    kde=True,
    ax=ax
)
ax.set_xlabel("Yearly Amount Spent")
ax.set_ylabel("Number of Customers")
st.pyplot(fig)
plt.close(fig)

# Graph 2: App usage
st.subheader("2. Time Spent on App")

fig, ax = plt.subplots()
sns.histplot(filtered_df["Time on App"], kde=True, ax=ax)
ax.set_xlabel("Time on App")
ax.set_ylabel("Frequency")
st.pyplot(fig)
plt.close(fig)

# Graph 3: App vs spending
st.subheader("3. App Usage vs Yearly Spending")

fig, ax = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="Time on App",
    y="Yearly Amount Spent",
    ax=ax
)
ax.set_xlabel("Time on App")
ax.set_ylabel("Yearly Amount Spent")
st.pyplot(fig)
plt.close(fig)

# Graph 4: Website vs spending
st.subheader("4. Website Usage vs Yearly Spending")

fig, ax = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="Time on Website",
    y="Yearly Amount Spent",
    ax=ax
)
ax.set_xlabel("Time on Website")
ax.set_ylabel("Yearly Amount Spent")
st.pyplot(fig)
plt.close(fig)

# Graph 5: Membership vs spending
st.subheader("5. Membership vs Yearly Spending")

fig, ax = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="Length of Membership",
    y="Yearly Amount Spent",
    ax=ax
)
ax.set_xlabel("Length of Membership")
ax.set_ylabel("Yearly Amount Spent")
st.pyplot(fig)
plt.close(fig)

# Graph 6: Correlation heatmap
st.subheader("6. Correlation Heatmap")

numeric_data = filtered_df.select_dtypes(include="number")

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(
    numeric_data.corr(),
    annot=True,
    cmap="coolwarm",
    ax=ax
)
st.pyplot(fig)
plt.close(fig)

# Raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)

# Main findings
st.subheader("Main Findings")

if len(filtered_df) > 1:
    app_corr = filtered_df["Time on App"].corr(
        filtered_df["Yearly Amount Spent"]
    )

    website_corr = filtered_df["Time on Website"].corr(
        filtered_df["Yearly Amount Spent"]
    )

    st.write(
        f"Average yearly spending is "
        f"{filtered_df['Yearly Amount Spent'].mean():.2f}."
    )

    if app_corr > website_corr:
        st.write("App usage has a stronger relationship with spending.")
    else:
        st.write("Website usage has a stronger relationship with spending.")

    st.write(
        "Membership duration and customer spending can be explored "
        "through the scatter plot and correlation heatmap."
    )
else:
    st.warning("Select more customers using the sidebar filters.")
