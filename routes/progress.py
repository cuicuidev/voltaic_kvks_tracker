import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from skills import Clicking

def run(anchor, db) -> None:
    username = anchor.text_input(label="Username", key="username_2")
    user_result = db.users.find_one({"username" : username})

    if user_result is None:
        anchor.warning("No existe el usuario")
    else:
        user_id = user_result["_id"]
        docs = [doc for doc in db.benchmarks.find({"user_id" : user_id})]
        df = pd.json_normalize(docs)
        if len(df) == 0:
            anchor.warning("No hay registros")
        else:
            skill = anchor.selectbox(label="Benchmark", options=["Clicking", "Tracking", "Switching"])
            progress_dashboard(anchor=anchor, df=df, skill=skill)

def rank(score, thresholds):
    ranks = ["Silver", "Gold", "Platinum", "Diamond", "Jade", "Master", "Grandmaster", "Nova", "Astra", "Celestial"]
    progress = score/thresholds[-1]
    for i, threshold in enumerate(thresholds):
        if score >= threshold:
            return score, ranks[i], progress
    return score, "Bronze", progress

def progress_dashboard(anchor, df, skill) -> None:
    # Ranking
    skills = {
        "tracking.smoothbot_easy" : "tracking.precise",
        "tracking.air_angelic_4_easy" : "tracking.precise",
        "tracking.pgti_easy" : "tracking.precise",
        "tracking.fuglaaxyz_easy" : "tracking.reactive",
        "tracking.ground_plaza_easy" : "tracking.reactive",
        "tracking.air_easy" : "tracking.reactive",
        "switching.patts_easy" : "switching.speed",
        "switching.psalmts_easy" : "switching.speed",
        "switching.voxts_easy" : "switching.speed",
        "switching.kints_easy" : "switching.evasive",
        "switching.b180t_easy" : "switching.evasive",
        "switching.smoothbot_ts_easy" : "switching.evasive",
    }

    # Clicking
    clicking = Clicking()
    clicking_latest = df[[col for col in df.columns if "clicking" in col]].iloc[-1]
    dyn_clicking = clicking.dynamic_rank(scores=clicking_latest.iloc[:3].to_list())
    stat_clicking = clicking.static_rank(scores=clicking_latest.iloc[3:].to_list()) 

    anchor.write(dyn_clicking)
    anchor.write(stat_clicking)
    
    clicking_best = df[[col for col in df.columns if "clicking" in col]].max(axis=0).to_dict()
    clicking_latest = clicking_latest.to_dict()
    progress_best = [x[2] for x in clicking.get_ranks(scores=list(clicking_best.values()))]
    progress_latest = [x[2] for x in clicking.get_ranks(scores=list(clicking_latest.values()))]

    tracking_thresholds = [
        [1700,2100,2400,2800,3100],
        [1800,2200,2600,3000,3300],
        [700,1000,1300,1600,1900],
        [7500,8500,10000,12000,14000],
        [835, 845, 855, 870, 880],
        [775, 800, 825, 852, 865]
    ]
    switching_thresholds = [
        [65,80,85,91,98],
        [50,58,67,76,85],
        [74,82,90,100,109],
        [45,54,60,66,72],
        [40, 51, 60, 69, 77],
        [35, 42, 46, 50, 54]
    ]
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=progress_best,
        theta=list(clicking_best.keys()),
        fill="toself",
        fillcolor="rgba(255,127,0,0.3)",
        line=dict(color="rgba(0,0,0,0)"),
        marker=dict(size=0),
        name="Best Performance"
    ))

    fig.add_trace(go.Scatterpolar(
        r=progress_latest + [progress_latest[0]],
        theta=list(clicking_latest.keys()) + [list(clicking_latest.keys())[0]],
        fill="toself",
        fillcolor="rgba(0,0,0,0)",
        line=dict(color="rgba(0,0,255,0.7)"),
        marker=dict(size=0),
        name="Latest Performance"
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0,1]))
    )

    anchor.plotly_chart(fig)
