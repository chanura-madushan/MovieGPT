import ollama


def ask_qwen(user_input):
    response = ollama.chat(
        model="qwen2.5:3b",
         messages=[
            {
                "role": "system",
                "content": """
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
                "role": "user",
                "content": user_input
            }
        ]
    )
    return response["message"]["content"]


user_input = input("You: ")
answer = ask_qwen(user_input)
print("Qwen:", answer)