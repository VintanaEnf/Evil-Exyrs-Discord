import google.generativeai as palm
import const


import sys
sys.path.append(const.keys_location)
import keys

palm.configure(api_key=keys.PALM)

def talkShort(message: str) -> str:
    response = palm.generate_text(prompt=message)
    return response.result;


def talkLong(message: str) -> str:
    completion = palm.generate_text(
    model="models/text-bison-001",
    prompt=message,
    temperature=0,
    # The maximum length of the response
    max_output_tokens=800,
    )
    return (completion.result)

def showModels():
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    for i in models:
        print(i.name)

def setModels(name: str):
    print("Hello")

def latexify(message: str) -> str:
    a = "return the LaTeX code only of this message (no /begin and /end needed): " + message
    return talkShort(a)