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
    # with st.expander("Check State"):
    #     st.write(st.session_state)


def handle_sidebar():

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
    # Per-user API key input
    st.sidebar.subheader("🔐 Authentication")
    api_key = st.sidebar.text_input(
        "Your Google Gemini API Key",
        type="password",
        placeholder="Enter your API key...",
        help="Your key is kept only in your current browser session.",
        value=st.session_state.get("api_key", ""),
    )

    if api_key:
        st.session_state.api_key = api_key
        if len(api_key) < 20:
            st.sidebar.error("⚠️ This API key looks too short. Please check it.")
        elif not api_key.startswith("AIza"):
            st.sidebar.warning(
                "⚠️ This doesn't look like a Google API key. Double-check it."
            )
        else:
            os.environ["GOOGLE_API_KEY"] = api_key
            st.sidebar.success("✅ API key set for this session")
    else:
        st.sidebar.info("💡 Enter your API key to start chatting")

    st.sidebar.divider()

    # Model Selection with categories
    st.sidebar.subheader("🤖 Model Selection")

    # Get model lists
    reliable_models = get_reliable_models()
    experimental_models = get_experimental_models()
    specialized_models = get_specialized_models()

    # Default to reliable models
    selected_model = st.sidebar.selectbox(
        "🎯 Recommended Models:",
        reliable_models,
        index=0,  # Default to first reliable model
        help="These models are stable and work consistently",
    )

    # Advanced options in expander
    with st.sidebar.expander("⚙️ Advanced Model Options"):
        model_category = st.radio(
            "Model Category:",
            ["🎯 Recommended", "🧪 Experimental", "⚡ Specialized"],
            help="Choose model category based on your needs",
        )

        if model_category == "🧪 Experimental":
            st.warning("⚠️ These models might be unstable or unavailable")
            experimental_choice = st.selectbox(
                "Experimental models:",
                experimental_models,
                help="Preview/experimental models - use at your own risk",
            )
            selected_model = experimental_choice
            st.error(f"🧪 Using experimental model: {experimental_choice}")

        elif model_category == "⚡ Specialized":
            st.info("ℹ️ Specialized models for specific use cases")
            specialized_choice = st.selectbox(
                "Specialized models:",
                specialized_models,
                help="Lightweight or specialized models",
            )
            selected_model = specialized_choice
            st.info(f"⚡ Using specialized model: {specialized_choice}")

    # Store selected model
    st.session_state.model = selected_model

    st.sidebar.divider()

    # Chat controls
    st.sidebar.subheader("💬 Chat Controls")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [
                SystemMessage(content="You are a helpful assistant.")
            ]
            st.rerun()

    with col2:
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("Cache cleared!")

    # Session info
    st.sidebar.divider()
    st.sidebar.subheader("📊 Session Info")

    # Message count
    message_count = len(st.session_state.messages) - 1  # Exclude system message
    st.sidebar.metric("Messages", message_count)

    # Current model info
    st.sidebar.info(f"**Current Model:**\n{selected_model}")

    # Model status indicator
    if selected_model in reliable_models:
        st.sidebar.success("🟢 Stable Model")
    elif selected_model in experimental_models:
        st.sidebar.warning("🟡 Experimental Model")
    else:
        st.sidebar.info("🔵 Specialized Model")

    # Download chat option
    if message_count > 0:
        st.sidebar.divider()
        chat_text = ""
        for msg in st.session_state.messages[1:]:  # Skip system message
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            chat_text += f"{role}: {msg.content}\n\n"

        st.sidebar.download_button(
            "📥 Download Chat",
            chat_text,
            f"chat_export_{selected_model}.txt",
            "text/plain",
            use_container_width=True,
            help="Download your conversation history",
        )

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
                    import time

                    start_time = time.time()
                    timeout = 30  # 30 seconds timeout

                    for chunk in chat_model.stream(st.session_state.messages):
                        if time.time() - start_time > timeout:
                            st.error(
                                "⏱️ Response timed out. This model might be unavailable. Try selecting a different model."
                            )
                            return

                        if chunk.content:
                            full_response += chunk.content
                            message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)
                    # Only add the message once, and only if there's content
                    if full_response.strip():
                        st.session_state.messages.append(
                            AIMessage(content=full_response)
                        )
                    else:
                        st.error(
                            "🚫 No response received. This model might not be working. Please try a different model."
                        )
                        
                except Exception as e:
                    error_message = str(e).lower()

                    # Specific error messages for different issues
                    if "not found" in error_message or "invalid" in error_message:
                        st.error(
                            "❌ This model is not available or has been deprecated. Please select a different model."
                        )
                    elif "permission" in error_message or "access" in error_message:
                        st.error(
                            "🔒 You don't have access to this model. Please select a different model or check your API permissions."
                        )
                    elif "quota" in error_message or "limit" in error_message:
                        st.error(
                            "📊 API quota exceeded. Please try again later or use a different model."
                        )
                    elif "timeout" in error_message:
                        st.error(
                            "⏱️ Request timed out. This model might be overloaded. Try a different model."
                        )
                    else:
                        st.error(f"❌ Error with this model: {str(e)}")
                        st.error(
                            "💡 **Suggestion**: Try selecting 'gemini-1.5-flash' or 'gemini-1.5-pro' - these are the most reliable models."
                        )

                    # Show recommended models
                    st.info(
                        "🎯 **Recommended models that usually work well:**\n"
                        "- gemini-1.5-flash\n"
                        "- gemini-1.5-pro\n"
                        "- gemini-2.0-flash"
                    )

                st.rerun()
        



def get_reliable_models():
    """Returns a list of models that are known to work reliably"""
    return [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro-latest",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-1.5-flash-002",
        "gemini-1.5-pro-002",
        "gemini-2.0-flash-001",
    ]


def get_experimental_models():
    """Returns experimental/preview models that might be unstable"""
    return [
        "gemini-exp-1206",
        "gemini-2.0-flash-thinking-exp",
        "gemini-2.0-flash-thinking-exp-01-21",
        "gemini-2.0-flash-thinking-exp-1219",
        "gemini-2.0-flash-exp",
        "gemini-2.0-pro-exp",
        "gemini-2.0-pro-exp-02-05",
        "learnlm-2.0-flash-experimental",
        "gemini-2.5-pro-preview-03-25",
        "gemini-2.5-flash-preview-05-20",
        "gemini-2.5-flash-lite-preview-06-17",
        "gemini-2.5-pro-preview-05-06",
        "gemini-2.5-pro-preview-06-05",
        "gemini-2.0-flash-exp-image-generation",
        "gemini-2.0-flash-preview-image-generation",
        "gemini-2.0-flash-lite-preview-02-05",
        "gemini-2.0-flash-lite-preview",
        "gemini-2.5-flash-preview-tts",
        "gemini-2.5-pro-preview-tts",
        "gemini-2.5-flash-image-preview",
    ]


def get_specialized_models():
    """Returns specialized models for specific use cases"""
    return [
        "gemini-1.5-flash-8b",
        "gemini-1.5-flash-8b-001",
        "gemini-1.5-flash-8b-latest",
        "gemini-2.0-flash-lite-001",
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash-lite",
        "gemma-3-1b-it",
        "gemma-3-4b-it",
        "gemma-3-12b-it",
        "gemma-3-27b-it",
        "gemma-3n-e4b-it",
        "gemma-3n-e2b-it",
    ]


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