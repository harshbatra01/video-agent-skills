# ElevenLabs TTS. Key comes only from the ELEVENLABS_API_KEY env var and is never printed or stored.
# python3 tts.py voices <out.txt>                      -> list voice names and ids
# python3 tts.py say <voice_id> <text_file> <out.mp3> [model] [stability]
import json, os, ssl, sys, urllib.request
import certifi
CTX = ssl.create_default_context(cafile=certifi.where())
KEY = os.environ.get("ELEVENLABS_API_KEY")
if not KEY: sys.exit("ELEVENLABS_API_KEY is not set in this shell")
def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300, context=CTX) as r: return r.read()
if sys.argv[1] == "voices":
    v = json.loads(call("https://api.elevenlabs.io/v1/voices"))["voices"]
    open(sys.argv[2], "w").write("\n".join(f"{x['voice_id']}\t{x['name']}\t{x.get('labels', {})}" for x in v))
    print(len(v), "voices listed")
else:
    vid, txt, out = sys.argv[2:5]
    model = sys.argv[5] if len(sys.argv) > 5 else "eleven_v3"
    stab = float(sys.argv[6]) if len(sys.argv) > 6 else 0.5
    audio = call(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
                 {"text": open(txt).read().strip(), "model_id": model,
                  "voice_settings": {"stability": stab, "similarity_boost": 0.8}})
    open(out, "wb").write(audio); print("wrote", out, len(audio), "bytes")
