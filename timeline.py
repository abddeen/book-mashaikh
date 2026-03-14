import pandas as pd
import plotly.graph_objects as go

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv("timeline_data.csv")
df = df.sort_values(["part", "born_ce"]).reset_index(drop=True)

# ── Era configuration ──────────────────────────────────────────────────────────
ERA = {
    1: {"label": "Part 1 · Seeds of Tasawwuf",          "color": "#C17817"},
    2: {"label": "Part 2 · Crystallization",             "color": "#4A90D9"},
    3: {"label": "Part 3 · Systematization",             "color": "#2A9D8F"},
    4: {"label": "Part 4 · The Golden Age",              "color": "#E9C46A"},
    5: {"label": "Part 5 · Age of Expansion",            "color": "#57A773"},
    6: {"label": "Part 6 · Era of Revival",              "color": "#C1666B"},
    7: {"label": "Part 7 · The Modern Era",              "color": "#9B72CF"},
}

# ── Build y-axis layout ────────────────────────────────────────────────────────
# Assign a y-integer to every figure, with a 2-row gap between eras.
y_tick_vals = []
y_tick_text = []
era_spans   = {}   # part -> (y_start, y_end)
current_y   = 0

for part_num in range(1, 8):
    part_df   = df[df["part"] == part_num]
    era_start = current_y

    for _, row in part_df.iterrows():
        y_tick_vals.append(current_y)
        y_tick_text.append(row["name"])
        current_y += 1

    era_spans[part_num] = (era_start, current_y - 1)

    if part_num < 7:
        current_y += 2          # gap between eras

total_rows = current_y

# ── Build figure ───────────────────────────────────────────────────────────────
fig = go.Figure()

# 1. Era background shading
for part_num, (y0, y1) in era_spans.items():
    fig.add_hrect(
        y0=y0 - 0.5, y1=y1 + 0.5,
        fillcolor=ERA[part_num]["color"],
        opacity=0.07,
        line_width=0,
        layer="below",
    )

# 2. Horizontal bars — one trace per era so the legend works
for part_num in range(1, 8):
    part_df    = df[df["part"] == part_num]
    color      = ERA[part_num]["color"]
    era_start  = era_spans[part_num][0]

    for idx, (_, row) in enumerate(part_df.iterrows()):
        y        = era_start + idx
        duration = row["died_ce"] - row["born_ce"]
        living   = bool(row["living"])

        fig.add_trace(go.Bar(
            x=[duration],
            y=[y],
            base=[row["born_ce"]],
            orientation="h",
            marker=dict(
                color=color,
                opacity=0.45 if living else 0.88,
                line=dict(
                    color="rgba(255,255,255,0.35)" if not living
                          else color,
                    width=0.4 if not living else 1.5,
                ),
            ),
            name=ERA[part_num]["label"],
            legendgroup=f"part{part_num}",
            showlegend=(idx == 0),        # one legend entry per era
            hovertemplate=(
                f"<b>{row['name']}</b><br>"
                f"Chapter {row['chapter']}<br>"
                f"Born: {row['born_ce']} CE<br>"
                + ("Still living" if living
                   else f"Died: {int(row['died_ce'])} CE")
                + "<br>"
                f"<i>{row['era_label']}</i>"
                "<extra></extra>"
            ),
        ))

# 3. Era divider lines
for part_num in range(1, 7):
    _, y_end = era_spans[part_num]
    fig.add_hline(
        y=y_end + 1,
        line_color="rgba(255,255,255,0.12)",
        line_width=1,
        line_dash="dot",
    )

# 4. Century grid lines + labels at top
for year in range(600, 2100, 100):
    fig.add_vline(
        x=year,
        line_color="rgba(255,255,255,0.07)",
        line_width=1,
    )

# 5. Era labels on the right-hand side
for part_num, (y0, y1) in era_spans.items():
    fig.add_annotation(
        x=2060, y=(y0 + y1) / 2,
        text=ERA[part_num]["label"],
        showarrow=False,
        font=dict(size=9, color=ERA[part_num]["color"]),
        xanchor="left",
        xref="x",
        yref="y",
    )

# ── Layout ─────────────────────────────────────────────────────────────────────
height = max(3000, total_rows * 19 + 120)

fig.update_layout(
    title=dict(
        text=(
            "<b>Book of the Mashaikh</b>"
            " · Timeline of 126 Sufi Luminaries"
            " · 600 – 2025 CE"
        ),
        font=dict(size=20, color="white", family="Georgia, serif"),
        x=0.5,
        xanchor="center",
        y=0.995,
        yanchor="top",
    ),
    xaxis=dict(
        title=dict(
            text="Year CE",
            font=dict(color="rgba(255,255,255,0.55)", size=12),
        ),
        range=[490, 2120],
        tickmode="linear",
        dtick=100,
        tickfont=dict(color="rgba(255,255,255,0.7)", size=11),
        gridcolor="rgba(255,255,255,0.07)",
        zeroline=False,
        showgrid=True,
        side="top",              # year labels at top AND bottom
        mirror=True,
    ),
    yaxis=dict(
        tickmode="array",
        tickvals=y_tick_vals,
        ticktext=y_tick_text,
        tickfont=dict(size=9.5, color="rgba(255,255,255,0.82)"),
        gridcolor="rgba(255,255,255,0.03)",
        range=[-0.5, total_rows + 0.5],
        autorange="reversed",   # earliest era at the top
    ),
    legend=dict(
        orientation="h",
        x=0.5, xanchor="center",
        y=-0.02, yanchor="top",
        font=dict(size=11, color="white"),
        bgcolor="rgba(0,0,0,0.4)",
        bordercolor="rgba(255,255,255,0.15)",
        borderwidth=1,
        traceorder="normal",
    ),
    plot_bgcolor="#0d0d1a",
    paper_bgcolor="#080810",
    font=dict(color="white", family="Georgia, serif"),
    height=height,
    width=1900,
    margin=dict(l=310, r=230, t=90, b=70),
    barmode="overlay",
)

# ── Export ─────────────────────────────────────────────────────────────────────
fig.write_html("timeline.html")
print(f"Saved: timeline.html  ({total_rows} rows, height={height}px)")

# Static image requires kaleido:  pip install kaleido
try:
    fig.write_image("timeline.png", scale=2)
    print("Saved: timeline.png")
except Exception as e:
    print(f"PNG skipped (install kaleido to enable): {e}")

fig.show()
