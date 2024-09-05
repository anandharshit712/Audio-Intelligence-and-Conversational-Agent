import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter



def generate_single_word_title(file_path):
    # Read the conversation text from the file
    with open(file_path, 'r') as file:
        conversation_text = file.read()

    # Tokenize the conversation into words
    words = word_tokenize(conversation_text.lower())

    # Remove stop words and punctuation
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalpha() and word not in stop_words]

    # Count the frequency of words
    word_freq = Counter(words)

    # Extract the most common word
    most_common_word = word_freq.most_common(1)[0][0]

    # Capitalize the title
    title = most_common_word.capitalize()

    return title

# Example usage
file_path = 'Transcript/Transcript2_med_mistral-nemo_7_breast_cancer.txt'  # Replace with your file path
title = generate_single_word_title(file_path)
print(f'Generated Title: {title}')
