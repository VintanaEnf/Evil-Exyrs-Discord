import sys
sys.path.append('E:/keys')
import keys

import google.generativeai as palm
palm.configure(api_key=keys.PALM)

response = palm.generate_text(prompt="Hello!")
