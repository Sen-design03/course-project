import requests

game_state = {
    "scene_id": "start",
    "choices_made": []
}

def get_scene_from_narrative(scene_id, choice=None):
    payload = {"scene_id": scene_id}
    if choice is not None:
        payload["choice"] = choice

    try:
        response = requests.post("http://localhost:5001/narrative", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"description": "An error occurred.", "choices": [], "scene_id": scene_id}

def get_user_choice(options):
    while True:
        print("\nWhat will you do?")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        choice = input(f"Enter your choice (1-{len(options)} or /help): ").strip()

        if choice.lower() == "/help":
            show_help()
        elif choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice) - 1
        else:
            print("Invalid input. Try again.")

def main():
    current_scene = get_scene_from_narrative("start")

    while True:
        print(f"\n{current_scene['description']}")
        if not current_scene['choices']:
            print("\nNo more choices. Game Over.")
            break

        choice_index = get_user_choice(current_scene['choices'])
        chosen_text = current_scene['choices'][choice_index]
        game_state["choices_made"].append(chosen_text)

        current_scene = get_scene_from_narrative(current_scene['scene_id'], choice_index)

# Help Service
def show_help():
    try:
        response = requests.get("http://localhost:5002/help")
        response.raise_for_status()
        print("\n" + response.json()["help"])
    except requests.exceptions.RequestException as e:
        print("\nHelp service not available.")

if __name__ == "__main__":
    main()