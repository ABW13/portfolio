import streamlit as st

# --- Page Config (MUST be first Streamlit command) ---
st.set_page_config(
    page_title="Reading Tracker",
    page_icon="📚",
    layout="wide"
)

# --- Hardcoded data ---
books = [
    {"Title": "Dune", "Author": "Frank Herbert", "Pages": 412, "Status": "Finished", "Genre": "Sci-Fi", "Rating": 5},
    {"Title": "1984", "Author": "George Orwell", "Pages": 328, "Status": "Finished", "Genre": "Sci-Fi", "Rating": 4},
    {"Title": "The Great Gatsby", "Author": "F. Scott Fitzgerald", "Pages": 180, "Status": "Finished", "Genre": "Classic", "Rating": 4},
    {"Title": "Educated", "Author": "Tara Westover", "Pages": 334, "Status": "Reading", "Genre": "Memoir", "Rating": None},
    {"Title": "Project Hail Mary", "Author": "Andy Weir", "Pages": 476, "Status": "Reading", "Genre": "Sci-Fi", "Rating": None},
    {"Title": "Sapiens", "Author": "Yuval Noah Harari", "Pages": 443, "Status": "To Read", "Genre": "History", "Rating": None},
    {"Title": "Atomic Habits", "Author": "James Clear", "Pages": 320, "Status": "To Read", "Genre": "Self-Help", "Rating": None},
]

GOAL_YEAR = 24  # Books to finish this year in this tracker
page_goal = 6000

# --- Sidebar controls ---
with st.sidebar:
    st.title("⚙️ Controls")

    genre_filter = st.selectbox(
        "Genre filter",
        ["All"] + sorted({b["Genre"] for b in books})
    )

    min_pages = st.slider("Minimum pages", 0, 500, 0, step=50)

    sort_by = st.radio(
        "Sort by",
        ["Title", "Pages", "Rating"]
    )

    show_unrated = st.checkbox("Include unrated books", value=True)

    st.divider()
    st.caption(f"Filtering: {genre_filter} | {min_pages}+ pages")

# --- Apply the sidebar filters ---
filtered = [
    b for b in books
    if (genre_filter == "All" or b["Genre"] == genre_filter)
    and b["Pages"] >= min_pages
    and (show_unrated or b["Rating"] is not None)
]

# Sort: books with no rating sink to the bottom when sorting by rating
if sort_by == "Title":
    filtered.sort(key=lambda b: b["Title"])
elif sort_by == "Pages":
    filtered.sort(key=lambda b: b["Pages"], reverse=True)
else:
    filtered.sort(key=lambda b: (b["Rating"] is None, -(b["Rating"] or 0)))

# --- Calculations ---
finished = [b for b in books if b["Status"] == "Finished"]
reading = [b for b in books if b["Status"] == "Reading"]
to_read = [b for b in books if b["Status"] == "To Read"]
pages_read = sum(b["Pages"] for b in finished)
rated = [b["Rating"] for b in books if b["Rating"] is not None]
avg_rating = round(sum(rated) / len(rated), 2) if rated else 0

# --- Main content ---
st.title("📚 Reading Tracker")
st.write(f"Tracking **{len(books)}** books across **{len({b['Genre'] for b in books})}** genres.")

# --- Metrics row ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Books Finished", len(finished), f"+{len(finished)}")
with col2:
    st.metric("Pages Read", f"{pages_read:,}", f"+{pages_read // 4} this week")
with col3:
    st.metric("Currently Reading", len(reading), f"{len(to_read)} queued")
with col4:
    st.metric("Avg Rating", f"{avg_rating} / 5", "+0.2")

st.divider()

# --- Tabs ---
tab_overview, tab_details = st.tabs(["📈 Overview", "🔍 Details"])

with tab_overview:
    st.subheader("Progress Toward Goal")
    book_progress = len(finished) / GOAL_YEAR
    st.progress(book_progress)
    st.write(f"**{len(finished)}** of **{GOAL_YEAR}** books finished this year.")

    page_progress = pages_read / page_goal
    st.progress(page_progress)
    st.write(f"**{pages_read:,}** of **{page_goal:,}** pages read.")

    if page_progress >= 0.5:
        st.success("Over halfway to your page goal. Nice pace.")
    else:
        st.warning("Behind the halfway mark. A few short sessions would close the gap.")

    with st.expander("💡 How these numbers are calculated"):
        st.write(
            "Books Finished counts entries marked **Finished**. Pages Read adds up "
            "the page counts of those books only, so books in progress don't inflate "
            "the total. The goal is a fixed yearly target stored in this file."
        )

    st.subheader("Pages by Genre")
    genre_pages = {}
    for b in finished:
        genre_pages[b["Genre"]] = genre_pages.get(b["Genre"], 0) + b["Pages"]
    st.bar_chart(genre_pages)

with tab_details:
    st.subheader(f"Book List ({len(filtered)} shown)")
    st.dataframe(filtered, use_container_width=True)

    st.subheader("Status Breakdown")
    status_counts = {"Finished": len(finished), "Reading": len(reading), "To Read": len(to_read)}
    st.bar_chart(status_counts)

    if not filtered:
        st.info("No books match the current filters. Widen the sidebar controls to see more.")