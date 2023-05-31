import asyncio
import os
import websockets
import json

async def relay_websockets(inputWebsocket, outputWebsocket, kinds):
    while True:
        try:
            # Wait for an event on websocket 1
            event = json.loads(await inputWebsocket.recv())
            try:
                if(event[0] == "EVENT"):
                    # Remove the event ID from the event
                    del event[1]
                    # log event
                    # print(json.dumps(event))
                    print("Sending event with id " + str(event[1]['id']) + " (kind: "+str(event[1]['kind'])+") to " + os.environ.get("OUTPUT_RELAY"))

                    # Relay the event to websocket 2
                    await outputWebsocket.send(json.dumps(event))
                elif(event[0] == "EOSE"):
                    print("End of stream")

            except Exception as error:
                print(f"Failed to relay event: {error}")
                if("sent 1011" in str(error)):
                    print("Got Code 1011 -> Closing websockets...")
                    websockets.close()
                continue

        except websockets.ConnectionClosed:
            # If either websocket is closed, attempt to reconnect
            print("Connection closed, attempting to reconnect...")
            await asyncio.sleep(1)
            try:
                async with websockets.connect(os.environ.get("INPUT_RELAY")) as inputWebsocket:
                    async with websockets.connect(os.environ.get("OUTPUT_RELAY")) as outputWebsocket:
                        message = '["REQ", "1337", {"kinds": '+kinds+', "limit": 10}]'
                        await inputWebsocket.send(message)
                        await relay_websockets(inputWebsocket, outputWebsocket, kinds)

            except Exception as error:
                # If the reconnection attempt fails, repeat the loop and try again
                print(f"Failed to reconnect: {error}")
                continue

async def main():
    print("Scraper started...")
    # Read the websocket URLs from environment variables
    inputUrl = os.environ.get("INPUT_RELAY")
    outputUrl = os.environ.get("OUTPUT_RELAY")
    kinds = os.environ.get("KINDS")

    # If either URL is missing, raise an error
    if not inputUrl or not outputUrl:
        raise ValueError("Please set the INPUT_RELAY and OUTPUT_RELAY environment variables")

    try:
        async with websockets.connect(inputUrl) as inputWebsocket:
            async with websockets.connect(outputUrl) as outputWebsocket:
                message = '["REQ", "1337", {"kinds": '+kinds+'}]'
                await inputWebsocket.send(message)
                await relay_websockets(inputWebsocket, outputWebsocket, kinds)

    except Exception as error:
        # If the initial connection attempt fails, attempt to reconnect immediately
        print(f"Failed to connect: {error}")
        await asyncio.sleep(1)
        await main()

# Start the script
asyncio.run(main())