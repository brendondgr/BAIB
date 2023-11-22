from BAI import BAI_commands as bc
from menu import QueryObject

apitoken = "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"
model = "llama-2-13b-chat"
personality = "You should be a standard AI. Give clear and concise answers. "
messagelength = "Please keep your answer to a single sentence. Less than 20 words preferred. "
tokenlimit = 100
question = "Why is the Sky Blue?"
emoji = False

query = QueryObject(apitoken, model, personality, messagelength, tokenlimit, question, emoji)
response = bc.askQuestion(query)

import json
parsed_data = json.loads(response.text)
content = parsed_data["choices"][0]["message"]["content"]
print(content)