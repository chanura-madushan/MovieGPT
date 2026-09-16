import ollama
from recommender import recommend, find_title

def get_intent(user_input):
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role":"system",
                "content":
                """
                    You are a movie chatbot.
                    Classify the user's message into exactly one of these categories:

                    GREETING
                    RECOMMENDATION
                    HELP
                    GOODBYE

                    Return only the category name.
                """
            },
            {
                "role":"user",
                "content":user_input
            }
        ]
    )

    return response["message"]["content"].strip()

user_input = input("You: ")
intent = get_intent(user_input)
title = find_title(user_input)

if intent == "GREETING":
    print("Movie-GPT: Hello! Tell me a movie or show you like.")
elif title:
    recommendations = recommend(title)
    print("Movie-GPT: Here are some recommendations:")
    for movie in recommendations:
        print("-", movie)
else:
    print("Movie-GPT: Sorry, I could not understand that.")