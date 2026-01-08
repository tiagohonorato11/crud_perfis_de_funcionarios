import requests

BASE_URL = "http://localhost:8000"

def test_login():
    print("Tentando login via script...")
    login_data = {"username": "admin", "password": "admin123"}
    try:
        resp = requests.post(f"{BASE_URL}/login", data=login_data)
        print(f"Status Code: {resp.status_code}")
        print(f"Response Body: {resp.text}")
    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    test_login()
