import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import UserRoom
from asgiref.sync import sync_to_async


@sync_to_async
def update_connected_user(id, who, connect=True):
    room = UserRoom.objects.get(id=id)
    if connect:
        if who == room.user:
            room.connected.add(who)
            room.save()
            return True
        else:
            if len(room.connected.all()) == 1 and room.user in room.connected.all():
                room.connected.add(who)
                room.save()
                return True
            else:
                return False
    else:
        if who in room.connected.all():
            if who == room.user:
                room.connected.remove(who)
                room.save()
                return True
            else:
                room.connected.remove(who)
                room.save()
                return True
        else:
            return False


@sync_to_async
def get_connected(id):
    return len(UserRoom.objects.get(id=id).connected.all())


@sync_to_async
def update_room(id, board, turn, scoreX, scoreO):
    room = UserRoom.objects.get(id=id)
    room.board = ''.join(map(str, board))
    room.turn = turn
    room.scoreX = scoreX
    room.scoreO = scoreO
    room.save()


@sync_to_async
def reset_room(id):
    room = UserRoom.objects.get(id=id)
    room.board = '000000000'
    room.turn = 'O'
    room.scoreX = 0
    room.scoreO = 0
    room.save()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['roomId']

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        if await update_connected_user(self.room_group_name, self.scope['user']):
            await self.accept()
        else:
            await self.close()


    async def disconnect(self, close_code):
        # Leave room group
        await update_connected_user(self.room_group_name, self.scope['user'], False)
        if not await get_connected(self.room_group_name):
            await reset_room(self.room_group_name)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        await update_room(self.room_group_name, data['board'], data['currentPlayer'], data['scoreX'], data['scoreO'])

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'board': data['board'],
                'currentPlayer': data['currentPlayer']
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'board': event['board'],
            'currentPlayer': event['currentPlayer']
        }))