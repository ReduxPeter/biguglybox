import websockets
import json
import asyncio

class WebSocketClient():

    def __init__(self):
        pass

    async def connect(self, handlerClass):
        '''
            Connecting to webSocket server

            websockets.client.connect returns a WebSocketClientProtocol, which is used to send and receive messages
        '''
        self.handlerClass = handlerClass
        self.connection = await websockets.client.connect('ws://10.0.178.15:81/')
        if self.connection.open:
            print('Connection stablished. Client correcly connected')
            # Send greeting
            await self.sendMessage('Hey server, this is webSocket client')
            return self.connection


    async def sendMessage(self, message):
        '''
            Sending message to webSocket server
        '''
        await self.connection.send(message)

    async def receiveMessage(self, connection):
        '''
            Receiving all server messages and handling them
        '''
        while True:
            try:
                message = await connection.recv()
                self.handlerClass.onMessage(json.loads(message))
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

    async def heartbeat(self, connection):
        '''
        Sending heartbeat to server every 5 seconds
        Ping - pong messages to verify connection is alive
        '''
        while True:
            try:
                await connection.send('ping')
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break