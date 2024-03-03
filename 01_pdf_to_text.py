import fitz
import pandas as pd 
import re 
import nltk.data


def clean_text(text):
    """
    Post-processes the extracted text to clean and reformat it.
    This is a basic function; you might need to customize it based on your document's layout and content.
    """
    # Remove image tags
    text = re.sub(r'<image:.*?>', '', text)
    # Replace hyphenations at the end of lines
    text = re.sub(r'-\n', '', text)
    # Replace newline characters with spaces
    text = re.sub(r'\n', ' ', text)
    # Optional: Additional cleaning rules can be added here
    return text

def separate_sentences(text, n=5):
    """
    Separates every N number of sentences with a new line in blank.
    """
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)
    separated_text = '\n\n'.join([' '.join(sentences[i:i+n]) for i in range(0, len(sentences), n)])
    return separated_text

def pdf_to_txt(pdf_path, txt_path, sentence_sep=1):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda block: (block[1], block[0]))  # Sort blocks top-to-bottom and left-to-right
        for block in blocks:
            block_text = block[4]  # The text is at index 4
            text += block_text + "\n"  # Add a newline character after each block for better readability
    
    # Post-process extracted text
    cleaned_text = clean_text(text)
    if sentence_sep > 1:
        cleaned_text = separate_sentences(cleaned_text, n=sentence_sep)
    
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(cleaned_text)
    
    print(f"Text extracted and saved to {txt_path}")



pdf_path = r"C:\Users\User\OneDrive\Desktop\programme_pdf_to_text_translate\input_data\Frankenstein_spanish.pdf"
txt_path = r"C:\Users\User\OneDrive\Desktop\programme_pdf_to_text_translate\output_data\Frankenstein_spanish.txt"
pdf_to_txt(pdf_path, txt_path, sentence_sep=2)
