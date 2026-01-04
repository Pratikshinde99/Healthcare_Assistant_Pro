# Deployment Guide for Healthcare Assistant Pro

This guide provides instructions for deploying the Healthcare Assistant Pro application to various platforms.

## Prerequisites

- Python 3.10+
- Git
- API keys for at least one AI provider (optional but recommended for full functionality)

## Deployment Options

### 1. Local Deployment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd healthcare-assistant-pro
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   # Edit .env to add your API keys
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

### 2. Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t healthcare-assistant .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 -e GROQ_API_KEY=your_key_here healthcare-assistant
   ```

### 3. Heroku Deployment

1. Create a Heroku app:
   ```bash
   heroku create your-app-name
   ```

2. Set environment variables:
   ```bash
   heroku config:set GROQ_API_KEY=your_key_here
   heroku config:set OPENAI_API_KEY=your_key_here
   # Add other API keys as needed
   ```

3. Deploy:
   ```bash
   git push heroku main
   ```

### 4. Streamlit Sharing Deployment

1. Connect your GitHub repository to Streamlit Sharing
2. Set environment variables in the Streamlit Sharing dashboard
3. Deploy directly from GitHub

## Environment Variables

The application supports the following environment variables:

- `GROQ_API_KEY` - API key for Groq (Llama-3.1-70B)
- `OPENAI_API_KEY` - API key for OpenAI (GPT-4o-mini)
- `ANTHROPIC_API_KEY` - API key for Anthropic (Claude 3.5)
- `INFERMEDICA_APP_ID` - App ID for Infermedica API
- `INFERMEDICA_APP_KEY` - App key for Infermedica API

## Important Notes

- The application will work with a local FLAN-T5 model if no API keys are provided, but this will be slower and require more resources
- For production deployments, ensure that sensitive API keys are properly secured
- The application requires internet access to download the FLAN-T5 model if not already cached
- Consider using a CDN or caching layer for production deployments to improve performance

## Troubleshooting

- If you encounter memory issues, consider using a smaller model or providing API keys for cloud-based AI services
- If the application fails to start, check that all required dependencies are installed
- For API-related issues, verify that your API keys are correct and have sufficient quota