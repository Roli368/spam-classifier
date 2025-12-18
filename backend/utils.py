import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('stopwords')

ps = PorterStemmer()

def preprocess_text(text: str) -> str:
    review = re.sub('[^a-zA-Z]', ' ', text)
    review = review.lower().split()
    review = [
        ps.stem(word)
        for word in review
        if word not in stopwords.words('english')
    ]
    return ' '.join(review)
