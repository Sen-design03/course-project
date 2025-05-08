from flask import Flask, jsonify

app = Flask(__name__)

HELP_TEXT = """
Game Help:
- At any point, type "/help" to see this message.
- Type the number of your chosen action to proceed.
- Choices affect the story, so think carefully!
- There is no wrong way to play, enjoy the game!

Tip: Curiosity often leads to interesting outcomes.
"""

@app.route('/help', methods=['GET'])
def get_help():
    return jsonify({"help": HELP_TEXT})

if __name__ == "__main__":
    app.run(host="localhost", port=5002)