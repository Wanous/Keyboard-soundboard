# SoundBoard

A lightweight desktop soundboard built with CustomTkinter.

SoundBoard allows you to play sounds using customizable keyboard shortcuts and send them directly through your microphone using VB-Cable. It includes real-time microphone mixing, per-sound volume control, and global hotkeys, making it useful for gaming, streaming, online meetings, or simply having fun with friends.

[Application screenshot]

## Features

### Audio Mixing

- Real-time microphone capture.
- Real-time soundboard audio injection.
- Audio mixing between microphone and soundboard.
- VB-Cable integration.
- Compatible with Discord, Teams, Zoom, and other voice applications.

### Sound Management

- Add sounds from audio files.
- Remove sounds.
- Play and stop sounds individually.
- Stop all sounds instantly.
- Per-sound volume control.
- Local playback monitoring (hear sounds yourself).

[Sound list screenshot]

### Hotkeys

- Custom keyboard shortcut for each sound.
- Global "Stop All" shortcut.
- Hotkeys work even when the application is not focused.

[Shortcut configuration screenshot]

### Microphone Controls

- Microphone selection.
- Real-time microphone level indicator.
- Microphone volume adjustment.

[Microphone panel screenshot]

### Configuration

The application automatically saves:

- Sound shortcuts.
- Sound volumes.
- Selected microphone.
- Microphone volume.
- Local playback state.
- Stop All shortcut.

## Requirements

### Software

- Python 3.11+
- VB-Cable

Download VB-Cable:

https://vb-audio.com/Cable/

### Python Dependencies

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/soundboard.git

cd soundboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Using VB-Cable

1. Install VB-Cable.
2. Launch SoundBoard.
3. Select your microphone.
4. In Discord (or another application), choose:

```text
CABLE Output (VB-Audio Virtual Cable)
```

as your microphone device.

5. Play sounds using the interface or keyboard shortcuts.

The application will automatically mix:

```text
Microphone + Soundboard
```

and send the result through VB-Cable.

## Configuration File

Settings are stored in:

```text
config/config.json
```

Example:

```json
{
    "parameters": {
        "local_playback_enabled": true,
        "microphone_volume": 1.0,
        "default_microphone": 5,
        "panic_shortcut": "middle mouse"
    },

    "sound_datas": {
        "kick.wav": {
            "shortcut": "ctrl+1",
            "volume": 0.75
        },

        "snare.wav": {
            "shortcut": "ctrl+2",
            "volume": 1.0
        }
    }
}
```

## Project Structure

```text
SoundBoard/
│
├── assets/
│   ├── sounds/
│   └── themes/
│
├── audio/
│   ├── audio_mixer.py
│   ├── microphone_manager.py
│   └── sound_manager.py
│
├── config/
│   └── config.json
│
├── dialogs/
│
├── widgets/
│
├── core/
│   └── config_manager.py
│
├── app.py
├── main.py
└── requirements.txt
```

## License

This project is distributed under the MIT License.