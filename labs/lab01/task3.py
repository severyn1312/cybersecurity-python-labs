"""Завдання 3: хешування, CSV-база та JSON-логування (варіант 2)."""

import csv
import functools
import hashlib
import hmac
import json
from datetime import datetime
from pathlib import Path

from shared.student import VARIANT_NUMBER

HASH_ALGORITHM = "sha3_224"
MIN_PASSWORD_LENGTH = 10

DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.csv"
LOG_FILE = DATA_DIR / "log.json"

# Персональна сіль: варіант, доповнений зліва нулями до 5 символів
PERSONAL_SALT = str(VARIANT_NUMBER).zfill(5)

users_to_register = (
    ("alice", "Alice#Secure2024"),
    ("bob", "Bob_Strong!Pass1"),
    ("charlie", "Charlie@Pass2024"),
    ("diana", "Diana$Secret77"),
    ("eve", "Eve!Hacker1234"),
    ("frank", "Frank#Admin2024"),
    ("grace", "Grace@Cyber2024"),
    ("heidi", "Heidi$Crypto99"),
    ("ivan", "Ivan#Python2024"),
    ("judy", "Judy@Network2024"),
)

# "База даних" у пам'яті: список кортежів (логін, хеш)
users_db = []


class ValidationError(Exception):
    """Пароль не відповідає вимогам безпеки."""


def generate_hash(password: str, salt: str = "00000") -> str:
    """Повертає шістнадцятковий хеш від password + salt."""
    if not password or not salt:
        raise ValueError("Пароль і сіль не можуть бути порожніми")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            f"Пароль коротший за {MIN_PASSWORD_LENGTH} символів"
        )
    data = (password + salt).encode("utf-8")
    return hashlib.new(HASH_ALGORITHM, data).hexdigest()


def create_user(username, password):
    """Повертає кортеж (username, hash_value)."""
    return username, generate_hash(password, PERSONAL_SALT)


def create_users(users_list):
    """Записує всіх користувачів у users.csv (логін,хеш)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with USERS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for username, password in users_list:
            writer.writerow(create_user(username, password))


def read_users():
    """Зчитує users.csv у список кортежів."""
    with USERS_FILE.open("r", newline="", encoding="utf-8") as file:
        return [tuple(row) for row in csv.reader(file) if row]


def print_users_table(db):
    """Виводить базу користувачів у вигляді таблиці."""
    line = "-" * 75
    print(line)
    print(f"{'Логін':<12}Хеш пароля ({HASH_ALGORITHM})")
    print(line)
    for username, hash_value in db:
        print(f"{username:<12}{hash_value}")
    print(line)


def write_log(entry):
    """Дописує подію до log.json (не ламає програму при помилці)."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with LOG_FILE.open("r", encoding="utf-8") as file:
                events = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            events = []
        events.append(entry)
        with LOG_FILE.open("w", encoding="utf-8") as file:
            json.dump(events, file, ensure_ascii=False, indent=4)
    except PermissionError:
        print("Помилка: немає прав на запис у log.json")
    except OSError as error:
        print(f"Помилка запису журналу: {error}")


def log_event(func):
    """Декоратор: записує кожну спробу входу у log.json."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = "failure"
        try:
            outcome = func(*args, **kwargs)
            result = "success" if outcome else "failure"
            return outcome
        finally:
            user = args[0] if args else kwargs.get("username", "")
            # Пароль у журнал НЕ пишемо - маскуємо
            safe_args = [args[0]] + ["***"] * (len(args) - 1) if args else []
            safe_kwargs = {
                key: ("***" if key == "password" else value)
                for key, value in kwargs.items()
            }
            write_log(
                {
                    "event": "login",
                    "user": user,
                    "result": result,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "args": safe_args,
                    "kwargs": safe_kwargs,
                }
            )

    return wrapper


@log_event
def login(username: str, password: str) -> bool:
    """Перевіряє логін і пароль користувача."""
    if not username or not password:
        raise ValueError("Логін і пароль не можуть бути порожніми")
    expected = dict(users_db).get(username)
    if expected is None:
        return False
    actual = generate_hash(password, PERSONAL_SALT)
    return hmac.compare_digest(expected, actual)


def try_login(username, password):
    """Спроба входу з обробкою винятків і виведенням результату."""
    try:
        ok = login(username, password)
        print(f"login({username!r}) -> {'УСПІХ' if ok else 'ВІДМОВА'}")
    except ValidationError as error:
        print(f"login({username!r}) -> ValidationError: {error}")
    except ValueError as error:
        print(f"login({username!r}) -> ValueError: {error}")


def main():
    """Запускає завдання 3."""
    try:
        create_users(users_to_register)
        users_db.clear()
        users_db.extend(read_users())
    except FileNotFoundError:
        print("Помилка: файл або папку не знайдено")
        return
    except PermissionError:
        print("Помилка: немає прав доступу до файлу")
        return
    except OSError as error:
        print(f"Помилка вводу/виводу: {error}")
        return
    except ValidationError as error:
        print(f"Помилка валідації: {error}")
        return
    except ValueError as error:
        print(f"Некоректні дані: {error}")
        return

    print(f"Сіль: {PERSONAL_SALT}, алгоритм: {HASH_ALGORITHM}")
    print_users_table(users_db)

    print("\nПеревірка автентифікації:")
    try_login("alice", "Alice#Secure2024")  # успіх
    try_login("alice", "WrongPassword123!")  # неправильний пароль
    try_login("nobody", "Some#Password123")  # немає такого користувача
    try_login("bob", "")  # порожній пароль
    try_login("bob", "short")  # закороткий пароль
    print(f"\nЖурнал подій збережено: {LOG_FILE}")


if __name__ == "__main__":
    main()
