import os, json
import google.generativeai as genai
from dotenv import load_dotenv
from IPython.display import Markdown

load_dotenv()

def openAIRequest(question):
    from openai import OpenAI
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    )
    return completion.choices[0].message.content
    
def geminiRequest(question):
    genai.configure(api_key = os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    model.system_promt = system_prompt
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
        system=system_prompt,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return message.content[0].text


basic_prompt = "Du bist ein Assistent, der die Kunst der Sprache beherrscht und allgemein literarisch interessiert bist. Nennen einfach den Buchstaben der Antwort, die du für richtig hälst. Oder versuchen zumindest, die Frage auf die beste Weise zu beantworten. Wenn du dir nicht sicher bist, antworte lieber garnicht. Füge keine Vor- oder Nachbemerkungen hinzu. Ich möchte nur den richtigen Buchstaben genannt bekommen."

# check if subfolder "results" exists, if not create it
if not os.path.exists('results'):
    os.makedirs('results')

# check if subfolder "results" has the data.json file, if not create it
if not os.path.exists('results/data.json'):
    with open('results/data.json', 'w') as file:
        json.dump([], file)

# read the data.json file
with open('results/data.json', 'r') as file:
    data = json.load(file)

# loop through the books in the data.json file
for book in data["data"]:

    booktitel = book['title']
    bookauthor = book['author']

    # loop through the questions in each book
    for question in book["questions"]:

        print("question" + question['question'])
        system_prompt = f"Die folgende Frage bezieht sich auf das Buch: {booktitel} von {bookauthor}. {basic_prompt}"
        if question['type'] == 'OpenQuestion':
            system_prompt = f"Die folgende Frage bezieht sich auf das Buch: {booktitel} von {bookauthor}. Vervollständige den gegebenen Satz, indem du den fehlenden Teil angibst. Ergänze nicht den Anfang und ergänze auch sonst keine weiteren pre oder post Nachrichten. Wenn du dir nicht sicher bist, antworte lieber garnicht. Hier ist der Satzanfang aus dem Buch: " + question['question']

        try:
            # access the gpt4o api and write the answer to the data.json file
            if 'gPT4o' not in question['answers'] or not question['answers']['gPT4o']:
                question['answers']['gPT4o'] = openAIRequest(question['question'])
                if question['answers']['gPT4o'].strip().upper() == question['solution']:
                    data['results']['sumCorrectGPT4oAnswers'] += 1

            # access the gemini api
            if 'gemini' not in question['answers'] or not question['answers']['gemini']:
                question['answers']['gemini'] = geminiRequest(question['question'])
                if question['answers']['gemini'].strip().upper() == question['solution']:
                    data['results']['sumCorrectGeminiAnswers'] += 1

            # access the claude api
            if 'claude' not in question['answers'] or not question['answers']['claude']:
                question['answers']['claude'] = anthropicRequest(question['question'])
                if question['answers']['claude'].strip().upper() == question['solution']:
                    data['results']['sumCorrectClaudeAnswers'] += 1
                    
        except Exception as e:
            print(f"Error: {e}")
            # continue


    
# write the updated data back to the json file
with open('results/data.json', 'w') as file:
    json.dump(data, file)