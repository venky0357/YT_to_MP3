const express = require('express');
const youtubedl = require('youtube-dl-exec');
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
    const process = youtubedl.exec(videoUrl, {
      extractAudio: true,
      audioFormat: 'mp3',
      audioQuality: 0,
      output: '-',
      quiet: true,
    });

    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Content-Disposition', 'inline; filename="audio.mp3"');

    process.stdout.pipe(res);

    process.stdout.on('end', () => {
      console.log('✅ Audio stream finished.');
    });

    process.stderr.on('data', (data) => {
      console.error('stderr:', data.toString());
    });

    process.on('error', (err) => {
      console.error('Streaming error:', err);
      res.status(500).send('Failed to stream audio');
    });
  } catch (err) {
    console.error('Download error:', err);
    res.status(500).send('Failed to convert video to MP3');
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
