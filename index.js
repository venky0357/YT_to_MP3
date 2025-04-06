const express = require('express');
const ytdl = require('ytdl-core');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());

app.get('/api/yt-to-mp3', async (req, res) => {
  const videoUrl = req.query.url;
  if (!videoUrl) {
    return res.status(400).json({ error: 'Missing YouTube URL' });
  }

  try {
    const info = await ytdl.getInfo(videoUrl);

    // Filter out only audio formats
    const audioFormats = ytdl.filterFormats(info.formats, 'audioonly');
    const bestAudio = audioFormats.find(format => format.mimeType.includes('audio/webm') || format.mimeType.includes('audio/mp4'));

    if (!bestAudio || !bestAudio.url) {
      return res.status(500).json({ error: 'No playable audio stream found' });
    }

    res.json({
      audio_url: bestAudio.url
    });
  } catch (err) {
    console.error('Error extracting audio:', err.message);
    res.status(500).json({ error: 'Failed to get audio URL' });
  }
});

app.listen(port, () => {
  console.log(`🚀 Server running on port ${port}`);
});
