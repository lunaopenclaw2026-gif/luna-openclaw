# Luna - ElevenLabs + Twilio Native Integration

## Überblick

Das ist die **einfachere Lösung** statt manueller WebSocket-Integration.

ElevenLabs hat eine **native Twilio-Integration** wo:
- Du deine Twilio-Nummer mit deinem Luna-Agent verbindest
- ElevenLabs kümmert sich um alles (Audio, STT, TTS, Gespräche)
- Du kannst **sofort anrufe tätigen und echte Gespräche führen**

**Setup-Zeit:** 10-15 Minuten

---

## Schritt 1: Luna Agent konfigurieren

Dein Agent existiert bereits: `agent_7301knaaafmxekdv2tscffjbpd1f`

Aber wir müssen die **Instruktionen für Restaurantbuchungen** aktualisieren.

Geh zu: https://elevenlabs.io/app/agents

1. Klick auf "Luna Openclaw" Agent
2. Geh zu "Settings" → "Instructions"
3. Ersetze die aktuellen Instruktionen mit:

```
Du bist Luna, ein virtueller Assistent von Christopher Baumann.

AUFGABEN:
1. Restauranttische buchen
2. Termine vereinbaren
3. Informationen sammeln

RESTAURANT-BUCHUNG:
- Begrüße freundlich: "Guten Tag, ich rufe im Auftrag von Christopher Baumann an."
- Frage systematisch nach:
  * Für welches Datum möchten Sie einen Tisch? (Format: z.B. "10. April")
  * Für wie viele Personen?
  * Zu welcher Uhrzeit?
  * Unter welchem Namen soll die Reservierung laufen?
- Wiederhole am Ende alle Details zur Bestätigung
- Bedanke dich und verabschiede dich professionell

WICHTIG:
- Sprich klar und deutlich Deutsch
- Sei höflich aber direkt
- Wenn etwas unklar ist, frage nach
- Du bist eine echte Person am Telefon — stelle dich so dar
```

4. **Speichern**

---

## Schritt 2: Twilio verbinden

Geh zu: https://elevenlabs.io/app/agents/settings

(Oder in deinem Agent → "Integrations" → "Twilio")

### Integration aktivieren:

1. Klick "Add Integration" → "Twilio"
2. Gib deine Twilio Credentials ein:
   - **Account SID:** <your-account-sid>
   - **Auth Token:** <your-auth-token>
3. Klick "Connect"

### Telefonnummer zuweisen:

Nach Verbindung wirst du aufgefordert, eine Nummer auszuwählen:
- Wähle: **+14159034051** (deine Twilio-Nummer)
- Bestätige

---

## Schritt 3: Test

Jetzt rufe deine Nummer an!

**Deine Luna-Nummer:** +14159034051

Ruf sie von deinem Handy an und sprich mit Luna.

---

## Outbound Calls (Luna ruft Restaurants an)

Nach dem Setup kannst du auch Luna-Anrufe initiieren.

### Via API:

```bash
curl -X POST https://api.elevenlabs.io/v1/conversational_ai/conversations/initiate_call \
  -H "xi-api-key: <your-api-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_7301knaaafmxekdv2tscffjbpd1f",
    "phone_number": "+4989123456789",
    "custom_data": {
      "restaurant": "Petit Fritz",
      "date": "2026-04-10",
      "time": "19:00",
      "people": 2
    }
  }'
```

### Via Python:

```python
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="<your-api-key>")

call = client.conversational_ai.conversations.initiate_call(
    agent_id="agent_7301knaaafmxekdv2tscffjbpd1f",
    phone_number="+4989123456789",
    custom_data={
        "restaurant": "Petit Fritz",
        "date": "2026-04-10",
        "time": "19:00",
        "people": 2
    }
)

print(f"Call started: {call.conversation_id}")
```

---

## Was passiert jetzt?

1. ✅ Luna empfängt deine Anrufe
2. ✅ Du kannst mit ihr sprechen (echte Konversation)
3. ✅ Sie kann Restaurants anrufen und buchen
4. ✅ Alles läuft über ElevenLabs + Twilio

**Kein Heroku, kein WebSocket-Setup, kein komplizierter Code.**

---

## Nächste Schritte

1. **Configure Agent** (Instruktionen setzen) — mach ich mit dir
2. **Connect Twilio** — 2 Minuten
3. **Test Call** — ruf Luna an
4. **Book Restaurant** — Luna ruft Restaurant an

Bereit?
