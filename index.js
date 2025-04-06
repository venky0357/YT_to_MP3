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

    const format = ytdl.chooseFormat(info.formats, {
      filter: 'audioonly',
      quality: 'highestaudio'
    });

    if (!format || !format.url) {
      return res.status(500).json({ error: 'Unable to extract audio URL' });
    }

    res.json({ audio_url: format.url }); // 🎯 This is the direct playable URL
  } catch (err) {
    console.error('Error extracting audio:', err);
    res.status(500).json({ error: 'Failed to get audio URL' });
  }
});

app.listen(port, () => {
  console.log(`🚀 Server running on port ${port}`);
});
