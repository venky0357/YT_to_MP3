const express = require("express");
const { spawn } = require("child_process");

const app = express();

app.get("/get-url", (req, res) => {
    const q = req.query.q;

    if (!q) {
        return res.status(400).json({ error: "query missing" });
    }

    const yt = spawn("python3", [
        "-m", "yt_dlp",
        "--cookies", "cookies.txt",
        "--force-ipv4",
        "--no-playlist",
        "--extractor-args", "youtube:player_client=web_safari",
        "-f", "ba[ext=m4a]/ba/b",
        "--get-url",
        `ytsearch1:${q}`
    ]);

    let output = "";
    let error = "";

    yt.stdout.on("data", d => output += d.toString());
    yt.stderr.on("data", d => error += d.toString());

    yt.on("close", code => {
        if (code !== 0) {
            return res.status(500).json({
                error: "yt-dlp failed",
                details: error
            });
        }

        const url = output.trim().split("\n")[0];

        if (!url) {
            return res.status(404).json({ error: "No audio URL found" });
        }

        res.json({ url });
    });
});

app.listen(process.env.PORT || 10000, () => {
    console.log("YT API running");
});