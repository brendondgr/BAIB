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
    def fileExists(location):
        from os import path
        return True if path.exists(location) else False
    
    @staticmethod
    def createFolders(location):
        from os import mkdir, path
        # Splits the location into a list
        loc_split = location.split("/")
        
        # Removes entry if the specific entry contains a "."
        newlist = [i for i in loc_split if "." not in i]
        
        # Creates the folders, going down the list one by one, if they don't exist.
        combined = ""
        for i in range(0, len(newlist)):
            # Checks to see if first entry exists, if not, creates it.
            if i == 0:
                combined = newlist[i]
                if not path.exists(combined):
                    mkdir(combined)
            else:
                combined = combined + "/" + newlist[i]
                if not path.exists(combined):
                    mkdir(combined)
    
    @staticmethod
    def ttsMessage(response, count, savetts):
        import gtts
        from datetime import datetime
        from configparser import ConfigParser
        
        # Creates a config parser
        config = ConfigParser()
        config.read("config.ini")
        
        # Loads file location from config file
        mainfolder = config["folders"]["messages"]
        date = datetime.now().strftime("%Y%m%d")
        
        combined_folder = f"{mainfolder}/{date}"
        
        # Creates folders if they don't exist
        if not BAI_commands.fileExists(combined_folder):
            BAI_commands.createFolders(combined_folder)
        
        # Creates name in the following format: tts_{count}_{timestamp}.mp3
        filename = f"tts_{count}_{datetime.now().strftime('%H%M%S')}.mp3"
        
        # Combines the folder and filename
        combined_folder = f"{combined_folder}/{filename}"
        
        # Reads the response from the API and converts it to an mp3 file
        tts = gtts.gTTS(response, lang="en")
        
        # Saves the mp3 file
        tts.save(combined_folder)
        
        # Plays the mp3 file
        from playsound import playsound
        playsound(combined_folder)
    
    @staticmethod
    def parseData(data):
        #print(data)
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