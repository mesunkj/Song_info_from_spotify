import requests
import base64
import urllib3
# from g_sp_token import  CLIENT_ID, CLIENT_SECRET
from g_sp_token import get_spotify_token, CLIENT_ID, CLIENT_SECRET
# 關閉 SSL 驗證警告 (等同 curl 的 --insecure)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# === 請換成你自己的 Client ID 和 Secret ===
# CLIENT_ID = "你的 Client ID"
# CLIENT_SECRET = "你的 Client Secret"

# Step 1: 取得 Access Token
def get_access_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    token_response = requests.post(
        auth_url,
        headers={"Authorization": f"Basic {auth_header}"},
        data={"grant_type": "client_credentials"},
        verify=False  # 等同 --insecure
    )

    if token_response.status_code != 200:
        raise Exception("無法取得 Token", token_response.text)

    return token_response.json()["access_token"]

# Step 2: 搜尋歌曲
def search_tracks(query, access_token):
    url = "https://api.spotify.com/v1/search"
    params = {"q": query, "type": "track", "limit": 10}
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        params=params,
        verify=False
    )
    if response.status_code != 200:
        raise Exception("搜尋失敗", response.text)
    return response.json()["tracks"]["items"]

# Step 3: 測試 audio-features
def get_audio_features(track_id, access_token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        verify=False
    )
    return response.status_code, response.json()

# 主流程
if __name__ == "__main__":
    # 取得 access token
    token = get_access_token()
    print("取得 Token:", token)

    # 搜尋歌曲 "朋友 周華健"
    tracks = search_tracks('track:朋友 artist:周華健', token)

    # 逐一測試每個 track ID
    for t in tracks:
        name = t["name"]
        track_id = t["id"]
        spotify_url = t["external_urls"]["spotify"]

        status, data = get_audio_features(track_id, token)
        if status == 200:
            print(f"[OK] {name} ({spotify_url})")
            print("  Audio Features:", data)
        else:
            print(f"[FAIL] {name} ({spotify_url}) -> 狀態碼 {status}")

