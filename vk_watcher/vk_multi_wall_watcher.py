import time
import json
import os
import requests

ACCESS_TOKEN = "2ea2903e2ea2903e2ea2903e032d9cdb1422ea22ea2903e47fa3cffb74f0cbbfb2efc22"
API_VERSION = "5.131"

CHECK_INTERVAL = 5  # секунд
STATE_FILE = "last_posts.json"

# группы для мониторинга (owner_id)
GROUPS = {
    -225463035: "Арбузик",
    -226109228: "Арбузик 2"
}


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_latest_posts(group_id):
    url = "https://api.vk.com/method/wall.get"
    params = {
        "owner_id": group_id,
        "count": 5,
        "access_token": ACCESS_TOKEN,
        "v": API_VERSION,
    }
    response = requests.get(url, params=params).json()

    if "error" in response:
        raise RuntimeError(response["error"])

    return response["response"]["items"]


def print_post(group_name, post):
    print("=" * 70)
    print(f"🆕 Новый пост из: {group_name}")
    print(f"ID поста: {post['id']}")
    print(f"Дата (unix): {post['date']}")
    print("Текст:")
    print(post.get("text", "").strip() or "[без текста]")

    attachments = post.get("attachments", [])
    if attachments:
        print(f"Вложения: {len(attachments)}")
        for a in attachments:
            print(f" - {a['type']}")


print("👀 Мониторинг нескольких групп VK запущен\n")

last_posts = load_state()

while True:
    try:
        for group_id, group_name in GROUPS.items():
            posts = get_latest_posts(group_id)

            group_key = str(group_id)
            last_id = last_posts.get(group_key)

            # первая инициализация группы
            if last_id is None:
                for post in posts:
                    if post.get("is_pinned"):
                        continue
                    last_posts[group_key] = post["id"]
                    print(f"ℹ️ Инициализация [{group_name}]: {post['id']}")
                    break
                continue

            new_posts = []

            for post in posts:
                if post.get("is_pinned"):
                    continue
                if post["id"] > last_id:
                    new_posts.append(post)

            if new_posts:
                new_posts.sort(key=lambda p: p["id"])
                for post in new_posts:
                    print_post(group_name, post)
                    last_posts[group_key] = post["id"]
            else:
                print(f"😴 [{group_name}] новых постов нет")

        save_state(last_posts)

    except Exception as e:
        print(f"❌ Ошибка: {e}")

    time.sleep(CHECK_INTERVAL)
