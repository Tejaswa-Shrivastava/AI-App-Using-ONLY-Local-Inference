# Local LLM Writer

A lightweight web application that generates various types of content using a locally running Large Language Model (LLM). The app provides an easy-to-use interface for generating blog intros, tweets, stories, and more, all while running entirely on your local machine.

## App Type
- **Type**: Web Application
- **Framework**: FastAPI (Backend) + HTML/CSS/JavaScript (Frontend)
- **Deployment**: Local development server

## Model Used
- **Default Model**: `tinyllama`
- **API Compatibility**: OpenAI-compatible API (works with any local LLM server that supports the OpenAI API format)
- **Tested With**: Ollama, but should work with any compatible local LLM server

## Features
- Generate different types of content (blog intros, tweets, stories, etc.)
- Adjust creativity with temperature control
- Clean, responsive UI
- Copy generated content to clipboard
- Automatic logging of all generations

## Prerequisites

1. **Python 3.8+**
2. **Local LLM Server** (e.g., Ollama, llama.cpp, etc.)
   - The app expects the LLM server to be running at `http://localhost:1234`
   - The default model is set to `tinyllama`

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Local LLM Server

Make sure you have a local LLM server running. For example, with Ollama:

```bash
# Install Ollama (if not already installed)
# See: https://ollama.ai/

# Pull the model
ollama pull tinyllama

# Start the server
ollama serve
```

### 5. Configure the Application (Optional)

By default, the app looks for the LLM server at `http://localhost:1234`. If your setup is different, modify the `LOCAL_LLM_URL` in `app.py`.

## How to Run the App

1. Make sure your local LLM server is running
2. Start the application:

```bash
# From the project directory
python app.py
```

3. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

4. Use the interface to:
   - Enter a topic
   - Select a writing style
   - Adjust the temperature (creativity)
   - Click "Generate"



### Changing the Model

To use a different model:
1. Make sure the model is available in your local LLM server
2. Update the `DEFAULT_MODEL` variable in `app.py`
3. Or select the model from the UI (if implemented)

## Troubleshooting

- **Connection refused errors**: Ensure your local LLM server is running and accessible at the specified URL
- **Slow responses**: Generation speed depends on your local hardware and the size of the LLM model
- **Blank output**: Check the application logs for any error messages

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Note: This application requires a locally running LLM server. Make sure you have the necessary hardware resources to run the model you choose.*
