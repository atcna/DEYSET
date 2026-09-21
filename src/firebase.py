# -*- coding: utf-8 -*-

import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

from config import FIREBASE_JSON, FIREBASE_URL


_firebase_initialized = False


def initialize_firebase():
    """
    Firebase bağlantısını başlatır.
    """

    global _firebase_initialized

    if _firebase_initialized:
        return

    cred = credentials.Certificate(FIREBASE_JSON)

    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": FIREBASE_URL
        }
    )

    _firebase_initialized = True

    print("[FIREBASE] Firebase bağlantısı başlatıldı.")


def send_collision_event():
    """
    Collision risk olayını Firebase'e kaydeder.
    """

    try:
        now = datetime.now()

        tarih = now.strftime("%d/%m/%Y")
        saat = now.strftime("%H:%M:%S")

        data = {
            "durum": "COLLISION_RISK",
            "tarih": tarih,
            "saat": saat
        }

        db.reference("Tehlikeli Durum Adı").push(data)

        print("[FIREBASE] Collision riski gönderildi.")

    except Exception as e:
        print(f"[FIREBASE ERROR] {e}")


def send_driver_log(user_id, warnings):
    """
    Sürücü/session verisini Firebase'e kaydetmek için
    kullanılabilecek yardımcı fonksiyon.
    """

    try:
        now = datetime.now()

        tarih = now.strftime("%d/%m/%Y")
        saat = now.strftime("%H:%M:%S")

        data = {
            "tarih": tarih,
            "saat": saat,
            "uyarilar": warnings
        }

        db.reference(f"session_logs/{user_id}").push(data)

        print(
            f"[FIREBASE] Driver log gönderildi: {user_id}"
        )

    except Exception as e:
        print(f"[FIREBASE ERROR] {e}")
