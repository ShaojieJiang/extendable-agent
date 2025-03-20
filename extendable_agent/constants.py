"""Constants."""

import streamlit as st


PAGES = [
    st.Page("extendable_agent/app/chatbot.py", title="Chatbot", icon="🤖"),
    st.Page("extendable_agent/app/extension.py", title="Extension", icon="🔧"),
]
GITHUB_REPO = "AI-Colleagues/tools-hub"
GITHUB_DIR = "tools"
GITHUB_TOKEN = st.secrets["api_keys"]["TOOLS_HUB_TOKEN"]
