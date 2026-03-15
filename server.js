const express = require("express");
const { spawn } = require("child_process");

const app = express();

app.get("/get-url", (req, res) => {
    const url = req.query.q;

    if (!url) {
        return res.status(400).json({ error: "url missing" });
    }

    const yt = spawn("python", [
        "-m", "yt_dlp",
        "--cookies", "cookies.txt",
        "--force-ipv4",
        "--no-playlist",
        "--extractor-args", "youtube:player_client=android",
        "-f", "ba[ext=m4a]/ba/b",
        "--get-url",
        url
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

        const finalUrl = output.trim().split("\n")[0];
        res.json({ url: finalUrl });
    });
});

app.listen(process.env.PORT || 10000, () => {
    console.log("YT API running");
});