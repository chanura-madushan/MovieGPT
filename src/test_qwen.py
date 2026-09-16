import ollama
response = ollama.chat(
     model="qwen2.5:3b",
     messages=[
         {
             "role": "user",
            "content": "Say hello to MovieGPT"
         }
     ]
)
print(response["message"]["content"])