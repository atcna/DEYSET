# -*- coding: utf-8 -*-
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
)
import sys
import os
# Allow importing project modules
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)
from firebase_admin import db
from firebase import initialize_firebase
app = Flask(__name__)

# Development secret.
# For deployment, use an environment variable.
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "development-secret-key"
)
# ============================================================
# Firebase
# ============================================================
try:
    initialize_firebase()
except Exception as e:
    print(
        f"[FIREBASE ERROR] {e}"
    )
# ============================================================
# Performance Weights can be changed.
# ============================================================
WEIGHTS = {
    "HIZ_IHLALI": 20,
    "SIGARA": 10,
    "TEHLIKELI_ARAC": 10,
    "TEHLIKELI_INSAN": 20,
    "TELEFON": 20,
    "UYKU_DURUMU": 30
}
# ============================================================
# Date Parser
# ============================================================
from datetime import datetime
def parse_date_str(value):
    formats = [
        "%d/%m/%Y",
        "%Y-%m-%d"
    ]
    for date_format in formats:
        try:

            return datetime.strptime(
                value,
                date_format
            )
        except ValueError:
            continue
    return None
# ============================================================
# Login
# ============================================================
@app.route(
    "/",
    methods=["GET", "POST"]
)
def login():
    if request.method == "POST":
        username = request.form[
            "username"
        ]
        password = request.form[
            "password"
        ]
        # Development/demo authentication.
        # Replace with a proper authentication system
        # before public deployment.
        if (
            username == "admin"
            and password == "1234"
        ):
            session["user"] = username

            return redirect(
                url_for("dashboard")
            )
        return render_template(
            "login.html",
            error=(
                "Hatalı kullanıcı adı "
                "veya şifre"
            )
        )
    return render_template(
        "login.html"
    )
# ============================================================
# Dashboard
# ============================================================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(
            url_for("login")
        )
    tab = request.args.get(
        "tab",
        "suruculer"
    )
    # --------------------------------------------------------
    # Drivers
    # --------------------------------------------------------
    if tab == "suruculer":
        ref = db.reference(
            "surucu_girisleri"
        )
        data = ref.get() or {}
        entries = list(
            data.values()
        )[::-1]
        return render_template(
            "dashboard.html",
            tab=tab,
            entries=entries
        )
    # --------------------------------------------------------
    # Logs
    # --------------------------------------------------------
    if tab == "kayitlar":
        ref = db.reference(
            "session_logs"
        )
        data = ref.get() or {}
        users = list(
            data.keys()
        )
        return render_template(
            "dashboard.html",
            tab=tab,
            users=users
        )
    # --------------------------------------------------------
    # Dangerous situations
    # --------------------------------------------------------
    if tab == "tehlikeli":
        ref = db.reference(
            "Tehlikeli Durum Adı"
        )
        data = ref.get() or {}
        collision_entries = []
        for key, value in data.items():
            if (
                value.get("durum")
                == "COLLISION_RISK"
            ):
                collision_entries.append(
                    {
                        "tarih":
                            value.get(
                                "tarih",
                                ""
                            ),
                      
                        "saat":
                            value.get(
                                "saat",
                                ""
                            ),

                        "id":
                            key
                    }
                )
        collision_entries.sort(
            key=lambda x: (
                x["tarih"],
                x["saat"]
            ),
            reverse=True
        )

        return render_template(
            "dashboard.html",
            tab=tab,
            collision_entries=
                collision_entries
        )
    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------
    if tab == "konum":
        return render_template(
            "dashboard.html",
            tab=tab
        )
    return redirect(
        url_for(
            "dashboard",
            tab="suruculer"
        )
    )
# ============================================================
# User Logs
# ============================================================
@app.route(
    "/logs/<user_id>"
)
def user_logs(user_id):
    if "user" not in session:

        return redirect(
            url_for("login")
        )
    date_filter = request.args.get(
        "date"
    )
    ref = db.reference(
        f"session_logs/{user_id}"
    )
    data = ref.get() or {}
    # --------------------------------------------------------
    # Date list
    # --------------------------------------------------------
    if not date_filter:
        raw_dates = {
            value.get("tarih", "")
            for value in data.values()
            if value.get("tarih")
        }
        parsed = []
        for date_string in raw_dates:
            parsed_date = (
                parse_date_str(
                    date_string
                )
            )
            if parsed_date:
                parsed.append(
                    (
                        date_string,
                        parsed_date
                    )
                )
        parsed.sort(
            key=lambda x: x[1]
        )
        date_scores = []
        for (
            date_string,
            _
        ) in parsed:

            records = [
                value
                for value in data.values()
                if (
                    value.get("tarih")
                    == date_string
                    and "uyarilar"
                    in value
                )
            ]
            score = 0

            for record in records:

                warnings = (
                    record["uyarilar"]
                )

                for key, weight in WEIGHTS.items():

                    score += (
                        int(
                            warnings.get(
                                key,
                                0
                            )
                        )
                        * weight
                    )
            date_scores.append(
                {
                    "date":
                        date_string,

                    "score":
                        score
                }
            )
        return render_template(
            "log_dates.html",
            user_id=user_id,
            user_name=user_id.replace(
                "_",
                " "
            ),
            date_scores=date_scores
        )
    # --------------------------------------------------------
    # Specific date
    # --------------------------------------------------------
    session_data = []
    for value in data.values():
        if (
            value.get("tarih")
            == date_filter
            and "uyarilar"
            in value
        ):

            session_data.append(
                {
                    "saat":
                        value.get(
                            "saat",
                            ""
                        ),

                    "uyarilar":
                        value["uyarilar"]
                }
            )
    session_data.sort(
        key=lambda x: x["saat"]
    )
    performance_score = 0

    for entry in session_data:
        warnings = (
            entry["uyarilar"]
        )

        for key, weight in WEIGHTS.items():

            performance_score += (
                int(
                    warnings.get(
                        key,
                        0
                    )
                )
                * weight
            )
    if performance_score <= 100:
        performance_category = (
            "İyi performans"
        )
    elif performance_score <= 200:

        performance_category = (
            "Orta performans"
        )

    else:

        performance_category = (
            "Kötü performans"
        )

    return render_template(
        "logs.html",
        user_id=user_id,
        user_name=user_id.replace(
            "_",
            " "
        ),
        date=date_filter,
        entries=session_data,
        performance_score=
            performance_score,
        performance_category=
            performance_category
    )
# ============================================================
# Logout
# ============================================================
@app.route("/logout")
def logout():
    session.pop(
        "user",
        None
    )
    return redirect(
        url_for("login")
    )
# ============================================================
# Run
# ============================================================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
