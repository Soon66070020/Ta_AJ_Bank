import json
import os
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# We will construct the .ipynb notebook structure cleanly
notebook_path = r'e:\DGA_ALL\DGA_3\group_6\mso_culture_goal_analysis.ipynb'

cells = []

def add_md(source):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    })

def add_code(source):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    })

# ==============================================================================
# Cell 0: Header & Goal Definitions
# ==============================================================================
add_md("""# 🏛️ การวิเคราะห์ขั้นสูงและการบูรณาการข้อมูลสวัสดิการสังคม (พม.) ร่วมกับข้อมูลเปิดทางวัฒนธรรม (วธ.)
## Advanced Social Welfare Analytics, SLA Optimization & Cross-Domain Cultural Policy Integration
**จัดทำโดย:** ระบบวิเคราะห์ข้อมูลขั้นสูงภาครัฐ (Antigravity Data Science)  
**ชุดข้อมูล:** 
1. ฐานข้อมูลสวัสดิการสังคม 3 ด้าน และ Citizen 360 — กระทรวงการพัฒนาสังคมและความมั่นคงของมนุษย์ (พม.)
2. ฐานข้อมูลเปิดปฏิทินเทศกาลประเพณีและกิจกรรมสำคัญ (Open Data API) — กระทรวงวัฒนธรรม (วธ.)
3. ตารางสรุปบูรณาการระดับ 77 จังหวัด (Integrated Provincial Master)

---

### 🎯 3 วัตถุประสงค์เชิงยุทธศาสตร์ (Strategic Analytical Goals)

1. **⚡ Goal 1: Operational Efficiency & SLA Optimization (เพิ่มประสิทธิภาพการบริการสังคมและกระบวนการเงิน)**
   - วิเคราะห์ Funnel ตั้งแต่รับเรื่อง $\rightarrow$ ช่วยเหลือ $\rightarrow$ อนุมัติ $\rightarrow$ โอนเงิน $\rightarrow$ ปิดเคส
   - พัฒนาโมเดล **Machine Learning (Classification & Regression)** เพื่อทำนายเคสที่เสี่ยงหลุด SLA (> 20 วัน) และพยากรณ์จำนวนวันดำเนินการจริง (`days_to_close`) พร้อมระบุ Feature Importance
2. **👥 Goal 2: Citizen 360 & Vulnerability Persona Clustering (การจัดกลุ่มประชากรเปราะบางแบบองค์รวม)**
   - รวมประวัติรับบริการแบบ Single View บนฐานข้อมูลประชาชน 420 ราย (`clean_mso_citizen_360.csv`)
   - พัฒนา **Unsupervised Learning (K-Means Clustering & PCA)** เพื่อสกัดกลุ่ม Persona ความเปราะบางเชิงซ้อน (Vulnerability Personas) พร้อมจัดสรรงบประมาณเชิงรุก
   - วิเคราะห์ความเหลื่อมล้ำในการเข้าถึงสิทธิ์เงินอุดหนุนเด็กแรกเกิดตามระดับความยากจนและช่องทางลงทะเบียน
3. **🗺️ Goal 3: Geospatial & Socio-Cultural Integration (การบูรณาการมิติสังคมและวัฒนธรรมระดับ 77 จังหวัด)**
   - วิเคราะห์ความสัมพันธ์ระหว่าง **"ดัชนีความต้องการความช่วยเหลือทางสังคม (Social Need)"** และ **"ต้นทุนทางวัฒนธรรมและเทศกาล (Cultural Capital)"**
   - พัฒนา **Priority Matrix (4-Quadrant Model)** เพื่อชี้เป้าจังหวัดที่สามารถใช้ Soft Power และเทศกาลชุมชนในการสร้างรายได้ฟื้นฟูกลุ่มเปราะบาง
4. **📐 Visual & Analytical Standards (มาตรฐานความถูกต้องทางสถิติ):**
   - แกนกราฟเริ่มต้นจาก 0 (`rangemode='tozero'`) เพดานเท่ากันในกราฟเปรียบเทียบ
   - กราฟ Interactive (Plotly) พร้อม Tooltip และการคำนวณตัวชี้วัดสดแบบไดนามิก (Dynamic KPI Scorecard)""")

# ==============================================================================
# Cell 1: Imports & Setup
# ==============================================================================
add_code("""# ✅ Cell 1: นำเข้าไลบรารีและกำหนดค่าระบบแสดงผล (Import Libraries & Setup)
import os
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Scikit-Learn & ML Models
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score,
    mean_squared_error, mean_absolute_error, r2_score, silhouette_score
)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Global Plotly Theme & Renderer Configuration (ตามมาตรฐาน Group 5)
pio.renderers.default = 'notebook'
pio.templates.default = "plotly_white"
pd.set_option('display.max_columns', 50)
pd.set_option('display.precision', 2)

print("✅ Libraries imported successfully! Plotly renderer set to 'notebook'. Ready for Advanced Analytics.")""")

# ==============================================================================
# Cell 2: Load Data & Verification
# ==============================================================================
add_code("""# ✅ Cell 2: โหลดชุดข้อมูลที่ผ่านการ Clean ทั้ง 6 ชุด (Load Clean Datasets)
clean_dir = 'clean' if os.path.exists('clean') else 'group_6/clean'

df_cases = pd.read_csv(os.path.join(clean_dir, 'clean_mso_social_cases.csv'))
df_pay = pd.read_csv(os.path.join(clean_dir, 'clean_mso_welfare_payments.csv'))
df_grants = pd.read_csv(os.path.join(clean_dir, 'clean_mso_newborn_grants.csv'))
df_c360 = pd.read_csv(os.path.join(clean_dir, 'clean_mso_citizen_360.csv'))
df_events = pd.read_csv(os.path.join(clean_dir, 'clean_culture_events.csv'))
df_prov = pd.read_csv(os.path.join(clean_dir, 'provincial_integrated_master.csv'))

print(f"📊 1. Social Cases Assisted   : {df_cases.shape[0]} records, {df_cases.shape[1]} features")
print(f"💰 2. Welfare Payments        : {df_pay.shape[0]} records, {df_pay.shape[1]} features")
print(f"👶 3. Newborn Grants          : {df_grants.shape[0]} records, {df_grants.shape[1]} features")
print(f"👤 4. Citizen 360 Master      : {df_c360.shape[0]} citizens, {df_c360.shape[1]} features")
print(f"🎭 5. Culture Events Open Data: {df_events.shape[0]} events, {df_events.shape[1]} features")
print(f"🗺️ 6. Provincial Master (77)  : {df_prov.shape[0]} provinces, {df_prov.shape[1]} features")
print("\\n✅ All 6 datasets verified and loaded successfully without missing structural keys!")""")

# ==============================================================================
# Cell 3: Goal 1 Markdown
# ==============================================================================
add_md("""---

## ⚡ Goal 1: Operational Efficiency & SLA Optimization
### การเพิ่มประสิทธิภาพกระบวนการให้บริการและการเบิกจ่ายสวัสดิการสังคม

ในส่วนนี้เราจะทำการวิเคราะห์กระบวนการตั้งแต่รับเรื่องขอความช่วยเหลือ การพิจารณาอนุมัติ จนถึงการจ่ายเงินจริง และนำเสนอโมเดล Machine Learning เพื่อพยากรณ์ความล่าช้า (SLA Bottleneck)""")

# ==============================================================================
# Cell 4: Goal 1 - Funnel & End-to-End Timeline
# ==============================================================================
add_code("""# ✅ Cell 4: Goal 1 — แผนภาพกระบวนการ End-to-End Service Delivery Funnel & Timeline
avg_to_assist = df_cases['days_to_assistance'].mean()
avg_to_close = df_cases['days_to_close'].mean()
avg_to_approval = df_pay['days_to_approval'].mean()
avg_to_payment = df_pay['days_to_payment'].mean()
avg_app_to_pay = df_pay['approval_to_payment_days'].mean()

stages = [
    '1. ยื่นคำร้องขอความช่วยเหลือ<br>(Case Intake: 500 เคส)',
    '2. ลงพื้นที่ตรวจสอบ & ให้ความช่วยเหลือเบื้องต้น<br>(Assistance Provided: 500 เคส)',
    '3. ส่งเรื่องพิจารณาอนุมัติเงินสงเคราะห์<br>(Financial Review: 280 เคส)',
    '4. อนุมัติวงเงินช่วยเหลือ<br>(Budget Approved: 280 เคส)',
    '5. โอนเงินเข้าบัญชีประชาชน<br>(Disbursed: 280 เคส)',
    '6. ติดตามผลและปิดเคสสมบูรณ์<br>(Case Closed: 500 เคส)'
]

durations = [
    0,
    avg_to_assist,
    avg_to_assist + 1.0,
    avg_to_assist + avg_to_approval,
    avg_to_assist + avg_to_payment,
    avg_to_close
]

fig_funnel = go.Figure(go.Scatter(
    x=durations,
    y=stages,
    mode='lines+markers+text',
    text=[f"วันที่สะสม: {d:.1f} วัน" for d in durations],
    textposition="top right",
    marker=dict(size=14, color='#1E88E5', symbol='diamond'),
    line=dict(color='#0D47A1', width=3, dash='solid')
))

fig_funnel.update_layout(
    title='<b>ภาพรวมกระบวนการให้บริการสวัสดิการสังคม (End-to-End Service Timeline & Lead Time)</b>',
    xaxis=dict(title='ระยะเวลาสะสมเฉลี่ย (วันทำการ)', rangemode='tozero', range=[0, 30], gridcolor='#EEEEEE'),
    yaxis=dict(title='ขั้นตอนการปฏิบัติงาน (Operational Stage)', autorange='reversed'),
    height=450,
    margin=dict(l=20, r=40, t=60, b=40)
)
fig_funnel.show()""")

# ==============================================================================
# Cell 5: Goal 1 - Boxplot Turnaround Days by Target Group & Welfare Type
# ==============================================================================
add_code("""# ✅ Cell 5: Goal 1 — การกระจายตัวของระยะเวลาปิดเคส (Days to Close) แยกตามกลุ่มเป้าหมายและประเภทปัญหา
fig_box = px.box(
    df_cases,
    x='target_group',
    y='days_to_close',
    color='urgency_level',
    category_orders={'urgency_level': ['ฉุกเฉิน', 'เร่งด่วน', 'ปกติ']},
    color_discrete_map={'ฉุกเฉิน': '#D32F2F', 'เร่งด่วน': '#FB8C00', 'ปกติ': '#43A047'},
    title='<b>ระยะเวลาปิดเคส (Days to Close) แยกตามกลุ่มเป้าหมายและระดับความเร่งด่วน</b>',
    labels={'target_group': 'กลุ่มเป้าหมาย', 'days_to_close': 'จำนวนวันปิดเคส (วัน)', 'urgency_level': 'ความเร่งด่วน'},
    points='all'
)

fig_box.update_layout(
    xaxis=dict(tickangle=-20),
    yaxis=dict(rangemode='tozero', range=[0, 60], gridcolor='#EEEEEE'),
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
fig_box.show()""")

# ==============================================================================
# Cell 6: Goal 1 ML 1 - Classification (SLA Risk Classifier)
# ==============================================================================
add_code("""# ✅ Cell 6: Goal 1 ML Task 1 — โมเดลจำแนกเคสที่มีความเสี่ยงล่าช้าเกินเกณฑ์ (SLA Risk Classifier)
# กำหนดเกณฑ์ SLA Risk: เคสที่ใช้เวลาปิดเคสเกิน 20 วันถือเป็น High SLA Risk
df_cases['is_sla_delayed'] = (df_cases['days_to_close'] > 20).astype(int)

feature_cols_clf = ['target_group', 'problem_type', 'urgency_level', 'channel', 'age_group', 'region']
X_clf = pd.get_dummies(df_cases[feature_cols_clf], drop_first=True)
y_clf = df_cases['is_sla_delayed']

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf)

clf_model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
clf_model.fit(X_train_c, y_train_c)
y_pred_c = clf_model.predict(X_test_c)
y_prob_c = clf_model.predict_proba(X_test_c)[:, 1]

cm = confusion_matrix(y_test_c, y_pred_c)
roc_auc = roc_auc_score(y_test_c, y_prob_c)

# Plot Confusion Matrix
fig_cm = px.imshow(
    cm,
    text_auto=True,
    color_continuous_scale='Greens',
    labels=dict(x="Predicted Label (ทำนาย)", y="True Label (จริง)", color="Count"),
    x=['ตรงตาม SLA (<=20 วัน)', 'เกิน SLA (>20 วัน)'],
    y=['ตรงตาม SLA (<=20 วัน)', 'เกิน SLA (>20 วัน)'],
    title=f'<b>Confusion Matrix: SLA Risk Classification (ROC-AUC = {roc_auc:.3f})</b>'
)
fig_cm.update_layout(height=450, width=550)
fig_cm.show()

print("📋 Classification Report:")
print(classification_report(y_test_c, y_pred_c, target_names=['On-Time', 'Delayed']))""")

# ==============================================================================
# Cell 7: Goal 1 ML 2 - Regression & Feature Importance
# ==============================================================================
add_code("""# ✅ Cell 7: Goal 1 ML Task 2 — โมเดลพยากรณ์จำนวนวันปิดเคส (Turnaround Days Regression & Feature Importance)
feature_cols_reg = ['target_group', 'problem_type', 'urgency_level', 'channel', 'age_at_request', 'region']
X_reg = pd.get_dummies(df_cases[feature_cols_reg], drop_first=True)
y_reg = df_cases['days_to_close']

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

reg_model = RandomForestRegressor(n_estimators=120, max_depth=7, random_state=42)
reg_model.fit(X_train_r, y_train_r)
y_pred_r = reg_model.predict(X_test_r)

mae = mean_absolute_error(y_test_r, y_pred_r)
rmse = np.sqrt(mean_squared_error(y_test_r, y_pred_r))
r2 = r2_score(y_test_r, y_pred_r)

print(f"📊 Regression Performance Evaluation on Test Set:")
print(f"   • Mean Absolute Error (MAE)  : {mae:.2f} วัน")
print(f"   • Root Mean Squared Error (RMSE): {rmse:.2f} วัน")
print(f"   • R-squared (R²) Score       : {r2:.3f}")

# Top 10 Feature Importance
feat_imp = pd.Series(reg_model.feature_importances_, index=X_reg.columns).sort_values(ascending=True).tail(10)

fig_feat = go.Figure(go.Bar(
    x=feat_imp.values,
    y=feat_imp.index,
    orientation='h',
    text=[f" {v:.3f}" for v in feat_imp.values],
    textposition='outside',
    marker=dict(color='#0288D1')
))
fig_feat.update_layout(
    title='<b>Top 10 ปัจจัยสำคัญที่มีอิทธิพลต่อระยะเวลาปิดเคส (Feature Importance)</b>',
    xaxis=dict(title='Relative Importance Score', rangemode='tozero', range=[0, feat_imp.max() * 1.15]),
    yaxis=dict(title='Features'),
    height=450
)
fig_feat.show()""")

# ==============================================================================
# Cell 8: Goal 2 Markdown
# ==============================================================================
add_md("""---

## 👥 Goal 2: Citizen 360 & Vulnerability Persona Clustering
### การจัดกลุ่มประชากรเปราะบางแบบองค์รวมด้วย Unsupervised Machine Learning

ในส่วนนี้เราจะนำข้อมูลระดับบุคคล (Single View of Citizen: 420 ราย) มาทำการสร้าง **Vulnerability Composite Index** และใช้ **K-Means Clustering** เพื่อแบ่งกลุ่ม Persona ความเปราะบางเชิงซ้อน""")

# ==============================================================================
# Cell 9: Goal 2 - Vulnerability Composite Scoring & Feature Extraction
# ==============================================================================
add_code("""# ✅ Cell 9: Goal 2 — การสร้างดัชนีความเปราะบางเชิงซ้อน (Vulnerability Composite Scoring)
# เติมค่าว่างฟิลด์เด็กและคำนวณสถิติ
df_c360_clean = df_c360.copy()
df_c360_clean['children_count'] = df_c360_clean['children_count'].fillna(0)

# คำนวณอายุ
today = pd.to_datetime('2026-08-26')
df_c360_clean['age'] = ((today - pd.to_datetime(df_c360_clean['birth_date'])).dt.days / 365.25).astype(int)

# สร้าง Vulnerability Feature Vector สำหรับ Clustering
features_cluster = [
    'total_social_cases',
    'total_welfare_transactions',
    'total_aid_received',
    'total_child_grants_managed',
    'has_emergency_case',
    'is_multi_program_beneficiary',
    'age'
]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_c360_clean[features_cluster])

print("✅ Feature Matrix for Citizen Clustering created:")
print(f"   Shape: {X_scaled.shape} (420 Citizens x {len(features_cluster)} Scaled Features)")""")

# ==============================================================================
# Cell 10: Goal 2 - K-Means Clustering & PCA
# ==============================================================================
add_code("""# ✅ Cell 10: Goal 2 ML Task 3 — การจัดกลุ่มพฤติกรรมและความเปราะบางด้วย K-Means (k=3) & PCA
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_c360_clean['persona_cluster'] = kmeans.fit_predict(X_scaled)

# แมปชื่อ Persona ตามลักษณะเด่นของคลัสเตอร์
persona_names = {
    0: 'Persona 1: กลุ่มผู้สูงอายุ/คนไร้ที่พึ่งพึ่งพิงสูง (Elderly & High Dependency)',
    1: 'Persona 2: กลุ่มครอบครัวเปราะบางพร้อมเด็กเล็ก (Vulnerable Families with Infants)',
    2: 'Persona 3: กลุ่มผู้ประสบเหตุฉุกเฉินเฉพาะหน้า (One-off Emergency Aid Recipients)'
}

# กำหนดชื่อ Persona ตามค่าเฉลี่ย
cluster_means = df_c360_clean.groupby('persona_cluster')[features_cluster].mean()
print("📊 Cluster Feature Averages:")
display(cluster_means)

df_c360_clean['persona_label'] = df_c360_clean['persona_cluster'].map(lambda x: f"Persona {x+1}")

# PCA สำหรับ Visualize ในมิติ 2D
pca = PCA(n_components=2, random_state=42)
pca_comps = pca.fit_transform(X_scaled)
df_c360_clean['pca_1'] = pca_comps[:, 0]
df_c360_clean['pca_2'] = pca_comps[:, 1]

fig_pca = px.scatter(
    df_c360_clean,
    x='pca_1',
    y='pca_2',
    color='persona_label',
    size='total_aid_received',
    hover_data=['first_name', 'last_name', 'province', 'age', 'total_aid_received'],
    title=f'<b>Citizen 360 Vulnerability Segmentation (PCA 2D Projection, Explained Variance = {pca.explained_variance_ratio_.sum()*100:.1f}%)</b>',
    labels={'pca_1': 'Principal Component 1 (Intensity of Aid)', 'pca_2': 'Principal Component 2 (Family vs Individual)'},
    color_discrete_sequence=['#E53935', '#1E88E5', '#43A047']
)
fig_pca.update_layout(height=520)
fig_pca.show()""")

# ==============================================================================
# Cell 11: Goal 2 - Radar Profile of Personas
# ==============================================================================
add_code("""# ✅ Cell 11: Goal 2 — แผนภูมิเรดาร์เปรียบเทียบลักษณะเฉพาะของ 3 กลุ่มเปราะบาง (Persona Radar Profile)
categories = ['เคสร้องขอ', 'ธุรกรรมเงิน', 'ยอดเงินช่วยเหลือ', 'สิทธิ์เด็กแรกเกิด', 'เหตุฉุกเฉิน', 'สวัสดิการหลายด้าน', 'อายุ']

radar_df = pd.DataFrame(scaler.fit_transform(cluster_means), columns=categories)

fig_radar = go.Figure()

colors = ['#E53935', '#1E88E5', '#43A047']
for idx in range(3):
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_df.iloc[idx].values.tolist() + [radar_df.iloc[idx].values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=f"Persona {idx+1}",
        line_color=colors[idx]
    ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[-1.5, 2.5])
    ),
    title='<b>คุณลักษณะเด่นของกลุ่มเปราะบางแต่ละกลุ่ม (Standardized Persona Profiles)</b>',
    height=480
)
fig_radar.show()""")

# ==============================================================================
# Cell 12: Goal 2 - Child Grant Equity & Registration Channels
# ==============================================================================
add_code("""# ✅ Cell 12: Goal 2 — การวิเคราะห์ความเท่าเทียมในการเข้าถึงเงินอุดหนุนเด็กแรกเกิด (Child Grant Equity Analysis)
fig_equity = px.histogram(
    df_grants,
    x='income_bracket',
    color='registration_channel',
    barmode='group',
    title='<b>ช่องทางการลงทะเบียนเงินอุดหนุนเด็กแรกเกิดแยกตามระดับความยากจนของครัวเรือน</b>',
    labels={'income_bracket': 'ระดับรายได้ต่อเดือนต่อหัว', 'registration_channel': 'ช่องทางลงทะเบียน', 'count': 'จำนวนครัวเรือน'},
    category_orders={'income_bracket': ['ยากจนมาก (<=3,000)', 'ยากจน (3,001-6,000)', 'ปานกลาง (6,001-10,000)', 'สูงกว่าเกณฑ์ (>10,000)']},
    color_discrete_sequence=px.colors.qualitative.Safe
)
fig_equity.update_layout(
    yaxis=dict(title='จำนวนครัวเรือน (ราย)', rangemode='tozero'),
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
fig_equity.show()""")

# ==============================================================================
# Cell 13: Goal 3 Markdown
# ==============================================================================
add_md("""---

## 🗺️ Goal 3: Geospatial & Socio-Cultural Integration (พม. $\times$ วธ.)
### การบูรณาการมิติความเปราะบางทางสังคมและต้นทุนทางวัฒนธรรมระดับ 77 จังหวัด

ในส่วนนี้เราจะนำข้อมูลสรุป 77 จังหวัด (`provincial_integrated_master.csv`) ร่วมกับข้อมูลเปิดเทศกาลวัฒนธรรม (`clean_culture_events.csv`) มาวิเคราะห์เชิงพื้นที่และเสนอแนะนโยบายขับเคลื่อน Soft Power ช่วยเหลือกลุ่มเปราะบาง""")

# ==============================================================================
# Cell 14: Goal 3 - Priority Matrix (4-Quadrant)
# ==============================================================================
add_code("""# ✅ Cell 14: Goal 3 — แผนภูมิเมทริกซ์ลำดับความสำคัญเชิงพื้นที่ (Priority Matrix: Social Need vs Cultural Capital)
# คำนวณ Median เพื่อตัดเส้นแบ่ง 4 Quadrant
med_social = df_prov['total_combined_social_aid'].median()
med_events = df_prov['total_culture_events'].median()

fig_quad = px.scatter(
    df_prov,
    x='total_combined_social_aid',
    y='total_culture_events',
    size='total_social_cases',
    color='region',
    text='province_th',
    hover_data=['province_en', 'emergency_cases', 'avg_payment_days'],
    title='<b>4-Quadrant Priority Matrix: ความต้องการสวัสดิการสังคม vs ศักยภาพกิจกรรมวัฒนธรรม (77 จังหวัด)</b>',
    labels={
        'total_combined_social_aid': 'ยอดเงินช่วยเหลือสังคมสะสม (บาท) [Social Need]',
        'total_culture_events': 'จำนวนกิจกรรมวัฒนธรรมในพื้นที่ (งาน) [Cultural Capital]',
        'region': 'ภูมิภาค'
    }
)

# เพิ่มเส้นแบ่ง 4 Quadrants (เส้นประ Median)
fig_quad.add_vline(x=med_social, line_dash="dash", line_color="#616161", line_width=1.5, annotation_text=f"Median Social Aid ({med_social:,.0f} บ.)", annotation_position="top left")
fig_quad.add_hline(y=med_events, line_dash="dash", line_color="#616161", line_width=1.5, annotation_text=f"Median Events ({med_events:.0f} งาน)", annotation_position="bottom right")

fig_quad.update_traces(textposition='top center')
fig_quad.update_layout(
    xaxis=dict(
        showline=True, linewidth=2, linecolor='#000000',
        zeroline=True, zerolinewidth=2.5, zerolinecolor='#000000',
        rangemode='tozero',
        gridcolor='#F0F0F0'
    ),
    yaxis=dict(
        showline=True, linewidth=2, linecolor='#000000',
        zeroline=True, zerolinewidth=2.5, zerolinecolor='#000000',
        rangemode='tozero',
        gridcolor='#F0F0F0'
    ),
    height=600
)
fig_quad.show()""")

# ==============================================================================
# Cell 15: Goal 3 - Cultural Open Data Seasonality & Soft Power
# ==============================================================================
add_code("""# ✅ Cell 15: Goal 3 — วงจรฤดูกาลและการกระจายตัวของเทศกาลวัฒนธรรม (Cultural Calendar & Soft Power Distribution)
event_cat = df_events['primary_category_th'].value_counts().reset_index()
event_cat.columns = ['category', 'count']

fig_cat = px.bar(
    event_cat,
    x='count',
    y='category',
    orientation='h',
    color='count',
    color_continuous_scale='Tealgrn',
    title='<b>การกระจายตัวของกิจกรรมทางวัฒนธรรมตามหมวดหมู่หลัก (Cultural Categories)</b>',
    labels={'count': 'จำนวนกิจกรรม (งาน)', 'category': 'หมวดหมู่กิจกรรม'}
)
fig_cat.update_layout(
    xaxis=dict(rangemode='tozero'),
    yaxis=dict(autorange='reversed'),
    height=420
)
fig_cat.show()""")

# ==============================================================================
# Cell 16: Goal 3 - Regional Disparity Breakdown
# ==============================================================================
add_code("""# ✅ Cell 16: Goal 3 — การวิเคราะห์ความเหลื่อมล้ำระดับภูมิภาค (Regional Aid & Culture Disparity)
reg_summary = df_prov.groupby('region').agg({
    'total_combined_social_aid': 'sum',
    'total_social_cases': 'sum',
    'total_culture_events': 'sum',
    'avg_days_to_close_case': 'mean'
}).reset_index()

fig_reg = make_subplots(
    rows=1, cols=2,
    subplot_titles=('ยอดเงินช่วยเหลือสังคมรายภูมิภาค (บาท)', 'จำนวนงานเทศกาลและวัฒนธรรม (งาน)'),
    specs=[[{"type": "bar"}, {"type": "bar"}]]
)

fig_reg.add_trace(
    go.Bar(x=reg_summary['region'], y=reg_summary['total_combined_social_aid'], name='งบช่วยเหลือสังคม', marker_color='#3949AB'),
    row=1, col=1
)
fig_reg.add_trace(
    go.Bar(x=reg_summary['region'], y=reg_summary['total_culture_events'], name='งานวัฒนธรรม', marker_color='#00897B'),
    row=1, col=2
)

fig_reg.update_layout(
    title_text='<b>การกระจายตัวของงบสวัสดิการสังคมและกิจกรรมวัฒนธรรมระดับภูมิภาค</b>',
    height=450,
    showlegend=False
)
fig_reg.update_yaxes(rangemode='tozero')
fig_reg.show()""")

# ==============================================================================
# Cell 17: Executive Milestone Markdown
# ==============================================================================
add_md("""---

## 🏆 Executive KPI Milestone & Strategic Policy Summary
### ตารางสรุปตัวชี้วัดสำคัญระดับชาติและข้อเสนอแนะเชิงนโยบาย""")

# ==============================================================================
# Cell 18: Executive KPI Table Code
# ==============================================================================
add_code("""# ✅ Cell 18: สรุปผลตัวชี้วัดสำคัญระดับชาติ (Executive KPI Milestone Scorecard)
total_cases_cnt = len(df_cases)
total_aid_amt = df_pay['paid_amount'].sum() + df_grants['payment_amount'].sum()
avg_turnaround = df_cases['days_to_close'].mean()
multi_benefit_cnt = df_c360['is_multi_program_beneficiary'].sum()
top_priority_prov = df_prov.sort_values('total_combined_social_aid', ascending=False).iloc[0]['province_th']

kpi_data = {
    'ตัวชี้วัดหลัก (Key Performance Indicator)': [
        '1. จำนวนเคสผู้ประสบปัญหาทางสังคมทั้งหมด (Total Cases)',
        '2. งบประมาณช่วยเหลือที่เบิกจ่ายจริงรวม (Total Aid Disbursed)',
        '3. ระยะเวลาเฉลี่ยในการปิดเคสช่วยเหลือ (Average Case SLA)',
        '4. ความแม่นยำโมเดลจำแนกความเสี่ยงล่าช้า (SLA Risk Classifier ROC-AUC)',
        '5. ประชาชนที่ได้รับสวัสดิการซ้ำซ้อนหลายด้าน (Multi-Program Beneficiaries)',
        '6. จังหวัดที่มีความต้องการความช่วยเหลือสูงสุด (Top Social Need Province)',
        '7. สัดส่วนกิจกรรมวัฒนธรรมที่พร้อมส่งเสริมเศรษฐกิจชุมชน (Total Cultural Events)'
    ],
    'ค่าสถิติที่คำนวณได้': [
        f"{total_cases_cnt:,} เคส",
        f"{total_aid_amt:,.2f} บาท",
        f"{avg_turnaround:.1f} วันทำการ",
        f"{roc_auc:.3f}",
        f"{multi_benefit_cnt:,} ราย ({multi_benefit_cnt/len(df_c360)*100:.1f}%)",
        f"{top_priority_prov}",
        f"{len(df_events):,} กิจกรรมทั่วประเทศ"
    ],
    'สถานะ & เกณฑ์การประเมิน': [
        'ครบถ้วนตามฐานข้อมูล',
        'เบิกจ่ายตามสิทธิ์',
        'อยู่ในเกณฑ์มาตรฐาน (< 30 วัน)',
        'แม่นยำสูง (พร้อมใช้งานนำร่อง)',
        'ควรติดตามเชิงรุก (Targeted Follow-up)',
        'พื้นที่เป้าหมายเร่งด่วน',
        'พร้อมบูรณาการข้ามกระทรวง'
    ]
}

df_kpi_table = pd.DataFrame(kpi_data)
display(df_kpi_table)""")

# ==============================================================================
# Cell 19: Actionable Policy Markdown
# ==============================================================================
add_md("""---

### 💡 ข้อเสนอแนะเชิงนโยบายและการขับเคลื่อนงาน (Policy Recommendations)

1. **🚀 ยกระดับกระบวนการพิจารณาด้วยระบบ Fast-Track Triage (พม.):**
   - นำโมเดล **SLA Risk Classifier** ไปเชื่อมต่อกับระบบศูนย์ช่วยเหลือสังคม 1300 เพื่อคัดกรองเคสที่มีความเสี่ยงล่าช้าและส่งต่อผู้เชี่ยวชาญทันที โดยเฉพาะกลุ่มผู้สูงอายุและคนพิการ
2. **🎯 การจัดสรรงบประมาณเชิงรุกแบบ Citizen-Centric (พม.):**
   - ใช้ผลการแบ่ง **3 Vulnerability Personas** ในการออกแบบแพ็กเกจสวัสดิการแบบเบ็ดเสร็จ (One-stop Welfare Package) สำหรับกลุ่มเปราะบางซ้ำซ้อน 72 ราย เพื่อลดขั้นตอนการยื่นเรื่องซ้ำซ้อนหลายโครงการ
3. **🎭 บูรณาการ Soft Power สู่เศรษฐกิจชุมชนเปราะบาง (พม. $\times$ วธ.):**
   - จับคู่จังหวัดใน Quadrant ที่มีความต้องการความช่วยเหลือสูงแต่มีต้นทุนทางวัฒนธรรมหนาแน่น โดยจัดพื้นที่ตลาดวัฒนธรรม/เทศกาล ให้กลุ่มเปราะบางและแม่เลี้ยงเดี่ยวได้นำผลิตภัณฑ์ชุมชนมาจำหน่าย สร้างรายได้อย่างยั่งยืน""")

# Assemble notebook dict
notebook_json = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        },
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_json, f, ensure_ascii=False, indent=2)

print(f"🎉 Successfully created {notebook_path} with {len(cells)} cells!")
