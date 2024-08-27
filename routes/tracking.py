import datetime
from typing import Any, Dict

import streamlit as st

def run(anchor, db) -> None:
    username = anchor.text_input(label="Username")

    wrong_passwd = False
    if username == "cuicui":
        passwd = anchor.text_input(label="Password", type="password")
        wrong_passwd = st.secrets["cuicui_passwd"] != passwd

    if wrong_passwd:
        anchor.warning("Invalid credentials")

    level = anchor.selectbox(label="Benchmark", options=["VT s3 Intermediate", "VT s3 Advanced"])
    diffs = {"VT s3 Intermediate" : " Easy", "VT s3 Advanced" : ""}
    suffix = diffs[level]

    user = {
        "username" : username,
    }

    cd_e, tp_e, ss_e = anchor.columns(3, gap="large")
    cs_e, tr_e, se_e = anchor.columns(3, gap="large")

    pasu_e = cd_e.number_input(label=f"Pasu Voltaic{suffix}", value=None)
    b180_e = cd_e.number_input(label=f"B180 Voltaic{suffix}", value=None)
    pop_e = cd_e.number_input(label=f"Popcorn Voltaic{suffix}", value=None)

    smooth_e = tp_e.number_input(label=f"Smoothbot Voltaic{suffix}", value=None)
    air_ang_e = tp_e.number_input(label=f"Air Angelic 4 Voltaic{suffix}", value=None)
    pgti_e = tp_e.number_input(label=f"PGTI Voltaic{suffix}", value=None)

    patts_e = ss_e.number_input(label=f"patTS Voltaic{suffix}", value=None)
    psalmts_e = ss_e.number_input(label=f"psalmTS Voltaic{suffix}", value=None)
    voxts_e = ss_e.number_input(label=f"voxTS Voltaic{suffix}", value=None)


    ww3t = cs_e.number_input(label="ww3t Voltaic", value=None)
    _1w4ts = cs_e.number_input(label="1w4ts Voltaic", value=None)
    _6sh = cs_e.number_input(label="6 Sphere Hipfire Voltaic", value=None)

    xyz_e = tr_e.number_input(label=f"FuglaaXYZ Voltaic{suffix}", value=None)
    plaza_e = tr_e.number_input(label=f"Ground Plaza Voltaic{suffix}", value=None)
    air_e = tr_e.number_input(label=f"Air Voltaic{suffix}", value=None)
    
    kints_e = se_e.number_input(label=f"kinTS Voltaic{suffix}", value=None)
    b180t_e = se_e.number_input(label=f"B180T Voltaic{suffix}", value=None)
    smoothts_e = se_e.number_input(label=f"Smoothbot TS Voltaic{suffix}", value=None)

    benchmark: Dict[str, Any] = {
        "clicking" : {
            f"pasu{suffix.lower().replace(" ", "_")}" : pasu_e,
            f"b180{suffix.lower().replace(" ", "_")}" : b180_e,
            f"popcorn{suffix.lower().replace(" ", "_")}" : pop_e,
            "ww3t" : ww3t,
            "1w4ts" : _1w4ts,
            "6_sphere_hipfire" : _6sh
        },
        "tracking" : {
            f"smoothbot{suffix.lower().replace(" ", "_")}" : smooth_e,
            f"air_angelic_4{suffix.lower().replace(" ", "_")}" : air_ang_e,
            f"pgti{suffix.lower().replace(" ", "_")}" : pgti_e,
            f"fuglaaxyz{suffix.lower().replace(" ", "_")}" : xyz_e,
            f"ground_plaza{suffix.lower().replace(" ", "_")}" : plaza_e,
            f"air{suffix.lower().replace(" ", "_")}" : air_e
        },
        "switching": {
            f"patts{suffix.lower().replace(" ", "_")}" : patts_e,
            f"psalmts{suffix.lower().replace(" ", "_")}" : psalmts_e,
            f"voxts{suffix.lower().replace(" ", "_")}" : voxts_e,
            f"kints{suffix.lower().replace(" ", "_")}" : kints_e,
            f"b180t{suffix.lower().replace(" ", "_")}" : b180t_e,
            f"smoothbot_ts{suffix.lower().replace(" ", "_")}" : smoothts_e
        }
    }
    
    benchmark["clicking"] = {k: v for k, v in benchmark["clicking"].items() if v is not None}
    benchmark["tracking"] = {k: v for k, v in benchmark["tracking"].items() if v is not None}
    benchmark["switching"] = {k: v for k, v in benchmark["switching"].items() if v is not None}

    benchmark = {k: v for k, v in benchmark.items() if len(v) > 0}

    mouse_curve = anchor.selectbox(label="Mouse Acceleration", options=["Flat", "Linear", "Sigmoid-like", "Logarithmic", "S-plateau", "Exponential"])
    dpi = anchor.number_input(label="Mouse DPI", step=1)
    kvks_sens = anchor.number_input(label="KovaaKs Sensibility")
    kvks_sens_type = anchor.selectbox(label="KovaaKs Sensibility Preset", options=["Valorant"])

    if anchor.button(label="Submit"):

        user_result = db.users.find_one({"username": username})
        if user_result is None:
            db_users_results = db.users.insert_one(user)
            user_id = db_users_results.inserted_id
        else:
            user_id = user_result["_id"]

        benchmark["user_id"] = user_id
        benchmark["submitted_at"] = datetime.datetime.now(datetime.UTC)
        benchmark["dpi"] = dpi
        benchmark["kvks_sens"] = {"preset" : kvks_sens_type, "value" : kvks_sens}
        if mouse_curve != "Flat":
            benchmark["mouse_curve"] = mouse_curve

        if not wrong_passwd:
            db.benchmarks.insert_one(benchmark)
        else:
            anchor.warning("Invalid credentials")
