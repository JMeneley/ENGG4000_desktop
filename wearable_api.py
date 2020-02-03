import logging
import asyncio
import platform

from bleak import BleakClient
from bleak import discover
from bleak import _logger as logger

class BLE:
    DATA_CHARACTERISTIC_UUID = (
        "79b7950e-b94e-4293-bace-1db832cac77c"
    )
    
    @staticmethod
    def format_notification_data(data):
        N = 2 # All data is assumed to be uint16s (2 bytes)
        grouped_data = [data[n:n+N] for n in range(0, len(data), N)]
        formatted_data = [int.from_bytes( temp, byteorder="little", signed=False ) for temp in grouped_data]
        return formatted_data

    def __init__(self):
        self.client = None
        self.scanned_devices = []

    def scan(self):
        asyncio.run( self.__scan() )
        return self.scanned_devices

    def connect(self, address):
        connected = asyncio.run( self.__connect( address ) )
        return connected

    def disconnect(self):
        asyncio.run( self.__disconnect() )

    def enable_notifications(self, uuid, callback):
        asyncio.run( self.__enable_notifications( uuid, callback ) )

    def disable_notifications(self, uuid):
        asyncio.run( self.__disable_notifications( uuid ) )

    async def __disable_notifications(self, uuid):
        asyncio.create_task( self.client.stop_notify(uuid) )

    async def __enable_notifications(self, uuid, callback):
        asyncio.create_task( self.client.start_notify(uuid, callback) )

    async def __connect(self, address):
        loop = asyncio.get_event_loop()
        self.client = BleakClient( address, loop )
        try:
            await self.client.connect()
            return True
        except:
            return False

    async def __disconnect(self):
        asyncio.create_task( self.client.disconnect() )
        

    async def __scan(self):
        dev = await discover()
        for i in range(0,len(dev)):
            self.scanned_devices.append(dev[i])
        