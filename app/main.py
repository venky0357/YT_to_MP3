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
def get_audio_url(q: str = Query(..., description="Search query")):
    try:
        command = [
            "yt-dlp",
            "-f", "bestaudio",
            "--no-playlist",
            "--get-url",
            "--quiet",
            "--no-warnings",
            "--extractor-args",
            "youtube:player_client=android,ios,tv",
            "--socket-timeout", "15",
            "--retries", "5",
            "--fragment-retries", "5",
            "--skip-unavailable-fragments",
            "--geo-bypass",
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
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
