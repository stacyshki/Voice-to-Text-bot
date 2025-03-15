import speech_recognition as sr
import os.path


class SpeechToText:
    '''
    This class is made to transcribe speech to text. Here nothing new is
    introduced. The main functionality is taken from speech_recognition
    
    See: https://pypi.org/project/SpeechRecognition/
    '''
    
    
    def __init__(self):
        self.__recognizer = sr.Recognizer()
    
    
    def transcribe_audio(self, file_path : str, lang : str) -> str:
        '''
        This function takes a wav/aiff files and transcribes them to text
        
        See also: https://pypi.org/project/SpeechRecognition/
        
        Args:
            file_path (str): Provide full path to the file
            lang (str): Provide language, e.g. en-US or ru-RU
        '''
        
        if not os.path.exists(file_path):
            return "The file does not exist at a given directory"
        
        with sr.AudioFile(file_path) as source:
            audio_data = self.__recognizer.record(source)
            
            try:
                return self.__recognizer.recognize_google(audio_data,
                                                        language=lang
                )
            except sr.UnknownValueError:
                return "Could not recognize speech"
            except sr.RequestError:
                return "Server recognition request error"
