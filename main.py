import asyncio
import os
import websockets
import json

async def relay_websockets(websocket1, websocket2):
    while True:
        try:
            # Wait for an event on websocket 1
            event = json.loads(await websocket1.recv())
            try:
                if(event[0] == "EVENT"):
                    # Remove the event ID from the event
                    del event[1]
                    # log event
                    # print(json.dumps(event))
                    print("Sending event with id " + str(event[1]['id']) + " to " + os.environ.get("OUTPUT_RELAY"))

                    # Relay the event to websocket 2
                    await websocket2.send(json.dumps(event))
                elif(event[0] == "EOSE"):
                    print("End of stream")

            except Exception as error:
                print(f"Failed to relay event: {error}")
                continue

        except websockets.ConnectionClosed:
            # If either websocket is closed, attempt to reconnect
            print("Connection closed, attempting to reconnect...")
            await asyncio.sleep(1)
            try:
                async with websockets.connect(os.environ.get("INPUT_RELAY")) as websocket1:
                    async with websockets.connect(os.environ.get("OUTPUT_RELAY")) as websocket2:
                        message = '["REQ", "1337", {"kinds": [1], "limit": 1}]'
                        await websocket1.send(message)
                        await relay_websockets(websocket1, websocket2)

            except Exception as error:
                # If the reconnection attempt fails, repeat the loop and try again
                print(f"Failed to reconnect: {error}")
                continue

async def main():
    print("Scraper started...")
    # Read the websocket URLs from environment variables
    websocket1_url = os.environ.get("INPUT_RELAY")
    websocket2_url = os.environ.get("OUTPUT_RELAY")

    # If either URL is missing, raise an error
    if not websocket1_url or not websocket2_url:
        raise ValueError("Please set the INPUT_RELAY and OUTPUT_RELAY environment variables")

    try:
        async with websockets.connect(websocket1_url) as websocket1:
            async with websockets.connect(websocket2_url) as websocket2:
                message = '["REQ", "1337", {"kinds": [1]}]'
                await websocket1.send(message)
                await relay_websockets(websocket1, websocket2)

    except Exception as error:
        # If the initial connection attempt fails, attempt to reconnect immediately
        print(f"Failed to connect: {error}")
        await asyncio.sleep(1)
        await main()

# Start the script
asyncio.run(main())