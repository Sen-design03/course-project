from flask import Flask, request, jsonify

app = Flask(__name__)

# Story structure
scenes = {
    # Act 1
    "start": {
        "description": "You wake up in a dark forest. What do you do?",
        "choices":{
            "Explore the forest": "forest",
            "Go back to sleep": "sleep",
        }
    },
    "forest": {
        "description": "You find a large waterfall from across a cliff. There seems to be cave behind it.",
        "choices":{
            "Jump towards the cave": "cave",
            "Walk away": "leave",
        }
    },
    "sleep":{
        "description": "You go back to sleep, forgetting your troubles.",
        "choices":{}
    }
    
}

@app.route('/narrative', methods=['POST'])
def narrative():
    data = request.get_json()
    scene_id = data.get('scene_id')
    chosen_index = data.get('choice')

    if scene_id not in scenes:
        return jsonify({"description": "Scene not found.", "choices": {}, "scene_id": scene_id}), 400

    current_scene = scenes[scene_id]
    choices = list(current_scene["choices"].keys())

    if chosen_index is not None:
        if 0 <= chosen_index < len(choices):
            next_scene_id = current_scene["choices"][choices[chosen_index]]
            next_scene = scenes[next_scene_id]
            return jsonify({
                "description": next_scene["description"],
                "choices": list(next_scene["choices"].keys()),
                "scene_id": next_scene_id
            })
        else:
            return jsonify({"description": "Invalid choice.", "choices": choices, "scene_id": scene_id}), 400

    return jsonify({
        "description": current_scene["description"],
        "choices": choices,
        "scene_id": scene_id
    })

if __name__ == "__main__":
    app.run(host="localhost", port=5001)