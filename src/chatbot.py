import ollama

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
print("Intent:", intent)