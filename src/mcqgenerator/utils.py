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
    
def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        if(quiz_str.startswith("```json")):
            clean_quiz = re.sub(r"^```json\s*|\s*```$", "", quiz_str.strip())
        else:
            clean_quiz = quiz_str.strip()
                   
        quiz_dict=json.loads(clean_quiz)
        quiz_table_data=[]
        
        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq=value["mcq"]
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
        return False