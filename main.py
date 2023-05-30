import asyncio
import os
import websockets

async def relay_websockets(websocket1, websocket2):
    while True:
        try:
            # Wait for an event on websocket 1
            event = await websocket1.recv()

            # log event
            # print(event)

            # Relay the event to websocket 2
            await websocket2.send(event)

        except websockets.ConnectionClosed:
            # If either websocket is closed, attempt to reconnect
            print("Connection closed, attempting to reconnect...")
            await asyncio.sleep(1)
            try:
                websocket1 = await websockets.connect(os.environ.get("INPUT_RELAY"))
                websocket2 = await websockets.connect(os.environ.get("OUTPUT_RELAY"))

            except:
                # If the reconnection attempt fails, repeat the loop and try again
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

    except:
        # If the initial connection attempt fails, attempt to reconnect immediately
        print("Connection failed, attempting to reconnect...")
        await asyncio.sleep(1)
        await main()

# Start the script
asyncio.run(main())