from flask import Flask, request, jsonify
from fuzzywuzzy import fuzz
import Levenshtein
import jellyfish

app = Flask(__name__)

def soundex_match(s1, s2):
    return jellyfish.soundex(s1) == jellyfish.soundex(s2)

@app.route("/compare", methods=["POST"])
def compare_strings():
    data = request.json
    string1 = data.get("string1", "")
    string2 = data.get("string2", "")

    if not string1 or not string2:
        return jsonify({"error": "Both 'string1' and 'string2' are required."}), 400

    result = {
        "levenshtein_distance": Levenshtein.distance(string1, string2),
        "fuzzy_ratio": fuzz.ratio(string1, string2),
        "token_sort_ratio": fuzz.token_sort_ratio(string1, string2),
        "jaro_winkler": round(jellyfish.jaro_winkler_similarity(string1, string2), 4),
        "soundex_match": soundex_match(string1, string2)
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
