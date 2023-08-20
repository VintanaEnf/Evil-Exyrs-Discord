import google.generativeai as palm

import sys
sys.path.append('E:/keys')
import keys

palm.configure(api_key=keys.PALM)

def talkShort(message: str) -> str:
    response = palm.generate_text(prompt=message)
    return response.result;
