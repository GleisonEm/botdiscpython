const express = require("express");
const ytdl = require("ytdl-core");
const fs = require("fs");

const app = express();
const PORT = process.env.PORT || 3000;

app.get("/download", async (req, res) => {
  try {
    const videoUrl = req.query.url;

    // Download stream with ytdl-core-discord
    const stream = await ytdl(videoUrl, {
      filter: "audioonly",
      quality: "highestaudio",
    });

    res.setHeader("Content-Type", "audio/mpeg");
    res.setHeader("Content-Disposition", 'attachment; filename="audio.mp3"');

    stream.pipe(res, { end: true });
  } catch (error) {
    console.error(error);
    res.status(500).send("Internal Server Error");
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
