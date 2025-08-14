import requests
import time
from g_sp_token import get_spotify_token, CLIENT_ID, CLIENT_SECRET

# 這裡放入您之前分析的 100 首歌曲清單
# 為了範例簡潔，我只放入幾首
songs_to_analyze = [
    '范瑋琪 - 可不可以不勇敢',
    '周華健 - 朋友',
    'The Beach Boys - Fun, Fun, Fun',
    'Christina Perri - A Thousand Years',
    '孫燕姿 - 天黑黑'
]

def search_track(track_name, artist, access_token):
    """
    在 Spotify 中搜尋歌曲並返回歌曲 ID。
    """
    # search_url = "https://api.spotify.com/v1/search"
    search_url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    print("DEBUG: headers =", headers)  # 新增這行
    # 組合搜尋 query
    query = f"track:{track_name} artist:{artist}"
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }
    
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            return track['id'], track['name'], track['artists'][0]['name']
        return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"搜尋 {track_name} 失敗: {e}")
        return None, None, None

def get_audio_features(track_id, access_token):
    """
    根據歌曲 ID 取得其音訊特徵。
    """
    # features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    print(f"DEBUG: audio-features url = {features_url}")
    print(f"DEBUG: headers = {headers}")
    try:
        response = requests.get(features_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"取得音訊特徵失敗: {e}")
        return None

if __name__ == "__main__":
    # 1. 取得 Access Token
    access_token = get_spotify_token(CLIENT_ID, CLIENT_SECRET)
    if not access_token:
        print("無法繼續，請檢查您的 Client ID 和 Client Secret。")
    else:
        time.sleep(10)  # 確保 token 已經生效
        print("--- 開始處理歌曲列表 ---")
        
        music_data = []
        for song_entry in songs_to_analyze:
            # 簡單地將歌曲名和歌手分開，這裡需要根據您的實際格式調整
            parts = song_entry.split(' - ')
            track_name = parts[1] if len(parts) > 1 else parts[0]
            artist = parts[0] if len(parts) > 1 else ''
            
            print(f"正在處理: {track_name} by {artist}...")
            
            # 2. 搜尋歌曲
            track_id, found_name, found_artist = search_track(track_name, artist, access_token)
            
            if track_id:
                # 3. 取得音訊特徵
                features = get_audio_features(track_id, access_token)
                if features:
                    print(f"  成功找到歌曲: {found_name} - {found_artist}")
                    
                    # 4. 儲存數據
                    song_info = {
                        'original_name': song_entry,
                        'found_name': found_name,
                        'artist': found_artist,
                        'id': track_id,
                        'tempo_bpm': features.get('tempo'),
                        'energy': features.get('energy'),
                        'valence': features.get('valence'),
                        'danceability': features.get('danceability'),
                        'acousticness': features.get('acousticness'),
                    }
                    music_data.append(song_info)
                
            # 為了避免 API 限制，每次請求後稍作延遲
            time.sleep(1)
        
        # 輸出所有獲取的數據
        print("\n--- 數據獲取完成 ---")
        for data in music_data:
            print(f"歌曲: {data['original_name']}")
            print(f"  BPM: {data['tempo_bpm']}")
            print(f"  能量 (Energy): {data['energy']}")
            print(f"  歡樂度 (Valence): {data['valence']}")
            print(f"  舞動性 (Danceability): {data['danceability']}\n")
        # 將 music_data 儲存到 JSON 檔案
        import json
        with open("music_data.json", "w", encoding="utf-8") as f:
            json.dump(music_data, f, ensure_ascii=False, indent=2)
        print("已將 music_data 儲存到 music_data.json")
        print("--- 結束處理歌曲列表 ---")        