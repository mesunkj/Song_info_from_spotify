import requests
import base64
from g_sp_token import  CLIENT_ID, CLIENT_SECRET

# === 請換成你自己的 Client ID 和 Secret ===
# CLIENT_ID = "你的 Client ID"
# CLIENT_SECRET = "你的 Client Secret"

# Step 1: 取得 access token
auth_url = "https://accounts.spotify.com/api/token"
auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

token_response = requests.post(
    auth_url,
    headers={"Authorization": f"Basic {auth_header}"},
    data={"grant_type": "client_credentials"}
)

if token_response.status_code != 200:
    raise Exception("無法取得 Token", token_response.text)

access_token = token_response.json()["access_token"]
print("取得 Token:", access_token)

# Step 2: 查詢 audio-features
track_id = "3Gl0Y21R2b5fPPxge18pTu"  # 周華健〈朋友〉
api_url = f"https://api.spotify.com/v1/audio-features/{track_id}"

response = requests.get(
    api_url,
    headers={"Authorization": f"Bearer {access_token}"}
)

if response.status_code == 200:
    print("音樂特徵資料：")
    print(response.json())
else:
    print("查詢失敗:", response.status_code, response.text)
