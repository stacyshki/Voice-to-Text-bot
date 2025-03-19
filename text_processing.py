from g4f.client import Client


class GenI:
    '''
    This class uses GPT to give some outcome. To know more about the model,
    please, visit https://github.com/xtekky/gpt4free
    '''
    
    def __init__(self):
        self.__client = Client()
    
    def ask_gpt(self, prompt : str):
        '''
        Give a prompt and get a text response
        
        Args:
            prompt (str): what do you want to ask
        '''
        
        return self.__client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [{"role": "user", "content": prompt}],
            web_search = False
        ).choices[0].message.content
