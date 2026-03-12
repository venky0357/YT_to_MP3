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

# ---------------------------
# from fastapi import FastAPI, Query
# from fastapi.responses import JSONResponse
# import subprocess

# app = FastAPI()

# @app.get("/get-url")
# def get_audio_url(q: str = Query(..., description="Search query")):
#     try:
#         command = [
#             "yt-dlp",
#             "--cookies", "cookies.txt",
#             "--extractor-args", "youtube:player_client=web",
#             "--js-runtime", "node",
#             "-f", "bestaudio/best",
#             "--no-playlist",
#             "--get-url",
#             f"ytsearch1:{q}"
#         ]

#         result = subprocess.run(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         if result.returncode != 0:
#             return JSONResponse(
#                 status_code=500,
#                 content={"error": result.stderr.strip()}
#             )

#         url = result.stdout.strip().split("\n")[0]

#         return {"url": url}

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import subprocess

app = FastAPI()

def run_ytdlp(command):
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

@app.get("/get-url")
def get_audio_url(q: str = Query(...)):
    try:
        command = [
            "yt-dlp",
            "--quiet",
            "--no-warnings",
            "-f", "bestaudio",
            "--no-playlist",
            "--get-url",

            # CRITICAL anti-bot flags
            "--extractor-args",
            "youtube:player_client=android_creator,android_embedded,tv_embedded",

            "--add-header",
            "User-Agent:com.google.android.youtube/19.09.37 (Linux; U; Android 11)",

            "--socket-timeout", "20",
            "--retries", "10",
            "--fragment-retries", "10",

            "--default-search", "ytsearch",

            q
        ]

        result = run_ytdlp(command)

        if result.returncode != 0:
            return JSONResponse(
                status_code=500,
                content={"error": result.stderr.strip()}
            )

        url = result.stdout.strip().split("\n")[0]

        return {"url": url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
