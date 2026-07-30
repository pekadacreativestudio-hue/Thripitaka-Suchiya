import json
import re
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="ත්‍රිපිටක සූචිය",
    page_icon="☸",
    layout="centered",
)

DATA_PATH = Path(__file__).parent / "data" / "final_rows.json"

PK_VAR = {
    "විනය පිටකය": "--vinaya",
    "සූත්‍ර පිටකය": "--sutta",
    "අභිධර්ම පිටකය": "--abhi",
}


@st.cache_data
def load_rows():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


ROWS = load_rows()
BOOK_COUNT = len({r["nf"] for r in ROWS})

st.markdown(
    """
<style>
:root {
  --bg: #FFFDF9;
  --surface: #FFFFFF;
  --surface-2: #F6F3EC;
  --text: #2B2620;
  --muted: #8C8478;
  --accent: #C8983F;
  --accent-ink: #2B2620;
  --border: #ECE7DA;
  --vinaya: #B2716B;
  --sutta: #A08148;
  --abhi: #8F877A;
  --shadow: 0 1px 2px rgba(43,38,32,0.03), 0 2px 8px rgba(43,38,32,0.03);
  --radius: 14px;
}

html, body, [class*="css"]  {
  font-family: "Noto Sans Sinhala", "Iskoola Pota", "Nirmala UI", "Sinhala Sangam MN", system-ui, sans-serif;
}
.stApp { background: var(--bg); color: var(--text); color-scheme: light; }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: visible; }

.suchiya-eyebrow {
  font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
  color: var(--muted); font-family: system-ui, sans-serif;
}
.suchiya-title {
  font-size: 32px; font-weight: 700; margin: 2px 0 4px; color: var(--text);
}
.suchiya-subtitle { color: var(--muted); font-size: 14.5px; margin-bottom: 6px; }

div[data-testid="stTextInputRootElement"] {
  position: relative;
  border-radius: 14px !important;
}
div[data-testid="stTextInputRootElement"]::before {
  content: "\\2638";
  position: absolute;
  left: 6px;
  top: 50%;
  transform: translateY(-50%);
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--surface-2);
  color: var(--accent);
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 34px;
  text-align: center;
  z-index: 2;
}
div[data-testid="stTextInputRootElement"]::after {
  content: "";
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 17px;
  height: 17px;
  background-color: var(--muted);
  -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='7'/%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='7'/%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'/%3E%3C/svg%3E");
  -webkit-mask-size: contain;
  mask-size: contain;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  pointer-events: none;
  z-index: 2;
}
div[data-testid="stTextInputRootElement"] input {
  border-radius: 14px !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
  color: var(--text) !important;
  padding: 14px 44px 14px 50px !important;
  font-size: 17px !important;
}
div[data-testid="stTextInputRootElement"]:focus-within input {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 4px rgba(200,152,63,0.12) !important;
}

/* pitaka filter pills */
div[data-testid="stPillsButtonGroup"] label {
  border-radius: 999px !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
  font-size: 12.5px !important;
}
div[data-testid="stPillsButtonGroup"] label:has(input:checked) {
  border-color: var(--accent) !important;
  background: var(--surface-2) !important;
}

.stat-row { display: flex; gap: 30px; justify-content: center; margin: 26px 0 6px;
  font-family: system-ui, sans-serif; flex-wrap: wrap; }
.stat-row div { text-align: center; }
.stat-row b { display: block; font-size: 24px; color: var(--text); font-variant-numeric: tabular-nums; }
.stat-row small { color: var(--muted); font-size: 11px; letter-spacing: .06em; text-transform: uppercase; }

.rowsWrap { display: flex; flex-direction: column; }
.row { display: flex; gap: 12px; padding: 16px 4px; border-bottom: 1px solid var(--border); }
.row:last-child { border-bottom: none; }
.row-dot { flex: none; width: 9px; height: 9px; margin-top: 7px; border-radius: 50%;
  background: var(--pk-color, var(--accent)); }
.row-body { min-width: 0; flex: 1; }
.row .sutra { font-size: 17.5px; font-weight: 600; margin: 0 0 8px; color: var(--text); }
.row .sutra mark { background: rgba(200,152,63,0.28); color: inherit; border-radius: 3px; padding: 0 1px; }

.fieldgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 8px 20px; font-size: 14px; }
.fieldgrid label { display: block; font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase;
  color: var(--muted); font-family: system-ui, sans-serif; margin-bottom: 2px; }
.fieldgrid .val { color: var(--text); }
.fieldgrid .grantha .val { font-weight: 700; color: var(--accent); font-variant-numeric: tabular-nums; }
.pk-badge { display: inline-block; font-size: 11px; padding: 1px 8px; border-radius: 999px;
  font-family: system-ui, sans-serif; letter-spacing: .03em;
  background: color-mix(in srgb, var(--pk-color, var(--accent)) 14%, transparent);
  color: var(--pk-color, var(--accent)); }

.suchiya-footer { margin-top: 30px; padding-top: 16px; border-top: 1px solid var(--border);
  font-size: 12px; color: var(--muted); line-height: 1.6; font-family: system-ui, sans-serif; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="suchiya-eyebrow">Buddha Jayanthi Tripitaka</div>', unsafe_allow_html=True)
st.markdown('<div class="suchiya-title">ත්‍රිපිටක සූචිය</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="suchiya-subtitle">සූත්‍ර නාමයෙන් සොයන්න — වර්ගය, නිකාය, ග්‍රන්ථ නාමය සහ ග්‍රන්ථ අංකය ක්ෂණිකව</div>',
    unsafe_allow_html=True,
)

query = st.text_input(
    "සොයන්න",
    placeholder="සූත්‍රයේ නම ටයිප් කරන්න — උදා: මංගල, සතිපට්ඨාන, කරණීය",
    label_visibility="collapsed",
)

selected_pk = st.pills(
    "පිටකය",
    options=list(PK_VAR.keys()),
    selection_mode="multi",
    label_visibility="collapsed",
)


def escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def highlight(text: str, terms: list[str]) -> str:
    out = escape_html(text)
    for t in terms:
        if not t:
            continue
        out = re.sub(re.escape(t), lambda m: f"<mark>{m.group(0)}</mark>", out)
    return out


MAX_RENDER = 60

q = (query or "").strip()
active_pk = set(selected_pk or [])

if not q and not active_pk:
    st.markdown(
        f"""
    <div class="stat-row">
      <div><b>{len(ROWS):,}</b><small>සූත්‍ර/ගාථා/ජාතක ආදිය</small></div>
      <div><b>{BOOK_COUNT}</b><small>ත්‍රිපිටක ග්‍රන්ථ</small></div>
      <div><b>3</b><small>පිටක</small></div>
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
    terms = q.split()
    matches = [r for r in ROWS if all(t in r["s"] for t in terms)]
    if active_pk:
        matches = [r for r in matches if r["pk"] in active_pk]
    if q:
        matches.sort(key=lambda r: (0 if r["s"].startswith(q) else 1, len(r["s"])))

    if not matches:
        reason = f'"{escape_html(q)}" සඳහා' if q else "තෝරාගත් පිටකය සඳහා"
        st.markdown(
            f'<div style="text-align:center;color:var(--muted);padding:40px 0;">{reason} ප්‍රතිඵල හමු නොවීය.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.caption(f"{len(matches):,} ප්‍රතිඵල හමු විය")
        rows_html = []
        for r in matches[:MAX_RENDER]:
            pk_var = PK_VAR.get(r["pk"], "--accent")
            varga = escape_html(r["v"]) if r["v"] else "—"
            rows_html.append(
                f"""<div class="row" style="--pk-color:var({pk_var})">
  <i class="row-dot"></i>
  <div class="row-body">
    <p class="sutra">{highlight(r['s'], terms)}</p>
    <div class="fieldgrid">
      <div><label>වර්ගය</label><div class="val">{varga}</div></div>
      <div><label>නිකාය (කෙටි යෙදුම)</label><div class="val">{escape_html(r['nk'])}</div></div>
      <div><label>ත්‍රිපිටක ග්‍රන්ථයේ නම</label><div class="val">{escape_html(r['nf'])} <span class="pk-badge">{r['pk']}</span></div></div>
      <div class="grantha"><label>ත්‍රිපිටක ග්‍රන්ථ අංකය</label><div class="val">{escape_html(r['ga'])}</div></div>
    </div>
  </div>
</div>"""
            )
        st.markdown(f'<div class="rowsWrap">{"".join(rows_html)}</div>', unsafe_allow_html=True)

        if len(matches) > MAX_RENDER:
            st.caption(f"තවත් ප්‍රතිඵල {len(matches) - MAX_RENDER:,}ක් ඇත — සෙවුම වඩාත් නිශ්චිත කරන්න")

st.markdown(
    """
<div class="suchiya-footer">
මූලාශ්‍රය: <em>බුද්ධ ජයන්ති ත්‍රිපිටක ග්‍රන්ථ මාලා සූත්‍ර සුචිය</em> (අකාරාදී පිළිවෙළට) සහ ත්‍රිපිටක ග්‍රන්ථ ලැයිස්තුව.
පැරණි ලේඛන අනුවර්තනයක් බැවින් වර්ගය/සූත්‍ර නාමවල සුළු අකුරු වෙනස්කම් තිබිය හැක; නිකාය සහ ග්‍රන්ථ අංකය සත්‍යාපනය කර ඇත.
</div>
""",
    unsafe_allow_html=True,
)
