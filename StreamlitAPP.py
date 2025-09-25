import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data # E:\genAI\mcq_project\src\mcqgenerator\utils.py
import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain #
from src.mcqgenerator.logger import logging
import google.generativeai as genai
from contextlib import contextmanager

with open('E:\genAI\mcq_project\Response.json','r') as file:
    RESPONSE_JSON = file.read()

st.title("MCQ Generator and Evaluator")

class GeminiUsageTracker:
    def __init__(self, model="gemini-2.5-flash"):
        self.model = model
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.total_cost = 0.0

    def add_usage(self, usage_metadata):
        pricing = {
            "gemini-2.5-flash": {"input": 0.075/1e6, "output": 0.30/1e6},
            "gemini-2.5-pro": {"input": 1.25/1e6, "output": 5.00/1e6},
        }
        self.prompt_tokens += usage_metadata.prompt_token_count
        self.completion_tokens += usage_metadata.candidates_token_count
        self.total_tokens += usage_metadata.total_token_count

        self.total_cost += (
            usage_metadata.prompt_token_count * pricing[self.model]["input"]
            + usage_metadata.candidates_token_count * pricing[self.model]["output"]
        )

@contextmanager
def get_gemini_callback(model="gemini-2.5-flash"):
    tracker = GeminiUsageTracker(model=model)
    yield tracker
    print("\n--- Gemini Usage Summary ---")
    print("Prompt tokens:", tracker.prompt_tokens)
    print("Completion tokens:", tracker.completion_tokens)
    print("Total tokens:", tracker.total_tokens)
    print(f"Estimated cost: ${tracker.total_cost:.6f}")







# from 

with st.form("user_inputs"):
    # file upload 
    uploaded_file = st.file_uploader("Choose a file")

    # Input fields
    mcq_count = st.number_input("Number of MCQs", min_value=3, max_value=20)

    #subject
    subject = st.text_input("Subject", max_chars=20)

    # Quiz Tone
    tone = st.text_input("Quiz Tone", max_chars=20, placeholder="Simple")

    # Add Button 
    button = st.form_submit_button("Generate and Evaluate MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating and Evaluating MCQs..."):
            try:
                text = read_file(uploaded_file)
                #Count token and the cost of API call
                with get_gemini_callback(model="gemini-2.5-flash") as cd:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
            except Exception as e:
                traceback.print_exception(type(e), e,e.__traceback__)
                st.error(f"An error occurred: {e}")
            else:
                print(f"total tokens:")
                if isinstance(response, dict):
                    quiz = response.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            #Display the review in a text box as well 
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)



