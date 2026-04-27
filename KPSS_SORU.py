import json
import random
import requests
import os
import time
from datetime import datetime

def send_questions():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    simdi = datetime.now().strftime('%d.%m.%Y %H:%M')

    # JSON oku
    try:
        with open('sorular.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"JSON Okuma Hatası: {e}")
        return

    # 🔥 SADECE TARİH SORULARI
    tarih_sorulari = data.get("tarih_sorulari", [])

    if not tarih_sorulari:
        print("❌ tarih_sorulari boş veya bulunamadı")
        return

    # Rastgele soru seç
    secilecek_sayi = min(27, len(tarih_sorulari))
    secilen_sorular = random.sample(tarih_sorulari, secilecek_sayi)

    print(f"{simdi} tarihinde {secilecek_sayi} adet TARİH sorusu gönderiliyor...\n")

    harf_to_id = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}

    for index, soru_obj in enumerate(secilen_sorular, 1):
        soru_metni = soru_obj.get('soru', 'Soru metni yok')
        secenekler = soru_obj.get('secenekler', {})
        dogru_harf = soru_obj.get('dogru_cevap')

        secenek_mesaji = "\n".join([f"🔹 {k}: {v}" for k, v in secenekler.items()])

        mesaj = (
            f"📅 {simdi}\n📌 TARİH\n"
            f"───────────────────\n"
            f"❓ **SORU {index}:**\n\n"
            f"{soru_metni}\n\n{secenek_mesaji}"
        )

        # Soru metni
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": mesaj,
                "parse_mode": "Markdown"
            }
        )

        # Quiz
        poll_data = {
            "chat_id": chat_id,
            "question": "Cevabınızı seçin 👇",
            "options": json.dumps(["A", "B", "C", "D", "E"]),
            "is_anonymous": False,
        }

        if dogru_harf in harf_to_id:
            poll_data["type"] = "quiz"
            poll_data["correct_option_id"] = harf_to_id[dogru_harf]
        else:
            poll_data["type"] = "regular"

        requests.post(
            f"https://api.telegram.org/bot{token}/sendPoll",
            data=poll_data
        )

        time.sleep(10)

    print("✅ Tüm tarih soruları başarıyla gönderildi.")

if __name__ == "__main__":
    send_questions()
