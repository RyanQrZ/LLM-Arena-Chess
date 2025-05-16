import requests, json

API_KEY =

ENDPOINT = "https://models.github.ai/inference/chat/completions"

# Start a chat with a given LLM model
def chat_llm( model, content ):
    header_msg = { "Authorization": f"Bearer {API_KEY}",
                   "Content-Type": "application/json" }

    body_msg = { "model": model,
                 "messages": [
                     {"role": "user",
                      "content": content } ],
                 "temperature": 0,
                 "top_p": 0.1 }

    # Serialize obj to json format
    encoded = json.dumps( body_msg )

    # Make a request
    request = requests.post( ENDPOINT, headers=header_msg, data=encoded )

    # Decode json response to string
    decoded = request.json()

    #print( decoded )
    return decoded["choices"][0]["message"]["content"]
