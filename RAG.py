from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import numpy as np
# Define model and tokenizer (replace with your chosen model/tokenizer)
model_name = "facebook/bart-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def read_utt_file(utt_file_path):
  """
  Reads a utt file and returns a dictionary mapping utterance IDs to audio file paths.

  Args:
      utt_file_path (str): Path to the utt file.

  Returns:
      dict: Dictionary mapping utterance IDs to audio file paths.
  """

  utt_dict = {}
  with open(utt_file_path, 'r') as f:
    for line in f:
      line = line.strip()  # Remove leading/trailing whitespace

      # Handle kaldi-style format
      if ' ' in line:
        utt_id, audio_path = line.split(' ', 1)
        utt_dict[utt_id] = audio_path
      # Handle simple format (single line)
      else:
        utt_dict['default'] = line  # Use a default key for the audio path

  return utt_dict

# Sample conversation transcripts for retrieval database
conversation_database =read_utt_file('C:/Users/anand/Downloads/Audio Conversation summerization/swb1_dialogact_annot/sw00utt/sw_0001_4325.utt')


def similarity(text1, text2):
  # Import necessary libraries (e.g., gensim for Word2Vec)
  # ...
  # Calculate word embeddings or sentence representations for text1 and text2
  embedding1 = ...
  embedding2 = ...
  # Calculate cosine similarity
  similarity_score = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
  return similarity_score


# Function to retrieve conversation based on query
def retrieve_conversation(query):
  encoded_query = tokenizer(query, return_tensors="pt")
  with torch.no_grad():
    outputs = model.generate(**encoded_query)
  decoded_response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
  # Find the most similar conversation in the database based on the generated response (replace with a more robust similarity metric)
  best_match_id = max(conversation_database, key=lambda id: similarity(decoded_response, conversation_database[id]))
  return conversation_database[best_match_id]

# Sample query
query = "Where are you from?"

# Retrieve conversation from database
retrieved_conversation = retrieve_conversation(query)

# Print retrieved conversation
print(f"Retrieved conversation: {retrieved_conversation}")
