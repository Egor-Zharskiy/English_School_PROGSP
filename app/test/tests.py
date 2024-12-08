import httpx
import pytest
from app.services.users import email_validator
from fastapi.testclient import TestClient
from app.main import app
from app.services.users import check_grade


@pytest.mark.asyncio
@pytest.mark.parametrize("email, expected", [
    ("user@example.com", False),
    ("user@gmail.com", True),
    ("invalid-email", False),
    ("user@.com", False),
    ("user@example", False),
    ("valid.user+tag@gmail.com", True),
    ("", False),
    ("a" * 320 + "@example.com", False),
    ("user@valid-domain.com", True),
    ("test@invalid_domain", False),
])
async def test_validate_email(email, expected):
    result = await email_validator(email)
    assert result == expected


client = TestClient(app)


@pytest.fixture
def valid_user():
    return {
        "email": "test@mail.ru",
        "username": "testuser",
        "password": "testpassword",
        "phone_number": "+375293400698",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.mark.asyncio
async def test_login_valid_data():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/jwt/login",
            data={
                "username": "admin@mail.ru",
                "password": "admin"
            }
        )

    print(response.text)

    assert response.status_code == 200

    response_data = response.json()
    print(response_data)
    assert "access_token" in response_data
    assert isinstance(response_data["access_token"], str)


@pytest.mark.asyncio
async def test_check_grade_valid_int_in_range():
    assert await check_grade(5) is True
    assert await check_grade(0) is True
    assert await check_grade(10) is True


@pytest.mark.asyncio
async def test_check_grade_invalid_int_out_of_range():
    assert await check_grade(-1) is False
    assert await check_grade(11) is False


@pytest.mark.asyncio
async def test_check_grade_invalid_types():
    assert await check_grade(5.5) is False
    assert await check_grade("5") is False
    assert await check_grade(None) is False
    assert await check_grade([5]) is False
    assert await check_grade({"grade": 5}) is False
