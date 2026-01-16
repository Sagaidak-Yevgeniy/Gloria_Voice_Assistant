import json
import pyaudio
import keyboard
import serial
import time
from vosk import Model, KaldiRecognizer

# ==============================
# Arduino
# ==============================

arduino = serial.Serial(
    port='COM3',  # <-- ИЗМЕНИ
    baudrate=9600,
    timeout=1
)
time.sleep(2)

def light_on():
    arduino.write(b'1')
    print("💡 Свет включён")

def light_off():
    arduino.write(b'0')
    print("💤 Свет выключен")

# ==============================
# Загрузка моделей
# ==============================

models = {
    "ru": Model("model_small"),
    "kz": Model("vosk_model_kz")
}

current_lang = "ru"
recognizer = KaldiRecognizer(models[current_lang], 16000)

print(f"🎤 Текущий язык: {current_lang.upper()}")
print("Нажми Q для переключения языка")

# ==============================
# Микрофон
# ==============================

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=8000
)
stream.start_stream()

# ==============================
# Переключение языка
# ==============================

def switch_language():
    global current_lang, recognizer
    current_lang = "kz" if current_lang == "ru" else "ru"
    recognizer = KaldiRecognizer(models[current_lang], 16000)
    print(f"\n🔄 Язык переключён на: {current_lang.upper()}")

keyboard.add_hotkey("q", switch_language)

# ==============================
# Основной цикл
# ==============================

while True:
    data = stream.read(8000, exception_on_overflow=False)

    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "")

        if not text:
            continue

        print(f"[{current_lang.upper()}] → {text}")

        # 🇷🇺 Русский
        if 'включи свет' in text:
            light_on()
        elif 'выключи свет' in text:
            light_off()

        # 🇰🇿 Казахский
        elif 'жарықты қосыңыз' in text:
            light_on()
        elif 'жарықты өшіріңіз' in text:
            light_off()
