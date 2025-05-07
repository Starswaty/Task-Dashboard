import pdfplumber
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

nltk.download("punkt")


def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file (uploaded as stream)."""
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text.strip()


def summarize_text(text, compression_ratio=0.1):
    """
    Summarizes the given text using TextRank.
    Returns a summary with approximately `compression_ratio` of the original sentence count.
    """
    sentences = nltk.sent_tokenize(text)
    total_sentences = len(sentences)
    summary_length = max(1, int(total_sentences * compression_ratio))
    
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, summary_length)
    
    return summary
