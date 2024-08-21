from pymongo.mongo_client import MongoClient
import streamlit as st

import datetime

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

from typing import Dict, Any, Optional


class MongoDatabaseHandler:

    def __init__(self, client: MongoClient) -> None:
        self._client = client

        self._db = client.database

        self.benchmarks = self._db.benchmarks
        self.users = self._db.users

@st.cache_resource
def get_client() -> MongoClient:
    return MongoClient(host="localhost", port=27017)

def main() -> None:
    db = MongoDatabaseHandler(get_client())

    st.write("# Voltaic")
    easy, hard, progress = st.tabs(["Easy", "Advanced", "Progress"])

    ###########################################

    username = easy.text_input(label="Username")

    user = {
        "username" : username,
    }

    cd_e, tp_e, ss_e = easy.columns(3, gap="small")
    cs_e, tr_e, se_e = easy.columns(3, gap="small")

    st.markdown("""
        <style>
            [data-testid="column"]{
                padding: 10px;
            }
            [data-testid="column"]:nth-child(1){
                background-color: #e3b75f;
            }
            [data-testid="column"]:nth-child(2){
                background-color: #36806b;
            }
            [data-testid="column"]:nth-child(3){
                background-color: #8c4873;
            }
            [data-testid="stHorizontalBlock"] + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(1){
                background-color: #eb6a60;
            }
            [data-testid="stHorizontalBlock"] + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(2){
                background-color: #2261a1;
            }
            [data-testid="stHorizontalBlock"] + [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(3){
                background-color: #6d4585;
            }
        </style>
        """, unsafe_allow_html=True
    )

    pasu_e = cd_e.number_input(label="Pasu Voltaic Easy", value=None)
    b180_e = cd_e.number_input(label="B180 Voltaic Easy", value=None)
    pop_e = cd_e.number_input(label="Popcorn Voltaic Easy", value=None)

    smooth_e = tp_e.number_input(label="Smoothbot Voltaic Easy", value=None)
    air_ang_e = tp_e.number_input(label="Air Angelic 4 Voltaic Easy", value=None)
    pgti_e = tp_e.number_input(label="PGTI Voltaic Easy", value=None)

    patts_e = ss_e.number_input(label="patTS Voltaic Easy", value=None)
    psalmts_e = ss_e.number_input(label="psalmTS Voltaic Easy", value=None)
    voxts_e = ss_e.number_input(label="voxTS Voltaic Easy", value=None)


    ww3t = cs_e.number_input(label="ww3t Voltaic", value=None)
    _1w4ts = cs_e.number_input(label="1w4ts Voltaic", value=None)
    _6sh = cs_e.number_input(label="6 Sphere Hipfire Voltaic", value=None)

    xyz_e = tr_e.number_input(label="FuglaaXYZ Voltaic Easy", value=None)
    plaza_e = tr_e.number_input(label="Ground Plaza Voltaic Easy", value=None)
    air_e = tr_e.number_input(label="Air Voltaic Easy", value=None)
    
    kints_e = se_e.number_input(label="kinTS Voltaic Easy", value=None)
    b180t_e = se_e.number_input(label="B180T Voltaic Easy", value=None)
    smoothts_e = se_e.number_input(label="Smoothbot TS Voltaic Easy", value=None)

    benchmark: Dict[str, Any] = {
        "clicking" : {
            "pasu_easy" : pasu_e,
            "b180_easy" : b180_e,
            "popcorn_easy" : pop_e,
            "ww3t" : ww3t,
            "1w4ts" : _1w4ts,
            "6_sphere_hipfire" : _6sh
        },
        "tracking" : {
            "smoothbot_easy" : smooth_e,
            "air_angelic_4_easy" : air_ang_e,
            "pgti_easy" : pgti_e,
            "fuglaaxyz_easy" : xyz_e,
            "ground_plaza_easy" : plaza_e,
            "air_easy" : air_e
        },
        "switching": {
            "patts_easy" : patts_e,
            "psalmts_easy" : psalmts_e,
            "voxts_easy" : voxts_e,
            "kints_easy" : kints_e,
            "b180t_easy" : b180t_e,
            "smoothbot_ts_easy" : smoothts_e
        }
    }
    
    benchmark["clicking"] = {k: v for k, v in benchmark["clicking"].items() if v is not None}
    benchmark["tracking"] = {k: v for k, v in benchmark["tracking"].items() if v is not None}
    benchmark["switching"] = {k: v for k, v in benchmark["switching"].items() if v is not None}

    benchmark = {k: v for k, v in benchmark.items() if len(v) > 0}

    if easy.button(label="Submit"):

        db_users_results = db.users.insert_one(user)
        user_id = db_users_results.inserted_id

        benchmark["user_id"] = user_id
        benchmark["submitted_at"] = datetime.datetime.now(datetime.UTC)
        db.benchmarks.insert_one(benchmark)

    ###################################################

    docs = [doc for doc in db.benchmarks.find({})]
    df = pd.json_normalize(docs)
    fig = px.line(
        data_frame=df,
        x="submitted_at",
        y=[col for col in df.columns if "." in col]
    )

    progress.plotly_chart(fig)

if __name__ == "__main__":
    main()
