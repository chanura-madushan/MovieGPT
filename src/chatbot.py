import ollama
from recommender import recommend, find_title


def get_intent(user_input):
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "system",
                "content": """
You are a movie chatbot.

Classify the user's message into exactly ONE category:

GREETING
RECOMMENDATION
HELP
GOODBYE

Examples:

hello -> GREETING
hi -> GREETING
hey -> GREETING

I want something like Blood & Water -> RECOMMENDATION
recommend me a movie -> RECOMMENDATION
what should I watch -> RECOMMENDATION

help -> HELP
what can you do -> HELP

bye -> GOODBYE
goodbye -> GOODBYE
see you later -> GOODBYE

Return ONLY the category name.
"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response["message"]["content"].strip().upper()


def start_chat():
    print("Movie-GPT: Hello! I can recommend movies and TV shows.")
    print("Movie-GPT: Type 'help' to see what I can do.")
    print("Movie-GPT: Type 'bye' to exit.\n")

    while True:

        user_input = input("You: ")

        intent = get_intent(user_input)

        if intent == "GREETING":
            print("Movie-GPT: Hello! Tell me a movie or show you like.")

        elif intent == "HELP":
            print("Movie-GPT: I can recommend movies and TV shows.")
            print("Movie-GPT: For example, try:")
            print("Movie-GPT: 'Something like Blood & Water'")

        elif intent == "GOODBYE":
            print("Movie-GPT: Goodbye!")
            break

        elif intent == "RECOMMENDATION":

            title = find_title(user_input)

            if title:
                recommendations = recommend(title)

                print("Movie-GPT: Here are some recommendations:\n")

                for i, movie in enumerate(recommendations, 1):
                    print(f"{i}. {movie}")

            else:
                print("Movie-GPT: I could not find that movie or show in my dataset.")
                print("Movie-GPT: Please mention a movie or show from Netflix.")

        else:
            print("Movie-GPT: Sorry, I did not understand that.")


start_chat()