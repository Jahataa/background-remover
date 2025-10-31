# Vectorizer Auth Project

A Python script to interact with the Vectorizer.ai API for image vectorization.

## Setup

1. **Clone the repository**
   ```bash
   git clone your-repo-url
   cd auth
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API credentials
   ```

5. **Add your API credentials to .env**
   ```
   VECTORIZER_API_KEY=your_actual_api_key
   VECTORIZER_SECRET=your_actual_secret
   ```

6. **Run the script**
   ```bash
   python auth.py
   ```

## Security Notes

- Never commit your `.env` file to Git
- Keep your API keys secure and private
- The `.env.example` file shows the required variables without exposing secrets

## Dependencies

- `requests` - HTTP library for API calls
- `python-dotenv` - Load environment variables from .env file