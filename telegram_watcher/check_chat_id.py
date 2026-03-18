from telethon import TelegramClient, events

api_id = 39053935
api_hash = "3237ac2e0bbdb92261016abb68174d36"

client = TelegramClient("session", api_id, api_hash)


@client.on(events.NewMessage)
async def handler(event):
    # if not event.is_channel:
    #     return

    chat = await event.get_chat()

    print("=" * 50)
    # print(f"Канал: {chat.title}")
    print(f"ID: {chat.id}")
    print(f"Username: {chat.username}")
    print(f"Текст: {event.text}")


client.start()
print("👀 Слушаем ВСЕ каналы (временно)...")
client.run_until_disconnected()
