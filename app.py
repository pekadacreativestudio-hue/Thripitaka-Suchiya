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

PK_CLASS = {
    "විනය පිටකය": "pk-vinaya",
    "සූත්‍ර පිටකය": "pk-sutta",
    "අභිධර්ම පිටකය": "pk-abhi",
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
  --bg: #FBF8F1;
  --surface: #FFFFFF;
  --surface-2: #F4EDDC;
  --text: #4A3B2E;
  --muted: #A79C8C;
  --accent: #D1A857;
  --accent-ink: #4A3B2E;
  --border: #EFE7D6;
  --vinaya: #B2716B;
  --sutta: #AD8E63;
  --abhi: #A39A8C;
  --shadow: 0 1px 2px rgba(74,59,46,0.04), 0 3px 12px rgba(74,59,46,0.05);
  --radius: 16px;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #241512;
    --surface: #2F1D17;
    --surface-2: #3A2419;
    --text: #F1E6D2;
    --muted: #B7A48C;
    --accent: #E0B23C;
    --accent-ink: #241512;
    --border: #4A3226;
    --vinaya: #E39AA2;
    --sutta: #CDA268;
    --abhi: #AFA79B;
    --shadow: 0 1px 2px rgba(0,0,0,0.35), 0 6px 20px rgba(0,0,0,0.4);
  }
}

html, body, [class*="css"]  {
  font-family: "Noto Sans Sinhala", "Iskoola Pota", "Nirmala UI", "Sinhala Sangam MN", system-ui, sans-serif;
}
.stApp { background: var(--bg); color: var(--text); }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: visible; }

.suchiya-eyebrow {
  font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
  color: var(--muted); font-family: system-ui, sans-serif;
}
.suchiya-title {
  font-size: 32px; font-weight: 700; margin: 2px 0 4px; color: var(--text);
}
.suchiya-subtitle { color: var(--muted); font-size: 14.5px; margin-bottom: 6px; }

div[data-testid="stTextInput"] input {
  border-radius: 999px !important;
  border: 1.5px solid var(--border) !important;
  background: var(--surface) !important;
  color: var(--text) !important;
  padding: 12px 20px !important;
  font-size: 17px !important;
}
div[data-testid="stTextInput"] input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(201,151,31,0.22) !important;
}

.legend { display: flex; gap: 16px; flex-wrap: wrap; font-size: 12.5px; color: var(--muted);
  font-family: system-ui, sans-serif; margin: 4px 0 18px; }
.legend span { display: inline-flex; align-items: center; gap: 5px; }
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

.stat-row { display: flex; gap: 30px; justify-content: center; margin: 18px 0 6px;
  font-family: system-ui, sans-serif; flex-wrap: wrap; }
.stat-row div { text-align: center; }
.stat-row b { display: block; font-size: 24px; color: var(--text); font-variant-numeric: tabular-nums; }
.stat-row small { color: var(--muted); font-size: 11px; letter-spacing: .06em; text-transform: uppercase; }

.card {
  background: var(--surface); border: 1px solid var(--border);
  border-left: 3px solid var(--pk-color, var(--accent));
  border-radius: var(--radius); padding: 14px 18px; margin-bottom: 10px;
  box-shadow: var(--shadow);
}
.card .sutra { font-size: 18px; font-weight: 600; margin: 0 0 8px; color: var(--text); }
.card .sutra mark { background: rgba(209,168,87,0.32); color: inherit; border-radius: 3px; padding: 0 1px; }
.fieldgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 8px 20px; font-size: 14px; }
.fieldgrid label { display: block; font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase;
  color: var(--muted); font-family: system-ui, sans-serif; margin-bottom: 2px; }
.fieldgrid .val { color: var(--text); }
.fieldgrid .grantha .val { font-weight: 700; color: var(--accent); font-variant-numeric: tabular-nums; }
.pk-badge { display: inline-block; font-size: 11px; padding: 1px 8px; border-radius: 999px;
  font-family: system-ui, sans-serif; letter-spacing: .03em; }
.pk-vinaya { background: rgba(178,113,107,0.14); color: var(--vinaya); }
.pk-sutta { background: rgba(173,142,99,0.16); color: var(--sutta); }
.pk-abhi { background: rgba(163,154,140,0.18); color: var(--abhi); }

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

st.markdown(
    """
<div class="legend">
  <span><i class="dot" style="background:var(--vinaya)"></i>විනය පිටකය</span>
  <span><i class="dot" style="background:var(--sutta)"></i>සූත්‍ර පිටකය</span>
  <span><i class="dot" style="background:var(--abhi)"></i>අභිධර්ම පිටකය</span>
</div>
""",
    unsafe_allow_html=True,
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

if not q:
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
    matches.sort(key=lambda r: (0 if r["s"].startswith(q) else 1, len(r["s"])))

    if not matches:
        st.markdown(
            f'<div style="text-align:center;color:var(--muted);padding:40px 0;">'
            f'"{escape_html(q)}" සඳහා ප්‍රතිඵල හමු නොවීය. වෙනත් යතුරු පදයක් උත්සාහ කරන්න.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.caption(f"{len(matches):,} ප්‍රතිඵල හමු විය")
        cards = []
        for r in matches[:MAX_RENDER]:
            pk_class = PK_CLASS.get(r["pk"], "pk-sutta")
            varga = escape_html(r["v"]) if r["v"] else "—"
            cards.append(
                f"""<div class="card" style="--pk-color:var({'--vinaya' if pk_class=='pk-vinaya' else '--sutta' if pk_class=='pk-sutta' else '--abhi'})">
  <p class="sutra">{highlight(r['s'], terms)}</p>
  <div class="fieldgrid">
    <div><label>වර්ගය</label><div class="val">{varga}</div></div>
    <div><label>නිකාය (කෙටි යෙදුම)</label><div class="val">{escape_html(r['nk'])}</div></div>
    <div><label>ත්‍රිපිටක ග්‍රන්ථයේ නම</label><div class="val">{escape_html(r['nf'])} <span class="pk-badge {pk_class}">{r['pk']}</span></div></div>
    <div class="grantha"><label>ත්‍රිපිටක ග්‍රන්ථ අංකය</label><div class="val">{escape_html(r['ga'])}</div></div>
  </div>
</div>"""
            )
        st.markdown("\n".join(cards), unsafe_allow_html=True)

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
