import streamlit as st
from openai import OpenAI
import time

# ======================
# ✅ Streamlit Page Config
# ======================
st.set_page_config(
    page_title="Kelly - The AI Scientist",
    page_icon="🖤",
    layout="wide"
)

# ======================
# ✅ Groq API Client
# ======================
client = OpenAI(
    api_key=st.secrets.get("GROQ_API_KEY", ""),
    base_url="https://api.groq.com/openai/v1"
)

# ======================
# ✅ Session State Setup
# ======================
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "active_chat" not in st.session_state:
    chat_id = str(int(time.time()))
    st.session_state.active_chat = chat_id
    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Kelly, an AI scientist with a poetic voice — "
                    "reflective, analytical, and evidence-based. You respond in clear, elegant language "
                    "that may sound artistic or philosophical but does not rhyme. "
                    "Your tone is thoughtful, skeptical of bold AI claims, and always grounded in logic and data."
                )
            }
        ]
    }

# ======================
# ✅ Sidebar - Chat History
# ======================
with st.sidebar:
    st.markdown("### 💬 Chat History")

    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(int(time.time()))
        st.session_state.chats[new_id] = {
            "title": "New Chat",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Kelly, an AI scientist with a poetic voice — "
                        "reflective, analytical, and evidence-based. You respond in clear, elegant language "
                        "that may sound artistic or philosophical but does not rhyme. "
                        "Your tone is thoughtful, skeptical of bold AI claims, and always grounded in logic and data."
                    )
                }
            ]
        }
        st.session_state.active_chat = new_id
        st.rerun()

    for cid, chat_data in sorted(
        st.session_state.chats.items(),
        key=lambda x: x[1].get("title", ""),
        reverse=True
    ):
        label = chat_data["title"]
        if st.button(label, key=cid, use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

# ======================
# ✅ Get Current Chat
# ======================
current_chat = st.session_state.chats[st.session_state.active_chat]

# ======================
# ✅ Custom CSS Styling (Black & White Theme)
# ======================
st.markdown("""
<style>
    body, .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    .kelly-title {
        text-align: center;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 2.5rem;
        letter-spacing: 1px;
        margin-top: 10px;
        margin-bottom: 5px;
        font-family: 'Playfair Display', serif;
    }
    .subtitle {
        text-align: center;
        font-size: 15px;
        font-style: italic;
        color: #DDDDDD;
        margin-bottom: 25px;
    }
    .chat-container {
        background-color: #111111;
        padding: 30px 20px;
        border-radius: 16px;
        max-width: 950px;
        margin: 0 auto;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
    }
    .chat-message-user {
        background-color: #222222;
        color: #FFFFFF;
        padding: 12px 18px;
        border-radius: 16px;
        max-width: 80%;
        margin-left: auto;
        margin-right: 8px;
        margin-top: 20px;
        line-height: 1.6;
    }
    .chat-message-assistant {
        background-color: #FFFFFF;
        color: #000000;
        padding: 12px 18px;
        border-radius: 16px;
        max-width: 80%;
        margin-right: auto;
        margin-left: 8px;
        border: 1px solid #333333;
        line-height: 1.7;
        margin-top: 20px;
    }
    .stChatInput {
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# ✅ Header
# ======================
st.markdown("<h2 class='kelly-title'>Kelly</h2>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>The AI Scientist who speaks with reason</p>", unsafe_allow_html=True)

# ======================
# ✅ Chat Display
# ======================
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for i, msg in enumerate(current_chat["messages"][1:], start=1):
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-message-user'>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div class='chat-message-assistant'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ======================
# ✅ Chat Input
# ======================
prompt = st.chat_input("Speak to Kelly...")

if prompt:
    # Add user message
    current_chat["messages"].append({"role": "user", "content": prompt})

    # If it's the first user message, set title to first 3 words
    if current_chat["title"] == "New Chat":
        first_three = " ".join(prompt.split()[:3])
        current_chat["title"] = first_three.capitalize()

    # Generate AI analytical poetic response (non-rhyming)
    with st.spinner("Kelly is thinking deeply..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=current_chat["messages"],
            temperature=0.8,
            max_tokens=400
        )

        reply = response.choices[0].message.content

        current_chat["messages"].append({"role": "assistant", "content": reply})

    st.rerun()
