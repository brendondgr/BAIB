class BAI_Bot:
    def __init__(self, history_len):
        self.history = {}
        self.max_history = history_len
    
    def saveHistory(self, question, answer):
        # If history is full, remove the oldest entry
        if len(self.history) >= self.max_history:
            self.history.popitem()
            
        self.history[question] = answer
        
    def listHistory(self):
        # Converts History to a string, format:
        # Question: Answer, specify question answer!
        if len(self.history) == 0:
            return "I have not asked you any questions yet. This is a new conversation. "
        else:
            return ''.join([f'I asked you the question "{question}", in which you responded "{answer}"\n' for question, answer in self.history.items()])

class BAI_commands:
    @staticmethod
    def parseData(data):
        print(data)
        import json
        # Parses the data from the API response.
        # Returns a list of strings.
        parsed_data = json.loads(data)
        content = parsed_data["choices"][0]["message"]["content"]
        return [content]
    
    @staticmethod
    def getModelName(model, models):
        # Reads through keys, if key matches "model", return the value
        for key in models:
            if key == model:
                return models[key]
    
    @staticmethod
    def getPersonality(personality, personalities):
        # Reads through keys, if key matches "personality", return the value
        for key in personalities:
            if key == personality:
                return personalities[key]
    
    @staticmethod
    def getMessageLength(length, lengths):
        # Reads through keys, if key matches "length", returns the first then second value
        for key in lengths:
            if key == length:
                return lengths[key]["message"], lengths[key]["token"]                   
    
    @staticmethod
    def personalityList(personalities):
        return list(personalities.keys())
    
    @ staticmethod
    def getMessageLengthList(messagelengths):
        return list(messagelengths.keys())
    
    @staticmethod
    def getModelList(models):
        return list(models.keys())
    
    @staticmethod
    def emojiUse(emoji):
        return "I want you to use emojis in your response. " if emoji else "By no means should you use any emojis whatsoever. "

    @staticmethod
    def askQuestion(query, baibot):
        import requests       
        
        url = "https://api.perplexity.ai/chat/completions"

        payload = {
            "model": f"{query.model}",
            "messages": [
                {
                    "role": "system",
                    "content": f'''{query.messagelength}{query.personality}{query.emoji}
                    Here are some previous questions I have asked you, so utilize these in the conversation:
                    {baibot.listHistory()}'''
                },
                {
                    "role": "user",
                    "content": f'{query.question}'
                }
            ],
            "max_tokens": int(query.tokenlimit),
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {query.apitoken}"
        }
        
        return requests.post(url, json=payload, headers=headers)