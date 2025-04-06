const express = require('express');
const { spawn } = require('child_process');
const app = express();
const PORT = 3000;

app.get('/stream/:videoId', (req, res) => {
  const { videoId } = req.params;
  const url = `https://www.youtube.com/watch?v=${videoId}`;

  res.setHeader('Content-Type', 'audio/mpeg');

  const ytdlp = spawn('yt-dlp', [
    '-f', 'bestaudio',
    '-x',
    '--audio-format', 'mp3',
    '--audio-quality', '0',
    '-o', '-', // send output to stdout
    url
  ]);

  // Pipe yt-dlp's stdout (audio) directly to response
  ytdlp.stdout.pipe(res);

  ytdlp.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  ytdlp.on('error', (err) => {
    console.error('yt-dlp failed to start:', err);
    res.status(500).send('Internal Server Error');
  });

  ytdlp.on('close', (code) => {
    if (code !== 0) {
      console.error(`yt-dlp exited with code ${code}`);
    }
  });
});

app.get('/', (req, res) => {
  res.send('YouTube to MP3 streaming API is running.');
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
