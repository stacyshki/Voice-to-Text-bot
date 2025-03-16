import whisper


class SpeechProcessing:
    '''
    Processes human speech and works with audio
    
    Model that is used: https://github.com/openai/whisper
    
    Args:
        model (str = "turbo"): load the model (see the link)
    '''
    
    
    def __init__(self, model : str = 'turbo'):
        self.__model = whisper.load_model(model)
    
    def to_text(self, filepath : str):
        '''
        Get text from audio or video file
        
        Args:
            filepath (str): provide filepath to what you are converting
        '''
        
        return self.__model.transcribe(filepath)['text']
