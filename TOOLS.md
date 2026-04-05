# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## ElevenLabs TTS
- API Key: (in GitHub Secrets gespeichert)
- Plan: Creator
- Bevorzugte Stimme: Sarah (EXAVITQu4vr4xnSDxMaL) — alternativ erkunden
- Model: eleven_multilingual_v2
- Workflow: MP3 generieren → mit ffmpeg zu OGG/Opus konvertieren → per message tool mit asVoice=true senden
- Skript: python3 mit elevenlabs SDK

## Twilio (Telefonie)
- Account SID: (in GitHub Secrets gespeichert)
- API Key: (in GitHub Secrets gespeichert)
- Zweck: Echte Telefonnummern, Anrufe tätigen/empfangen, Verbindung mit ElevenLabs Conversational AI
- Nur nach expliziter Freigabe durch Chris verwenden

## Eversports (Tennisplatzbuchung München)
- URL: https://www.eversports.de
- Bevorzugter Weg für Tennisplatzbuchungen in München
- Benutzer: (in GitHub Secrets gespeichert)
- Passwort: (in GitHub Secrets gespeichert)
- Nur nach expliziter Freigabe durch Chris verwenden

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Engine: edge-tts (binary: /Users/luna-openclaw/Library/Python/3.9/bin/edge-tts)
- Voice: de-DE-SeraphinaMultilingualNeural
- Rate: +15%
- Pitch: -2Hz
- Works in German AND English (multilingual)
- Command: edge-tts --voice de-DE-SeraphinaMultilingualNeural --rate="+15%" --pitch="-2Hz" --text "..." --write-media out.mp3
- Convert to ogg for Telegram: ffmpeg -i out.mp3 -c:a libopus out.ogg -y
- Send via message tool with asVoice=true from workspace dir
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
