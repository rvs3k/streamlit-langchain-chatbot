# ⚡ Streamlit x LangChain Chatbot

A modern, responsive chatbot built with Streamlit and LangChain, powered by Google's Gemini AI models. Features real-time streaming responses, multiple model selection, and a clean, professional interface.

![Chatbot Demo](https://img.shields.io/badge/Status-Live-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## 🌟 Features

- **🤖 Multiple AI Models**: Support for 40+ Google Gemini models (Gemini 1.5, 2.0, 2.5, and experimental)
- **💬 Streaming Responses**: Real-time token streaming for smooth interaction
- **🔐 API Key Management**: Secure per-session key entry via sidebar
- **🎨 Clean UI**: Modern chat interface with avatars + dark/light theme toggle
- **📊 Chat Stats**: Track messages in current session
- **⚡ Optimized**: Smart caching with st.cache_resource and st.cache_data
- **📱 Mobile Friendly**: Works well on different devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/streamlit-langchain-chatbot.git
cd streamlit-langchain-chatbot
```

2. **Create virtual environment & install dependencies**

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. **Run the application**

```bash
streamlit run app.py
```

4. **Open in browser**
   - The app will automatically open in your default browser
   - Or navigate to `http://localhost:8501`

## 📦 Dependencies

Create a `requirements.txt` file with these dependencies:

```
streamlit>=1.28.0
langchain-core>=0.1.0
langchain-google-genai>=1.0.0
python-dotenv>=1.0.0
```

## 🔧 Configuration

### API Key Setup

You can provide your Google Gemini API key in two ways:

1. **Through the UI** (Recommended for security):

   - Enter your API key in the sidebar when you run the app
   - The key is stored only in your browser session

2. **Environment Variable**:
   - Create a `.env` file in the project root
   - Add: `GOOGLE_API_KEY=your_api_key_here`

### Model Selection

Choose from 40+ available models including:

- **Gemini 2.0 Flash** - Latest and fastest
- **Gemini 2.5 Pro** - Most capable for complex tasks
- **Gemini 1.5 Flash** - Good balance of speed and quality
- **Experimental models** - Cutting-edge features

## 🎯 Usage

1. **Start the app** and enter your Google Gemini API key
2. **Select a model** from the dropdown in the sidebar
3. **Start chatting** - type your message and press Enter
4. **Watch responses stream** in real-time
5. **Use chat controls**:
   - Clear chat history
   - Switch between models mid-conversation

## 🏗️ Project Structure

```
streamlit-langchain-chatbot/
│
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project metadata (uv/PEP 621)
├── uv.lock                 # uv lockfile (auto-generated)
├── .gitignore              # Git ignore file
├── .python-version         # Python version pin (optional)
├── LICENSE                 # MIT License
├── README.md               # Documentation
├── .env                    # Local env vars (optional, not committed)
└── .venv/                  # Local virtual env (ignored)
```

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set your `GOOGLE_API_KEY` in the secrets management
5. Deploy!

### Other Deployment Options

- **Heroku**: Use the Heroku CLI with a `Procfile`
- **Railway**: Connect your GitHub repo for automatic deployment
- **Replit**: Import from GitHub and run directly
- **Local Network**: Use `streamlit run app.py --server.address 0.0.0.0`

## 🔒 Security Notes

- API keys are handled securely per session
- No conversation data is stored permanently
- Environment variables are used for sensitive configuration
- Input validation prevents malformed requests

## 🛠️ Development

### Local Development Setup

1. **Clone and setup**:

```bash
git clone <your-repo>
cd streamlit-langchain-chatbot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Run in development mode**:

```bash
streamlit run app.py --server.runOnSave true
```

### Adding New Features

The code is modular and easy to extend:

- `configure_page()` - UI and page setup
- `handle_sidebar()` - Sidebar controls and settings
- `display_chat_messages()` - Message rendering
- `handle_user_input()` - Input processing and AI interaction

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [LangChain](https://langchain.com/) for AI integration tools
- [Google AI](https://ai.google/) for the Gemini API
- The open-source community for inspiration and support

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/yourusername/repo/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/yourusername/repo/discussions)
- ❓ **Questions**: Check existing issues or create a new one

## 🔗 Links

- [Live Demo](https://strchatapp.streamlit.app) 
- [Google Gemini API](https://makersuite.google.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)

---

Made with ❤️ by Zohaib Khan
