import random

from shared.student import STUDENT_NAME, VARIANT_NUMBER

PASSWORDS = [
    "Hello123!",
    "simple",
    "CompL3x@Pass",
    "password",
    "Str0ng#2023",
    "weak",
    "MySecur3!",
    "12345",
    "Advanced@1",
    "basic",
]
CRITERIA = {
    "min_length": 10,
    "require_digits": True,
    "require_upper": True,
    "require_special": True,
}
FORBIDDEN_PASSWORDS = {
    "password",
    "simple",
    "weak",
    "basic",
    "12345",
    "hello",
}


def add_random_duplicates(passwords, count=3):
    result = list(passwords)
    for index in random.sample(range(len(passwords)), count):
        result.append(passwords[index])
    return result


def evaluate_password(password, all_passwords, criteria, forbidden):
    min_length = criteria["min_length"]

    if password.lower() in forbidden or len(password) < min_length:
        return "Заборонений"

    has_digit = any(ch.isdigit() for ch in password)
    has_upper = any(ch.isupper() for ch in password)
    has_special = any(not ch.isalnum() for ch in password)

    met = sum([has_digit, has_upper, has_special])

    if met == 3:
        is_long = len(password) >= min_length + 4
        is_unique = all_passwords.count(password) == 1
        if is_long and is_unique:
            return "Дуже сильний"
        return "Сильний"
    if met == 2:
        return "Середній"
    return "Слабкий"


def print_table(passwords, results):
    line = "-" * 56
    print(line)
    print(f"{'№':<4}{'Пароль':<22}{'Довжина':<10}{'Результат'}")
    print(line)
    for number, (password, result) in enumerate(
        zip(passwords, results), start=1
    ):
        print(f"{number:<4}{password:<22}{len(password):<10}{result}")
    print(line)


def main():
    print(f"Студент: {STUDENT_NAME}, варіант {VARIANT_NUMBER}")
    passwords = add_random_duplicates(PASSWORDS, 3)
    print(f"Додано дублікати, всього паролів: {len(passwords)}")

    results = [
        evaluate_password(p, passwords, CRITERIA, FORBIDDEN_PASSWORDS)
        for p in passwords
    ]
    print_table(passwords, results)


if __name__ == "__main__":
    main()
