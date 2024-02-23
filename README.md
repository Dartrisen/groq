# Groq
Custom client for the Groq API.

# Usage
```python
from groq.client import Client


groq_client = Client()
chat = groq_client.create_chat(
    r"Please give me some ideas for a startup.",
    model_id="llama2-70b-4096",
    max_tokens=4096,
    temperature=0.5,
    max_input_tokens=2048,
)
```

# Live streaming chat
You can use it as a live chat without waiting for the full response.
```python
groq_client = Client()
while True:
    query = input("Query (type 'exit' to quit): ")

    if query == "exit":
        break

    with groq_client.create_streaming_chat(
        query,
        model_id="llama2-70b-4096",
    ) as response:
        for line in response:
            if line:
                print(line, end="")
    print()
```
