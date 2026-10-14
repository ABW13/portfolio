import streamlit as st

st.set_page_config(page_title="Course Quiz", page_icon="🧠", layout="centered")

# --- Question bank ---
questions = [
    {
        "question": "What does HTML stand for?",
        "options": ["Hyper Text Markup Language", "High Tech Modern Language",
                    "Hyper Transfer Markup Language", "Home Tool Markup Language"],
        "answer": 0
    },
    {
        "question": "Which CSS property controls the space INSIDE an element's border?",
        "options": ["margin", "padding", "border", "gap"],
        "answer": 1
    },
    {
        "question": "Which event fires on every keystroke in a text field?",
        "options": ["change", "click", "input", "keyup"],
        "answer": 2
    },
    {
        "question": "Does fetch() throw an error on a 404 response?",
        "options": ["Yes, it always throws", "No, you must check response.ok",
                    "Only for POST requests", "Only if CORS is enabled"],
        "answer": 1
    },
    {
        "question": "What status code does FastAPI return for a wrong request body?",
        "options": ["200", "404", "422", "500"],
        "answer": 2
    },
]

TOTAL = len(questions)

# --- Initialize session state ---
defaults = {
    "current_question": 0,
    "score": 0,
    "answered": False,
    "choice": None,
    "finished": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def reset_quiz():
    """Reset every piece of quiz state back to the start."""
    st.session_state["current_question"] = 0
    st.session_state["score"] = 0
    st.session_state["answered"] = False
    st.session_state["choice"] = None
    st.session_state["finished"] = False

# --- Header and progress ---
st.title("🧠 Course Quiz")
st.write("Five questions on HTML, CSS, JavaScript, Python, and APIs.")

# --- Results screen ---
if st.session_state["finished"]:
    final = st.session_state["score"]
    pct = round(final / TOTAL * 100)

    st.header("🎉 Quiz Complete")
    st.metric("Your Score", f"{final} / {TOTAL}", f"{pct}%")

    if pct == 100:
        st.balloons()
        st.success("Perfect score. Every answer correct.")
    elif pct >= 60:
        st.success(f"Nice work. You got {final} of {TOTAL} right.")
    else:
        st.warning(f"You scored {final} of {TOTAL}. Worth a review of the earlier lessons.")

    with st.expander("📋 Answer key"):
        for i, q in enumerate(questions):
            st.write(f"**{i + 1}. {q['question']}**")
            st.write(f"Correct answer: {q['options'][q['answer']]}")

    if st.button("🔄 Restart Quiz"):
        reset_quiz()
        st.rerun()

else:
    # --- Current question ---
    idx = st.session_state["current_question"]
    q = questions[idx]

    st.progress((idx) / TOTAL)
    st.caption(f"Question {idx + 1} of {TOTAL}  —  Score: {st.session_state['score']}")

    st.subheader(q["question"])

    # Radio for the answer. Disabled once answered so the choice locks in.
    choice = st.radio(
        "Select your answer:",
        options=list(range(len(q["options"]))),
        format_func=lambda i: q["options"][i],
        index=None,
        key=f"radio_{idx}",
        disabled=st.session_state["answered"],
    )

    if not st.session_state["answered"]:
        if st.button("Submit Answer"):
            if choice is None:
                st.warning("Pick an answer first.")
            else:
                st.session_state["choice"] = choice
                st.session_state["answered"] = True
                if choice == q["answer"]:
                    st.session_state["score"] += 1
                st.rerun()
    else:
        # Feedback for the question just answered
        correct_index = q["answer"]
        if st.session_state["choice"] == correct_index:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Not quite. The correct answer is: **{q['options'][correct_index]}**")

        st.divider()
        if idx + 1 < TOTAL:
            if st.button("Next Question ➡️"):
                st.session_state["current_question"] += 1
                st.session_state["answered"] = False
                st.session_state["choice"] = None
                st.rerun()
        else:
            if st.button("See Results 🏁"):
                st.session_state["finished"] = True
                st.rerun()