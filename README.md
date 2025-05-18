# AI Travel Assistant

An intelligent travel companion that helps users with language translation, sentiment analysis, and travel recommendations.

## Features

- Multi-language Translation using Google Translate API
- Sentiment Analysis for Travel Reviews using BERT
- Common Travel Phrases with categorized sections
- Interactive Language Exercises
- AI Travel Assistant Chat powered by OpenAI

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection (for downloading models on first run)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai_travel_assistant.git
cd ai_travel_assistant
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

5. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
ai_travel_assistant/
├── app.py                 # Main Streamlit application
├── deep_learning.py       # Sentiment analysis and language detection
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
├── pages/                 # Streamlit pages
│   ├── translation.py     # Translation feature
│   ├── phrases.py        # Common phrases
│   ├── exercises.py      # Language exercises
│   ├── reviews.py        # Review analysis
│   └── assistant.py      # AI assistant
└── components/           # Reusable components
    └── sentiment_viz.py  # Sentiment visualization
```

## First Run

On first run, the application will:
1. Download required ML models
2. Create necessary cache directories
3. Initialize Streamlit interface

This may take a few minutes depending on your internet connection.

## Usage

1. **Translation**
   - Supports 100+ languages
   - Real-time translation
   - Common phrase categories

2. **Sentiment Analysis**
   - Analyze travel reviews
   - Get aspect-based sentiment
   - Visualization of results

3. **Language Exercises**
   - Interactive learning
   - Multiple difficulty levels
   - Progress tracking

4. **AI Assistant**
   - Travel recommendations
   - Personalized advice
   - Context-aware responses

## Troubleshooting

1. **ModuleNotFoundError**:
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **API Key Error**:
   - Check `.env` file exists
   - Verify API key is correct
   - No quotes around API key

3. **Model Download Issues**:
   - Check internet connection
   - Clear cache and retry
   - Ensure sufficient disk space

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Note

The models will be downloaded automatically on first run. Make sure you have:
- Stable internet connection
- Sufficient disk space (~500MB for models)
- Valid API keys in `.env` 