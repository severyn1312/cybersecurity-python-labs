"""Головний файл лабораторної роботи №1: запуск усіх завдань."""

import sys
from pathlib import Path

# Додаємо корінь репозиторію в шлях пошуку, щоб бачити папку shared
sys.path.append(str(Path(__file__).resolve().parents[2]))

from labs.lab01 import task1, task2, task3  # noqa: E402
from shared.student import (  # noqa: E402
    GROUP_NAME,
    STUDENT_NAME,
    VARIANT_NUMBER,
)


def main():
    """Послідовно запускає завдання 1, 2 і 3."""
    print(f"{STUDENT_NAME} | {GROUP_NAME} | варіант {VARIANT_NUMBER}")
    for number, task in enumerate((task1, task2, task3), start=1):
        print(f"\n{'=' * 20} ЗАВДАННЯ {number} {'=' * 20}")
        task.main()


if __name__ == "__main__":
    main()
