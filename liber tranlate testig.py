
from libretranslatepy import LibreTranslateAPI

lt = LibreTranslateAPI("http://127.0.0.1:5000/")
#lt = LibreTranslateAPI("https://libretranslate.com/")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

#print(lt.translate("Hello Dude! Nice to meet you. Whats your name? Help me with your Application.", "en", "fr"))
# LibreTranslate es impresionante!

#print(lt.detect("Hello World"))
# [{"confidence": 0.6, "language": "en"}]

print(lt.languages())
# [{"code":"en", "name":"English"}]
destination_language="hi"
input_filename = 'Response2.txt'  # Specify your input text file
with open(input_filename, 'r', encoding='utf-8') as file:
            input_text = file.read()
            #print(input_text)
            print(input_filename)
            print(lt.detect(input_text))
            translated_text=lt.translate(input_text, "en", destination_language)
            #print(translated_text)
output_file = input_filename.replace('.txt', f'_{destination_language}.txt')
with open(output_file, 'w', encoding='utf-8') as file:
            file.write(translated_text)
print(f"Translation saved to {output_file}")
            