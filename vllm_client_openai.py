import openai

openai.api_base = 'http://100.65.8.31:8000/v1'
openai.api_key = ''

def stream_chat_response(messages):
    response = openai.ChatCompletion.create(
        model="Qwen/Qwen2-7B-Instruct",
        messages=messages,
        stream=True
    )

    full_response = ""
    for event in response:
        if event.get('choices'):
            for choice in event['choices']:
                if choice.get('delta') and choice['delta'].get('content'):
                    content = choice['delta']['content']
                    print(content, end='', flush=True)
                    full_response += content
    print()
    return full_response

def chat_loop():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Assistant: Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})
        print("Assistant: ", end='', flush=True)
        
        assistant_response = stream_chat_response(messages)
        messages.append({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    chat_loop()