import asyncio
import websockets
from openai import OpenAI

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        client = OpenAI()
        completion = client.chat.completions.create(
          #model="gpt-4-0125-preview",
          model="gpt-4-turbo-preview",
          #model="gpt-4-plugins",
          response_format={ "type": "json_object" },
          messages=[
        	{"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": {message}}
          ]
        )
        #print(completion.choices[0].message)
        print(completion.choices)

        await websocket.send(f"Echo: {completion.choices[0].message}")

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
