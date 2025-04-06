const express = require("express");
const ytdl = require("ytdl-core");
const ffmpeg = require("fluent-ffmpeg");
const app = express();

app.get("/api/audio", async (req, res) => {
  const videoId = req.query.videoId;

  if (!videoId) {
    return res.status(400).json({ error: "Missing videoId parameter" });
  }

  const videoURL = `https://www.youtube.com/watch?v=${videoId}`;

  try {
    const info = await ytdl.getInfo(videoURL);
    const title = info.videoDetails.title.replace(/[^\w\s]/gi, "");

    res.setHeader("Content-Disposition", `attachment; filename="${title}.mp3"`);
    res.setHeader("Content-Type", "audio/mpeg");

    const audioStream = ytdl(videoURL, { quality: "highestaudio" });

    ffmpeg(audioStream)
      .audioBitrate(128)
      .format("mp3")
      .pipe(res, { end: true });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to process video" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
