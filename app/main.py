# from fastapi import FastAPI, Query
# from fastapi.responses import JSONResponse
# import subprocess

# app = FastAPI()

# @app.get("/get-url")
# def get_audio_url(q: str = Query(..., description="Search query")):
#     try:
#         command = ["yt-dlp","--cookies", "cookies.txt", "-f", "bestaudio", "--get-url", f"ytsearch:{q}"]
#         result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

#         if result.returncode != 0:
#             return JSONResponse(status_code=500, content={"error": result.stderr.strip()})

#         url = result.stdout.strip().split("\n")[0]
#         return {"url": url}

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})



from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import subprocess
import json
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

CACHE_FILE = "cached_songs.json"
TOP_SONGS = [
    "Bujji Thalli",
    "Godari Kattu Meedha",
    "Chuttamalle",
    "Hey Rangule",
    "Sooseki",
    "Ammayi",
    "Nenu Nuvvantu",
    "Ayudha Pooja",
    "College Papa",
    "Evarevaro",
    "Meenu",
    "Hilesso Hilessa",
    "Peelings",
    "Fear Song",
    "Blockbuster Pongal",
    "Kissik",
    "Dabidi Dibidi",
    "Buttabomma",
    "Ramuloo Ramulaa",
    "Kurchi Madatha Petti",
    "Oo Antava Oo Oo Antava",
    "Bullettu Bandi",
    "Saranga Dariya",
    "Vachinde",
    "Jigelu Rani",
    "Pillaa Raa",
    "iSmart Title Song",
    "Inkem Inkem Kavaalee",
    "Choosi Choodamgaane",
    "Minnalvala"
]

# -------------- CACHE HANDLING ------------------

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

# -------------- FETCH FROM YOUTUBE ------------------

def fetch_song_url(song_name):
    command = [
        "yt-dlp", "--cookies", "cookies.txt",
        "-f", "bestaudio", "--get-url", f"ytsearch:{song_name}"
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(result.stderr.strip())
    return result.stdout.strip().split("\n")[0]

# -------------- DAILY PREFETCH ------------------

def update_daily_cache():
    print(f"🔄 Updating daily cache at {datetime.now()}")
    cache = {}
    for song in TOP_SONGS:
        try:
            url = fetch_song_url(song)
            cache[song.lower()] = {
                "url": url,
                "cached_at": str(datetime.now())
            }
            print(f"✅ Cached: {song}")
        except Exception as e:
            print(f"❌ Failed to cache {song}: {e}")
    save_cache(cache)
    print("✅ Daily cache updated!")

# -------------- SCHEDULER ------------------

scheduler = BackgroundScheduler()
scheduler.add_job(update_daily_cache, "interval", days=1)
scheduler.start()

# Run once on startup
update_daily_cache()

# -------------- API ENDPOINT ------------------

@app.get("/get-url")
def get_audio_url(q: str = Query(..., description="Search query")):
    try:
        cache = load_cache()
        query_lower = q.lower()

        # ✅ If already cached → return instantly
        if query_lower in cache:
            return {"url": cache[query_lower]["url"], "source": "cache"}

        # ❌ Not cached → fetch live
        url = fetch_song_url(q)

        # ✅ Save newly searched song to cache for next time
        cache[query_lower] = {
            "url": url,
            "cached_at": str(datetime.now())
        }
        save_cache(cache)

        return {"url": url, "source": "live"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
