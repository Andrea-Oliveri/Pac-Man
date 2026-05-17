## Generating the Reference Gameplay Video

Reference videos for the comparison are not provided as part of the repository due to their large size. This README explains how to create them yourself.

### Requirements

To run the commands below, you will need:

- `MAME 0.257`
- A Pac-Man ROM compatible with `MAME 0.257`
- `ffmpeg`


## Steps

### 0) Setup

#### 0.1) Check your MAME version

In this guide we are going to assume you use `MAME 0.257`. You can check the version like so:
```bash
mame.exe -version
```

#### 0.2) Configure MAME

Place the Pac-Man ROM inside the `roms` folder of your MAME installation so that MAME can locate it correctly:

```text
mame0257/
├── roms/
│   └── pacman.zip
├── mame.exe
└── ...
```

Then create a folder called `inp` if it doesn't already exist in the folder of your MAME installation:

```text
mame0257/
├── roms/
├── inp/
├── mame.exe
└── ...
```

### 1) Obtain a MAME `.inp` file

You will need to record a game in a `.inp` file. You can either play a game yourself, using the following command:

```bash
mame.exe pacman -record pacman_reference_game.inp
```

or use the `pacman_reference_game.inp` provided in this folder, by copying it to the `inp` folder we created in step 0.1.

**Warning:** `.inp` files are tied to specific version of MAME. So if you were not able to find exactly `MAME 0.257` the provided `.inp` file will likely not work in the next steps.

*Heartfelt thanks to [TwinGalaxies.com](https://www.twingalaxies.com/games/leaderboard-details/pac-man/mame) and the gamer who submitted this run for the provided `.inp` file.*

### 2) Generate the raw reference video

Once the `.inp` file has been placed inside the `inp` folder, run the following command from the same directory as `mame.exe`:

```bash
mame.exe pacman -playback pacman_reference_game.inp -nothrottle -nosleep -video none -sound none -str 0 -aviwrite pacman_reference_game.avi
```

This replays the recorded game deterministically and generates a raw AVI video file. You can find the video inside of the `snap` folder of your MAME installation.

**Warning:** The generated AVI file can be extremely large! For the reference file, it will require roughly 131 GB of free disk space!

### 3) Compress the video using FFmpeg

After the AVI file has been generated successfully, run:

```bash
ffmpeg.exe -i pacman_reference_game.avi -c:v libx265 -x265-params lossless=1 -preset ultrafast -c:a flac pacman_reference_game.mkv
```

This converts the raw AVI file into a lossless compressed MKV video, taking up much less space.

**Note:** you may want to crop the `.avi` file so it starts and ends whenever you want. You can do so by adding `-ss xx:xx:xx -t xx:xx:xx` to the command above. For instance for the provided `.inp` file I reccomend:

```bash
ffmpeg.exe -i pacman_reference_game.avi -ss 00:00:05 -to 03:16:22 -c:v libx265 -x265-params lossless=1 -preset ultrafast -c:a flac pacman_reference_game.mkv
```

### 4) Cleanup

After verifying that the .mkv file was generated correctly, the large temporary `.avi` file can safely be deleted.
