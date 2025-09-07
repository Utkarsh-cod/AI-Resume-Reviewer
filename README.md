# AI Resume Reviewer 📄✨

This project was built for the [Name of Hackathon]. It is an AI-powered application that provides instant, expert-level feedback on resumes to help job seekers tailor their applications for specific roles.

## Features
- **PDF Resume Parsing:** Upload your resume in the most common format.
- **AI-Powered Analysis:** Leverages Google's Gemini 1.5 Flash model for state-of-the-art text analysis.
- **Targeted Feedback:** Analyzes resumes against a specific job title and description.
- **Comprehensive Reporting:** Provides an overall score, keyword analysis, strengths, areas for improvement, and a suggested rewrite for an impactful bullet point.

## Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **AI Model:** Google Gemini 1.5 Flash
- **PDF Parsing:** PyMuPDF
- **Version Control:** Git & GitHub

## How to Run
1. Clone the repository: `git clone [your-repo-url]`
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Add your Gemini API key to `.streamlit/secrets.toml`.
5. Run the app: `streamlit run main.py`
