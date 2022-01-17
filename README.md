# Quest Synth Sync

This application synchronizes playlists from SynthRiderz with your local Synth Riders game.  This app was initially created since there was no real easy Quest-based song syncing for Synth Riders and also due to the existence of my existing Quest-Beast-Sync codebase (just used that as a template).

![Android Build](https://github.com/KyujuuAlpha/Quest-Synth-Sync/actions/workflows/build-android.yml/badge.svg)

## Features

- Multi-playlist syncing support

## Known Bugs
- Text deletion in the user input field is broken because of Android.  A workaround is to select the existing text and type over it.

## Usage

1. Open the application under the `Unknown Sources` section on your Quest.
2. Set the playlist id to whatever SynthRiderz playlist you want to synchronize (this does not delete local levels).  For multiple playlists, separate the IDs using commas.  For example: `id1,id2,id3`
3. Click `Synchronize` and wait
4. Open Synth Riders to play!

## Installation

The recommended installation method is by sideloading the APK through SideQuest.  Please follow the instructions on the SideQuest [download page](https://sidequestvr.com/download) if you don't have it installed already.

1. First download the latest APK from the `Actions` tab on this Github page
2. Follow [these instructions](https://learn.adafruit.com/sideloading-on-oculus-quest/install-and-use-sidequest#install-a-custom-apk-3051314-9) on how to sideload the downloaded APK through SideQuest

## License

Quest Synth Sync is released under the MIT License terms.  Please refer to the LICENSE file.

## Credits
- [Kivy](https://kivy.org/#home)
- [KivyMD](https://github.com/kivymd/KivyMD)
- [buildozer-action](https://github.com/ArtemSBulgakov/buildozer-action)
