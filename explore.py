import streamlit as st

st.title("☕ Coffee Brew Calculator")
st.write("Dial in your next cup of pour-over coffee.")

# --- Widgets ---
st.subheader("Your Setup")

method = st.selectbox(
    "Brewing method",
    ["Pour Over (V60)", "French Press", "AeroPress", "Chemex"]
)

beans = st.text_input("What beans are you using?", placeholder="e.g. Ethiopian Yirgacheffe")

cups = st.slider("How many cups?", min_value=1, max_value=6, value=2)

strength = st.radio(
    "Strength",
    ["Light", "Balanced", "Strong"],
    index=1
)

extras = st.multiselect(
    "Add-ons",
    ["Oat milk", "Sugar", "Cinnamon", "Extra shot"],
    default=["Oat milk"]
)

grind_fresh = st.checkbox("Grind beans fresh", value=True)

notes = st.text_area("Tasting notes", placeholder="What did you notice?")

# --- Metadata that varies by method ---
methods = {
    "Pour Over (V60)": {"ratio": 16, "temp": 93, "time": "2:30"},
    "French Press":    {"ratio": 12, "temp": 95, "time": "4:00"},
    "AeroPress":       {"ratio": 13, "temp": 85, "time": "1:30"},
    "Chemex":          {"ratio": 15, "temp": 94, "time": "4:30"},
}

info = methods[method]

# --- Calculations ---
strength_ratio = {"Light": 2, "Balanced": 0, "Strong": -2}
ratio = info["ratio"] + strength_ratio[strength]

cup_ml = 240
total_water = cups * cup_ml
coffee_grams = round(total_water / ratio, 1)

# --- Results ---
st.divider()
st.header("Your Recipe")

col1, col2, col3 = st.columns(3)
col1.metric("Coffee", f"{coffee_grams} g")
col2.metric("Water", f"{total_water} ml")
col3.metric("Water Temp", f"{info['temp']} °C")

st.write(f"**Ratio:** 1:{ratio}")
st.write(f"**Total brew time:** {info['time']}")

if grind_fresh:
    st.success("Freshly ground beans make a noticeable difference. Grind just before brewing.")
else:
    st.warning("Pre-ground coffee loses aroma quickly. Consider grinding fresh next time.")

# --- Method-specific guidance ---
st.subheader("How to Brew")

if method == "Pour Over (V60)":
    st.info("Rinse the filter, then pour in slow circles. Keep the bed level.")
    st.code("bloom 30s → pour 3x → total 2:30", language="text")
elif method == "French Press":
    st.info("Coarse grind. Stir once, then press slowly and evenly.")
    st.code("stir at 0:30 → press at 4:00", language="text")
elif method == "AeroPress":
    st.info("Inverted method gives more control. Press gently for 30 seconds.")
    st.code("add water → stir 10s → press at 1:30", language="text")
elif method == "Chemex":
    st.info("Thick filters mean a cleaner cup. Expect a longer brew.")
    st.code("bloom 40s → 4 pours → total 4:30", language="text")

# --- Brew strength estimate ---
st.subheader("Strength Estimate")

# Rough extraction gauge based on ratio
if ratio >= 16:
    gauge = 0.35
    verdict = "Light and tea-like"
elif ratio >= 14:
    gauge = 0.6
    verdict = "Balanced and sweet"
elif ratio >= 12:
    gauge = 0.8
    verdict = "Rich and bold"
else:
    gauge = 0.95
    verdict = "Very intense"

st.progress(gauge)
st.write(f"Estimated profile: **{verdict}**")

# --- Summary ---
st.divider()
st.write(f"**{method}** with **{beans or 'some beans'}** for **{cups} cup(s)**.")
if extras:
    st.write("Add-ons: " + ", ".join(extras))
if notes:
    st.info(f"Your tasting notes: {notes}")