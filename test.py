from langchain_community.llms import Ollama

# Function to read content from a text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Initialize the Ollama model with the base URL and model name
ollama = Ollama(base_url="http://localhost:11434", model="llama3")

# Specify the path to your text file
file_path = 'transcription1.txt'

# Read the content from the text file
content = read_text_file(file_path)

# Create the summarization prompt
prompt = "What is the main topic of the conversations:\n\n" + content

# Use the prompt for the model
response = ollama(prompt)

# Print the response from the model
# print(response)

with open("response1.txt", "w") as file:
    file.write(response)

print("Response saved to response.txt")