import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

def configure_page():
    st.set_page_config(
        page_title="Langchain Chat App",
        page_icon="💬",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.title("⚡Streamlit x LangChain Chatbot")
    with st.expander("Check State"):
        st.write(st.session_state)


def handle_sidebar():
    # Per-user API key input
    st.sidebar.subheader("Authentication")
    api_key = st.sidebar.text_input(
        "Your Google Gemini API Key",
        type="password",
        placeholder="GOOGLE_API_KEY",
        help="Your key is kept only in your current browser session.",
        value=st.session_state.get("api_key", ""),
    )
    if api_key:
        st.session_state.api_key = api_key
        if len(api_key) < 20:  # Google API keys are usually longer
            st.sidebar.error("⚠️ This API key looks too short. Please check it.")
        elif not api_key.startswith("AIza"):  # Google keys usually start with this
            st.sidebar.warning("⚠️ This doesn't look like a Google API key. Double-check it.")
        # Set env var for libraries that read from environment
        else:
            os.environ["GOOGLE_API_KEY"] = api_key
            st.sidebar.success("API key set for this session")
    else:
        st.sidebar.info("Enter your API key to start chatting")

    selected_model = st.sidebar.selectbox(
        "Select Model",
        (
            "gemini-1.5-pro-latest",
            "gemini-1.5-pro-002",
            "gemini-1.5-pro",
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash",
            "gemini-1.5-flash-002",
            "gemini-1.5-flash-8b",
            "gemini-1.5-flash-8b-001",
            "gemini-1.5-flash-8b-latest",
            "gemini-2.5-pro-preview-03-25",
            "gemini-2.5-flash-preview-05-20",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite-preview-06-17",
            "gemini-2.5-pro-preview-05-06",
            "gemini-2.5-pro-preview-06-05",
            "gemini-2.5-pro",
            "gemini-2.0-flash-exp",
            "gemini-2.0-flash",
            "gemini-2.0-flash-001",
            "gemini-2.0-flash-exp-image-generation",
            "gemini-2.0-flash-lite-001",
            "gemini-2.0-flash-lite",
            "gemini-2.0-flash-preview-image-generation",
            "gemini-2.0-flash-lite-preview-02-05",
            "gemini-2.0-flash-lite-preview",
            "gemini-2.0-pro-exp",
            "gemini-2.0-pro-exp-02-05",
            "gemini-exp-1206",
            "gemini-2.0-flash-thinking-exp-01-21",
            "gemini-2.0-flash-thinking-exp",
            "gemini-2.0-flash-thinking-exp-1219",
            "gemini-2.5-flash-preview-tts",
            "gemini-2.5-pro-preview-tts",
            "learnlm-2.0-flash-experimental",
            "gemma-3-1b-it",
            "gemma-3-4b-it",
            "gemma-3-12b-it",
            "gemma-3-27b-it",
            "gemma-3n-e4b-it",
            "gemma-3n-e2b-it",
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash-image-preview",
        ),
    )
    st.session_state.model = selected_model
    st.sidebar.divider()

    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.rerun()

    if st.sidebar.button("🗑️Clear Cache"):
        st.cache_data.clear()
        st.cache_resource.clear()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Model Information")
    st.sidebar.write(f"Current Model: {selected_model}")
    
    return selected_model, st.session_state.get("api_key")


@st.cache_resource()
def get_chat_model(model_name: str, api_key_keyed_for_cache: str | None):
    # api_key_keyed_for_cache is unused except for cache key isolation across different keys
    return ChatGoogleGenerativeAI(model=model_name)


def display_chat_messages():
    for message in st.session_state.messages[1:]:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)

        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)


def handle_user_input(chat_model, input_disabled: bool = False):
    if prompt := st.chat_input("What would you like to know?", disabled=input_disabled):
        st.session_state.messages.append(HumanMessage(content=prompt))

        with st.chat_message("user"):
            if prompt and prompt.strip():
                st.write(prompt)
            elif prompt == "":
                st.warning("Please type a message before sending!")

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in chat_model.stream(st.session_state.messages):
                        if chunk.content:
                            full_response += chunk.content
                            message_placeholder.markdown(full_response + "")

                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append(AIMessage(content=full_response))
                except Exception as e:
                    st.error("Please check your API key and try again.")


configure_page()

selected_model, user_api_key = handle_sidebar()

# Initialize chat model only when API key is present
chat_model = None
if user_api_key:
    # Ensure env var is set for the underlying client
    os.environ["GOOGLE_API_KEY"] = user_api_key
    chat_model = get_chat_model(selected_model, user_api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="You are a helpful assistant.")]

# Show messages regardless; input is disabled until key present
display_chat_messages()

if chat_model is None:
    st.warning(
        "Please enter your Google Gemini API key in the sidebar to start chatting."
    )

handle_user_input(chat_model, input_disabled=(chat_model is None))
