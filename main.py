import asyncio
import websockets
import os
import json

inputRelay = os.environ.get('INPUT_RELAY')
outputRelay = os.environ.get('OUTPUT_RELAY')

async def listen():
    async with websockets.connect(inputRelay) as websocket:
        async with websockets.connect(outputRelay) as websocketOutput:
            message = '["REQ", "1337", {"kinds": [1], "limit": 10}]'
            await websocket.send(message)
            while True:
                response = await websocket.recv()
                responseJson = json.loads(response)
                try:
                    print(responseJson)
                    try:
                        await websocketOutput.send(json.dumps(responseJson))
                    except Exception as e:
                        print(e)
                except:
                    pass

asyncio.get_event_loop().run_until_complete(listen())