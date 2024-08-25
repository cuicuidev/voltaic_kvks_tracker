import pandas as pd
import datetime
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
    next_rank = [x[3] for x in skill.get_ranks(scores=list(best.values()))]

    fig = go.Figure()

    # Best
    fig.add_trace(go.Scatterpolar(
        r=progress_best + [progress_best[0]],
        theta=[key.split(".")[1] for key in best.keys()] + [list(best.keys())[0].split(".")[1]],
        fill="toself",
        fillcolor="rgba(0,0,0,0)",
        line=dict(color="rgba(225,0,0,1)", width=1),
        marker=dict(color="rgba(0,0,0,0)"),
        name="Best Performance"
    ))

    # Latest
    fig.add_trace(go.Scatterpolar(
        r=progress_latest,
        theta=[key.split(".")[1] for key in latest.keys()],
        fill="toself",
        fillcolor="rgba(0,0,255,0.5)",
        line=dict(color="rgba(0,0,0,0)"),
        marker=dict(size=0),
        name="Latest Performance"
    ))

    # Next rank
    fig.add_trace(go.Scatterpolar(
        r = next_rank + [next_rank[0]],
        theta = [key.split(".")[1] for key in best.keys()] + [list(best.keys())[0].split(".")[1]],
        fill="toself",
        fillcolor="rgba(0,0,0,0)",
        line=dict(color="rgba(0,127,63,0.7)", width=1),
        marker=dict(color="rgba(0,0,0,0)"),
        name="Next Rank"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
            angularaxis=dict(visible=True)
        ),
        showlegend=True
    )

    return fig

def time_series(df, skill) -> go.Figure:
    min_date = df.submitted_at.min()
    max_date = df.submitted_at.max()
    df = df.set_index("submitted_at")
    s = df.apply(lambda x: [rank[2] for rank in skill.get_ranks(x.to_list())], axis=1)
    df = pd.DataFrame(s.to_list(), index=s.index, columns = [col.split(".")[1] for col in df.columns])
    fig = px.line(df)
    fig.update_yaxes(
        range=[0,1],
        title="Progress"
    )

    min_width = datetime.timedelta(days=30)

    current_width = max_date - min_date
    if current_width < min_width:
        max_date = min_date + min_width

    fig.update_xaxes(range=[min_date, max_date])

    fig.update_layout(height=300)
    return fig


def progress_dashboard(anchor, df) -> None:
    c_tab, t_tab, s_tab = anchor.tabs(["Clicking".center(20,"\u2001"), "Tracking".center(20,"\u2001"), "Switching".center(20,"\u2001")])
    # Skills
    clicking = Clicking()
    clicking_latest = df[[col for col in df.columns if "clicking" in col]].dropna().iloc[-1]
    clicking_best = df[[col for col in df.columns if "clicking" in col]].max(axis=0)
    dyn_clicking_rank = clicking.dynamic_rank(scores=clicking_latest.iloc[:3].to_list())
    stat_clicking_rank = clicking.static_rank(scores=clicking_latest.iloc[3:].to_list()) 
    clicking_fig = polar_plot(clicking_latest, clicking_best, clicking)
    clicking_prog = time_series(df[[col for col in df.columns if "clicking" in col] + ["submitted_at"]].dropna(), clicking)

    tracking = Tracking()
    tracking_latest = df[[col for col in df.columns if "tracking" in col]].dropna().iloc[-1]
    tracking_best = df[[col for col in df.columns if "tracking" in col]].max(axis=0)
    prec_tracking_rank = tracking.precise_rank(scores=tracking_latest.iloc[:3].to_list())
    reac_tracking_rank = tracking.reactive_rank(scores=tracking_latest.iloc[3:].to_list()) 
    tracking_fig = polar_plot(tracking_latest, tracking_best, tracking)
    tracking_prog = time_series(df[[col for col in df.columns if "tracking" in col] + ["submitted_at"]].dropna(), tracking)

    switching = Switching()
    switching_latest = df[[col for col in df.columns if "switching" in col]].dropna().iloc[-1]
    switching_best = df[[col for col in df.columns if "switching" in col]].max(axis=0)
    speed_switching_rank = switching.speed_rank(scores=switching_latest.iloc[:3].to_list())
    eva_switching_rank = switching.evasive_rank(scores=switching_latest.iloc[3:].to_list()) 
    switching_fig = polar_plot(switching_latest, switching_best, switching)
    switching_prog = time_series(df[[col for col in df.columns if "switching" in col] + ["submitted_at"]].dropna(), switching)

    stat1, stat2 = c_tab.columns(2)
    stat1.write(f'Dynamic _**{' '.join(dyn_clicking_rank).strip()}**_')
    stat2.write(f"Static _**{' '.join(stat_clicking_rank).strip()}**_")
    c_tab.plotly_chart(clicking_fig)
    c_tab.plotly_chart(clicking_prog)
    
    stat1, stat2 = t_tab.columns(2)
    stat1.write(f"Precise _**{' '.join(prec_tracking_rank).strip()}**_")
    stat2.write(f"Reactive _**{' '.join(reac_tracking_rank).strip()}**_")
    t_tab.plotly_chart(tracking_fig)
    t_tab.plotly_chart(tracking_prog)

    stat1, stat2 = s_tab.columns(2)
    stat1.write(f"Speed _**{' '.join(speed_switching_rank).strip()}**_")
    stat2.write(f"Evasive _**{' '.join(eva_switching_rank).strip()}**_")
    s_tab.plotly_chart(switching_fig)
    s_tab.plotly_chart(switching_prog)
