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

def run_cmd(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

@app.get("/get-url")
def get_audio_url(q: str = Query(...)):
    try:
        # STEP 1: get video id first
        search_cmd = [
            "yt-dlp",
            "--get-id",
            "--default-search", "ytsearch1",
            "--quiet",
            q
        ]

        search = run_cmd(search_cmd)

        if search.returncode != 0 or not search.stdout.strip():
            return JSONResponse(status_code=500, content={"error": "Search failed"})

        video_id = search.stdout.strip().split("\n")[0]

        # STEP 2: extract audio url
        extract_cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "--get-url",
            "--quiet",
            "--no-warnings",
            "--extractor-args",
            "youtube:player_client=android_embedded,tv_embedded",
            f"https://youtube.com/watch?v={video_id}"
        ]

        extract = run_cmd(extract_cmd)

        if extract.returncode != 0 or not extract.stdout.strip():
            return JSONResponse(status_code=500, content={"error": "Extraction failed"})

        url = extract.stdout.strip().split("\n")[0]

        return {"url": url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

        return {"url": url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
