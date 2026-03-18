from telethon import TelegramClient, events

api_id = 39053935
api_hash = "3237ac2e0bbdb92261016abb68174d36"

client = TelegramClient("session", api_id, api_hash)

# TEST_CHANNEL_NAME = "test_watcher_123"  # username, без @

WATCHED_CHANNEL_IDS = {
    -1003551499956,  # приватный тестовый
    -1003548915855,  # публичный тестовый
    -1001019233853,  # реальный канал матч тв
    1072134387,  # Маша
}


@client.on(events.NewMessage)
async def handler(event):
    # if not event.is_channel:
    #     return
    
    if event.chat_id not in WATCHED_CHANNEL_IDS:
        return

    chat = await event.get_chat()

    # if chat.username != TEST_CHANNEL_NAME:
    #     return

    print("=" * 40)
    print("📢 Новый пост пойман")
    # print(f"Канал: {chat.title}")
    print(f"ID канала: {chat.id}")
    print(f"Текст: {event.text}")

    # 🔁 Пересылка в Избранное
    await client.send_message(
        "me",
        event.message
    )


client.start()
print("👀 Слушаем тестовый канал...")
client.run_until_disconnected()