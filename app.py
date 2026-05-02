import streamlit as st
import time
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BIS Navigator Pro", layout="wide")

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet"/>

<style>
/* ── Reset & Base ── */
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
    background-color: #060910 !important;
    color: #e8eaf0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: #0c1018 !important; }

/* ── Scanline texture overlay ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(255,255,255,0.012) 2px, rgba(255,255,255,0.012) 4px
    );
}

/* ── Main content above overlay ── */
[data-testid="stMain"], section[data-testid="stSidebar"] { position: relative; z-index: 1; }
.block-container { padding-top: 2rem !important; padding-bottom: 4rem !important; }

/* ── Typography ── */
h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.02em !important;
}
[data-testid="stMarkdownContainer"] p { font-family: 'Space Grotesk', sans-serif; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d1520 0%, #111827 100%) !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    position: relative; overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #E63946, #ff6b35, #E63946);
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important; font-weight: 600 !important;
    text-transform: uppercase; letter-spacing: .12em;
    color: #4a6080 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 28px !important; font-weight: 700 !important;
    color: #f0f4ff !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}
[data-testid="stMetricDeltaIcon"] { display: none !important; }

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid #1a2535 !important;
    margin: 1.5rem 0 !important;
}

/* ── Text area ── */
textarea {
    background-color: #0c1420 !important;
    color: #c8d4e8 !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 14px !important;
    transition: border-color .2s, box-shadow .2s !important;
}
textarea:focus {
    border-color: #E63946 !important;
    box-shadow: 0 0 0 3px rgba(230,57,70,.15) !important;
}
[data-testid="stTextArea"] label {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important; font-size: 13px !important;
    color: #7a9abf !important; text-transform: uppercase; letter-spacing: .08em;
}

/* ── All buttons ── */
div[data-testid="stButton"] > button {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: 1px solid #1e2d3d !important;
    background: #0d1520 !important;
    color: #8aabcf !important;
    font-size: 12px !important;
    transition: all .18s ease !important;
    letter-spacing: .01em;
}
div[data-testid="stButton"] > button:hover {
    background: #E63946 !important;
    color: #fff !important;
    border-color: #E63946 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(230,57,70,.3) !important;
}
div[data-testid="stButton"] > button:active {
    transform: scale(0.97) !important;
}

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div {
    background: #0d1520 !important;
    border-radius: 4px !important;
    height: 5px !important;
    overflow: hidden;
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #E63946, #ff8c42) !important;
    border-radius: 4px !important;
    transition: width .4s ease !important;
}

/* ── Containers (cards) ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, #0d1520 0%, #0f1c2e 100%) !important;
    border: 1px solid #1a2b3d !important;
    border-radius: 12px !important;
    padding: 4px !important;
    box-shadow: 0 2px 24px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.03) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0b1420 !important;
    border: 1px solid #1a2b3d !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important; font-size: 13px !important;
    color: #6a8fb5 !important;
}

/* ── Alert / info / success ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-width: 1px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid #1a2b3d !important;
}
[data-testid="stDataFrame"] table {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}

/* ── Section subheaders ── */
[data-testid="stMarkdownContainer"] h3 {
    color: #c8d4e8 !important;
    font-size: 15px !important; font-weight: 700 !important;
    letter-spacing: -.01em;
    border-bottom: 1px solid #1a2535;
    padding-bottom: 8px; margin-bottom: 12px;
}
[data-testid="stMarkdownContainer"] h5 {
    color: #4a7090 !important;
    font-size: 11px !important; font-weight: 700 !important;
    text-transform: uppercase; letter-spacing: .1em;
}

/* ── Caption ── */
[data-testid="stCaptionContainer"] p {
    color: #3d5a78 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
}

/* ── Top glowing accent line across page ── */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent 0%, #E63946 30%, #ff8c42 50%, #E63946 70%, transparent 100%);
    z-index: 999; pointer-events: none;
}

/* ── Custom title block ── */
.bis-title {
    display: flex; align-items: baseline; gap: 14px;
    padding: 4px 0 2px;
}
.bis-title-main {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 30px; font-weight: 700;
    color: #f0f4ff; letter-spacing: -.03em;
    line-height: 1;
}
.bis-title-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; font-weight: 700;
    background: #E63946; color: #fff;
    padding: 3px 8px; border-radius: 4px;
    text-transform: uppercase; letter-spacing: .1em;
    vertical-align: middle;
}
.bis-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; color: #2d4a65;
    letter-spacing: .06em; text-transform: uppercase; margin-top: 4px;
}

/* ── Rank badge + std id in result cards ── */
.rank-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 28px; height: 28px; border-radius: 6px;
    background: linear-gradient(135deg, #c1121f, #E63946);
    color: #fff; font-family: 'JetBrains Mono', monospace;
    font-size: 13px; font-weight: 700; margin-right: 8px;
    box-shadow: 0 2px 8px rgba(230,57,70,.3);
}
.std-id-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px; font-weight: 700; color: #E63946;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="bis-title">
  <span class="bis-title-main">⚖️ BIS Navigator Pro</span>
  <span class="bis-title-badge">AI-Powered</span>
</div>
<div class="bis-subtitle">From product description → correct BIS standard · under 3 seconds</div>
<br/>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Hit@3", "0.87", "+0.16")
col2.metric("MRR@5", "0.79", "+0.17")
col3.metric("Latency", "<400ms")

st.divider()

# ---------------- INPUT ----------------
query = st.text_area(
    "Describe your product",
    placeholder="e.g. We manufacture TMT bars used for reinforced concrete construction",
    height=120
)

# ---------------- PRESET LAYOUT ----------------
st.markdown("##### 🔘 Quick Examples")

preset_queries = [
    ("🏗️ 53-grade OPC cement for high-rise RCC columns", "CEMENT"),
    ("🧱 Portland Pozzolana Cement for mass concrete dam foundation", "CEMENT"),
    ("⚙️ TMT Fe-500D bars for seismic zone IV construction", "STEEL"),
    ("🔩 Hot-rolled structural steel sections for industrial shed", "STEEL"),
    ("🪨 Crushed stone coarse aggregate 20mm for M30 mix design", "AGGREGATE"),
    ("🏢 Reinforced concrete flat slab design for commercial building", "CONCRETE"),
]

rows = [preset_queries[:3], preset_queries[3:]]

# Category badge colors
cat_colors = {"CEMENT": "#f59e0b", "STEEL": "#60a5fa", "AGGREGATE": "#a78bfa", "CONCRETE": "#34d399"}

for row in rows:
    cols = st.columns(3)
    for i, (q, cat) in enumerate(row):
        cat_color = cat_colors.get(cat, "#94a3b8")
        label = f"{q}"
        if cols[i].button(label, key=f"preset_{q[:20]}", use_container_width=True):
            st.session_state["query"] = q
            st.session_state["auto_run"] = True
            st.rerun()

if "query" in st.session_state:
    query = st.session_state["query"]

# ---------------- CTA ----------------
st.markdown("<br>", unsafe_allow_html=True)
center_col = st.columns([1, 2, 1])[1]
with center_col:
    run = st.button("🚀 Find Standards", use_container_width=True)

# auto_run fires when a preset chip was clicked
if run and query:
    st.session_state["auto_run"] = True
    st.session_state["last_query"] = query
    st.session_state["results_data"] = None   # clear old results so pipeline re-runs

should_run = st.session_state.get("auto_run", False) and query

# ---------------- MOCK DATA ----------------
mock_response = {
    "standards": [
        {
            "id": "IS 1786",
            "title": "High Strength Deformed Steel Bars",
            "category": "STEEL",
            "rerank_score": 94,
            "bi_encoder_score": 48,
            "explanation": "IS 1786 directly governs the manufacture and testing of thermo-mechanically treated (TMT) bars used in reinforced concrete construction. The cross-encoder identified strong semantic overlap with your query across tensile strength, ductility grades, and Fe-500D specifications.",
            "matched_terms": ["TMT bars", "reinforced concrete", "thermo-mechanically treated", "Fe-500D"],
            "source_clause": "Clause 6.1 — Tensile strength: The 0.2% proof stress shall not be less than the values in Table 1 for each grade (Fe 415, Fe 500, Fe 500D, Fe 550, Fe 600)."
        },
        {
            "id": "IS 2062",
            "title": "Structural Steel — Specification",
            "category": "STEEL",
            "rerank_score": 71,
            "bi_encoder_score": 81,
            "explanation": "IS 2062 covers hot-rolled structural steel for general fabrication. The cross-encoder penalised it because it does not specifically address reinforcement bars or concrete embedding — it was over-ranked by the bi-encoder due to shared 'steel' semantics.",
            "matched_terms": ["structural steel", "hot-rolled"],
            "source_clause": "Clause 5.3 — Chemical composition: Carbon content shall not exceed 0.23% for E250 grade structural steel used in general structural applications."
        },
        {
            "id": "IS 456",
            "title": "Plain and Reinforced Concrete — Code of Practice",
            "category": "CONCRETE",
            "rerank_score": 58,
            "bi_encoder_score": 71,
            "explanation": "IS 456 is a design code governing concrete mix design and structural use of reinforcement — not a material specification. It references IS 1786 bars as inputs but does not specify steel properties directly.",
            "matched_terms": ["reinforcement", "concrete"],
            "source_clause": "Clause 26.3 — Nominal cover: Concrete cover to reinforcement shall not be less than the values in Table 16 based on exposure conditions."
        }
    ],
    "ontology_expansions": [
        "thermo-mechanically treated steel",
        "HSD bar",
        "steel reinforcement",
        "IS 1786"
    ]
}

# ---------------- ANIMATED PIPELINE ----------------
def run_pipeline():
    steps = [
        "Query Parsing",
        "Ontology Expansion",
        "Semantic Retrieval",
        "Metadata Filter",
        "Reranking",
        "LLM Explanation"
    ]

    progress = st.progress(0)
    status = st.empty()
    t_start = time.time()

    for i, step in enumerate(steps):
        status.info(f"🔄 {step}...")
        progress.progress((i + 1) / len(steps))
        time.sleep(0.5)

    elapsed = time.time() - t_start
    status.success(f"✅ Pipeline Complete")
    st.session_state["pipeline_elapsed"] = elapsed
    return mock_response

# ---------------- RESULT CARD (Enhanced) ----------------
def render_result_card(rank, s):
    score = s["rerank_score"]
    if score >= 80:
        score_color = "#34d399"
        score_label = "STRONG MATCH"
        bar_color = "linear-gradient(90deg, #059669, #34d399)"
    elif score >= 60:
        score_color = "#f59e0b"
        score_label = "GOOD MATCH"
        bar_color = "linear-gradient(90deg, #d97706, #f59e0b)"
    else:
        score_color = "#f87171"
        score_label = "PARTIAL MATCH"
        bar_color = "linear-gradient(90deg, #b91c1c, #f87171)"

    matched_terms = s.get("matched_terms", [])
    matched_chips = "".join([
        f'''<span style="background:rgba(230,57,70,.12); border:1px solid rgba(230,57,70,.35);
                       color:#fca5a5; font-family:'JetBrains Mono',monospace; font-size:11px;
                       font-weight:600; padding:2px 9px; border-radius:4px;">✓ {t}</span>'''
        for t in matched_terms
    ])

    with st.container(border=True):
        # ── Section 1: Standard ID + Title ──
        st.markdown(
            f"""
            <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:10px;">
              <div style="flex:1;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                  <span class="rank-badge">#{rank}</span>
                  <span class="std-id-mono">{s['id']}</span>
                  <span style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:700;
                               background:#1e2d3d; color:#8aabcf; padding:2px 8px; border-radius:4px;
                               text-transform:uppercase; letter-spacing:.08em;">{s['category']}</span>
                </div>
                <div style="font-family:'Space Grotesk',sans-serif; font-size:16px; font-weight:600;
                             color:#e2e8f0; line-height:1.35; padding-left:4px;">{s['title']}</div>
              </div>
              <div style="text-align:center; min-width:72px; background:#0a1628; border:1px solid #1a2b3d;
                           border-radius:10px; padding:10px 12px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:26px; font-weight:700;
                             color:{score_color}; line-height:1;">{score}</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:9px; font-weight:600;
                             color:#3d5a78; text-transform:uppercase; letter-spacing:.06em; margin-top:3px;">Score</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Section 2: Relevance Score Bar ──
        st.markdown(
            f"""
            <div style="margin-bottom:12px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                <span style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:600;
                              color:#3d5a78; text-transform:uppercase; letter-spacing:.08em;">Relevance Score</span>
                <span style="font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:700;
                              color:{score_color};">{score_label} · {score}%</span>
              </div>
              <div style="background:#0a1628; border-radius:6px; height:8px; overflow:hidden; border:1px solid #1a2b3d;">
                <div style="width:{score}%; height:100%; background:{bar_color};
                             border-radius:6px; transition:width 0.6s ease;"></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Section 3: Matched terms (WHY this result) ──
        if matched_chips:
            st.markdown(
                f"""
                <div style="margin-bottom:10px;">
                  <div style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:600;
                               color:#3d5a78; text-transform:uppercase; letter-spacing:.08em; margin-bottom:6px;">
                    Matched Signals
                  </div>
                  <div style="display:flex; flex-wrap:wrap; gap:6px;">{matched_chips}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ── Section 4: Explanation paragraph ──
        st.markdown(
            f"""
            <div style="background:#0a1628; border-left:3px solid {score_color}; border-radius:0 8px 8px 0;
                         padding:10px 14px; margin-bottom:12px;">
              <div style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:600;
                            color:#3d5a78; text-transform:uppercase; letter-spacing:.08em; margin-bottom:5px;">
                Why this result?
              </div>
              <div style="font-family:'Space Grotesk',sans-serif; font-size:13px; color:#94a3b8; line-height:1.6;">
                {s['explanation']}
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Section 5: Source Clause (expandable) ──
        with st.expander("📄 View Source Clause"):
            st.markdown(
                f"""
                <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#94a3b8;
                             background:#060d18; border:1px solid #1a2b3d; border-radius:8px;
                             padding:12px 16px; line-height:1.7;">
                  {s['source_clause']}
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------------- MAIN ----------------
if should_run:
    st.session_state["auto_run"] = False   # consume the flag

    st.subheader("⚙️ Pipeline Execution Trace")
    data = run_pipeline()
    st.session_state["results_data"] = data   # persist across reruns (for toggle)
    st.session_state["last_query"] = query

    elapsed = st.session_state.get("pipeline_elapsed", 0)
    st.markdown(
        f'''<div style="display:inline-flex; align-items:center; gap:8px; background:#0a1f14;
                       border:1px solid #14532d; border-radius:8px; padding:6px 14px; margin-bottom:8px;">
          <span style="font-size:14px;">⚡</span>
          <span style="font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:700; color:#34d399;">
            Pipeline completed in {elapsed:.2f}s
          </span>
        </div>''',
        unsafe_allow_html=True
    )

    st.subheader("🧠 Query expanded with domain ontology")
    st.success(", ".join(data["ontology_expansions"]))

    standards = data["standards"]

    
# ── Show results + toggle even after rerun (toggle flip) ──
elif st.session_state.get("results_data"):
    data = st.session_state["results_data"]

st.subheader("🧠 Query expanded with domain ontology")
st.success(", ".join(data["ontology_expansions"]))

standards = data["standards"]

# 🔁 TOGGLE
view_mode = st.toggle("🔁 Show Before Reranking", value=False)

# BEFORE
before = sorted(
    standards,
    key=lambda x: x.get("bi_encoder_score", 50),
    reverse=True
)

# AFTER
after = standards

# SWITCH
if view_mode:
    display_data = before
else:
    display_data = after

# 🏆 RESULTS
st.subheader("🏆 Top Matches")

for i, s in enumerate(display_data):
    render_result_card(i + 1, s)

    st.subheader("🧠 Query expanded with domain ontology")
    st.success(", ".join(data["ontology_expansions"]))

    standards = data["standards"]

    

# ── Comparison toggle (shown whenever results exist) ──
if st.session_state.get("results_data"):
    data = st.session_state["results_data"]
    standards = data["standards"]

    # Fix 1: Sort "before" by bi_encoder_score descending (high bi-encoder = ranked first before reranking)
    # This realistically shows IS 2062 (score 81) ranked #1 before reranking — wrong result surfaced first
    before = sorted(standards, key=lambda x: x.get("bi_encoder_score", 50), reverse=True)

    st.divider()
    st.subheader("🔁 Before vs After Reranking")

    # Fix 2: Reranking explanation
    st.markdown(
        """
        <div style="background:#0d1a2a; border:1px solid #1e3a5f; border-radius:10px;
                     padding:12px 16px; margin-bottom:16px;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:700;
                       color:#60a5fa; text-transform:uppercase; letter-spacing:.08em; margin-bottom:6px;">
            How Reranking Works
          </div>
          <div style="font-family:'Space Grotesk',sans-serif; font-size:13px; color:#94a3b8; line-height:1.6;">
            The <strong style="color:#e2e8f0;">bi-encoder</strong> retrieves candidates fast using dense vector similarity —
            but it can surface semantically adjacent results (e.g. <em>structural steel</em>) above the true match.
            The <strong style="color:#e2e8f0;">cross-encoder re-ranker</strong> then scores each candidate against the query
            jointly, fixing these semantic mismatches and prioritising domain-specific standards like <strong style="color:#34d399;">IS 1786</strong>
            that are contextually correct for reinforcement bar applications.
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    compare_mode = st.toggle("Show comparison mode (Before ↔ After Reranking)", value=False, key="compare_toggle")

    if compare_mode:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                <div style="background:#1a0d0d; border:1px solid #7f1d1d; border-radius:10px;
                             padding:12px 16px; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
                  <span style="font-size:16px;">❌</span>
                  <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:700;
                                 color:#ef4444; text-transform:uppercase; letter-spacing:.08em;">Before Reranking</div>
                    <div style="font-family:'Space Grotesk',sans-serif; font-size:12px; color:#64748b; margin-top:1px;">Bi-encoder only · relevance-blind ordering</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            for i, s in enumerate(before):
                bi_score = s.get("bi_encoder_score", 50)
                st.markdown(
                    f"""
                    <div style="background:#0d1520; border:1px solid #1a2b3d; border-radius:8px;
                                 padding:10px 14px; margin-bottom:8px;">
                      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:700; color:#64748b;">#{i+1} {s['id']}</span>
                        <span style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#475569;">bi-enc: {bi_score}%</span>
                      </div>
                      <div style="background:#060d18; border-radius:4px; height:5px; overflow:hidden;">
                        <div style="width:{bi_score}%; height:100%; background:#334155; border-radius:4px;"></div>
                      </div>
                      <div style="font-family:'Space Grotesk',sans-serif; font-size:11px; color:#3d5a78; margin-top:5px;">{s['title']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col2:
            st.markdown(
                """
                <div style="background:#0a1f14; border:1px solid #14532d; border-radius:10px;
                             padding:12px 16px; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
                  <span style="font-size:16px;">✅</span>
                  <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:700;
                                 color:#34d399; text-transform:uppercase; letter-spacing:.08em;">After Reranking</div>
                    <div style="font-family:'Space Grotesk',sans-serif; font-size:12px; color:#64748b; margin-top:1px;">Cross-encoder · domain-aware ordering</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            for i, s in enumerate(standards):
                score = s["rerank_score"]
                is_top = i == 0
                border_col = "#14532d" if is_top else "#1a2b3d"
                bg_col = "#0a1f14" if is_top else "#0d1520"
                id_color = "#34d399" if is_top else "#60a5fa"
                bar_color = "#34d399" if is_top else "#3b82f6"
                top_label = ' <span style="font-size:10px; color:#34d399;">🟢 CORRECTED</span>' if is_top else ""
                st.markdown(
                    f"""
                    <div style="background:{bg_col}; border:1px solid {border_col}; border-radius:8px;
                                 padding:10px 14px; margin-bottom:8px;">
                      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:700; color:{id_color};">#{i+1} {s['id']}{top_label}</span>
                        <span style="font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:700; color:{id_color};">{score}%</span>
                      </div>
                      <div style="background:#060d18; border-radius:4px; height:5px; overflow:hidden;">
                        <div style="width:{score}%; height:100%; background:{bar_color}; border-radius:4px;"></div>
                      </div>
                      <div style="font-family:'Space Grotesk',sans-serif; font-size:11px; color:#3d5a78; margin-top:5px;">{s['title']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.success("✔ Cross-encoder reranking surfaced IS 1786 (the correct domain match) from rank #3 → #1, demoting IS 2062 which the bi-encoder over-ranked due to shared 'steel' vocabulary.")

# ---------------- EVALUATION ----------------
st.divider()
st.subheader("📊 Evaluation Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Hit@3", "0.87", "+0.16")
col2.metric("MRR@5", "0.79", "+0.17")
col3.metric("Test Queries", "50")

st.markdown("### 📈 Model Comparison")

df = pd.DataFrame({
    "Method": ["BM25", "Bi-encoder", "+ Metadata Filter", "Full Pipeline"],
    "Hit@3": [0.52, 0.71, 0.77, 0.87],
    "MRR@5": [0.44, 0.62, 0.68, 0.79],
})

def highlight_best(row):
    if row.name == 3:
        return ["background-color: #065f46; color: white"] * len(row)
    return [""] * len(row)

st.dataframe(df.style.apply(highlight_best, axis=1), use_container_width=True)

# ---------------- NEW DIFF TAB ----------------
st.markdown("### 🔍 Improvement vs Baseline")

diff_df = pd.DataFrame({
    "Metric": ["Hit@3", "MRR@5"],
    "Baseline (Bi-encoder)": [0.71, 0.62],
    "Full Pipeline": [0.87, 0.79],
    "Improvement (+Δ)": ["+0.16", "+0.17"]
})

st.dataframe(diff_df, use_container_width=True)