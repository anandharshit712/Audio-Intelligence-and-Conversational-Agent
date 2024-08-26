import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("AdaptLLM/medicine-LLM", use_auth_token="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")
model = AutoModelForCausalLM.from_pretrained("AdaptLLM/medicine-LLM", use_auth_token="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")

# Move model to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Read prompt and content from text file
with open("Transcript/Transcript2_med_mistral-nemo_4.txt", "r") as file:
    content = file.read().strip()     # Read the rest as the content

prompt = "What is the main cause of the disease mentioned in the conversation and what are the ways to solve or reduce it."

# Combine prompt and content
input_text = content + "\n" +prompt

# Tokenize input and move input tensors to GPU if available
inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=1024).to(device)

# Generate response
output = model.generate(**inputs, max_new_tokens=150)

# Decode the response
response = tokenizer.decode(output[0], skip_special_tokens=True)

# Save the response to a text file
with open("Response_med.txt", "w") as file:
    file.write(response)

print("Response saved to Response_med.txt")
