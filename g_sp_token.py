import requests
import base64

# --- 將這裡替換成您自己的 Client ID 和 Client Secret ---
CLIENT_ID = 'cbe96eee8beb4ad4890359598081983e'
CLIENT_SECRET = '63d25871db4c4b178eb69ec8064b9285'

def get_spotify_token(client_id, client_secret):
    """
    使用 Client Credentials Flow 取得 Spotify API 的 Access Token。
    """
    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    
    try:
        response = requests.post(token_url, headers=headers, data=data)
        
        # --- 新增的偵錯程式碼 ---
        print(f"Token 請求狀態碼: {response.status_code}")
        print(f"Token 請求回覆內容: {response.json()}")
        
        response.raise_for_status()  # 如果請求失敗會拋出異常
        token_data = response.json()
        return token_data['access_token']
    except requests.exceptions.RequestException as e:
        print(f"取得 Access Token 失敗: {e}")
        return None
# def get_spotify_token(client_id, client_secret):
#     """
#     使用 Client Credentials Flow 取得 Spotify API 的 Access Token。
#     """
#     # 組合憑證字串
#     auth_string = f"{client_id}:{client_secret}"
#     # 將憑證字串進行 Base64 編碼
#     auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
#     token_url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": f"Basic {auth_base64}",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {
#         "grant_type": "client_credentials"
#     }
    
#     try:
#         response = requests.post(token_url, headers=headers, data=data)
#         response.raise_for_status()  # 如果請求失敗會拋出異常
#         token_data = response.json()
#         return token_data['access_token']
#     except requests.exceptions.RequestException as e:
#         print(f"取得 Access Token 失敗: {e}")
#         return None

if __name__ == "__main__":
    access_token = get_spotify_token(CLIENT_ID, CLIENT_SECRET)
    if access_token:
        print("成功取得 Access Token！")
        print(f"Access Token: {access_token}")