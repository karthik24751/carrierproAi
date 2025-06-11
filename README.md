# CareerPro AI - Offline Career Assistant

An intelligent, all-in-one career assistant that helps job seekers streamline their application process. This application works 100% offline and provides comprehensive career development tools.

## Features

- **Resume Analysis & Job Matching**
  - Upload resume (PDF/TXT) and job descriptions
  - Automatic skill match scoring using NLP
  - Personalized cover letter generation

- **Mock Interview System**
  - Speech-to-text conversion
  - Real-time answer analysis
  - Keyword relevance scoring
  - Confidence level assessment
  - Instant feedback generation

- **Career Path Recommender**
  - Rule-based job role suggestions
  - Education and skills analysis
  - Interest-based career path mapping
  - Local data processing and storage

## Technical Stack

- **Backend**: Flask
- **NLP Processing**: NLTK, spaCy
- **Machine Learning**: Scikit-learn
- **Document Processing**: PyPDF2, python-docx
- **Speech Recognition**: SpeechRecognition
- **Data Processing**: Pandas, NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/careerpro-ai.git
cd careerpro-ai
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

4. Download required NLTK data:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"
```

5. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
careerpro-ai/
├── app.py                 # Main application entry point
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
├── config.py             # Configuration settings
├── static/              # Static files (CSS, JS, etc.)
├── templates/           # HTML templates
└── modules/            # Core functionality modules
    ├── resume_analyzer.py
    ├── cover_letter.py
    ├── interview.py
    ├── career_recommender.py
    └── utils/
        ├── nlp_utils.py
        └── file_utils.py
```

## Data Privacy

All data processing is done locally on your machine. No data is sent to external servers or APIs.

## License

MIT License - See LICENSE file for details 