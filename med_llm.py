from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("AdaptLLM/medicine-LLM", use_auth_token="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")
model = AutoModelForCausalLM.from_pretrained("AdaptLLM/medicine-LLM", use_auth_token="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")

# Read content from text file
with open("input_text.txt", "r") as file:
    input_text = file.read()

# Tokenize and generate response
inputs = tokenizer(input_text, return_tensors="pt")
output = model.generate(**inputs)
response = tokenizer.decode(output[0], skip_special_tokens=True)

# Save the response to a text file
with open("Response_med.txt", "w") as file:
    file.write(response)

print("Response saved to Response_med.txt")
