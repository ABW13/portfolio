import streamlit as st
import time

st.set_page_config(page_title="AI Assistant", page_icon="🧠", layout="centered")

# --- Session state init ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Sidebar: context controls ---
with st.sidebar:
    st.title("⚙️ Assistant Settings")

    api_key = st.text_input("API Key (optional)", type="password",
                            placeholder="sk-... — leave blank for mock mode")

    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"])

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful AI assistant for students learning AI engineering.",
        help="Sets the assistant's personality and base behavior."
    )

    st.subheader("Context Areas")
    st.caption("Checked areas are appended to the system prompt.")

    include_python = st.checkbox("Include Python expertise")
    include_web = st.checkbox("Include web development context")
    include_ai = st.checkbox("Include AI/ML context")

    st.divider()
    st.metric("Messages", len(st.session_state["messages"]))

    if st.button("🗑️ Clear Chat"):
        st.session_state["messages"] = []
        st.rerun()


# --- Build context list and the full system prompt ---
context_map = {
    "Python": include_python,
    "web development": include_web,
    "AI/ML": include_ai,
}
contexts = [name for name, checked in context_map.items() if checked]

context_block = ""
if contexts:
    context_block = (
        "\n\nYou have deep expertise in the following areas: "
        + ", ".join(contexts)
        + ". Lean on this expertise when answering."
    )

full_system_prompt = system_prompt + context_block

use_real_api = bool(api_key) and len(api_key) > 10


# --- Mock response generator ---
def mock_response(prompt, contexts):
    context_str = ", ".join(contexts) if contexts else "general knowledge"
    response = (
        f"Based on my {context_str} expertise, here's my take on "
        f"'{prompt[:40]}': [This would be a real AI response in production. "
        f"The system prompt and {len(contexts)} context areas would shape "
        f"how the AI responds.]"
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.03)


# --- Real API call ---
def real_response(messages, api_key, model, system_prompt):
    import openai  # imported here so the app runs without openai installed
    client = openai.OpenAI(api_key=api_key)
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}] + messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# --- Main chat interface ---
st.title("🧠 AI Assistant")

if use_real_api:
    st.caption("Using the real API.")
else:
    st.caption("Mock mode — no API key set.")

# Re-render the whole conversation on every run
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# New input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if use_real_api:
                try:
                    response = st.write_stream(
                        real_response(st.session_state["messages"], api_key, model, full_system_prompt)
                    )
                except Exception as e:
                    response = f"API Error: {e}"
                    st.error(response)
            else:
                response = st.write_stream(mock_response(prompt, contexts))

    st.session_state["messages"].append({"role": "assistant", "content": response})