from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.tokenize import WordPunctTokenizer
import nltk
from nltk import pos_tag
import re
import preprocessor as p


def clean_text(text):
    p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.NUMBER, p.OPT.HASHTAG)

    text = p.clean(re.sub(r'RT\s?:?', '', text, flags=re.IGNORECASE))
    text = text.replace(':', '')
    return text


class TextAnalyzer(object):
    """
    Assign sentiment to text
    """
    def __init__(self):

        self._sent_analyzer = SIA()
        self._word_tokenizer = WordPunctTokenizer().tokenize
        self._sent_tokenizer = nltk.data.LazyLoader(
            'tokenizers/punkt/english.pickle'
        ).tokenize
        self._ids = []

    def sentiment(self, sentences):
        for sentence in sentences:
            yield self._sent_analyzer.polarity_scores(sentence)

    def sentences(self, text):
        """
        Uses the built in sentence tokenizer to extract sentences from the
        paragraphs. Note that this method uses BeautifulSoup to parse HTML.
        """
        for sentence in self._sent_tokenizer(text):
            yield sentence

    def words(self, text):
        """
        Uses the built in word tokenizer to extract tokens from sentences.
        Note that this method uses BeautifulSoup to parse HTML content.
        """
        for sentence in self.sentences(text):
            for token in self._word_tokenizer(sentence):
                yield token

    def tokenized(self, text):
        """
        Segments, tokenizes, and tags a document in the corpus.
        """
        yield [pos_tag(self._word_tokenizer(sent)) for sent in self._sent_tokenizer(text)]
