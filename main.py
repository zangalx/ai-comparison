import os, csv, pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from IPython.display import Markdown

load_dotenv()

def openAIRequest(question):
    from openai import OpenAI
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a assistant, skilled in the art of speech. Use no comma in your answer."},
        {"role": "user", "content": question}
    ]
    )
    return completion.choices[0].message.content
    
def geminiRequest(question):
    genai.configure(api_key = os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    model.system_promt = "You are a assistant, skilled in the art of speech. Use no comma in your answer."
    response = model.generate_content(question)
    Markdown(response.text)
    return response.text

def anthropicRequest(question):
    import anthropic
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.0,
        system="You are a assistant, skilled in the art of speech. Use no comma in your answer.",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    print(message.content)
    return message.content[0].text

#check if subfolder "results" exists, if not create it
if not os.path.exists('results'):
    os.makedirs('results')

#check if subfolder "results" has the data.csv file, if not create it
if not os.path.exists('results/data.csv'):
    with open('results/data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Question", "GPT4o", "Gemini", "Claude"])

#read the data.csv file
df = pd.read_csv('results/data.csv')

#loop through the questions in the data.csv file
for index, row in df.iterrows():
    #print(row['Questions'])

    # access the gpt4o api and write the answer to the data.csv file
    if pd.isna(row['GPT4o']):
        row['GPT4o'] = openAIRequest(row['Question'])
        df['GPT4o'] = df['GPT4o'].astype(object)
        df.at[index, 'GPT4o'] = row['GPT4o']
        df.to_csv('results/data.csv', index=False)

    # access the gemini api
    if pd.isna(row['Gemini']):
        row['Gemini'] = geminiRequest(row['Question'])
        df['Gemini'] = df['Gemini'].astype(object) 
        df.at[index, 'Gemini'] = row['Gemini']
        df.to_csv('results/data.csv', index=False)

    # access the claude api
    if pd.isna(row['Claude']):
        row['Claude'] = anthropicRequest(row['Question'])
        df['Claude'] = df['Claude'].astype(object)
        df.at[index, 'Claude'] = row['Claude']
        df.to_csv('results/data.csv', index=False)
    