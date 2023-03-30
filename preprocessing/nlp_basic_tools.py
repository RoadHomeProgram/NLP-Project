import nltk
from nltk.tokenize import word_tokenize

class Text():
    def __init__(self, text: str):
        self.text = text
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        words = word_tokenize(text)
        self.pos_tags = nltk.pos_tag(words)

    def get_text(self) -> str:
        return self.text

    def is_sentence(self) -> bool:
        # pretty naive, just checks for subject and verb
        has_subject = any(tag.startswith('NN') for _, tag in self.pos_tags)
        has_verb = any(tag.startswith('VB') for _, tag in self.pos_tags)
        return has_subject and has_verb
    
    def to_string(self, verbose: bool = False):
        outstr = ''
        if verbose:
            outstr += '[structured text] ' if self.is_sentence() else '[item] '
        return outstr + self.get_text()