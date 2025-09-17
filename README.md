# MCQ Generator

This project is an AI-powered Multiple Choice Question (MCQ) generator built using LangChain, OpenAI, Google Generative AI, and Streamlit for the web interface.

## Features

- Generate MCQs from text or PDF inputs
- Supports multiple LLM providers (OpenAI GPT, Google Gemini)
- Streamlit web app for easy interaction
- Logging and utility functions

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd mcq_project
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_key
   GOOGLE_API_KEY=your_google_key
   ```

## Usage

Run the Streamlit app:
```
streamlit run StreamlitAPP.py
```

## Project Structure

- `src/mcqgenerator/`: Core MCQ generation logic
- `experiment/`: Experimental notebooks and data
- `StreamlitAPP.py`: Web app interface

## Author

Satendra Sharma (satendra.sharma.ai)


# level of logging 

Level

Numeric value

What it means / When to use it

logging.NOTSET
0

When set on a logger, indicates that ancestor loggers are to be consulted to determine the effective level. If that still resolves to NOTSET, then all events are logged. When set on a handler, all events are handled.

logging.DEBUG
10

Detailed information, typically only of interest to a developer trying to diagnose a problem.

logging.INFO
20

Confirmation that things are working as expected.

logging.WARNING
30

An indication that something unexpected happened, or that a problem might occur in the near future (e.g. ‘disk space low’). The software is still working as expected.

logging.ERROR
40

Due to a more serious problem, the software has not been able to perform some function.

logging.CRITICAL
50

A serious error, indicating that the program itself may be unable to continue running.