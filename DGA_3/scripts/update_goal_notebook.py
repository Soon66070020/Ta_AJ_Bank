import json
import re
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

nb_path = 'group_5/shipment_goal_analysis.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 1 Source (Top 5 Categories Overview)
cell_top5_overview_src = """# ✅ Cell 8: Goal 2 — Focus ภาพรวม Top 5 หมวดหมู่อุตสาหกรรมหลัก (Top 5 TSIC Product Categories Overview)
# สกัดและวิเคราะห์ 5 หมวดหมู่อุตสาหกรรมที่มีขนาดใหญ่ที่สุดในไทย (ค่าน้ำหนักรวมกัน 58.24% ของผลผลิตอุตสาหกรรมทั้งประเทศ)

df_div = df_tidy[df_tidy['category_level'] == 1].copy()
div_summary = df_div.groupby(['tsic_division_code', 'tsic_division_name']).agg(
    weight=('weight', 'first'),
    avg_index=('shipment_index', 'mean'),
    min_index=('shipment_index', 'min'),
    max_index=('shipment_index', 'max'),
    latest_index=('shipment_index', 'last')
).reset_index().sort_values(by='weight', ascending=False)

top5_div = div_summary.head(5).copy()
top5_div_names = top5_div['tsic_division_name'].tolist()

# กำหนดโทนสีเฉพาะสำหรับ 5 หมวดหมู่อุตสาหกรรมหลัก
div_colors_top5 = {
    'การผลิตผลิตภัณฑ์อาหาร': '#E9C46A',                                            # เหลืองทองมัสตาร์ด
    'การผลิตยานยนต์ รถพ่วง และรถกึ่งพ่วง': '#E76F51',                               # แดงส้มอิฐ
    'การผลิตถ่านโค้กและผลิตภัณฑ์ที่ได้จากการกลั่นปิโตรเลียม': '#457B9D',              # ฟ้าหม่นคลาสสิก
    'การผลิตผลิตภัณฑ์คอมพิวเตอร์ อิเล็กทรอนิกส์ และอุปกรณ์ที่ใช้ในทางทัศนศาสตร์': '#F4A261',  # ส้มทอง
    'การผลิตผลิตภัณฑ์ยางและพลาสติก': '#1D3557'                                     # กรมท่าสุขุม
}

# สร้างกราฟเปรียบเทียบ 2 มิติ: สัดส่วนค่าน้ำหนัก vs ดัชนีการส่งสินค้าเฉลี่ย
fig_top5_overview = make_subplots(
    rows=1, cols=2,
    subplot_titles=(
        '<b>1. สัดส่วนค่าน้ำหนักทางเศรษฐกิจ (Weight Share %)</b>',
        '<b>2. ดัชนีการส่งสินค้าเฉลี่ยตลอด 66 เดือน (Avg Shipment Index)</b>'
    ),
    horizontal_spacing=0.15,
    specs=[[{"type": "bar"}, {"type": "bar"}]]
)

top5_div_sorted_w = top5_div.sort_values(by='weight', ascending=True)
top5_div_sorted_idx = top5_div.sort_values(by='avg_index', ascending=True)

# 1. Bar Chart: สัดส่วนค่าน้ำหนัก (Weight Share)
fig_top5_overview.add_trace(
    go.Bar(
        y=[n[:26] + '...' if len(n) > 26 else n for n in top5_div_sorted_w['tsic_division_name']],
        x=top5_div_sorted_w['weight'],
        orientation='h',
        marker=dict(color=[div_colors_top5.get(n, '#2A9D8F') for n in top5_div_sorted_w['tsic_division_name']]),
        text=[f"{w:.2f}%" for w in top5_div_sorted_w['weight']],
        textposition='outside',
        customdata=np.stack((top5_div_sorted_w['tsic_division_name'], top5_div_sorted_w['weight'], top5_div_sorted_w['avg_index']), axis=-1),
        hovertemplate='<b>หมวด:</b> %{customdata[0]}<br><b>ค่าน้ำหนัก:</b> %{customdata[1]:.2f}%<br><b>ดัชนีเฉลี่ย:</b> %{customdata[2]:.2f} จุด<extra></extra>',
        showlegend=False
    ),
    row=1, col=1
)

# 2. Bar Chart: ดัชนีการส่งสินค้าเฉลี่ย (Avg Shipment Index)
fig_top5_overview.add_trace(
    go.Bar(
        y=[n[:26] + '...' if len(n) > 26 else n for n in top5_div_sorted_idx['tsic_division_name']],
        x=top5_div_sorted_idx['avg_index'],
        orientation='h',
        marker=dict(color=[div_colors_top5.get(n, '#2A9D8F') for n in top5_div_sorted_idx['tsic_division_name']]),
        text=[f"{idx:.2f} จุด" for idx in top5_div_sorted_idx['avg_index']],
        textposition='outside',
        customdata=np.stack((top5_div_sorted_idx['tsic_division_name'], top5_div_sorted_idx['avg_index'], top5_div_sorted_idx['weight']), axis=-1),
        hovertemplate='<b>หมวด:</b> %{customdata[0]}<br><b>ดัชนีเฉลี่ย:</b> %{customdata[1]:.2f} จุด<br><b>ค่าน้ำหนัก:</b> %{customdata[2]:.2f}%<extra></extra>',
        showlegend=False
    ),
    row=1, col=2
)

# เส้นอ้างอิงระดับปีฐาน (Base Year = 100 จุด)
fig_top5_overview.add_vline(x=100, line_width=2, line_dash="dash", line_color="#777777", row=1, col=2)

fig_top5_overview.update_xaxes(title_text='<b>สัดส่วนค่าน้ำหนักในตะกร้า (%) — เริ่มจาก 0%</b>', rangemode='tozero', range=[0, 20], row=1, col=1)
fig_top5_overview.update_xaxes(title_text='<b>ดัชนีการส่งสินค้าเฉลี่ย (จุด) — ฐาน 100</b>', rangemode='tozero', range=[0, 145], row=1, col=2)

fig_top5_overview.update_layout(
    title='<b>🏭 ภาพรวม 5 หมวดหมู่อุตสาหกรรมหลักของประเทศไทย (Top 5 TSIC Product Categories Overview)</b><br><sup>ครองสัดส่วนค่าน้ำหนักรวมกัน 58.24% ของประเทศ (เปรียบเทียบขนาดทางเศรษฐกิจ vs ประสิทธิภาพการส่งมอบเฉลี่ย 66 เดือน)</sup>',
    template=PLOTLY_TEMPLATE,
    height=480,
    margin=dict(t=90, l=10, r=40, b=60)
)

fig_top5_overview.show()
"""

# Cell 2 Source (Drill-down to Top 10 Products under Top 5 Categories)
cell_drilldown_top10_src = """# ✅ Cell 9: Goal 2 — เจาะลึกขยายจาก Top 5 หมวดหมู่ สู่ Top 10 สินค้าขับเคลื่อนหลัก (Drill-down to Top 10 Products under Top 5 Categories)
# สกัดสินค้าลึกสุด (Level 4: PRODUCT_ITEM) ที่สังกัดอยู่ใน 5 หมวดหลัก พร้อมปุ่มสลับดูตามดัชนีส่งมอบ (Performance) และค่าน้ำหนัก (Weight)

l4_in_top5 = df_tidy[(df_tidy['category_level'] == 4) & (df_tidy['tsic_division_name'].isin(top5_div_names))].copy()

# รวมสถิติรายสินค้า
l4_top5_summary = l4_in_top5.groupby(['product_code', 'item_name', 'tsic_division_name', 'tsic_class_name', 'weight']).agg(
    avg_index=('shipment_index', 'mean'),
    latest_index=('shipment_index', 'last')
).reset_index()

# 1. Top 10 ตามดัชนีส่งสินค้าเฉลี่ย (Growth / Performance)
top10_by_performance = l4_top5_summary.sort_values(by='avg_index', ascending=False).head(10).sort_values(by='avg_index', ascending=True)

# 2. Top 10 ตามค่าน้ำหนักทางเศรษฐกิจ (Weight / Size)
top10_by_weight_share = l4_top5_summary.sort_values(by='weight', ascending=False).head(10).sort_values(by='weight', ascending=True)

# ฟังก์ชันจัดเตรียม Payload สำหรับ Trace
def create_trace_payload(df, val_col, unit_label, max_len=34):
    y_labels = [n[:max_len] + '...' if len(n) > max_len else n for n in df['item_name']]
    colors = [div_colors_top5.get(d, '#2A9D8F') for d in df['tsic_division_name']]
    texts = [f"{v:.2f} {unit_label}" for v in df[val_col]]
    customdata = []
    for _, r in df.iterrows():
        customdata.append([r['item_name'], r['product_code'], r['tsic_division_name'], r['tsic_class_name'], r['avg_index'], r['weight']])
    return {
        'x': df[val_col].tolist(),
        'y': y_labels,
        'colors': colors,
        'texts': texts,
        'customdata': customdata
    }

payload_perf = create_trace_payload(top10_by_performance, 'avg_index', 'จุด')
payload_wt = create_trace_payload(top10_by_weight_share, 'weight', '%')

fig_drilldown = go.Figure()

# Main Trace 0 (Default: Top 10 by Shipment Index)
fig_drilldown.add_trace(go.Bar(
    x=payload_perf['x'],
    y=payload_perf['y'],
    orientation='h',
    marker=dict(color=payload_perf['colors']),
    text=payload_perf['texts'],
    textposition='outside',
    customdata=payload_perf['customdata'],
    showlegend=False,
    hovertemplate=(
        "<b>สินค้า:</b> %{customdata[0]}<br>" +
        "<b>รหัสสินค้า:</b> %{customdata[1]}<br>" +
        "<b>หมวดหลัก (Div):</b> %{customdata[2]}<br>" +
        "<b>กิจกรรมย่อย (Class):</b> %{customdata[3]}<br>" +
        "<b>ดัชนีส่งสินค้าเฉลี่ย:</b> %{customdata[4]:.2f} จุด<br>" +
        "<b>ค่าน้ำหนักในตะกร้า:</b> %{customdata[5]:.3f}%<extra></extra>"
    )
))

# 🏷️ เพิ่ม Legend กำกับ 5 หมวดหมู่อุตสาหกรรมสังกัด
for div_name in top5_div_names:
    fig_drilldown.add_trace(go.Bar(
        x=[None], y=[None],
        name=div_name,
        marker=dict(color=div_colors_top5.get(div_name, '#2A9D8F')),
        showlegend=True
    ))

# ปุ่ม Toggle ระหว่างดูตามดัชนีส่งมอบ (Performance) และค่าน้ำหนัก (Weight)
btn_performance = {
    'args': [
        {
            'x': [payload_perf['x']],
            'y': [payload_perf['y']],
            'marker.color': [payload_perf['colors']],
            'text': [payload_perf['texts']],
            'customdata': [payload_perf['customdata']]
        },
        {
            'title.text': '<b>🔍 Drill-down: Top 10 สินค้าที่มีดัชนีส่งมอบสูงสุด (ภายใต้ 5 หมวดหมู่อุตสาหกรรมหลัก)</b><br><sup>สะท้อนสินค้าที่มีการเติบโตและส่งมอบสินค้าก้าวกระโดดสูงสุดในช่วง 66 เดือน (แกน X เริ่มจาก 0 จุด)</sup>',
            'xaxis.title.text': '<b>ดัชนีการส่งสินค้าเฉลี่ย (จุด) — เริ่มต้นจาก 0.00 จุด</b>',
            'xaxis.range': [0, 460]
        },
        [0]
    ],
    'label': '🏆 Top 10 ตามดัชนีการส่งสินค้า (Growth / Performance)',
    'method': 'update'
}

btn_weight = {
    'args': [
        {
            'x': [payload_wt['x']],
            'y': [payload_wt['y']],
            'marker.color': [payload_wt['colors']],
            'text': [payload_wt['texts']],
            'customdata': [payload_wt['customdata']]
        },
        {
            'title.text': '<b>🔍 Drill-down: Top 10 สินค้าที่มีค่าน้ำหนักสูงสุด (ภายใต้ 5 หมวดหมู่อุตสาหกรรมหลัก)</b><br><sup>สะท้อนสินค้าเสาหลักที่มีบทบาทและขนาดเชิงมูลค่าผลผลิตสูงที่สุดของประเทศ (แกน X เริ่มจาก 0%)</sup>',
            'xaxis.title.text': '<b>สัดส่วนค่าน้ำหนักในตะกร้าดัชนี (%) — เริ่มต้นจาก 0.00%</b>',
            'xaxis.range': [0, 7.0]
        },
        [0]
    ],
    'label': '⚖️ Top 10 ตามค่าน้ำหนักทางเศรษฐกิจ (Weight / Size)',
    'method': 'update'
}

fig_drilldown.update_xaxes(
    rangemode='tozero',
    range=[0, 460],
    title='<b>ดัชนีการส่งสินค้าเฉลี่ย (จุด) — เริ่มต้นจาก 0.00 จุด</b>'
)

fig_drilldown.update_layout(
    title='<b>🔍 Drill-down: Top 10 สินค้าที่มีดัชนีส่งมอบสูงสุด (ภายใต้ 5 หมวดหมู่อุตสาหกรรมหลัก)</b><br><sup>สะท้อนสินค้าที่มีการเติบโตและส่งมอบสินค้าก้าวกระโดดสูงสุดในช่วง 66 เดือน (สีแท่งตามหมวดหมู่สังกัด)</sup>',
    template=PLOTLY_TEMPLATE,
    height=680,
    margin=dict(t=110, l=10, r=40, b=80),
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1.0,
        xanchor="left",
        x=1.02,
        title=dict(text="<b>หมวดอุตสาหกรรมสังกัด (Division)</b>"),
        bgcolor="rgba(255,255,255,0.95)",
        bordercolor="#cccccc",
        borderwidth=1,
        font=dict(size=11)
    ),
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=[btn_performance, btn_weight],
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.0,
            xanchor="left",
            y=1.18,
            yanchor="top",
            bgcolor="#ffffff",
            bordercolor="#1E3D59",
            font=dict(size=12, color="#1E3D59")
        )
    ]
)

fig_drilldown.show()
"""

new_cell_1 = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + '\n' for line in cell_top5_overview_src.strip().split('\n')]
}
# remove trailing newline on last line
new_cell_1["source"][-1] = new_cell_1["source"][-1].rstrip('\n')

new_cell_2 = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + '\n' for line in cell_drilldown_top10_src.strip().split('\n')]
}
new_cell_2["source"][-1] = new_cell_2["source"][-1].rstrip('\n')

# Find insertion point: We want it right after Section 2 Markdown header (Index 9)
# or right before Cell Index 10 (which was Cell 8 calculation).
insert_idx = 10
print(f"Original cell at insert_idx: {''.join(nb['cells'][insert_idx]['source'])[:60]}...")

nb['cells'].insert(insert_idx, new_cell_1)
nb['cells'].insert(insert_idx + 1, new_cell_2)

# Renumber all code cells (# ✅ Cell X:)
code_cell_counter = 1
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        src_lines = cell.get('source', [])
        if src_lines and src_lines[0].startswith('# ✅ Cell'):
            # Replace '# ✅ Cell \d+:' with new number
            src_lines[0] = re.sub(r'^# ✅ Cell \d+:', f'# ✅ Cell {code_cell_counter}:', src_lines[0])
            cell['source'] = src_lines
        code_cell_counter += 1

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"✅ Successfully inserted 2 new cells! Total cells now: {len(nb['cells'])}, total code cells: {code_cell_counter - 1}")
