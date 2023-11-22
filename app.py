from flask import Flask, request, jsonify
import spacy
from spellchecker import SpellChecker
from unidecode import unidecode

app = Flask(__name__)

# Carga el modelo de lenguaje de spaCy en español
nlp = spacy.load("es_core_news_sm")
spell = SpellChecker(language='es')

# Diccionario de palabras disponibles
available_words = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "ll",
    "m",
    "n",
    "ñ",
    "o",
    "p",
    "q",
    "r",
    "rr",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    'hola',
]

not_active_words = [
    "es",
    "la",
    "los",
    "las",
    "el",
    "les",
    "de",
    "del",
    "al"
]

def formatText(input_str):
    # temp = spell.correction(input_str.lower())
    temp = input_str.lower()
    temp = temp.replace("ñ","__tempni__")
    return unidecode(temp).replace("__tempni__","ñ")

def translate_to_array(sign_language_phrase):
    doc = nlp(sign_language_phrase)
    translated_array = []

    corrected_tokens = [{
                        "token":token,
                        "text": formatText(token.text)}
                for token in doc]
    
    cleaned_tokens = [item for item in corrected_tokens if not item['token'].is_punct]

    for item in cleaned_tokens:
        if item["text"] in available_words:
            translated_array.append({"sign":item["text"], "text":item["text"]})
        else:
            if item["text"] in not_active_words:
                translated_array.append({"sign":None, "text":item["token"].text })
            elif "rr" in item["text"]:
                for part in item["text"].split("rr"):
                    for letter in part:
                        translated_array.append({"sign":letter, "text":letter})
                    if part != item["text"].split("rr")[-1]:
                        translated_array.append({"sign":"rr", "text":"rr"})
            elif "ll" in item["text"]:
                for part in item["text"].split("ll"):
                    for letter in part:
                        translated_array.append({"sign":letter, "text":letter})
                    if part != item["text"].split("ll")[-1]:
                        translated_array.append({"sign":"ll", "text":"ll"})
            else:
                for letter in item["text"]:
                    translated_array.append({"sign":letter, "text":letter})
        translated_array.append({"sign":None, "text":" " })
    return translated_array

@app.route("/")
def hello_world():
    return "funcionando"

@app.route('/translate', methods=['POST'])
def translate():
    try:
        print("request: ", request, flush=True)
        data = request.get_json()
        input_phrase = data.get("phrase", "")
        print("input_phrase: ", input_phrase, flush=True)
        if input_phrase:
            translated_result = translate_to_array(input_phrase)
            return jsonify({"result": translated_result}), 200
        else:
            return jsonify({"error": "No input phrase provided"}), 400
    except Exception as e:
        print(e, flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)