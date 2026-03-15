from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import subprocess

app = FastAPI()

@app.get("/get-url")
def get_audio_url(q: str = Query(..., description="Search query")):
    try:
        command = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "--no-playlist",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "-f", "bestaudio",
            "--get-url",
            f"ytsearch1:{q}"
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "yt-dlp failed",
                    "details": result.stderr
                }
            )

        urls = result.stdout.strip().split("\n")

        if not urls or urls[0] == "":
            return JSONResponse(
                status_code=404,
                content={"error": "No audio URL found"}
            )

        return {"url": urls[0]}

    except subprocess.TimeoutExpired:
        return JSONResponse(
            status_code=500,
            content={"error": "yt-dlp timeout"}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
