import json
import re
import random_response
import os

class Chatbot:

    def __init__(self):
        # Return the directory name of a path
        script_dir = os.path.dirname(os.path.abspath(__file__)) # Return the absolute path of the given path
        #  Join the directory path with the filename
        json_path = os.path.join(script_dir, "response.json")
        self.responses_data = self.load_json(json_path)

    # Load the json file
    def load_json(self, file):
        with open(file) as bot_responses:
            print(f"Loaded {file} successfully!")
            return json.load(bot_responses)

    # Function which splits the message,
    # calculates the required words from the json file
    # returns the appropriate response from the chatbot
    def get_response(self, input_string):
        # Split the input string into lowercase words and remove common punctuation
        split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
        score_list = []

        for item in self.responses_data:
            response_score = 0
            required_score = 0  # how many of the required words are in the .json
            required_words = item["required_words"]

            # Check if required words are included to split message and increase the required score
            if required_words:
                for word in split_message:
                    if word in required_words:
                        required_score += 1

            # If all required words are present, check for user_input words
            if required_score == len(required_words):
                for word in split_message:
                    if word in item["user_input"]:
                        response_score += 1

            # Append the response score to the score_list
            score_list.append(response_score)

        # Find the best response based on the highest score
        best_response = max(score_list)
        # Retrieve the index of the best_response in the score_list
        response_index = score_list.index(best_response)

        if input_string == "":
            return "Please type something."

        # Return the best response
        if best_response != 0:
            return self.responses_data[response_index]["bot_response"]

        # If no specific match, return a random string from the random_response()
        return random_response.get_random_string()

if __name__ == "__main__":
    chatbot = Chatbot()
    while True:
        user_input = input("Me:")
        print("Bot: ", chatbot.get_response(user_input))
