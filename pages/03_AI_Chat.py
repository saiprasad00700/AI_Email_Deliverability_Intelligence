import streamlit as st
import ollama

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Chat",
    page_icon="💬",
    layout="wide"
)

st.title("💬 AI Deliverability Chat Support")
st.caption("Ask questions about Email Deliverability, Python, SQL, Machine Learning, or general technical topics.")

st.divider()

# =====================================================
# CHAT HISTORY
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """# 👋 Welcome!

I'm your **Local AI Assistant** powered by **Llama 3.2**.

### You can ask me about:

- 📧 Email Deliverability
- 🛡️ SPF, DKIM & DMARC
- 📊 SQL & Database queries
- 🐍 Python programming
- 🤖 Machine Learning & AI
- 📈 Campaign Analytics
- 💡 General technical questions

**👇 Type your question in the chat box below.**
"""
        }
    ]

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

prompt = st.chat_input("✍️ Ask your question here...")

if prompt:

    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant reply
    with st.chat_message("assistant"):

        with st.spinner("🧠 Thinking..."):

            try:

                response = ollama.chat(
                    model="llama3.2:3b",
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are a helpful AI assistant.

Guidelines:
- Answer in clear, simple English.
- Be accurate and practical.
- Use bullet points whenever useful.
- Keep answers concise unless the user asks for detailed explanation.
- You can answer both email deliverability and general technical questions.
- If the user asks coding questions, provide complete working code.
"""
                        }
                    ] + st.session_state.messages
                )

                answer = response["message"]["content"]

            except Exception as e:

                answer = f"""
❌ **Ollama Connection Error**

Make sure:
1. Ollama is installed.
2. `llama3.2:3b` is downloaded.
3. Ollama service is running.

**Error:** `{e}`
"""

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )