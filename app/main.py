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

app = FastAPI()

@app.get("/get-url")
def get_audio_url(q: str = Query(..., description="Search query")):
    try:
        command = [
            "yt-dlp",
            "--cookies", "app/cookies.txt",
            "-f", "bestaudio[acodec!=none]/bestaudio",
            "-g",
            f"ytsearch1:{q}",
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "yt-dlp failed",
                    "stderr": result.stderr.strip(),
                    "stdout": result.stdout.strip(),
                },
            )

        url = result.stdout.strip().split("\n")[0]
        return {"url": url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
