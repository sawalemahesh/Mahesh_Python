import pytest
# from login_module import login   # ✅ IMPORTANT LINE


def login(username, password):
    valid_users = {
        "admin": "admin123",
        "user": "user123"
    }
    if username in valid_users and valid_users[username] == password:
        return "Success"
    return "Fail"

@pytest.fixture
def login_data():
    return [
        ("admin", "admin123", "Success"),
        ("user", "user123", "Success"),
        ("admin", "wrongpass", "Fail"),
        ("wronguser", "admin123", "Fail"),
        ("", "", "Fail")
    ]

@pytest.mark.parametrize("username,password,expected", [
    ("admin", "admin123", "Success"),
    ("user", "user123", "Success"),
    ("admin", "wrongpass", "Fail"),
    ("wronguser", "admin123", "Fail"),
    ("", "", "Fail")
])
def test_login(username, password, expected):
    assert login(username, password) == expected