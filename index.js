const express = require('express');
const ytdl = require('ytdl-core');
const ffmpeg = require('fluent-ffmpeg');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());

const streamMap = {}; // Store mapping from ID to YouTube URL

// Step 1: Request audio -> returns a streaming URL
app.get('/api/yt-to-mp3', async (req, res) => {
  const videoUrl = req.query.url;
  if (!videoUrl) return res.status(400).json({ error: 'Missing YouTube URL' });

  const streamId = uuidv4();
  streamMap[streamId] = videoUrl;

  const audioUrl = `${req.protocol}://${req.get('host')}/stream/${streamId}`;
  res.json({ audio_url: audioUrl });

  // Optional cleanup after 10 mins
  setTimeout(() => delete streamMap[streamId], 10 * 60 * 1000);
});

// Step 2: Access audio via returned URL
app.get('/stream/:id', async (req, res) => {
  const videoUrl = streamMap[req.params.id];
  if (!videoUrl) return res.status(404).send('Stream expired or not found');

  try {
    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Content-Disposition', 'inline; filename="audio.mp3"');

    const stream = ytdl(videoUrl, { quality: 'highestaudio' });

    ffmpeg(stream)
      .audioBitrate(128)
      .format('mp3')
      .on('error', (err) => {
        console.error('FFmpeg error:', err);
        res.status(500).send('Stream error');
      })
      .pipe(res, { end: true });

  } catch (err) {
    console.error('Stream fetch error:', err);
    res.status(500).send('Failed to stream audio');
  }
});

app.listen(port, () => {
  console.log(`🚀 Server running on port ${port}`);
});
