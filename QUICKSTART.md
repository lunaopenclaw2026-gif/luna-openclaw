# Luna Phone System - Quick Start

## 🎯 Ziel
Du möchtest Luna anrufen (+14159034051) und mit mir sprechen — per Telefon, mit vollem Chat-Kontext.

## 📋 Dokumentation (lies in dieser Reihenfolge)

1. **QUICKSTART.md** ← Du bist hier
2. **LUNA_PHONE_SYSTEM_SETUP.md** — Was ich gebaut habe & wie es funktioniert
3. **RAILWAY_DEPLOYMENT_GUIDE.md** — Schritt für Schritt deployen (einfach!)

## 🚀 Super Quick Start (5 Minuten)

### 1. Railway Account (1 Minute)
```
https://railway.app
Sign up with GitHub
```

### 2. Connect Repo (1 Minute)
```
Create New Project → Deploy from GitHub
Choose luna-openclaw Repo → main branch
```

Railway deployt automatisch! ✨

### 3. Set Environment Variables (2 Minuten)
In Railway UI → Variables:
```
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+14159034051
ELEVENLABS_API_KEY=sk_b330d85b28e2cbb5449b75bea6b6cde92255c92ab33b577b
CHRISTOPHER_PHONE=+4915770368632
FLASK_SECRET_KEY=<random hex>
```

### 4. Twilio Webhook (1 Minute)
```
https://www.twilio.com/console/phone-numbers/incoming
+14159034051 → Voice URL → https://[railway-url]/incoming-call
```

### 5. Test Call
Anrufen: **+14159034051**
Luna antwortet! 🎉

## 📁 Wichtige Dateien

```
/workspace/
├── twilio_elevenlabs_integration.py  ← Flask Backend
├── media_stream_handler.py           ← WebSocket Handler
├── luna_phone_system.py              ← CLI Tools
├── chat_context_manager.py           ← Chat Context
├── requirements.txt                  ← Dependencies
├── Procfile                          ← Server Config
│
├── QUICKSTART.md                     ← Du bist hier
├── LUNA_PHONE_SYSTEM_SETUP.md        ← Details
├── RAILWAY_DEPLOYMENT_GUIDE.md       ← Deployen
└── memory/                           ← Our chat history
    └── 2026-04-04.md
```

## ⚙️ Tech Stack

- **Twilio** — Telefon-Infrastruktur
- **ElevenLabs** — Speech-to-Text + LLM + Text-to-Speech
- **Flask** — Web Server
- **Railway** — Hosting
- **Git/GitHub** — Deployment

## 🎙️ Was passiert wenn du anrufst?

```
Du: +14159034051 anrufen
    ↓
Twilio: Verbindung zu Railway Server
    ↓
Luna (mein LLM): Verarbeitet deine Stimme + Chat-Kontext
    ↓
ElevenLabs: Spricht die Antwort
    ↓
Du: Hörst Luna's Stimme
```

## 💰 Kosten
- Railway: €5/Monat (großzügiges credit system)
- Twilio: ~€1/Monat + 0,01€/Minute
- ElevenLabs: Included
- **Total:** ~€6-8/Monat

## ✅ Checklist für Deployment

- [ ] Railway Account erstellt
- [ ] GitHub Repo verbunden
- [ ] Environment Variables gesetzt
- [ ] Twilio Webhook konfiguriert
- [ ] Test call gemacht
- [ ] Erfolgreich mit Luna gesprochen! 🎉

## 🆘 Wenn was nicht funktioniert

1. Überprüf Railway Logs (Deployments Tab)
2. Überprüf Twilio Webhook URL
3. Überprüf Environment Variables
4. Schreib mir eine Nachricht!

## 🎓 Lernen/Verstehen?

- **Technische Details:** LUNA_PHONE_SYSTEM_SETUP.md
- **Step-by-Step:** RAILWAY_DEPLOYMENT_GUIDE.md
- **Troubleshooting:** Jeweils am Ende der Docs

## 🔮 Nach dem Setup

Coole Sachen die ich später machen kann:
- Voice cloning (deine Stimme statt ElevenLabs)
- Bessere Restaurant-Integrationen
- Call recordings + Transkripte
- Analytics (welche bookings funktionieren)
- Inbound calls (Restaurants rufen dich zurück)

---

**Ready?** Los geht's! 🚀

Folg einfach der RAILWAY_DEPLOYMENT_GUIDE.md — super ausführlich.
