import os
import PyPDF2
import json
import traceback
import re


def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error reading PDF file: " + str(e))
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        raise Exception("Unsupported file type. Please upload a PDF or TXT file.")


def get_table_data(quiz_data):
    try:
        # Handle both string and dictionary inputs
        if isinstance(quiz_data, str):
            # convert the quiz from a str to dict
            if(quiz_data.startswith("```json")):
                clean_quiz = re.sub(r"^```json\s*|\s*```$", "", quiz_data.strip())
            else:
                clean_quiz = quiz_data.strip()

            quiz_dict = json.loads(clean_quiz)
        elif isinstance(quiz_data, dict):
            # Already a dictionary
            quiz_dict = quiz_data
        else:
            raise ValueError("Input must be either a JSON string or dictionary")

        quiz_table_data=[]

        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.list():
            mcq = value["question"]
            options=" || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()

                 ]
            )

            correct=value["correct"]
            quiz_table_data.append({"MCQ": mcq,"Choices": options, "Correct": correct})

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return None
