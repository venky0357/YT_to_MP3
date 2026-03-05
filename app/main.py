# # from fastapi import FastAPI, Query
# # from fastapi.responses import JSONResponse
# # import subprocess

# # app = FastAPI()

# # @app.get("/get-url")
# # def get_audio_url(q: str = Query(..., description="Search query")):
# #     try:
# #         command = ["yt-dlp","--cookies", "cookies.txt", "-f", "bestaudio", "--get-url", f"ytsearch:{q}"]
# #         result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# #         if result.returncode != 0:
# #             return JSONResponse(status_code=500, content={"error": result.stderr.strip()})

# #         url = result.stdout.strip().split("\n")[0]
# #         return {"url": url}

# #     except Exception as e:
# #         return JSONResponse(status_code=500, content={"error": str(e)})
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
import requests
import time

app = FastAPI()

GITHUB_TOKEN = "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"
OWNER = "venky0357"
REPO = "GITHub_MP3_workflowr"
WORKFLOW = "extract.yml"

def trigger_workflow(query):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW}/dispatches"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "ref": "main",
        "inputs": {
            "query": query
        }
    }

    requests.post(url, headers=headers, json=data)


def get_latest_run():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    r = requests.get(url, headers=headers).json()

    return r["workflow_runs"][0]["id"]


def get_logs(run_id):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}/logs"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    r = requests.get(url, headers=headers)

    text = r.text

    for line in text.split("\n"):
        if "googlevideo.com" in line:
            return line.strip()

    return None


@app.get("/get-url")
def get_audio_url(q: str = Query(...)):
    try:
        trigger_workflow(q)

        time.sleep(10)

        run_id = get_latest_run()

        time.sleep(10)

        url = get_logs(run_id)

        if not url:
            return JSONResponse(status_code=500, content={"error": "Extraction failed"})

        return {"url": url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})