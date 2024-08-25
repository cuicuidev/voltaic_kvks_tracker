import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from skills import Clicking, Tracking, Switching

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
            progress_dashboard(anchor=anchor, df=df)

def polar_plot(latest, best, skill) -> go.Figure:
    latest = latest.to_dict()
    best = best.to_dict()
    progress_best = [x[2] for x in skill.get_ranks(scores=list(best.values()))]
    progress_latest = [x[2] for x in skill.get_ranks(scores=list(latest.values()))]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=progress_best,
        theta=[key.split(".")[1] for key in best.keys()],
        fill="toself",
        fillcolor="rgba(255,127,0,0.3)",
        line=dict(color="rgba(0,0,0,0)"),
        marker=dict(size=0),
        name="Best Performance"
    ))

    fig.add_trace(go.Scatterpolar(
        r=progress_latest + [progress_latest[0]],
        theta=[key.split(".")[1] for key in latest.keys()] + [list(latest.keys())[0].split(".")[1]],
        fill="toself",
        fillcolor="rgba(0,0,0,0)",
        line=dict(color="rgba(0,0,255,0.7)"),
        marker=dict(size=0),
        name="Latest Performance"
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0,1]))
    )

    return fig

def progress_dashboard(anchor, df) -> None:
    # Skills
    clicking = Clicking()
    clicking_latest = df[[col for col in df.columns if "clicking" in col]].dropna().iloc[-1]
    clicking_best = df[[col for col in df.columns if "clicking" in col]].max(axis=0)
    dyn_clicking_rank = clicking.dynamic_rank(scores=clicking_latest.iloc[:3].to_list())
    stat_clicking_rank = clicking.static_rank(scores=clicking_latest.iloc[3:].to_list()) 
    clicking_fig = polar_plot(clicking_latest, clicking_best, clicking)

    tracking = Tracking()
    tracking_latest = df[[col for col in df.columns if "tracking" in col]].dropna().iloc[-1]
    tracking_best = df[[col for col in df.columns if "tracking" in col]].max(axis=0)
    prec_tracking_rank = tracking.precise_rank(scores=tracking_latest.iloc[:3].to_list())
    reac_tracking_rank = tracking.reactive_rank(scores=tracking_latest.iloc[3:].to_list()) 
    tracking_fig = polar_plot(tracking_latest, tracking_best, tracking)

    switching = Switching()
    switching_latest = df[[col for col in df.columns if "switching" in col]].dropna().iloc[-1]
    switching_best = df[[col for col in df.columns if "switching" in col]].max(axis=0)
    speed_switching_rank = switching.speed_rank(scores=switching_latest.iloc[:3].to_list())
    eva_switching_rank = switching.evasive_rank(scores=switching_latest.iloc[3:].to_list()) 
    switching_fig = polar_plot(switching_latest, switching_best, switching)

    anchor.write(f"Dynamic clicking rank {dyn_clicking_rank}")
    anchor.write(f"Static clicking rank {stat_clicking_rank}")
    anchor.plotly_chart(clicking_fig)
    
    anchor.write(f"Precise tracking rank {prec_tracking_rank}")
    anchor.write(f"Reactive tracking rank {reac_tracking_rank}")
    anchor.plotly_chart(tracking_fig)

    anchor.write(f"Speed switching rank {speed_switching_rank}")
    anchor.write(f"Evasive switching rank {eva_switching_rank}")
    anchor.plotly_chart(switching_fig)
