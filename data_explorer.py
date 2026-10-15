import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="User Data Explorer", page_icon="🌍", layout="wide")


@st.cache_data  # Cache the fetch so it runs once, not on every re-run
def fetch_users():
    response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
    response.raise_for_status()  # Raise on 4xx/5xx, which requests does not do by default
    return response.json()


st.title("🌍 User Data Explorer")

try:
    users = fetch_users()
except Exception as e:
    st.error(f"Could not fetch users: {e}")
    st.stop()  # Stop the script here so nothing below runs with no data

# --- Flatten the nested JSON into a flat table ---
rows = []
for user in users:
    rows.append({
        "Name": user["name"],
        "Email": user["email"],
        "City": user["address"]["city"],
        "Company": user["company"]["name"],
    })

df = pd.DataFrame(rows)

# --- Sidebar filter ---
with st.sidebar:
    st.title("🔍 Filter")
    name_filter = st.text_input("Filter by name", placeholder="Type a name...")
    st.caption("Filters are case-insensitive.")

filtered = df[df["Name"].str.contains(name_filter, case=False, na=False)]

# --- Metrics row ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Users", len(df))
with col2:
    st.metric("Unique Cities", df["City"].nunique())
with col3:
    st.metric("Unique Companies", df["Company"].nunique())

st.divider()

# --- Filterable table ---
st.subheader(f"Users ({len(filtered)} shown)")
st.dataframe(filtered, use_container_width=True)

st.divider()

# --- Bar chart: users per city ---
st.subheader("Users per City")
city_counts = df["City"].value_counts().sort_values(ascending=False)
st.bar_chart(city_counts)