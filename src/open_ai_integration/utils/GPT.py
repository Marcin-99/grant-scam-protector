## Commands required to run on server: 
## pip install openai

import openai
# Set API key
openai.api_key = ""


def select_gpt_model(input_text):
    completions = openai.Completion.create(
        engine="text-babbage-001",
        prompt=input_text,
        max_tokens=256,
        n=1,
        stop=None,
        temperature=0.2,

    )
    return completions


def get_gpt_summary(input_text):
    completions = select_gpt_model(input_text)
    return completions.choices[0].text

#Caller: This is Chief Investigator Sharon right Am I speaking with Yes again my name is investigator Sharon right I am investigating a criminal complaint that has been for to hear in the office against you But cash express we are in the process of proceeding against you legally Now prior to for this to your local authorities and returned them it should have warned for your Russ I did want to contact you get a statement and find out exactly what were your intentions But what it wouldnt this Im not understanding what it is Cash express is stating that you did walk into their facility to obtain a payday loan You did give them your personal check and information along with a data to when they can extract the funds to be paid bike for the loan once they went to receive the funds the funds were
