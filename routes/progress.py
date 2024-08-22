import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        "clicking.pasu_easy" : "clicking.dynamic",
        "clicking.b180_easy" : "clicking.dynamic",
        "clicking.popcorn_easy" : "clicking.dynamic",
        "clicking.ww3t" : "clicking.static",
        "clicking.1w4ts" : "clicking.static",
        "clicking.6_sphere_hipire" : "clicking.static",
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
    clicking_latest = df[[col for col in df.columns if "clicking" in col]].iloc[-1]
    clicking_thresholds = [
        [40,50,56,66,75],
        [52,61,70,77,86],
        [100,150,200,250,310],
        [83,93,103,113,123],
        [70, 82, 91, 100, 110],
        [95, 108, 120, 132, 142]
    ]
    clicking_latest = {k : rank(v, t) for (k, v), t in zip(clicking_latest.to_dict().items(), clicking_thresholds)}
    clicking_best = df[[col for col in df.columns if "clicking" in col]].max(axis=0)
    clicking_best = {k : rank(v, t) for (k, v), t in zip(clicking_best.to_dict().items(), clicking_thresholds)}


    # Tracking

    tracking_latest = df[[col for col in df.columns if "tracking" in col]].iloc[-1]
    tracking_thresholds = [
        [1700,2100,2400,2800,3100],
        [1800,2200,2600,3000,3300],
        [700,1000,1300,1600,1900],
        [7500,8500,10000,12000,14000],
        [835, 845, 855, 870, 880],
        [775, 800, 825, 852, 865]
    ]
    tracking_latest = {k : rank(v, t) for (k, v), t in zip(tracking_latest.to_dict().items(), tracking_thresholds)}
    tracking_best = df[[col for col in df.columns if "tracking" in col]].max(axis=0)
    tracking_best = {k : rank(v, t) for (k, v), t in zip(tracking_best.to_dict().items(), tracking_thresholds)}

    # Switching
    switching_latest = df[[col for col in df.columns if "switching" in col]].iloc[-1]
    switching_thresholds = [
        [65,80,85,91,98],
        [50,58,67,76,85],
        [74,82,90,100,109],
        [45,54,60,66,72],
        [40, 51, 60, 69, 77],
        [35, 42, 46, 50, 54]
    ]
    switching_latest = {k : rank(v, t) for (k, v), t in zip(switching_latest.to_dict().items(), switching_thresholds)}
    switching_best = df[[col for col in df.columns if "switching" in col]].max(axis=0)
    switching_best = {k : rank(v, t) for (k, v), t in zip(switching_best.to_dict().items(), switching_thresholds)}

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[val[2] for val in clicking_best.values()],
        theta=list(clicking_best.keys()),
        fill="toself",
        fillcolor="rgba(255,127,0,0.3)",
        line=dict(color="rgba(0,0,0,0)"),
        marker=dict(size=0),
        name="Best Performance"
    ))

    fig.add_trace(go.Scatterpolar(
        r=[val[2] for val in clicking_latest.values()] + [list(clicking_latest.values())[0][2]],
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

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[val[2] for val in tracking_best.values()],
        theta=list(tracking_best.keys()),
        fill="toself",
        fillcolor="rgba(255,127,0,0.3)",
        line=dict(color="rgba(0,0,0,0)"),
        marker=dict(size=0),
        name="Best Performance"
    ))

    fig.add_trace(go.Scatterpolar(
        r=[val[2] for val in tracking_latest.values()] + [list(tracking_latest.values())[0][2]],
        theta=list(tracking_latest.keys()) + [list(tracking_latest.keys())[0]],
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

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[val[2] for val in switching_best.values()],
        theta=list(switching_best.keys()),
        fill="toself",
        fillcolor="rgba(255,127,0,0.3)",
        line=dict(color="rgba(0,0,0,0)"),
        marker=dict(size=0),
        name="Best Performance"
    ))

    fig.add_trace(go.Scatterpolar(
        r=[val[2] for val in switching_latest.values()] + [list(switching_latest.values())[0][2]],
        theta=list(switching_latest.keys()) + [list(switching_latest.keys())[0]],
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
