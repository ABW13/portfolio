import streamlit as st
from datetime import datetime

st.title("Streamlit Execution Demo")

# Step 1: runs on EVERY re-run, so the timestamp changes each time
st.write(f"Script ran at: **{datetime.now().strftime('%H:%M:%S')}**")

# Step 2: widgets return their current values
st.divider()
st.header("Widget Values")

name = st.text_input("What's your name?", placeholder="Type here...")
volume = st.slider("Volume", min_value=0, max_value=100, value=50)
color = st.selectbox("Favorite color", ["Red", "Blue", "Green", "Purple"])

st.write(f"Name: **{name or '(empty)'}**")
st.write(f"Volume: **{volume}**")
st.write(f"Color: **{color}**")

# Step 3: conditional rendering
st.divider()
st.header("Conditional Content")

topic = st.radio(
    "What would you like to learn about?",
    ["Python", "JavaScript", "SQL", "FastAPI"]
)

if topic == "Python":
    st.info("Python is a versatile language used in AI, data science, web development, and automation.")
    st.code('print("Hello from Python!")', language="python")
elif topic == "JavaScript":
    st.info("JavaScript makes web pages interactive. It runs in the browser.")
    st.code('console.log("Hello from JS!");', language="javascript")
elif topic == "SQL":
    st.info("SQL queries and manages data in relational databases.")
    st.code('SELECT * FROM users WHERE active = true;', language="sql")
elif topic == "FastAPI":
    st.info("FastAPI builds high-performance Python APIs with auto-validation.")
    st.code('@app.get("/hello")\ndef hello():\n    return {"message": "Hello!"}', language="python")

# Step 4: multiselect driving calculations
st.divider()
st.header("Dynamic Calculations")

all_modules = [
    "Pre-work: Python", "Module 1: AI Fundamentals", "Module 2: Advanced Python",
    "Module 3: Databases", "Module 4: REST APIs", "Module 5: FastAPI",
]

modules = st.multiselect(
    "Which modules have you completed?",
    all_modules,
    default=["Pre-work: Python"]
)

total_modules = len(all_modules)
completed = len(modules)
progress = completed / total_modules

st.write(f"Completed: **{completed}** of **{total_modules}** modules")
st.progress(progress)

if progress == 1.0:
    st.balloons()
    st.success("Congratulations! You've completed the course!")
elif progress >= 0.5:
    st.write("More than halfway there! Keep going!")
else:
    st.write("Great start! Every module builds on the last.")