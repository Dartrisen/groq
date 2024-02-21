# Groq
Custom client for the Groq API.

# Usage
```python
from groq.client import Client


groq_client = Client()
chat = groq_client.create_chat(
    r"Please give me some ideas for a startup which can generate some money. Ideally some crypto and python stuff but I'm open to some new ideas.",
    model_id="llama2-70b-4096",
    max_tokens=4096,
    temperature=0.5,
    max_input_tokens=2048,
)
```
