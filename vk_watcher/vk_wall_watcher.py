import time
import requests

ACCESS_TOKEN = "2ea2903e2ea2903e2ea2903e032d9cdb1422ea22ea2903e47fa3cffb74f0cbbfb2efc22"
API_VERSION = "5.131"

# ID группы (отрицательный!)
# GROUP_ID = 193532348 # СТОН СИПИ
# GROUP_ID = 225463035 # Арбузик
GROUP_ID = 226109228 #Арбузик2

CHECK_INTERVAL = 5  # секунд

last_post_id = None


def get_latest_posts():
    url = "https://api.vk.com/method/wall.get"
    params = {
        "owner_id": -GROUP_ID,
        "count": 5,
        "access_token": ACCESS_TOKEN,
        "v": API_VERSION,
    }

    response = requests.get(url, params=params).json()

    if "error" in response:
        raise RuntimeError(response["error"])

    return response["response"]["items"]


def print_post(post):
    print("=" * 60)
    print(f"🆕 Новый пост!")
    print(f"ID: {post['id']}")
    print(f"Дата (unix): {post['date']}")
    print(f"Текст:\n{post.get('text', '').strip() or '[без текста]'}")

    attachments = post.get("attachments", [])
    if attachments:
        print(f"Вложения: {len(attachments)}")
        for a in attachments:
            print(f" - {a['type']}")


print("👀 Запущен мониторинг стены VK...")
print(f"⏱ Проверка каждые {CHECK_INTERVAL} сек\n")

while True:
    try:
        posts = get_latest_posts()

        # Инициализация при первом запуске
        if last_post_id is None:
            for post in posts:
                if post.get("is_pinned"):
                    continue
                last_post_id = post["id"]
                print(f"ℹ️ Инициализация. Последний пост: {last_post_id}")
                break

            time.sleep(CHECK_INTERVAL)
            continue

        new_posts = []

        for post in posts:
            if post.get("is_pinned"):
                continue

            if post["id"] > last_post_id:
                new_posts.append(post)

        if new_posts:
            # сортируем от старого к новому
            new_posts.sort(key=lambda p: p["id"])

            for post in new_posts:
                print_post(post)
                last_post_id = post["id"]

        else:
            print("😴 Новых постов нет")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

    time.sleep(CHECK_INTERVAL)
