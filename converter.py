from pydub import AudioSegment
import os.path


class Converter:
    '''
    The class converts different ffmpeg formats
    
    Args:
        import_folder (str): Where to take from, leave empty if none
        export_folder (str): Where to export the converted file, leave empty if none
    '''
    
    def __init__(self, import_folder : str, export_folder : str):
        self.__imf = import_folder
        self.__exf = export_folder
    
    
    def any_to_wav(self, file : str) -> None:
        '''
        This function converts any ffmpeg format to wav
        Args:
            file (str): Provide filename
        '''
        
        if not os.path.exists(f"{self.__imf}{file}"):
            return "File does not exist at a given directory"
        
        if not os.path.exists(f"{self.__exf}"):
            return "Directory does not exist"
        
        AudioSegment.from_file(f"{self.__imf}{file}").export(
                                        f"{self.__exf}{file.split('.')[0]}.wav",
                                        format="wav"
        )
