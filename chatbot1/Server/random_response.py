import random

# Function which returns a random response
# in case the client asks a question
# to the chatbot which is not known (not included to the json file)
def get_random_string():
    random_list = [
        "Please try writing something more descriptive.",
        "Oh! It appears you wrote something I don't understand yet",
        "Do you mind trying to rephrase that?",
        "I'm terribly sorry, I didn't quite catch that.",
        "I can't answer that yet, please try asking something else."
    ]

    list_count = len(random_list)
    random_selection = random.randrange(list_count)

    return random_list[random_selection]