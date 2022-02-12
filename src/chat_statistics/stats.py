import json
from collections import Counter
from pathlib import Path
from tarfile import DIRTYPE
from typing import Union

import arabic_reshaper
from bidi.algorithm import get_display
from hazm import *
from src.data.Pyfun import DATA_DIR
from wordcloud import WordCloud


class ChatStatistics:
    def __init__(self,jsonfile: Union[str,Path]):
        
        with open(Path(jsonfile)) as f:
            self.chat_data = json.load(f)

        #Loading the persian stop words file
        stopwords =  open(DATA_DIR/ "PersianStopWords.txt").readlines()
        stopwords = list(map(str.strip,stopwords))

        #Noarmalizing the stop wrods
        self.normalize = Normalizer()
        self.stopwords = list(map(self.normalize.normalize, stopwords))

    def generate_word_cloud(self, output_dir:Union[str,Path]):
        
        #Extracting the messages
        msg = self.chat_data["messages"]
        text = ""
        for i in range(len(msg)):
            if type(msg[i]["text"]) is str:
                text += msg[i]["text"] + " "

        #Normalizing the messages
        normalizing = Normalizer()
        normalized_text = normalizing.normalize(text)

        #Tokenizing
        tokens = word_tokenize(normalized_text)

        #Removing stop wrods from tokens list
        pur_token = list(filter(lambda item: item not in self.stopwords,tokens))

        # Merging the pur tokens
        tokenized_text = ""
        for token, freq in Counter(pur_token).most_common()[:100]:
            tokenized_text += f"{token} " * freq

        # Make text readable for a non-Arabic library like wordcloud
        try:
            arabic_text = arabic_reshaper.reshape(tokenized_text)
            arabic_text = get_display(text)
        except AssertionError:
            pass   
        
        #Make a word cloud
        wordcloud = WordCloud(
            
            font_path=str(DATA_DIR / "font.ttf") ,
            background_color="white",
            width=1200,
            height=1200
    
        ).generate(arabic_text)

        # Export to an image
        wordcloud.to_file(str(Path(output_dir) / "wordcloud.png"))

if __name__ == "__main__":
    chat_stats = ChatStatistics(jsonfile= DATA_DIR / "result.json")
    chat_stats.generate_word_cloud(output_dir=DATA_DIR)
    print(f"Your image is ready!!\nIt is located in {DATA_DIR} directory.")
