// const express = require('express');
// const { spawn } = require('child_process');
// const path = require('path');
// const app = express();
// const PORT = 3000;

// app.get('/stream/:videoId', (req, res) => {
//   const { videoId } = req.params;
//   const url = `https://www.youtube.com/watch?v=${videoId}`;

//   res.setHeader('Content-Type', 'audio/mpeg');

//   const ytdlp = spawn('yt-dlp', [
//     '--cookies', path.join(__dirname, 'cookies.txt'), // ✅ using the cookie file
//     '-f', 'bestaudio',
//     '-x',
//     '--audio-format', 'mp3',
//     '--audio-quality', '0',
//     '-o', '-', // stream to stdout
//     url
//   ]);

//   ytdlp.stdout.pipe(res);

//   ytdlp.stderr.on('data', (data) => {
//     console.error(`stderr: ${data}`);
//   });

//   ytdlp.on('error', (err) => {
//     console.error('yt-dlp failed to start:', err);
//     res.status(500).send('Internal Server Error');
//   });

//   ytdlp.on('close', (code) => {
//     if (code !== 0) {
//       console.error(`yt-dlp exited with code ${code}`);
//     }
//   });
// });

// app.get('/', (req, res) => {
//   res.send('YouTube to MP3 streaming API is running.');
// });

// app.listen(PORT, () => {
//   console.log(`Server running at http://localhost:${PORT}`);
// });

const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const tmp = require('tmp');
const { createClient } = require('@supabase/supabase-js');

const app = express();
const PORT = 3000;

// Supabase config
const supabase = createClient(
  'https://htiqqxnpmiqbymxvaunh.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh0aXFxeG5wbWlxYnlteHZhdW5oIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODMyNDEzNywiZXhwIjoyMDUzOTAwMTM3fQ.I1ILBmrp_eWKMabHlZqTSFqjs3D20UnZfhRrxHkOMWM'
);

app.get('/stream/:videoId', async (req, res) => {
  const { videoId } = req.params;
  const url = `https://www.youtube.com/watch?v=${videoId}`;

  // Create a temporary file
  const tempFile = tmp.fileSync({ postfix: '.mp3' });
  const outputPath = tempFile.name;

  const ytdlp = spawn('yt-dlp', [
    '--cookies', path.join(__dirname, 'cookies.txt'),
    '-f', 'bestaudio',
    '-x',
    '--audio-format', 'mp3',
    '--audio-quality', '0',
    '-o', outputPath,
    url
  ]);

  ytdlp.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  ytdlp.on('error', (err) => {
    console.error('yt-dlp failed to start:', err);
    res.status(500).send('Download failed');
  });

  ytdlp.on('close', async (code) => {
    if (code !== 0) {
      return res.status(500).send('yt-dlp failed');
    }

    // Upload to Supabase
    const fileStream = fs.createReadStream(outputPath);
    const { error: uploadError } = await supabase.storage
      .from('audios')
      .upload(`${videoId}.mp3`, fileStream, {
        contentType: 'audio/mpeg',
        upsert: true,
      });

    fs.unlinkSync(outputPath); // delete temp file

    if (uploadError) {
      console.error('Supabase upload error:', uploadError);
      return res.status(500).send('Upload failed');
    }

    const { data: urlData } = supabase.storage
      .from('audios')
      .getPublicUrl(`${videoId}.mp3`);

    res.json({ publicUrl: urlData.publicUrl });
  });
});

app.get('/', (req, res) => {
  res.send('YouTube to MP3 streaming + Supabase upload API is running.');
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
