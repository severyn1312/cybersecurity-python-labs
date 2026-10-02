"""Завдання 2: багаторівнева система контролю доступу (варіант 2)."""

USERS = {
    "sysadmin02": {
        "role": "system_admin",
        "clearance": 4,
        "department": "Infrastructure",
        "active": True,
    },
    "analyst234": {
        "role": "security_analyst",
        "clearance": 3,
        "department": "SOC",
        "active": True,
    },
    "developer567": {
        "role": "developer",
        "clearance": 2,
        "department": "Development",
        "active": True,
    },
    "intern890": {
        "role": "intern",
        "clearance": 1,
        "department": "HR",
        "active": True,
    },
    "external123": {
        "role": "external",
        "clearance": 1,
        "department": "Vendor",
        "active": False,
    },
}
RESOURCES = [
    ("prod_database", 4),
    ("dev_environment", 2),
    ("documentation", 1),
    ("source_code", 3),
    ("server_configs", 4),
    ("test_data", 2),
    ("compliance_docs", 3),
    ("system_logs", 4),
    ("project_files", 2),
    ("public_wiki", 1),
]
SECURITY_LEVELS = ("Open", "Internal", "Restricted", "Top Secret")
BLOCKED_USERS = {"external123", "old_account", "test_user"}


def check_access(username, resource_level):
    """Повертає кортеж (дозволено?, причина відмови)."""
    if username not in USERS:
        return False, "User not found"
    if username in BLOCKED_USERS:
        return False, "User is blocked"
    user = USERS[username]
    if not user["active"]:
        return False, "Account inactive"
    if user["clearance"] >= resource_level:
        return True, ""
    return False, "Insufficient clearance"


def print_resources():
    """Виводить ресурси з текстовими назвами рівнів безпеки."""
    print("Ресурси системи:")
    for name, level in RESOURCES:
        print(f"  {name:<18} -> {SECURITY_LEVELS[level - 1]}")


def main():
    """Запускає завдання 2."""
    print_resources()
    print("\nПеревірка доступу:")
    # Додатково перевіряємо двох користувачів, яких немає в словнику
    usernames = list(USERS) + ["old_account", "unknown_user"]
    for username in usernames:
        for resource_name, level in RESOURCES:
            allowed, reason = check_access(username, level)
            if allowed:
                verdict = "ALLOW"
            else:
                verdict = f"DENY ({reason})"
            print(f"user={username} resource={resource_name} -> {verdict}")


if __name__ == "__main__":
    main()
