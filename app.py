import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ───────────── الهوية     ─────────────
APP_NAME = "Dust Risk Analyzer"
APP_SUB = "تحليل مخاطر الغبار والإنذار المبكر — منطقة حائل"
MODEL_AUC = 0.985

st.set_page_config(page_title=f"{APP_NAME} | حائل", page_icon="🌪️", layout="wide", initial_sidebar_state="collapsed")

BG, CARD, BORDER, TEXT, MUTED = "#16151C", "#1B1F26", "#272C35", "#E9ECF1", "#8B94A3"
MINT, PINK, ORANGE, GREEN, RED, YELLOW = "#3CCB9B", "#F26B8A", "#F5A623", "#2FD08E", "#F0536B", "#F2C94C"


def rgba(h, a):
    h = h.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"


LOGO_SVG = """<svg viewBox="0 0 96 96" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
<rect x="2" y="2" width="92" height="92" rx="26" fill="#1B1F26" stroke="#2E343E" stroke-width="2"/>
<circle cx="64" cy="32" r="11" fill="#F5A623"/>
<path d="M18 44 H54 a8 8 0 1 0 -8 -8" fill="none" stroke="#3CCB9B" stroke-width="5" stroke-linecap="round"/>
<path d="M18 58 H70 a8 8 0 1 1 -8 8" fill="none" stroke="#3CCB9B" stroke-width="5" stroke-linecap="round"/>
<path d="M18 72 H40" fill="none" stroke="#3CCB9B" stroke-opacity=".55" stroke-width="5" stroke-linecap="round"/>
</svg>"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
html, body, [class*="css"], .stApp { font-family:'Tajawal','Segoe UI',sans-serif; direction:rtl; text-align:right; }
.stApp { background:@BG@; color:@TEXT@; }
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
.block-container { padding-top:1.4rem; padding-bottom:2.5rem; max-width:1180px; }
h1,h2,h3,p,label,span { color:inherit; }

.head { display:flex; align-items:center; gap:1rem; margin-bottom:.4rem; }
.head-t { font-size:1.7rem; font-weight:800; color:@TEXT@; direction:ltr; text-align:right; line-height:1.15; }
.head-s { color:@MUTED@; font-size:.95rem; margin-top:.2rem; }

div[data-baseweb="tab-list"] { gap:.55rem; background:transparent; margin:.9rem 0 .4rem 0; overflow-x:auto; }
div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display:none; }
button[data-baseweb="tab"] { background:@CARD@; border:1px solid @BORDER@; border-radius:14px; padding:.55rem 1.25rem; height:auto; white-space:nowrap; }
button[data-baseweb="tab"] p { font-size:.98rem; font-weight:700; color:#C3CAD5; }
button[data-baseweb="tab"][aria-selected="true"] { background:@MINT@; border-color:@MINT@; }
button[data-baseweb="tab"][aria-selected="true"] p { color:#0B1F19; }

.notice { background:rgba(60,203,155,.10); border:1px solid rgba(60,203,155,.28); color:#BFEBDD; border-radius:14px; padding:.9rem 1.1rem; line-height:1.9; font-size:.95rem; margin:.7rem 0 1rem 0; }

.kpi { background:@CARD@; border:1px solid @BORDER@; border-radius:16px; padding:1.1rem 1rem; text-align:center; height:100%; }
.kpi-v { font-size:2rem; font-weight:800; line-height:1.2; color:var(--c); }
.kpi-l { color:@MUTED@; font-size:.88rem; margin-top:.3rem; }

.sec { font-size:1.2rem; font-weight:800; color:@TEXT@; margin:1.6rem 0 .7rem 0; }
.cap { color:@MUTED@; font-size:.88rem; margin:-.4rem 0 .7rem 0; }

.card { background:@CARD@; border:1px solid @BORDER@; border-radius:16px; padding:1rem 1.2rem; }
.tip { background:@CARD@; border:1px solid @BORDER@; border-top:3px solid var(--c); border-radius:16px; padding:1.1rem 1.2rem; height:100%; }
.tip-h { font-weight:800; color:@TEXT@; font-size:1.02rem; margin-bottom:.35rem; }
.tip-b { color:#B5BDC9; line-height:1.85; font-size:.93rem; }

@keyframes glow { 0% { box-shadow:0 0 0 0 var(--g); } 70% { box-shadow:0 0 0 16px rgba(0,0,0,0); } 100% { box-shadow:0 0 0 0 rgba(0,0,0,0); } }
.alert { background:var(--bg); border:1px solid var(--c); border-radius:20px; padding:1.4rem 1.5rem; margin:.6rem 0 1.1rem 0; }
.alert.pulse { animation:glow 2.2s infinite; }
.alert-top { display:flex; align-items:center; gap:1.1rem; }
.alert-ic { width:66px; height:66px; border-radius:18px; background:var(--bg2); border:1px solid var(--c); display:flex; align-items:center; justify-content:center; font-size:2.2rem; flex:none; }
.alert-t { font-size:1.6rem; font-weight:800; color:var(--c); line-height:1.2; }
.alert-s { color:#C9D0DA; margin-top:.25rem; }
.chips { display:flex; gap:.5rem; flex-wrap:wrap; margin:1rem 0; }
.chip { background:rgba(255,255,255,.06); border:1px solid @BORDER@; border-radius:999px; padding:.3rem .85rem; font-size:.87rem; color:#D4DAE3; }
.scale { display:flex; gap:.45rem; }
.seg { flex:1; text-align:center; padding:.45rem; border-radius:10px; background:rgba(255,255,255,.05); color:@MUTED@; font-weight:700; font-size:.9rem; }
.seg.on { background:var(--c); color:#0B1117; }

.bars { background:@CARD@; border:1px solid @BORDER@; border-radius:16px; padding:1rem 1.2rem; }
.bar-row { display:flex; align-items:center; gap:.8rem; margin:.5rem 0; }
.bar-l { width:78px; font-size:.9rem; color:#D4DAE3; flex:none; }
.bar-track { flex:1; height:12px; background:#252A33; border-radius:99px; overflow:hidden; }
.bar-fill { height:100%; border-radius:99px; background:var(--c); }
.bar-v { width:46px; text-align:left; font-weight:700; font-size:.9rem; color:@TEXT@; flex:none; direction:ltr; }

.tbl-wrap { background:@CARD@; border:1px solid @BORDER@; border-radius:16px; overflow-x:auto; }
.tbl { width:100%; border-collapse:collapse; font-size:.9rem; }
.tbl th { background:#20252D; color:#C3CAD5; font-weight:700; padding:.7rem .8rem; text-align:right; white-space:nowrap; }
.tbl td { padding:.65rem .8rem; border-top:1px solid @BORDER@; color:#D4DAE3; white-space:nowrap; }
.badge { background:var(--b); color:var(--c); border:1px solid var(--c); padding:.12rem .7rem; border-radius:99px; font-size:.8rem; font-weight:700; }

div[data-testid="stPlotlyChart"] { background:@CARD@; border:1px solid @BORDER@; border-radius:16px; padding:.4rem; }
div[data-testid="stDataFrame"] { border-radius:14px; overflow:hidden; }
.stDownloadButton button { background:@MINT@; color:#0B1F19; border:0; border-radius:12px; font-weight:700; }
.foot { text-align:center; color:#6D7685; font-size:.82rem; margin-top:2.2rem; }
</style>
"""
for k, v in {"@BG@": BG, "@CARD@": CARD, "@BORDER@": BORDER, "@TEXT@": TEXT, "@MUTED@": MUTED, "@MINT@": MINT}.items():
    CSS = CSS.replace(k, v)
st.markdown(CSS, unsafe_allow_html=True)


# ───────────── دوال مساعدة ─────────────
LEVELS = {
    0: ("الوضع آمن", "✅", GREEN, "لا يُتوقع غبار، والأجواء مناسبة للأنشطة المعتادة."),
    1: ("مراقبة", "👀", YELLOW, "رياح نشطة قد تثير الغبار، تابع التحديثات."),
    2: ("تحذير: غبار متوقع", "⚠️", ORANGE, "يُتوقع غبار، خذ احتياطاتك خصوصاً الفئات الحساسة."),
    3: ("خطر: عاصفة غبار محتملة", "🚨", RED, "رياح قوية وغبار متوقع، تجنب الخروج غير الضروري."),
}
SHORT = {0: "آمن", 1: "مراقبة", 2: "تحذير", 3: "خطر"}
ADVICE = {
    0: [("🫁", "مرضى الربو", "لا توجد قيود، وأبقِ البخاخ معك كالمعتاد."), ("🧒", "الأطفال", "اللعب في الخارج آمن."), ("🚗", "السائقون", "الرؤية طبيعية على الطرق.")],
    1: [("🫁", "مرضى الربو", "احمل البخاخ وتجنب الجهد الشديد في الخارج."), ("🧒", "الأطفال", "يُفضّل تقليل وقت اللعب في الأماكن المفتوحة."), ("🚗", "السائقون", "انتبه لتغيّر الرؤية على الطرق المفتوحة.")],
    2: [("🫁", "مرضى الربو", "ابقَ في الداخل قدر الإمكان والتزم بخطة العلاج."), ("🧒", "الأطفال", "أجّل الأنشطة الخارجية والرياضة المدرسية."), ("🚗", "السائقون", "خفّض السرعة وشغّل الإضاءة، وابتعد عن الطرق السريعة عند ضعف الرؤية.")],
    3: [("🫁", "مرضى الربو", "لا تخرج وأغلق النوافذ، وراجع الطوارئ عند ضيق التنفس."), ("🧒", "الأطفال", "ابقوا في الداخل وأوقفوا الأنشطة الخارجية."), ("🚗", "السائقون", "تجنب السفر إن أمكن، وعند انعدام الرؤية توقف في مكان آمن.")],
}
MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]


@st.cache_data
def load_data() -> pd.DataFrame:
    d = pd.read_csv("hail_dust_predictions.csv")
    d["time"] = pd.to_datetime(d["time"])
    return d.sort_values("time").reset_index(drop=True)


def risk_level(row, mod_thr, high_thr):
    g = row["wind_gusts_10m_max"]
    if row["predicted_dust"] == 1 and g >= high_thr:
        return 3
    if row["predicted_dust"] == 1:
        return 2
    return 1 if g >= mod_thr else 0


def estimate_risk(data, temp, wind, gust):
    for tol in (4, 6, 9, 14):
        m = data[(data["wind_gusts_10m_max"].sub(gust).abs() <= tol)
                 & (data["wind_speed_10m_max"].sub(wind).abs() <= tol)
                 & (data["temperature_2m_max"].sub(temp).abs() <= tol * 1.5)]
        if len(m) >= 20:
            return float(m["predicted_dust"].mean()), len(m)
    m = data[data["wind_gusts_10m_max"].sub(gust).abs() <= 15]
    return (float(m["predicted_dust"].mean()), len(m)) if len(m) else (0.0, 0)


def style(fig, h=400):
    fig.update_layout(
        height=h, margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Tajawal, Segoe UI, sans-serif", size=13, color="#C9D1DC"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, linecolor=BORDER)
    fig.update_yaxes(gridcolor="#262B33", zerolinecolor="#262B33")
    return fig


def kpi(value, label, color):
    return f'<div class="kpi" style="--c:{color}"><div class="kpi-v">{value}</div><div class="kpi-l">{label}</div></div>'


def bars_html(items, color=MINT):
    mx = max([v for _, v in items] + [1])
    rows = "".join(
        f'<div class="bar-row"><div class="bar-l">{l}</div><div class="bar-track"><div class="bar-fill" style="width:{v / mx * 100:.1f}%;--c:{color}"></div></div><div class="bar-v">{v:,}</div></div>'
        for l, v in items)
    return f'<div class="bars">{rows}</div>'


def badge(lvl):
    c = LEVELS[lvl][2]
    return f'<span class="badge" style="--c:{c};--b:{rgba(c, .14)}">{SHORT[lvl]}</span>'


def table_html(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def scale_html(lvl):
    cols = [GREEN, YELLOW, ORANGE, RED]
    segs = "".join(f'<div class="seg {"on" if i == lvl else ""}" style="--c:{cols[i]}">{SHORT[i]}</div>' for i in range(4))
    return f'<div class="scale">{segs}</div>'


# ───────────── التطبيق ─────────────
try:
    df = load_data()
    dust_df = df[df["predicted_dust"] == 1]
    base = dust_df if len(dust_df) >= 10 else df
    mod_thr = float(base["wind_gusts_10m_max"].quantile(0.25))
    high_thr = float(base["wind_gusts_10m_max"].quantile(0.75))
    df["level"] = df.apply(lambda r: risk_level(r, mod_thr, high_thr), axis=1)
    min_d, max_d = df["time"].min().date(), df["time"].max().date()

    st.markdown(f'<div class="head">{LOGO_SVG}<div><div class="head-t">{APP_NAME}</div><div class="head-s">{APP_SUB}</div></div></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["نظرة عامة", "مركز الإنذار", "المحاكي", "التحليل", "المنهجية"])

    # ═════════ نظرة عامة ═════════
    with tab1:
        st.markdown('<div class="notice">📌 البيانات سجلات مناخية يومية لمنطقة حائل منذ 2015. أيام الغبار «متوقعة» من مخرجات النموذج التنبؤي وليست رصداً فعلياً.</div>', unsafe_allow_html=True)
        k = st.columns(4)
        k[0].markdown(kpi(f"{len(df):,}", "الأيام المحللة", TEXT), unsafe_allow_html=True)
        k[1].markdown(kpi(f"{int(df['predicted_dust'].sum()):,}", "أيام الغبار المتوقعة", ORANGE), unsafe_allow_html=True)
        k[2].markdown(kpi(f"{int((df['level'] == 3).sum()):,}", "أيام الخطر المرتفع", PINK), unsafe_allow_html=True)
        k[3].markdown(kpi(f"{MODEL_AUC * 100:.1f}%", "دقة النموذج (ROC-AUC)", GREEN), unsafe_allow_html=True)

        st.markdown('<div class="sec">هبات الرياح عبر الزمن</div>', unsafe_allow_html=True)
        d2, d3 = df[df["level"] == 2], df[df["level"] == 3]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time"], y=df["wind_gusts_10m_max"], mode="lines", name="هبات الرياح",
                                 line=dict(color=MINT, width=1.5), fill="tozeroy", fillcolor=rgba(MINT, .08)))
        fig.add_trace(go.Scatter(x=d2["time"], y=d2["wind_gusts_10m_max"], mode="markers", name="تحذير",
                                 marker=dict(color=ORANGE, size=6)))
        fig.add_trace(go.Scatter(x=d3["time"], y=d3["wind_gusts_10m_max"], mode="markers", name="خطر",
                                 marker=dict(color=RED, size=7)))
        fig.update_yaxes(title_text="كم/س")
        st.plotly_chart(style(fig, 400), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="sec">الأشهر الأكثر غباراً</div>', unsafe_allow_html=True)
            m = dust_df.groupby(dust_df["time"].dt.month).size().sort_values(ascending=False)
            st.markdown(bars_html([(MONTHS[i - 1], int(v)) for i, v in m.items()], MINT), unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="sec">أيام الغبار حسب السنة</div>', unsafe_allow_html=True)
            y = dust_df.groupby(dust_df["time"].dt.year).size().sort_index(ascending=False)
            st.markdown(bars_html([(str(i), int(v)) for i, v in y.items()], ORANGE), unsafe_allow_html=True)

    # ═════════ مركز الإنذار ═════════
    with tab2:
        pick = st.date_input("📅 اختر اليوم لعرض حالته", value=max_d, min_value=min_d, max_value=max_d, key="pick_day")
        r = df[df["time"].dt.date == pick]
        r = r.iloc[-1] if not r.empty else df.iloc[-1]
        lvl = int(r["level"])
        title, icon, color, sub = LEVELS[lvl]

        if lvl >= 2 and not st.session_state.get("toasted"):
            st.toast(f"{title} — {r['time']:%Y-%m-%d}", icon=icon)
            st.session_state["toasted"] = True

        st.markdown(f"""
<div class="alert {'pulse' if lvl >= 2 else ''}" style="--c:{color};--bg:{rgba(color, .10)};--bg2:{rgba(color, .18)};--g:{rgba(color, .55)}">
<div class="alert-top"><div class="alert-ic">{icon}</div><div><div class="alert-t">{title}</div><div class="alert-s">{sub}</div></div></div>
<div class="chips"><span class="chip">📅 {r['time']:%Y-%m-%d}</span><span class="chip">💨 الهبات {r['wind_gusts_10m_max']:.1f} كم/س</span><span class="chip">🌬️ الرياح {r['wind_speed_10m_max']:.1f} كم/س</span><span class="chip">🌡️ الحرارة {r['temperature_2m_max']:.1f}°م</span></div>
{scale_html(lvl)}
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="sec">الإرشادات الصحية حسب الفئة</div>', unsafe_allow_html=True)
        for col, (ic, grp, txt) in zip(st.columns(3), ADVICE[lvl]):
            col.markdown(f'<div class="tip" style="--c:{color}"><div class="tip-h">{ic} {grp}</div><div class="tip-b">{txt}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec">آخر أيام الغبار المتوقعة</div>', unsafe_allow_html=True)
        recent = df[df["predicted_dust"] == 1].sort_values("time", ascending=False).head(8)
        rows = [[f"{x['time']:%Y-%m-%d}", f"{x['temperature_2m_max']:.1f}", f"{x['wind_speed_10m_max']:.1f}", f"{x['wind_gusts_10m_max']:.1f}", badge(int(x['level']))] for _, x in recent.iterrows()]
        st.markdown(table_html(["التاريخ", "الحرارة (°م)", "سرعة الرياح", "الهبات", "المستوى"], rows), unsafe_allow_html=True)

    # ═════════ المحاكي ═════════
    with tab3:
        st.markdown('<div class="sec">جرّب ظروفاً جوية وشاهد احتمال الغبار</div>', unsafe_allow_html=True)
        st.markdown('<div class="cap">يقارن المحاكي الظروف المحددة بالأيام المشابهة في السجل التاريخي ويحسب نسبة الأيام التي حدث فيها غبار. هذا تقدير إرشادي وليس مخرج النموذج نفسه.</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        temp = s1.slider("🌡️ الحرارة العظمى (°م)", float(df["temperature_2m_max"].min()), float(df["temperature_2m_max"].max()), float(df["temperature_2m_max"].median()))
        wind = s2.slider("🌬️ سرعة الرياح (كم/س)", float(df["wind_speed_10m_max"].min()), float(df["wind_speed_10m_max"].max()), float(df["wind_speed_10m_max"].median()))
        gust = s3.slider("💨 هبات الرياح (كم/س)", float(df["wind_gusts_10m_max"].min()), float(df["wind_gusts_10m_max"].max()), float(df["wind_gusts_10m_max"].median()))
        prob, n = estimate_risk(df, temp, wind, gust)

        g1, g2 = st.columns([1.4, 1])
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=prob * 100, number={"suffix": "%", "font": {"size": 48, "color": TEXT}},
            title={"text": "احتمال حدوث الغبار", "font": {"color": "#C9D1DC"}},
            gauge={"axis": {"range": [0, 100], "tickcolor": MUTED}, "bar": {"color": MINT, "thickness": 0.28}, "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
                   "steps": [{"range": [0, 25], "color": "#1B3B34"}, {"range": [25, 50], "color": "#3A3420"},
                             {"range": [50, 75], "color": "#3D2C1C"}, {"range": [75, 100], "color": "#3D1F26"}]},
        ))
        gauge.update_layout(height=330, margin=dict(l=20, r=20, t=70, b=10), paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Tajawal, Segoe UI, sans-serif"))
        g1.plotly_chart(gauge, use_container_width=True)
        with g2:
            lv = 3 if prob >= 0.75 else 2 if prob >= 0.5 else 1 if prob >= 0.25 else 0
            msg = ["احتمال منخفض للغبار", "احتمال متوسط، يلزم المراقبة", "احتمال مرتفع للغبار", "احتمال مرتفع جداً للغبار"][lv]
            _, i_, c_, _ = LEVELS[lv]
            st.markdown(f'<div class="tip" style="--c:{c_}"><div class="tip-h">{i_} {msg}</div><div class="tip-b">بناءً على {n:,} يوماً مشابهاً في السجل التاريخي.</div></div>', unsafe_allow_html=True)

    # ═════════ التحليل ═════════
    with tab4:
        f1, f2, f3 = st.columns([1.3, 1.3, 1])
        dr = f1.date_input("الفترة الزمنية", value=(min_d, max_d), min_value=min_d, max_value=max_d, key="range")
        user_thr = f2.slider("حد تنبيه لهبات الرياح (كم/س)", 20, int(df["wind_gusts_10m_max"].max()), int(mod_thr))
        only_dust = f3.toggle("أيام الغبار المتوقعة فقط", value=False)
        start, end = (dr if isinstance(dr, (tuple, list)) and len(dr) == 2 else (min_d, max_d))
        view = df[(df["time"].dt.date >= start) & (df["time"].dt.date <= end)]
        if only_dust:
            view = view[view["predicted_dust"] == 1]

        if view.empty:
            st.warning("لا توجد بيانات ضمن الفلاتر المحددة.")
        else:
            dd = int(view["predicted_dust"].sum())
            k = st.columns(4)
            k[0].markdown(kpi(f"{len(view):,}", "الأيام ضمن الفترة", TEXT), unsafe_allow_html=True)
            k[1].markdown(kpi(f"{dd:,}", "أيام الغبار المتوقعة", ORANGE), unsafe_allow_html=True)
            k[2].markdown(kpi(f"{dd / len(view) * 100:.1f}%", "نسبة أيام الغبار", PINK), unsafe_allow_html=True)
            k[3].markdown(kpi(f"{view['wind_gusts_10m_max'].max():.0f}", "أعلى هبة رياح (كم/س)", GREEN), unsafe_allow_html=True)

            st.markdown('<div class="sec">هبات الرياح وموجات الغبار</div>', unsafe_allow_html=True)
            pts = view[view["predicted_dust"] == 1]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=view["time"], y=view["wind_gusts_10m_max"], mode="lines", name="هبات الرياح",
                                     line=dict(color=MINT, width=1.5), fill="tozeroy", fillcolor=rgba(MINT, .08)))
            fig.add_trace(go.Scatter(x=pts["time"], y=pts["wind_gusts_10m_max"], mode="markers", name="غبار متوقع",
                                     marker=dict(color=ORANGE, size=7, line=dict(color=BG, width=1))))
            fig.add_hline(y=user_thr, line_dash="dash", line_color=PINK, annotation_text="حد التنبيه")
            fig.update_xaxes(rangeslider_visible=True)
            fig.update_yaxes(title_text="كم/س")
            st.plotly_chart(style(fig, 460), use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="sec">الخريطة الحرارية: الشهر والسنة</div>', unsafe_allow_html=True)
                hm = (view.assign(y=view["time"].dt.year, m=view["time"].dt.month)
                      .pivot_table(index="y", columns="m", values="predicted_dust", aggfunc="sum", fill_value=0)
                      .reindex(columns=range(1, 13), fill_value=0))
                fh = go.Figure(go.Heatmap(z=hm.values, x=MONTHS, y=hm.index.astype(str),
                                          colorscale=[[0, "#1F242C"], [0.5, ORANGE], [1, RED]],
                                          hovertemplate="%{y} - %{x}: %{z} يوم<extra></extra>"))
                st.plotly_chart(style(fh, 360), use_container_width=True)
            with c2:
                st.markdown('<div class="sec">الرياح مقابل الحرارة</div>', unsafe_allow_html=True)
                smp = view if len(view) <= 3000 else view.sample(3000, random_state=1)
                fs = px.scatter(smp, x="temperature_2m_max", y="wind_gusts_10m_max",
                                color=smp["predicted_dust"].map({0: "بدون غبار", 1: "غبار متوقع"}),
                                color_discrete_map={"بدون غبار": "#5B6574", "غبار متوقع": ORANGE},
                                labels={"temperature_2m_max": "الحرارة (°م)", "wind_gusts_10m_max": "هبات الرياح", "color": ""}, opacity=0.75)
                st.plotly_chart(style(fs, 360), use_container_width=True)

            st.markdown('<div class="sec">السجل التفصيلي</div>', unsafe_allow_html=True)
            tbl = view[["time", "temperature_2m_max", "wind_speed_10m_max", "wind_gusts_10m_max", "level"]].copy()
            tbl["time"] = tbl["time"].dt.strftime("%Y-%m-%d")
            tbl["level"] = tbl["level"].map(SHORT)
            tbl.columns = ["التاريخ", "الحرارة العظمى (°م)", "سرعة الرياح", "هبات الرياح", "المستوى"]
            with st.expander("عرض الجدول الكامل"):
                st.dataframe(tbl, use_container_width=True, hide_index=True, height=380)
            st.download_button("⬇️ تحميل البيانات (CSV)", tbl.to_csv(index=False).encode("utf-8-sig"), "dust_risk_filtered.csv", "text/csv")

    # ═════════ المنهجية ═════════
    with tab5:
        st.markdown('<div class="sec">عن المشروع</div>', unsafe_allow_html=True)
        a1, a2, a3 = st.columns(3)
        a1.markdown(f'<div class="tip" style="--c:{MINT}"><div class="tip-h">🎯 الهدف</div><div class="tip-b">إنذار مبكر بعواصف الغبار في منطقة حائل لحماية الصحة العامة، وخاصة مرضى الربو والأطفال.</div></div>', unsafe_allow_html=True)
        a2.markdown(f'<div class="tip" style="--c:{ORANGE}"><div class="tip-h">🗂️ البيانات</div><div class="tip-b">سجلات مناخية يومية منذ 2015 تشمل درجة الحرارة العظمى وسرعة الرياح وهبات الرياح.</div></div>', unsafe_allow_html=True)
        a3.markdown(f'<div class="tip" style="--c:{GREEN}"><div class="tip-h">🧠 النموذج</div><div class="tip-b">نموذج تنبؤي لأيام الغبار بدقة ROC-AUC تبلغ {MODEL_AUC * 100:.1f}%.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec">مستويات الإنذار</div>', unsafe_allow_html=True)
        lc = st.columns(4)
        descs = ["لا يُتوقع غبار.", f"هبات الرياح ≥ {mod_thr:.0f} كم/س بدون توقع غبار.", "النموذج يتوقع حدوث غبار.", f"غبار متوقع مع هبات رياح ≥ {high_thr:.0f} كم/س."]
        for col, k_ in zip(lc, range(4)):
            t_, i_, c_, _ = LEVELS[k_]
            col.markdown(f'<div class="tip" style="--c:{c_}"><div class="tip-h">{i_} {t_}</div><div class="tip-b">{descs[k_]}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec">ملاحظات</div>', unsafe_allow_html=True)
        st.markdown('<div class="card tip-b">• حدود المستويات تُحسب من توزيع هبات الرياح في أيام الغبار المتوقعة تاريخياً.<br>• المحاكي تقدير إرشادي من السجل التاريخي وليس مخرج النموذج.<br>• الإرشادات الصحية عامة ولا تغني عن استشارة الطبيب.</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="foot">{APP_NAME} · {APP_SUB}</div>', unsafe_allow_html=True)

except FileNotFoundError:
    import streamlit as st
import pandas as pd
import plotly.express as px

def render_emergency_dust_analysis():
    st.markdown("---")
    st.subheader("🏥 تحليل تأثير العواصف الرملية على طوارئ المستشفيات بمنطقة حائل")
    st.write("ربط بيانات تركيز الغبار بزيارات أقسام الطوارئ وحالات ضيق التنفس وجلسات البخار.")

    # بيانات تجريبية توضيحية لربط الغبار بزيارات الطوارئ (يمكنك استبدالها بملف CSV حقيقي لاحقاً)
    data = {
        "اليوم": ["السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"],
        "مستوى الغبار (AQI)": [120, 350, 420, 180, 90, 310, 450],
        "حالات الطوارئ (جلسات البخار)": [25, 65, 80, 35, 20, 55, 95],
        "حالة الخطورة": ["متوسط", "عالي", "حرج", "متوسط", "منخفض", "عالي", "حرج"]
    }
    
    df_emergency = pd.DataFrame(data)

    # رسم بياني تفاعلي يوضح العلاقة
    fig = px.scatter(
        df_emergency, 
        x="مستوى الغبار (AQI)", 
        y="حالات الطوارئ (جلسات البخار)", 
        size="حالات الطوارئ (جلسات البخار)", 
        color="حالة الخطورة",
        hover_name="اليوم",
        title="العلاقة بين مؤشر الغبار وأعداد مراجعين الطوارئ (حالات التنفس وبخار الصدر)",
        color_discrete_map={"منخفض": "green", "متوسط": "orange", "عالي": "red", "حرج": "darkred"}
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # تنبيهات وإرشادات استباقية للمنشآت الصحية
    st.warning("⚠️ **توصية استباقية للطوارئ:** عند تجاوز مؤشر الغبار لـ 300 AQI، يُنصح بزيادة الاستعداد الطبي في مستشفيات حائل وتوفير أجهزة البخار والأدوية الإسعافية في أقسام التنويه والطوارئ.")

# تشغيل الدالة داخل التطبيق
# render_emergency_dust_analysis()
    
    st.error("لم يتم العثور على الملف `hail_dust_predictions.csv`. تأكد من وجوده في نفس مجلد التطبيق.")
except Exception as e:
    st.error(f"حدث خطأ غير متوقع: {e}")
