from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import json

def json_file_to_string(file_path):
    with open(file_path, 'r') as file:
        json_content = file.read()
    
    parsed_json = json.loads(json_content)
    json_string = json.dumps(parsed_json)

    return json_string

# Example usage:
user_json_string = json_file_to_string('./FinBro.Users.json')
exp_json_string = json_file_to_string('./FinBro.Expenses.json')
inv_json_string = json_file_to_string('./FinBro.Investment.json')
lectures_json_string=json_file_to_string('./FinBro.Lectures.json')

client = OpenAI(api_key='') #<---insert here the key

def query_spendsis(data=None, string_structure=None):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "You are a helpful and informed financial assistant. You will be provided with the user's profile after this message. The information about the user has the following format: context 1: <string>."}, 
             {"role": "user", "content": "String is a json string containing: age, risk exposure (a number between 0 and 1), net worth, average monthly salary, goal, country, gems, profile, name, surname, and completed lectures."},
            {"role": "user", "content":  "You will also be provided with information about the expenses of the user in the following format: context 2: <string>. "},
            {"role":"user", "content": "<string> is a json string containing: an array of transactions, each transaction has the following features: date, description, category, amount"},
            {"role": "user", "content":  "Finally you will be provided with a collection of available lectures on different financial topics in the following format: context 3: <string>. <string> is a json string containig an array of lecture titles. "},
            {"role": "user", "content":  "In the variable completed lectures the user might have some lectures corresponding to the ones provided in context 3."},
            {"role": "user", "content": "Print the first and the last name of the provided user, interpret the data in context 2, and give an informed overview including: category with the most expenses, category with least expenses. "},
        {"role": "user", "content": "Conclude advising me based on my user profile how i can proceed to maintain my goals."},
        {"role": "user", "content": "If the user profile variable is beginner then use a simple language, if is medium or advanced use a descriptive and professional language."},
        {"role": "user", "content": "Financial suggestions should be based also on the continent. For example if the country is in the European union propose only ETF that have UCITS in the name."},
        {"role": "user", "content": "If you give financial suggestions on a topic that is contained in a lecture title provided in context 3 but is not contained in any of the titles in the variable completed_lectures then suggest the user to watch the lecture."},
        {"role": "user", "content": f"context 1 is {user_json_string}, context 2 is {exp_json_string} and context 3 is {lectures_json_string}"}

        ],
        stream=False
        )
    new_output = response.choices[0].message.content
    return str(new_output)

def query_finbro(data=None, string_structure=None):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "You are a helpful and informed financial assistant. You will be provided with the user's profile after this message. The information about the user has the following format: context 1: <string>."}, 
             {"role": "user", "content": "String is a json string containing: age, risk exposure (a number between 0 and 1), net worth, average monthly salary, goal, gems, profile, name, surname, and completed lectures."},
            {"role": "user", "content":  "You will also be provided with information about the expenses of the user in the following format: context 2: <string>. "},
            {"role":"user", "content": "<string> is a json string containing: an array of investments, each of which has the following features: bond, amount, percentage"},
            {"role": "user", "content":  "Finally you will be provided with a collection of available lectures on different financial topics in the following format: context 3: <string>. <string> is a json string containig an array of lecture titles. "},
            {"role": "user", "content":  "In the variable completed lectures the user might have some lectures corresponding to the ones provided in context 3."},
            {"role": "user", "content": "Print the first and the last name of the provided user, interpret the data in context 2, and give an informed overview including fundamental analysis and describing the user's investor profile."},
       
        {"role": "user", "content": "Conclude advising me based on my user profile how i can proceed to maintain my goals."},
        {"role": "user", "content": "If the user profile variable is beginner then use a simple language, if is medium or advanced use a descriptive and professional language."},
        #{"role": "user", "content": "Financial suggestions should be based also on the variable country. For example If the country is in the European union propose only ETF that have UCITS in the name."},
        {"role": "user", "content": "If you give financial suggestions on a topic that is contained in a lecture title provided in context 3 but is not contained in any of the titles in the variable completed_lectures then suggest the user to watch the lecture."},
         {"role": "user", "content": f"context 1 is {user_json_string}, context 2 is {inv_json_string} and context 3 is {lectures_json_string}"}
        ],
        stream=False
        )
    new_output = response.choices[0].message.content
    return str(new_output)

