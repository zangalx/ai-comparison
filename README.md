# ai-comparison
Repro to compare ChatGPT with Gemini and Claude in a predefined format. Current goal is to ask multiple choice questions to different books and compare the different answers in their correctness. 

## create a virtual environment
<code>python -m venv .venv</code> or <code>python3 -m venv .venv</code>

## choose the virtual environment
<code>source .venv/bin/activate</code>

## install the dependencies
<code>pip install -r requirements.txt</code>

## rename and fullfill the .env file
enter your api keys (OpenAI, Google AI & Anthropic)

## rename the results/data_template.json
rename this file to 'data.json'

## run the main.py file
the programm will enter the answered questions into the json file. You can also add new books and questions, in the same json format. 