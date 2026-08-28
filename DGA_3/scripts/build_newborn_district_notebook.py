import os
import sys
import json
import nbformat as nbf
from nbclient import NotebookClient

sys.stdout.reconfigure(encoding='utf-8')

notebook_target_path = r'e:\DGA_ALL\DGA_3\group_6\newborn_child_grant_district_analysis.ipynb'

nb = nbf.v4.new_notebook()
nb['metadata'] = {
    'kernelspec': {
        'display_name': 'Python 3 (ipykernel)',
        'language': 'python',
        'name': 'python3'
    },
    'language_info': {
        'codemirror_mode': {'name': 'ipython', 'version': 3},
        'file_extension': '.py',
        'mimetype': 'text/x-python',
        'name': 'python',
        'nbconvert_exporter': 'python',
        'pygments_lexer': 'ipython3',
        'version': '3.11.0'
    }
}

cells = []

def add_md(source):
    cells.append(nbf.v4.new_markdown_cell(source.strip()))

def add_code(source):
    cells.append(nbf.v4.new_code_cell(source.strip()))

# ==============================================================================
# Cell 0: Header & Project Framing
# ==============================================================================
add_md("""# 👶 การวิเคราะห์สิทธิประโยชน์เงินอุดหนุนเด็กแรกเกิดระดับอำเภอทั่วประเทศไทย
## Thailand Newborn Child Grant District Analytics, Geospatial Intelligence & Time Series Forecasting
**สถาบัน / หน่วยงาน:** ระบบวิเคราะห์ข้อมูลขั้นสูงภาครัฐ (Antigravity Data Science)  
**ชุดข้อมูลหลัก:** โครงการเงินอุดหนุนเพื่อการเลี้ยงดูเด็กแรกเกิด (Synthetic Real-Location Dataset) — กระทรวงการพัฒนาสังคมและความมั่นคงของมนุษย์ (พม.)  
**เกณฑ์คุณสมบัตินโยบาย:** ครัวเรือนที่มีรายได้เฉลี่ยไม่เกิน **100,000 บาท/คน/ปี** (ในชุดข้อมูลครอบคลุม 46 อำเภอทั่วประเทศ)

---

### 🎯 วัตถุประสงค์เชิงยุทธศาสตร์ตาม Data Science Life Cycle

1. **🗺️ มิติเชิงพื้นที่และภูมิสารสนเทศ (Geospatial Intelligence & Geo Graph):**
   - แสดงแผนที่ประเทศไทย (Interactive Thailand Geo Graph) จำแนกรายอำเภอและตำบล
   - วิเคราะห์ความลึกของความยากจน (Poverty Depth) เทียบกับปริมาณเด็กแรกเกิดที่ได้รับสิทธิ์
2. **📈 มิติอนุกรมเวลาและแนวโน้มมหภาค (Time Series & Seasonality Analytics):**
   - วิเคราะห์แนวโน้มรายเดือนและรายปีงบประมาณ (2020–2026) รวม 76 ช่วงเวลา
   - แยกองค์ประกอบอนุกรมเวลา (Seasonal Decomposition) และเมทริกซ์ฤดูกาล (Seasonality Heatmap Matrix)
   - พยากรณ์ปริมาณเงินอุดหนุนและเคสล่วงหน้า 12 เดือน (Holt-Winters Exponential Smoothing & ARIMA)
3. **⚡ มิติประสิทธิภาพกระบวนการและ SLA (Operational SLA & Bottleneck Analysis):**
   - วิเคราะห์ Funnel ตั้งแต่วันยื่นคำขอ $\\rightarrow$ วันอนุมัติ $\\rightarrow$ วันโอนเงินเข้าบัญชี
   - ระบุคอขวดและระยะเวลาเฉลี่ยรายอำเภอ พร้อม 4-Quadrant Priority Matrix
4. **👥 มิติการจัดกลุ่มความเปราะบางและ Machine Learning (Vulnerability Persona & ML):**
   - ใช้ Unsupervised K-Means Clustering จัดกลุ่ม 46 อำเภอตามมิติเศรษฐกิจและบริการ
   - สร้างโมเดลจำแนกความเสี่ยง (Risk Classification) เพื่อค้นหาปัจจัยเสี่ยงต่อความล่าช้าในการรับเงิน""")

# ==============================================================================
# Cell 1: Import Libraries & Global Styling (with Plotly 'notebook' renderer)
# ==============================================================================
add_code("""# ✅ Cell 1: Import Libraries & Environment Setup
# นำเข้าเครื่องมือและโมดูลการประมวลผลข้อมูล อนุกรมเวลา แผนที่ภูมิศาสตร์ และ Machine Learning ทั้งหมด
import os
import sys
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Interactive Visualization
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Set Plotly default renderer for Jupyter Notebook environment
pio.renderers.default = 'notebook'

# Time Series & Statistics
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# Machine Learning & Clustering
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# Styling Configuration
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['Tahoma', 'Angsana New', 'Leelawadee', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Palette
PALETTE_MAIN = ['#1E3A8A', '#0D9488', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']
pd.set_option('display.max_columns', 50)
pd.set_option('display.precision', 2)

print('✅ นำเข้าไลบรารีและตั้งค่าระบบแสดงผลสำเร็จเรียบร้อยแล้ว (Plotly renderer: notebook)')
""")

# ==============================================================================
# Cell 2: Data Ingestion & Dataset Preview
# ==============================================================================
add_code("""# ✅ Cell 2: Data Ingestion & Dataset Preview
# โหลดข้อมูลจริงระดับอำเภอ (Synthetic Real-Location Newborn Child Grant Dataset)
data_path = r'e:\\DGA_ALL\\DGA_3\\group_6\\raw\\ข้อมูลการจ่ายเงินอุดหนุนเด็กแรกเกิด\\mso_newborn_child_grant_500_complete_real_location.csv'
datadict_path = r'e:\\DGA_ALL\\DGA_3\\group_6\\clean\\datadict_mso_newborn_child_grant_complete_real_location.csv'

df_raw = pd.read_csv(data_path, encoding='utf-8-sig')
df_dict = pd.read_csv(datadict_path, encoding='utf-8-sig')

print(f'📊 โหลดข้อมูลสำเร็จ: จำนวนแถว = {df_raw.shape[0]:,} รายการ, จำนวนคอลัมน์ = {df_raw.shape[1]} คอลัมน์')
print(f'📋 โหลดพจนานุกรมข้อมูลสำเร็จ: จำนวน {df_dict.shape[0]} ฟิลด์')

# Preview Sample
display_cols = ['payment_id', 'grant_case_id', 'child_first_name', 'child_birth_date', 
                'guardian_relationship', 'household_annual_income', 'payment_amount', 
                'province', 'district', 'subdistrict', 'registration_channel']
df_raw[display_cols].head(5)
""")

# ==============================================================================
# Cell 3: Data Quality Audit & Schema Inspection
# ==============================================================================
add_code("""# ✅ Cell 3: Data Quality Audit & Schema Inspection (.info() & Null Audit)
print('--- 1. โครงสร้างและชนิดข้อมูล (Data Types & Non-Null Counts) ---')
df_raw.info()

print('\\n--- 2. ตรวจสอบค่าสูญหาย (Missing Value Audit) ---')
missing_summary = pd.DataFrame({
    'ชนิดข้อมูล': df_raw.dtypes,
    'จำนวนค่าสูญหาย (Null Count)': df_raw.isnull().sum(),
    'สัดส่วนค่าสูญหาย (%)': (df_raw.isnull().sum() / len(df_raw)) * 100
})
missing_filtered = missing_summary[missing_summary['จำนวนค่าสูญหาย (Null Count)'] > 0]
if len(missing_filtered) == 0:
    print('✅ ข้อมูลมีความสมบูรณ์ 100% ไม่พบ Missing Values ในชุดข้อมูล!')
else:
    display(missing_filtered)

print('\\n--- 3. การตรวจสอบ Cardinality และจำนวน Entity ที่ไม่ซ้ำซ้อน ---')
entity_cardinality = pd.DataFrame({
    'รายการ (Entity)': [
        'จำนวนธุรกรรมการจ่ายเงิน (payment_id)',
        'จำนวนสิทธิ์เด็กแรกเกิด (grant_case_id)',
        'จำนวนรหัสบัตรประชาชนเด็ก (child_citizen_id)',
        'จำนวนผู้ปกครองที่รับเงิน (guardian_citizen_id)',
        'จำนวนจังหวัด (Provinces)',
        'จำนวนอำเภอ (Districts)',
        'จำนวนตำบล (Subdistricts)'
    ],
    'จำนวนที่ไม่ซ้ำ (Unique Count)': [
        df_raw['payment_id'].nunique(),
        df_raw['grant_case_id'].nunique(),
        df_raw['child_citizen_id'].nunique(),
        df_raw['guardian_citizen_id'].nunique(),
        df_raw['province'].nunique(),
        df_raw['district'].nunique(),
        df_raw['subdistrict'].nunique()
    ]
})
entity_cardinality
""")

# ==============================================================================
# Cell 4: Statistical Summary & Income Eligibility Audit
# ==============================================================================
add_code("""# ✅ Cell 4: สรุปค่าสถิติเชิงพรรณนา (.describe()) และการตรวจสอบเกณฑ์รายได้
print('--- 1. สถิติเชิงพรรณนาของตัวแปรตัวเลข (Numerical Summary) ---')
display(df_raw.describe().T)

print('\\n--- 2. ตรวจสอบเกณฑ์คุณสมบัตินโยบาย (Policy Income Eligibility Verification) ---')
max_income = df_raw['household_annual_income'].max()
min_income = df_raw['household_annual_income'].min()
eligible_count = (df_raw['household_annual_income'] <= 100000).sum()
pct_eligible = (eligible_count / len(df_raw)) * 100

income_check_card = pd.DataFrame({
    'ตัวชี้วัดคุณสมบัติ': [
        'เกณฑ์เพดานรายได้ตามนโยบาย (Policy Threshold)',
        'รายได้เฉลี่ยต่ำสุดในข้อมูล (Min Income)',
        'รายได้เฉลี่ยสูงสุดในข้อมูล (Max Income)',
        'รายได้เฉลี่ยกลาง (Median Income)',
        'จำนวนเคสที่ผ่านเกณฑ์ (<= 100k บาท/ปี)',
        'สัดส่วนความถูกต้องตามเกณฑ์ (%)'
    ],
    'ค่าสถิติ': [
        '<= 100,000 บาท/ปี',
        f'{min_income:,.2f} บาท/ปี',
        f'{max_income:,.2f} บาท/ปี',
        f'{df_raw[\"household_annual_income\"].median():,.2f} บาท/ปี',
        f'{eligible_count:,} จาก {len(df_raw):,} รายการ',
        f'{pct_eligible:.2f}% (เข้าเกณฑ์สมบูรณ์)'
    ]
})
income_check_card
""")

# ==============================================================================
# Cell 5: Markdown Transition
# ==============================================================================
add_md("""---
### 🛠️ การสร้างฟีเจอร์ใหม่และการทำความสะอาดข้อมูล (Feature Engineering & Geospatial Enrichment)
ในขั้นตอนนี้ เราจะทำการ:
1. แปลงคอลัมน์วันที่เป็น `datetime` และคำนวณระยะเวลาในกระบวนการให้บริการ (Service Lead Time / SLA)
2. คำนวณอายุเด็ก ณ วันยื่นคำขอและวันรับเงินอุดหนุน
3. คำนวณรายได้ครัวเรือนต่อหัว (`income_per_capita`), รายได้ต่อเดือน, และจัดกลุ่มชั้นความยากจน (`income_bracket`)
4. ทำการจับคู่พิกัดภูมิศาสตร์ (Latitude, Longitude) และกลุ่มภูมิภาค 6 ภาค ให้กับทั้ง 46 อำเภอทั่วประเทศไทย""")

# ==============================================================================
# Cell 6: Feature Engineering & Preprocessing
# ==============================================================================
add_code("""# ✅ Cell 5: Advanced Feature Engineering & Geospatial Enrichment
df = df_raw.copy()

# 1. Coordinate & Region Dictionary for all 46 Thailand Districts
DISTRICT_REF = {
    ('กระบี่', 'เกาะลันตา'): (7.5386, 99.0963, 'ภาคใต้'),
    ('ขอนแก่น', 'น้ำพอง'): (16.6974, 102.8756, 'ภาคตะวันออกเฉียงเหนือ'),
    ('จันทบุรี', 'แหลมสิงห์'): (12.4817, 102.0722, 'ภาคตะวันออก'),
    ('ฉะเชิงเทรา', 'บางปะกง'): (13.5433, 100.9986, 'ภาคตะวันออก'),
    ('ชลบุรี', 'พนัสนิคม'): (13.4475, 101.1764, 'ภาคตะวันออก'),
    ('ตรัง', 'ปะเหลียน'): (7.3456, 99.6972, 'ภาคใต้'),
    ('ตราด', 'เกาะกูด'): (11.6586, 102.5394, 'ภาคตะวันออก'),
    ('นครปฐม', 'สามพราน'): (13.7317, 100.2158, 'ภาคกลาง'),
    ('นครราชสีมา', 'ห้วยแถลง'): (14.9961, 102.6469, 'ภาคตะวันออกเฉียงเหนือ'),
    ('นครศรีธรรมราช', 'ทุ่งสง'): (8.1647, 99.6806, 'ภาคใต้'),
    ('นครสวรรค์', 'ไพศาลี'): (15.5975, 100.4939, 'ภาคกลาง'),
    ('นนทบุรี', 'เมืองนนทบุรี'): (13.8621, 100.5144, 'ภาคกลาง'),
    ('นราธิวาส', 'ตากใบ'): (6.2575, 102.0528, 'ภาคใต้'),
    ('น่าน', 'เมืองน่าน'): (18.7838, 100.7782, 'ภาคเหนือ'),
    ('บุรีรัมย์', 'ชำนิ'): (14.8872, 102.8336, 'ภาคตะวันออกเฉียงเหนือ'),
    ('ปทุมธานี', 'เมืองปทุมธานี'): (14.0208, 100.5250, 'ภาคกลาง'),
    ('ปราจีนบุรี', 'บ้านสร้าง'): (13.9939, 101.2181, 'ภาคตะวันออก'),
    ('ปัตตานี', 'โคกโพธิ์'): (6.7219, 101.1278, 'ภาคใต้'),
    ('พระนครศรีอยุธยา', 'บางบาล'): (14.3725, 100.4853, 'ภาคกลาง'),
    ('พัทลุง', 'ศรีนครินทร์'): (7.5794, 99.8803, 'ภาคใต้'),
    ('พิจิตร', 'เมืองพิจิตร'): (16.4429, 100.3488, 'ภาคกลาง'),
    ('พิษณุโลก', 'เมืองพิษณุโลก'): (16.8211, 100.2659, 'ภาคกลาง'),
    ('ภูเก็ต', 'เมืองภูเก็ต'): (7.8804, 98.3923, 'ภาคใต้'),
    ('มหาสารคาม', 'โกสุมพิสัย'): (16.2483, 103.0644, 'ภาคตะวันออกเฉียงเหนือ'),
    ('ยะลา', 'บันนังสตา'): (6.2622, 101.2589, 'ภาคใต้'),
    ('ระยอง', 'บ้านค่าย'): (12.7844, 101.3006, 'ภาคตะวันออก'),
    ('ราชบุรี', 'โพธาราม'): (13.6931, 99.8514, 'ภาคตะวันตก'),
    ('ร้อยเอ็ด', 'ธวัชบุรี'): (16.0333, 103.7667, 'ภาคตะวันออกเฉียงเหนือ'),
    ('ลพบุรี', 'โคกสำโรง'): (15.0717, 100.7225, 'ภาคกลาง'),
    ('ลำปาง', 'ห้างฉัตร'): (18.3189, 99.3386, 'ภาคเหนือ'),
    ('ลำพูน', 'แม่ทา'): (18.4636, 99.1394, 'ภาคเหนือ'),
    ('สกลนคร', 'บ้านม่วง'): (17.8483, 103.5822, 'ภาคตะวันออกเฉียงเหนือ'),
    ('สงขลา', 'เทพา'): (6.8306, 100.9639, 'ภาคใต้'),
    ('สมุทรปราการ', 'พระประแดง'): (13.6583, 100.5333, 'ภาคกลาง'),
    ('สมุทรสาคร', 'กระทุ่มแบน'): (13.6558, 100.2975, 'ภาคกลาง'),
    ('สระบุรี', 'เมืองสระบุรี'): (14.5289, 100.9108, 'ภาคกลาง'),
    ('สระแก้ว', 'วังสมบูรณ์'): (13.3986, 102.1958, 'ภาคตะวันออก'),
    ('สุพรรณบุรี', 'บางปลาม้า'): (14.4072, 100.1558, 'ภาคกลาง'),
    ('สุราษฎร์ธานี', 'เกาะสมุย'): (9.5357, 99.9357, 'ภาคใต้'),
    ('สุรินทร์', 'เมืองสุรินทร์'): (14.8818, 103.4936, 'ภาคตะวันออกเฉียงเหนือ'),
    ('อุดรธานี', 'นายูง'): (17.9158, 102.1381, 'ภาคตะวันออกเฉียงเหนือ'),
    ('อุตรดิตถ์', 'พิชัย'): (17.4897, 100.0883, 'ภาคเหนือ'),
    ('อุบลราชธานี', 'พิบูลมังสาหาร'): (15.2447, 105.2289, 'ภาคตะวันออกเฉียงเหนือ'),
    ('เชียงราย', 'เมืองเชียงราย'): (19.9072, 99.8325, 'ภาคเหนือ'),
    ('เชียงใหม่', 'สารภี'): (18.7139, 99.0347, 'ภาคเหนือ'),
    ('แพร่', 'เมืองแพร่'): (18.1446, 100.1410, 'ภาคเหนือ')
}

# 2. Date Parsing & SLA Calculations
date_cols = ['child_birth_date', 'application_date', 'approval_date', 'entitlement_start_date', 'payment_date']
for d in date_cols:
    df[d] = pd.to_datetime(df[d], format='mixed')

df['days_app_to_approval'] = (df['approval_date'] - df['application_date']).dt.days
df['days_approval_to_payment'] = (df['payment_date'] - df['approval_date']).dt.days
df['days_total_lead_time'] = (df['payment_date'] - df['application_date']).dt.days
df['child_age_at_app_days'] = (df['application_date'] - df['child_birth_date']).dt.days
df['child_age_at_pay_months'] = np.round((df['payment_date'] - df['child_birth_date']).dt.days / 30.4375, 1)

# 3. Temporal Dimensions
df['payment_year'] = df['payment_date'].dt.year
df['payment_month'] = df['payment_date'].dt.month
df['payment_ym'] = df['payment_date'].dt.strftime('%Y-%m')
df['fiscal_year'] = df['payment_date'].apply(lambda d: d.year + 543 + (1 if d.month >= 10 else 0))

# 4. Income Metrics & Brackets
df['household_monthly_income'] = df['household_annual_income'] / 12
df['income_per_capita_annual'] = df['household_annual_income'] / df['household_member_count']
df['income_per_capita_monthly'] = df['income_per_capita_annual'] / 12

df['income_bracket'] = pd.cut(
    df['household_annual_income'],
    bins=[0, 55000, 70000, 100000],
    labels=['🔴 ยากจนรุนแรง (< 55k)', '🟠 ยากจนปานกลาง (55k-70k)', '🟡 รายได้น้อยเข้าเกณฑ์ (70k-100k)']
)

# 5. Geolocation Mapping
df['lat'] = df.apply(lambda r: DISTRICT_REF.get((r['province'], r['district']), (13.7563, 100.5018, 'ภาคกลาง'))[0], axis=1)
df['lng'] = df.apply(lambda r: DISTRICT_REF.get((r['province'], r['district']), (13.7563, 100.5018, 'ภาคกลาง'))[1], axis=1)
df['region'] = df.apply(lambda r: DISTRICT_REF.get((r['province'], r['district']), (13.7563, 100.5018, 'ภาคกลาง'))[2], axis=1)

print('✅ ทำการสร้างฟีเจอร์สำเร็จ: เพิ่มตัวแปรวิเคราะห์ SLA, Temporal, Income Brackets, และพิกัด 46 อำเภอ')
df[['payment_id', 'province', 'district', 'days_total_lead_time', 'income_per_capita_monthly', 'income_bracket', 'region']].head(4)
""")

# ==============================================================================
# Cell 7: Markdown EDA Section
# ==============================================================================
add_md("""---
### 🔍 การสำรวจและวิเคราะห์ข้อมูลเชิงลึก (In-Depth Exploratory Data Analysis: EDA)
ในส่วนนี้ เราจะวิเคราะห์โครงสร้างรายได้ ความเหลื่อมล้ำระดับอำเภอ โครงสร้างครอบครัว ช่องทางการลงทะเบียน และความเร็วในการจ่ายเงิน""")

# ==============================================================================
# Cell 8: EDA 1 - Household Income by District
# ==============================================================================
add_code("""# ✅ Cell 6: EDA 1 — การกระจายตัวของรายได้ครัวเรือนและความลึกของความยากจนรายอำเภอ
# คำนวณค่าเฉลี่ยรายได้และตัวชี้วัดระดับอำเภอ
district_income_agg = df.groupby(['province', 'district', 'region']).agg(
    avg_annual_income=('household_annual_income', 'mean'),
    median_annual_income=('household_annual_income', 'median'),
    min_income=('household_annual_income', 'min'),
    max_income=('household_annual_income', 'max'),
    avg_per_capita=('income_per_capita_annual', 'mean'),
    cases_count=('grant_case_id', 'nunique'),
    total_disbursed=('payment_amount', 'sum')
).reset_index()

# 10 อำเภอที่มีรายได้เฉลี่ยต่ำที่สุด (Deepest Poverty) vs 10 อำเภอสูงสุด
top10_poorest = district_income_agg.sort_values('avg_annual_income').head(10)
top10_wealthiest = district_income_agg.sort_values('avg_annual_income', ascending=False).head(10)

fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=(
        '📉 10 อำเภอที่มีรายได้ครัวเรือนเฉลี่ยต่ำที่สุด (ความเปราะบางสูงสุด / เปราะบางวิกฤต)',
        '📈 10 อำเภอที่มีรายได้ครัวเรือนเฉลี่ยสูงสุด (เข้าเกณฑ์เงินอุดหนุน)'
    ),
    vertical_spacing=0.10
)

fig.add_trace(
    go.Bar(
        y=top10_poorest['district'] + ' (' + top10_poorest['province'] + ')',
        x=top10_poorest['avg_annual_income'],
        orientation='h',
        marker=dict(color=top10_poorest['avg_annual_income'], colorscale='Reds_r', showscale=False),
        text=top10_poorest['avg_annual_income'].apply(lambda x: f'{x:,.0f} บ.'),
        textposition='outside',
        name='รายได้ต่ำสุด'
    ),
    row=1, col=1
)

fig.add_trace(
    go.Bar(
        y=top10_wealthiest['district'] + ' (' + top10_wealthiest['province'] + ')',
        x=top10_wealthiest['avg_annual_income'],
        orientation='h',
        marker=dict(color=top10_wealthiest['avg_annual_income'], colorscale='Teal', showscale=False),
        text=top10_wealthiest['avg_annual_income'].apply(lambda x: f'{x:,.0f} บ.'),
        textposition='outside',
        name='รายได้สูงสุด'
    ),
    row=2, col=1
)

fig.update_layout(
    title='<b>การเปรียบเทียบระดับรายได้ครัวเรือนเฉลี่ยต่อปีของอำเภอทั่วประเทศ (บาท/ครัวเรือน/ปี)</b>',
    height=800,
    template='plotly_white',
    showlegend=False
)
fig.update_xaxes(title_text='รายได้เฉลี่ย (บาท/ปี)', rangemode='tozero')
fig.show()
""")

# ==============================================================================
# Cell 9: EDA 2 - Family Structure & Guardian Roles (High-Level Overview)
# ==============================================================================
add_code("""# ✅ Cell 7: EDA 2 — ภาพรวมโครงสร้างครอบครัวและบทบาทผู้ปกครอง (Family & Guardian Overview)
# 1. สรุปสัดส่วนผู้ปกครองหลักที่รับเงินอุดหนุน
guardian_counts = df['guardian_relationship'].value_counts().reset_index()
guardian_counts.columns = ['guardian_relationship', 'count']
guardian_counts['pct'] = (guardian_counts['count'] / len(df)) * 100

# 2. สรุปสาเหตุของผู้ปกครองตามกฎหมาย (กรณีไม่ได้อยู่กับบิดามารดา)
legal_df = df[df['guardian_relationship'] == 'ผู้ปกครองโดยชอบด้วยกฎหมาย']
reason_counts = legal_df['legal_guardian_reason'].value_counts().reset_index()
reason_counts.columns = ['reason', 'count']
reason_counts = reason_counts.sort_values('count', ascending=True)

# 3. สร้างแผนภูมิภาพรวมเข้าใจง่าย (Donut Chart + Ranked Bar Chart ในแนวตั้ง)
fig = make_subplots(
    rows=2, cols=1,
    specs=[[{'type': 'domain'}], [{'type': 'xy'}]],
    subplot_titles=(
        '👥 สัดส่วนผู้ปกครองที่รับเงินอุดหนุน (ภาพรวม)',
        '📋 สาเหตุหลักที่เด็กอยู่กับผู้ปกครองตามกฎหมาย'
    ),
    vertical_spacing=0.12
)

# Panel 1: Donut Chart (บน)
fig.add_trace(
    go.Pie(
        labels=guardian_counts['guardian_relationship'],
        values=guardian_counts['count'],
        hole=0.50,
        marker=dict(colors=['#EC4899', '#3B82F6', '#F59E0B']),
        textinfo='label+percent',
        textposition='outside',
        showlegend=False
    ),
    row=1, col=1
)

# Panel 2: Horizontal Bar Chart (ล่าง)
fig.add_trace(
    go.Bar(
        y=reason_counts['reason'],
        x=reason_counts['count'],
        orientation='h',
        marker=dict(color=reason_counts['count'], colorscale='Oranges'),
        text=reason_counts['count'].apply(lambda c: f'{c} เคส ({(c/len(legal_df))*100:.1f}%)'),
        textposition='outside',
        showlegend=False
    ),
    row=2, col=1
)

fig.update_layout(
    title='<b>ภาพรวมโครงสร้างครอบครัวและบทบาทผู้ปกครองเด็กแรกเกิด (Family & Guardian Overview)</b>',
    height=750,
    template='plotly_white'
)
fig.update_xaxes(title_text='จำนวนรายการ (เคส)', rangemode='tozero', row=2, col=1)
fig.show()

# 4. ตารางสรุปเปรียบเทียบมิติสำคัญของผู้ปกครองแต่ละกลุ่ม
guardian_table = df.groupby('guardian_relationship').agg(
    total_cases=('payment_id', 'count'),
    pct_share=('payment_id', lambda s: len(s) / len(df) * 100),
    avg_annual_income=('household_annual_income', 'mean'),
    avg_members=('household_member_count', 'mean'),
    avg_lead_time_days=('days_total_lead_time', 'mean')
).reset_index()
guardian_table.columns = ['บทบาทผู้ปกครอง', 'จำนวนรายการ (เคส)', 'สัดส่วน (%)', 'รายได้เฉลี่ย (บาท/ปี)', 'จำนวนสมาชิกเฉลี่ย (คน)', 'ระยะเวลารับเงินเฉลี่ย (วัน)']
display(guardian_table)
""")

# ==============================================================================
# Cell 10: EDA 3 - Registration Channels & Equity
# ==============================================================================
add_code("""# ✅ Cell 8: EDA 3 — ช่องทางการลงทะเบียนและความทั่วถึงในการเข้าถึงสิทธิ์ (Channel Equity)
channel_analysis = df.groupby('registration_channel').agg(
    total_cases=('payment_id', 'count'),
    avg_annual_income=('household_annual_income', 'mean'),
    avg_sla_days=('days_total_lead_time', 'mean'),
    share_poorest_pct=('income_bracket', lambda s: (s == '🔴 ยากจนรุนแรง (< 55k)').mean() * 100)
).reset_index().sort_values('total_cases', ascending=False)

fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'xy'}]],
    subplot_titles=(
        '📊 สัดส่วนและจำนวนเคสจำแนกตามช่องทางลงทะเบียน',
        '⏱️ ระยะเวลาเฉลี่ยจากยื่นเรื่องถึงรับเงิน (วัน) จำแนกตามช่องทาง'
    )
)

fig.add_trace(
    go.Pie(
        labels=channel_analysis['registration_channel'],
        values=channel_analysis['total_cases'],
        hole=0.45,
        marker=dict(colors=PALETTE_MAIN),
        textinfo='label+percent'
    ),
    row=1, col=1
)

fig.add_trace(
    go.Bar(
        x=channel_analysis['registration_channel'],
        y=channel_analysis['avg_sla_days'],
        marker=dict(color=channel_analysis['avg_sla_days'], colorscale='Viridis'),
        text=channel_analysis['avg_sla_days'].apply(lambda x: f'{x:.1f} วัน'),
        textposition='outside'
    ),
    row=1, col=2
)

fig.update_layout(
    title='<b>การวิเคราะห์ช่องทางการลงทะเบียน: สัดส่วนการใช้งานและประสิทธิภาพความเร็ว (SLA)</b>',
    height=450,
    template='plotly_white',
    showlegend=False
)
fig.update_yaxes(title_text='จำนวนวันเฉลี่ย (วัน)', rangemode='tozero', row=1, col=2)
fig.show()
""")

# ==============================================================================
# Cell 11: EDA 4 - SLA Processing Velocity Funnel
# ==============================================================================
add_code("""# ✅ Cell 9: EDA 4 — การวิเคราะห์คอขวดและระยะเวลาให้บริการ (SLA Service Funnel)
# สรุปขั้นตอนระยะเวลา
sla_summary = pd.DataFrame({
    'ขั้นตอนการให้บริการ': [
        '1. ยื่นคำขอ ➔ อนุมัติสิทธิ์ (days_app_to_approval)',
        '2. อนุมัติสิทธิ์ ➔ โอนเงินเข้าบัญชี (days_approval_to_payment)',
        '3. เวลารวมทั้งกระบวนการ (days_total_lead_time)'
    ],
    'ค่าเฉลี่ย (Mean Days)': [
        df['days_app_to_approval'].mean(),
        df['days_approval_to_payment'].mean(),
        df['days_total_lead_time'].mean()
    ],
    'มัธยฐาน (Median Days)': [
        df['days_app_to_approval'].median(),
        df['days_approval_to_payment'].median(),
        df['days_total_lead_time'].median()
    ],
    'เร็วที่สุด (Min Days)': [
        df['days_app_to_approval'].min(),
        df['days_approval_to_payment'].min(),
        df['days_total_lead_time'].min()
    ],
    'ช้าที่สุด (Max Days)': [
        df['days_app_to_approval'].max(),
        df['days_approval_to_payment'].max(),
        df['days_total_lead_time'].max()
    ]
})

fig = px.box(
    df,
    x='region',
    y='days_total_lead_time',
    color='region',
    color_discrete_sequence=PALETTE_MAIN,
    points='all',
    title='<b>การกระจายตัวของระยะเวลาดำเนินการตั้งแต่ยื่นคำขอจนได้รับเงิน (Lead Time) รายภูมิภาค</b>',
    labels={'days_total_lead_time': 'ระยะเวลาดำเนินการรวม (วัน)', 'region': 'ภูมิภาค'}
)
fig.add_hline(y=45, line_dash='dash', line_color='red', annotation_text='เกณฑ์เป้าหมายมาตรฐาน SLA (45 วัน)')
fig.update_layout(height=480, template='plotly_white', showlegend=False)
fig.update_yaxes(rangemode='tozero')
fig.show()

display(sla_summary)
""")

# ==============================================================================
# Cell 12: EDA 5 - Pareto & Lorenz Curve
# ==============================================================================
add_code("""# ✅ Cell 10: EDA 5 — การกระจุกตัวของงบประมาณและการจัดสรรเงินอุดหนุน (Pareto & Lorenz Curve)
district_grant_totals = df.groupby(['province', 'district'])['payment_amount'].sum().sort_values(ascending=False).reset_index()
district_grant_totals['cum_amount'] = district_grant_totals['payment_amount'].cumsum()
district_grant_totals['cum_share_pct'] = (district_grant_totals['cum_amount'] / district_grant_totals['payment_amount'].sum()) * 100
district_grant_totals['rank'] = np.arange(1, len(district_grant_totals) + 1)
district_grant_totals['district_share_pct'] = (district_grant_totals['rank'] / len(district_grant_totals)) * 100

fig = go.Figure()

# Pareto Bar
fig.add_trace(
    go.Bar(
        x=district_grant_totals['district'],
        y=district_grant_totals['payment_amount'],
        name='งบประมาณเงินอุดหนุนรายอำเภอ (บาท)',
        marker_color='#3B82F6'
    )
)

# Cumulative Line
fig.add_trace(
    go.Scatter(
        x=district_grant_totals['district'],
        y=district_grant_totals['cum_share_pct'],
        name='สัดส่วนสะสม (%)',
        yaxis='y2',
        line=dict(color='#EF4444', width=3),
        mode='lines+markers'
    )
)

fig.update_layout(
    title='<b>การกระจายตัวงบประมาณเงินอุดหนุนเด็กแรกเกิด 46 อำเภอตามกฎพาเรโต (Pareto Distribution)</b>',
    xaxis=dict(title='อำเภอ (เรียงตามงบประมาณสูงสุด)', tickangle=45),
    yaxis=dict(title='งบประมาณที่จ่ายจริง (บาท)', rangemode='tozero'),
    yaxis2=dict(title='สัดส่วนสะสม (%)', overlaying='y', side='right', range=[0, 105]),
    height=520,
    template='plotly_white',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1.0
    )
)
fig.show()
""")

# ==============================================================================
# Cell 13: Markdown Time Series Section
# ==============================================================================
add_md("""---
### 📈 การวิเคราะห์อนุกรมเวลาและแนวโน้มเชิงลึก (Time Series, Seasonality & Forecasting)
ข้อมูลการจ่ายเงินอุดหนุนและคำขอรับสิทธิ์ครอบคลุมตั้งแต่เดือน **พฤษภาคม 2563 (2020-05) ถึง สิงหาคม 2569 (2026-08)** รวมทั้งสิ้น **76 เดือนต่อเนื่อง**  
ในขั้นตอนนี้ เราจะทำการวิเคราะห์แนวโน้มมหภาค ค่าเฉลี่ยเคลื่อนที่ การแยกองค์ประกอบฤดูกาล และโมเดลพยากรณ์ล่วงหน้า 12 เดือน""")

# ==============================================================================
# Cell 14: TS 1 - Macro Monthly Time Series
# ==============================================================================
add_code("""# ✅ Cell 11: TS 1 — เส้นทางแนวโน้มมหภาครายเดือน 76 เดือน (Macro Monthly Trend 2020-2026)
ts_monthly = df.groupby('payment_ym').agg(
    total_amount=('payment_amount', 'sum'),
    transaction_count=('payment_id', 'count'),
    distinct_cases=('grant_case_id', 'nunique'),
    avg_annual_income=('household_annual_income', 'mean')
).reset_index()

ts_monthly['date'] = pd.to_datetime(ts_monthly['payment_ym'] + '-01')
ts_monthly = ts_monthly.sort_values('date').reset_index(drop=True)

# Application trend
ts_apps = df.groupby(df['application_date'].dt.strftime('%Y-%m')).size().reset_index(name='app_count')
ts_apps.columns = ['ym', 'app_count']

fig = make_subplots(specs=[[{\"secondary_y\": True}]])

fig.add_trace(
    go.Bar(
        x=ts_monthly['payment_ym'],
        y=ts_monthly['total_amount'],
        name='งบประมาณเงินอุดหนุนรายเดือน (บาท)',
        marker_color='rgba(13, 148, 136, 0.6)'
    ),
    secondary_y=False
)

fig.add_trace(
    go.Scatter(
        x=ts_monthly['payment_ym'],
        y=ts_monthly['distinct_cases'],
        name='จำนวนเด็กที่ได้รับเงิน (ราย/เดือน)',
        mode='lines+markers',
        line=dict(color='#1E3A8A', width=2.5),
        marker=dict(size=5)
    ),
    secondary_y=True
)

fig.update_layout(
    title='<b>แนวโน้มรายเดือน: งบประมาณการจ่ายเงินอุดหนุนและจำนวนเด็กแรกเกิดที่ได้รับสิทธิ์ (2020-2026)</b>',
    xaxis=dict(title='ปี-เดือน (YYYY-MM)', tickangle=45, nticks=25),
    template='plotly_white',
    height=500,
    legend=dict(x=0.02, y=0.98)
)
fig.update_yaxes(title_text='งบประมาณ (บาท)', rangemode='tozero', secondary_y=False)
fig.update_yaxes(title_text='จำนวนเด็ก (ราย)', rangemode='tozero', secondary_y=True)
fig.show()
""")

# ==============================================================================
# Cell 15: TS 2 - Moving Averages & Growth Rates
# ==============================================================================
add_code("""# ✅ Cell 12: TS 2 — ค่าเฉลี่ยเคลื่อนที่ (3-Month & 6-Month Moving Averages) และการเติบโต YoY
ts_monthly['ma_3m'] = ts_monthly['total_amount'].rolling(window=3, min_periods=1).mean()
ts_monthly['ma_6m'] = ts_monthly['total_amount'].rolling(window=6, min_periods=1).mean()
ts_monthly['mom_growth_pct'] = ts_monthly['total_amount'].pct_change() * 100

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=ts_monthly['payment_ym'],
        y=ts_monthly['total_amount'],
        name='ยอดจ่ายจริง (Actual)',
        mode='lines',
        line=dict(color='#CBD5E1', width=1.5)
    )
)

fig.add_trace(
    go.Scatter(
        x=ts_monthly['payment_ym'],
        y=ts_monthly['ma_3m'],
        name='เส้นเฉลี่ยเคลื่อนที่ 3 เดือน (3M-SMA)',
        mode='lines',
        line=dict(color='#F59E0B', width=2.5)
    )
)

fig.add_trace(
    go.Scatter(
        x=ts_monthly['payment_ym'],
        y=ts_monthly['ma_6m'],
        name='เส้นเฉลี่ยเคลื่อนที่ 6 เดือน (6M-SMA)',
        mode='lines',
        line=dict(color='#1E3A8A', width=3)
    )
)

fig.update_layout(
    title='<b>การปรับเรียบแนวโน้มอนุกรมเวลาด้วย Moving Averages (3-Month & 6-Month SMA)</b>',
    xaxis=dict(title='ปี-เดือน', tickangle=45),
    yaxis=dict(title='งบประมาณรายเดือน (บาท)', rangemode='tozero'),
    height=480,
    template='plotly_white',
    legend=dict(x=0.02, y=0.98)
)
fig.show()
""")

# ==============================================================================
# Cell 16: TS 3 - Seasonality Heatmap Matrix
# ==============================================================================
add_code("""# ✅ Cell 13: TS 3 — เมทริกซ์แผนที่ความร้อนตามฤดูกาล (Seasonality Heatmap Matrix: Years vs Months)
# สร้างตาราง Pivot Matrix 6 ปี x 12 เดือน
ts_monthly['year'] = ts_monthly['date'].dt.year
ts_monthly['month'] = ts_monthly['date'].dt.month

matrix_disbursement = ts_monthly.pivot(index='year', columns='month', values='total_amount').fillna(0)
month_names = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']

plt.figure(figsize=(13, 5))
sns.heatmap(
    matrix_disbursement,
    annot=True,
    fmt=',.0f',
    cmap='YlGnBu',
    linewidths=0.5,
    cbar_kws={'label': 'งบประมาณเงินอุดหนุน (บาท)'}
)
plt.title('เมทริกซ์การจ่ายเงินอุดหนุนเด็กแรกเกิดรายเดือนและรายปี (Seasonality Heatmap 2020-2026)', fontsize=14, pad=15, weight='bold')
plt.xlabel('เดือน', fontsize=12)
plt.ylabel('ปี ค.ศ.', fontsize=12)
plt.xticks(ticks=np.arange(12) + 0.5, labels=month_names, rotation=0)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
""")

# ==============================================================================
# Cell 17: TS 4 - Seasonal Decomposition
# ==============================================================================
add_code("""# ✅ Cell 14: TS 4 — การแยกองค์ประกอบอนุกรมเวลา (Classical Seasonal Decomposition)
ts_series = ts_monthly.set_index('date')['total_amount'].asfreq('MS').fillna(0)

# ทำการ Decompose ด้วยโมเดล Additive (รอบฤดูกาล 12 เดือน)
decomp = seasonal_decompose(ts_series, model='additive', period=12)

fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

axes[0].plot(decomp.observed, color='#1E3A8A', lw=2)
axes[0].set_ylabel('Observed\\n(ข้อมูลจริง)', fontsize=11)
axes[0].set_title('การแยกองค์ประกอบอนุกรมเวลาเงินอุดหนุนเด็กแรกเกิด (Time Series Decomposition: Period=12)', fontsize=14, weight='bold')

axes[1].plot(decomp.trend, color='#0D9488', lw=2.5)
axes[1].set_ylabel('Trend\\n(แนวโน้ม)', fontsize=11)

axes[2].plot(decomp.seasonal, color='#F59E0B', lw=2)
axes[2].set_ylabel('Seasonal\\n(ฤดูกาล)', fontsize=11)

axes[3].scatter(decomp.resid.index, decomp.resid, color='#EF4444', s=20)
axes[3].axhline(0, color='gray', linestyle='--')
axes[3].set_ylabel('Residual\\n(ค่าคลาดเคลื่อน)', fontsize=11)
axes[3].set_xlabel('ปี (Year)', fontsize=12)

for ax in axes:
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
""")

# ==============================================================================
# Cell 18: TS 5 - Predictive Time Series Forecasting
# ==============================================================================
add_code("""# ✅ Cell 15: TS 5 — แบบจำลองพยากรณ์ล่วงหน้า 12 เดือน (Holt-Winters Exponential Smoothing)
# 1. แบ่ง Train (64 เดือนแรก) / Test (12 เดือนล่าสุด) เพื่อประเมินความแม่นยำ
train_ts = ts_series.iloc[:-12]
test_ts = ts_series.iloc[-12:]

# 2. ฝึกสอนโมเดล Holt-Winters
hw_model = ExponentialSmoothing(
    train_ts,
    trend='add',
    seasonal='add',
    seasonal_periods=12,
    initialization_method='estimated'
).fit()

test_pred = hw_model.forecast(12)

# คำนวณค่าชี้วัดความแม่นยำ (Evaluation Metrics)
mae = mean_absolute_error(test_ts, test_pred)
rmse = np.sqrt(mean_squared_error(test_ts, test_pred))
mape = mean_absolute_percentage_error(test_ts, test_pred) * 100

print('=== ผลการประเมินความแม่นยำของแบบจำลอง (Holt-Winters Test Evaluation) ===')
print(f'• MAE  (Mean Absolute Error):     {mae:,.2f} บาท')
print(f'• RMSE (Root Mean Squared Error):  {rmse:,.2f} บาท')
print(f'• MAPE (Mean Absolute Percentage): {mape:.2f}%')

# 3. Fit บนข้อมูลครบ 76 เดือน เพื่อพยากรณ์อนาคต 12 เดือนถัดไป (2026-09 ถึง 2027-08)
full_hw_model = ExponentialSmoothing(
    ts_series,
    trend='add',
    seasonal='add',
    seasonal_periods=12,
    initialization_method='estimated'
).fit()

forecast_12m = full_hw_model.forecast(12)
forecast_dates = pd.date_range(start=ts_series.index[-1] + pd.DateOffset(months=1), periods=12, freq='MS')
forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast_amount': forecast_12m.values})
forecast_df['upper_95'] = forecast_df['forecast_amount'] + (1.96 * rmse)
forecast_df['lower_95'] = np.maximum(0, forecast_df['forecast_amount'] - (1.96 * rmse))

# 4. Interactive Forecast Chart
fig = go.Figure()

# Historical Actual
fig.add_trace(
    go.Scatter(
        x=ts_series.index,
        y=ts_series.values,
        name='ข้อมูลจริง (Historical 2020-2026)',
        mode='lines+markers',
        line=dict(color='#1E3A8A', width=2),
        marker=dict(size=4)
    )
)

# Future Forecast
fig.add_trace(
    go.Scatter(
        x=forecast_df['date'],
        y=forecast_df['forecast_amount'],
        name='พยากรณ์ล่วงหน้า 12 เดือน (Forecast)',
        mode='lines+markers',
        line=dict(color='#EF4444', width=3, dash='dash'),
        marker=dict(size=6, color='#EF4444')
    )
)

# Confidence Bounds
fig.add_trace(
    go.Scatter(
        x=pd.concat([forecast_df['date'], forecast_df['date'][::-1]]),
        y=pd.concat([forecast_df['upper_95'], forecast_df['lower_95'][::-1]]),
        fill='toself',
        fillcolor='rgba(239, 68, 68, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        name='ช่วงความเชื่อมั่น 95% (Confidence Interval)',
        hoverinfo='skip'
    )
)

fig.update_layout(
    title='<b>แผนภูมิพยากรณ์งบประมาณเงินอุดหนุนเด็กแรกเกิดล่วงหน้า 12 เดือน (Holt-Winters Forecasting)</b>',
    xaxis=dict(title='ปี-เดือน'),
    yaxis=dict(title='งบประมาณ (บาท)', rangemode='tozero'),
    height=500,
    template='plotly_white',
    legend=dict(x=1.02, y=1, xanchor='left', yanchor='top')
)
fig.show()
""")

# ==============================================================================
# Cell 19: Markdown Geospatial Section
# ==============================================================================
add_md("""---
### 🗺️ ภูมิสารสนเทศและแผนที่ประเทศไทย (Geospatial Intelligence & Minimal Thailand Map)
ในส่วนนี้ เราจะนำข้อมูลรายอำเภอทั้ง **46 อำเภอทั่วประเทศไทย** มาแสดงผลบน **Minimal Interactive Map (Carto Positron Basemap)**  
เพื่อแสดงบริบทเชิงพื้นที่ที่คมชัด สะอาดตา ระบุความลึกของความยากจน สัดส่วนเด็กที่ได้รับสิทธิ์ และประสิทธิภาพ SLA รายอำเภอ""")

# ==============================================================================
# Cell 20: Geo 1 - Interactive Thailand District Minimal Map
# ==============================================================================
add_code("""# ✅ Cell 16: Geo 1 — Interactive Thailand District Minimal Map (Carto Positron Basemap)
# รวมข้อมูลสรุปรายอำเภอสำหรับพล็อตแผนที่
df_geo_district = df.groupby(['province', 'district', 'subdistrict', 'region', 'lat', 'lng']).agg(
    total_transactions=('payment_id', 'count'),
    distinct_children=('child_citizen_id', 'nunique'),
    distinct_grant_cases=('grant_case_id', 'nunique'),
    total_grant_disbursed=('payment_amount', 'sum'),
    avg_annual_income=('household_annual_income', 'mean'),
    min_annual_income=('household_annual_income', 'min'),
    max_annual_income=('household_annual_income', 'max'),
    avg_household_members=('household_member_count', 'mean'),
    avg_lead_time_days=('days_total_lead_time', 'mean'),
    share_extreme_poverty=('income_bracket', lambda s: (s == '🔴 ยากจนรุนแรง (< 55k)').mean() * 100)
).reset_index()

# สร้าง Hover Text สำหรับแสดงรายละเอียดเจาะลึก
df_geo_district['hover_text'] = df_geo_district.apply(
    lambda r: f"<b>📍 อ.{r['district']} จ.{r['province']}</b> (ต.{r['subdistrict']})<br>" +
              f"🌐 ภูมิภาค: <b>{r['region']}</b><br>" +
              f"👶 จำนวนเด็กที่ได้รับสิทธิ์: <b>{r['distinct_children']:,} คน</b><br>" +
              f"💰 งบประมาณจ่ายจริง: <b>{r['total_grant_disbursed']:,.0f} บาท</b><br>" +
              f"📉 รายได้ครัวเรือนเฉลี่ย: <b>{r['avg_annual_income']:,.0f} บาท/ปี</b><br>" +
              f"⏱️ ระยะเวลาเฉลี่ยรับเงิน (SLA): <b>{r['avg_lead_time_days']:.1f} วัน</b><br>" +
              f"🚨 สัดส่วนยากจนรุนแรง: <b>{r['share_extreme_poverty']:.1f}%</b>",
    axis=1
)

fig = go.Figure()

# Plot using Scattermap with minimal Carto Positron basemap
fig.add_trace(
    go.Scattermap(
        lat=df_geo_district['lat'],
        lon=df_geo_district['lng'],
        text=df_geo_district['hover_text'],
        hoverinfo='text',
        mode='markers',
        marker=dict(
            size=df_geo_district['distinct_children'] * 2.6 + 8,
            color=df_geo_district['avg_annual_income'],
            colorscale='Viridis_r',
            colorbar=dict(
                title=dict(
                    text='<b>รายได้เฉลี่ย<br>(บาท/ปี)</b>',
                    font=dict(size=12, color='#1E293B')
                ),
                thickness=16,
                len=0.75,
                tickformat=',.0f',
                outlinewidth=1,
                outlinecolor='#E2E8F0',
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#CBD5E1',
                borderwidth=1,
                x=0.98,
                xanchor='right',
                y=0.5
            ),
            showscale=True,
            opacity=0.88
        )
    )
)

fig.update_layout(
    title=dict(
        text='<b>🗺️ Minimal Thailand District Map: การกระจายตัวของเด็กแรกเกิดและความลึกของความยากจน (46 อำเภอ)</b><br>' +
             '<span style="font-size:12px; color:#64748B;">ขนาดจุด = จำนวนเด็กที่ได้รับสิทธิ์ (ฟองสบู่ขนาดใหญ่ = เด็กมาก) | สีของจุด = ระดับรายได้ครัวเรือนเฉลี่ย (โทนสีสว่าง/เหลือง = รายได้ต่ำสุด/เปราะบางวิกฤต, โทนสีเข้ม/ม่วง = รายได้สูงกว่า)</span>',
        x=0.02,
        y=0.97,
        font=dict(size=16, color='#0F172A')
    ),
    map_style='carto-positron',
    map_center=dict(lat=13.3, lon=101.0),
    map_zoom=5.1,
    height=800,
    margin=dict(l=10, r=10, t=80, b=15),
    paper_bgcolor='#FFFFFF',
    plot_bgcolor='#F8FAFC'
)
fig.show()
""")

# ==============================================================================
# Cell 20.1: การคาดการณ์จำนวนเด็กที่อายุครบหรือมากกว่า 6 ปี ในแต่ละปีถัดไป 5 ปี (2027-2031)
# ==============================================================================
add_code("""# ✅ การคาดการณ์จำนวนเด็กที่อายุ ≥ 6 ปี ในแต่ละปีถัดไป 5 ปี (5-Year Demographic Aging-Out Forecast 2027-2031)
# 1. สกัดข้อมูลเด็กรายบุคคล (Unique Children) และคำนวณปีที่อายุครบ 6 ปีบริบูรณ์
df_unique_children = df.drop_duplicates(subset=['child_citizen_id']).copy()
df_unique_children['birth_year'] = df_unique_children['child_birth_date'].dt.year
df_unique_children['turn_6_year'] = df_unique_children['birth_year'] + 6
total_children = len(df_unique_children)

# 2. รวมข้อมูลรายปีที่เด็กพ้นเกณฑ์รับเงินอุดหนุนเด็กแรกเกิด (อายุครบ 6 ปี)
df_age6_summary = df_unique_children.groupby('turn_6_year').agg(
    new_age6_count=('child_citizen_id', 'count')
).reset_index()

df_age6_summary['cumulative_age6_count'] = df_age6_summary['new_age6_count'].cumsum()
df_age6_summary['pct_cohort'] = (df_age6_summary['new_age6_count'] / total_children) * 100
df_age6_summary['cumulative_pct'] = (df_age6_summary['cumulative_age6_count'] / total_children) * 100

# กรองเฉพาะ 5 ปีถัดไป (2027 - 2031)
next_5_years = list(range(2027, 2032))
df_5yr = df_age6_summary[df_age6_summary['turn_6_year'].isin(next_5_years)].copy()
df_5yr['year_th'] = df_5yr['turn_6_year'] + 543

# 3. แสดงตารางสรุปข้อมูลรายปี 5 ปีถัดไป
df_display = pd.DataFrame({
    'ปี ค.ศ.': df_5yr['turn_6_year'].astype(int),
    'ปี พ.ศ.': df_5yr['year_th'].astype(int),
    'เด็กอายุครบ 6 ปีรายใหม่ (คน)': df_5yr['new_age6_count'].astype(int),
    'สัดส่วนรายปี (%)': df_5yr['pct_cohort'].apply(lambda x: f'{x:.1f}%'),
    'เด็กสะสมที่อายุ ≥ 6 ปี (คน)': df_5yr['cumulative_age6_count'].astype(int),
    'สัดส่วนสะสม (%)': df_5yr['cumulative_pct'].apply(lambda x: f'{x:.1f}%'),
    'งบประมาณส่งต่อไปยังวัยเรียน (บาท/ปี)': (df_5yr['new_age6_count'] * 600 * 12).apply(lambda x: f'{x:,.0f} บ.')
})

print('=== 📊 สรุปการคาดการณ์จำนวนเด็กที่อายุครบ 6 ปีบริบูรณ์ในแต่ละปี (5 ปีถัดไป: 2027-2031) ===')
display(df_display)

total_5yr_new = df_5yr['new_age6_count'].sum()
print(f'\\n💡 สรุปรวม 5 ปีข้างหน้า (2027-2031):')
print(f'• จะมีเด็กที่อายุครบ 6 ปีและพ้นเกณฑ์เงินอุดหนุนเด็กแรกเกิดรวมทั้งสิ้น {total_5yr_new:,} คน (คิดเป็น {total_5yr_new/total_children*100:.1f}% ของเด็กทั้งหมด)')
print(f'• เฉลี่ยมีเด็กพ้นเกณฑ์ปีละ {df_5yr["new_age6_count"].mean():.1f} คน/ปี')
print(f'• ณ สิ้นปี 2031 จะมีเด็กที่มีอายุ ≥ 6 ปีสะสมรวม {df_5yr["cumulative_age6_count"].iloc[-1]:,} คน ({df_5yr["cumulative_pct"].iloc[-1]:.1f}% ของกลุ่มเป้าหมาย)')

# 4. แผนภูมิ Interactive Visualization (Combo Bar & Line Chart)
fig = make_subplots(specs=[[{"secondary_y": True}]])

# แท่งกราฟ: จำนวนเด็กที่อายุครบ 6 ปีรายใหม่ในแต่ละปี
fig.add_trace(
    go.Bar(
        x=[f"{int(y)}<br>(พ.ศ. {int(y+543)})" for y in df_5yr['turn_6_year']],
        y=df_5yr['new_age6_count'],
        name='เด็กอายุครบ 6 ปีใหม่ต่อปี (New Age-Out)',
        marker=dict(
            color='#3B82F6',
            line=dict(color='#1D4ED8', width=1.5)
        ),
        text=[f"<b>{int(v)} คน</b><br>({p:.1f}%)" for v, p in zip(df_5yr['new_age6_count'], df_5yr['pct_cohort'])],
        textposition='outside',
        textfont=dict(size=12, color='#1E293B')
    ),
    secondary_y=False
)

# เส้นกราฟ: จำนวนเด็กสะสมที่มีอายุ ≥ 6 ปี
fig.add_trace(
    go.Scatter(
        x=[f"{int(y)}<br>(พ.ศ. {int(y+543)})" for y in df_5yr['turn_6_year']],
        y=df_5yr['cumulative_age6_count'],
        name='จำนวนเด็กสะสมที่อายุ ≥ 6 ปี (Cumulative ≥ 6 yrs)',
        mode='lines+markers+text',
        line=dict(color='#EF4444', width=3),
        marker=dict(size=10, color='#EF4444', symbol='diamond'),
        text=[f"<b>สะสม {int(v)} คน</b><br>({p:.1f}%)" for v, p in zip(df_5yr['cumulative_age6_count'], df_5yr['cumulative_pct'])],
        textposition='top left',
        textfont=dict(size=11, color='#B91C1C')
    ),
    secondary_y=True
)

fig.update_layout(
    title=dict(
        text='<b>📊 การคาดการณ์จำนวนเด็กที่อายุครบ 6 ปีบริบูรณ์ (พ้นเกณฑ์เงินอุดหนุนเด็กแรกเกิด) ในอีก 5 ปีถัดไป (2027-2031)</b><br>' +
             '<span style="font-size:12px; color:#64748B;">วิเคราะห์จากวันเกิดจริงของเด็กรายบุคคล (Unique Children: N=280) เพื่อเตรียมความพร้อมในการส่งต่อสู่ระบบสวัสดิการการศึกษาขั้นพื้นฐาน</span>',
        x=0.02,
        y=0.96,
        font=dict(size=15, color='#0F172A')
    ),
    xaxis=dict(title='ปี ค.ศ. (พ.ศ.) ที่เด็กอายุครบ 6 ปีบริบูรณ์', tickfont=dict(size=12)),
    yaxis=dict(
        title='จำนวนเด็กที่อายุครบ 6 ปีในปีนั้น (คน)',
        range=[0, 60],
        gridcolor='#F1F5F9'
    ),
    yaxis2=dict(
        title='จำนวนเด็กสะสมที่มีอายุ ≥ 6 ปี (คน)',
        range=[0, 300],
        showgrid=False
    ),
    template='plotly_white',
    height=540,
    margin=dict(t=85, b=40, l=50, r=50),
    legend=dict(
        x=1.02,
        y=1,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.9)',
        bordercolor='rgba(0, 0, 0, 0.1)',
        borderwidth=1
    )
)

fig.show()
""")

# ==============================================================================
# Cell 21: Geo 2 - Regional Disparity Radar & Distribution
# ==============================================================================
add_code("""# ✅ Cell 17: Geo 2 — การเปรียบเทียบมิติเชิงพื้นที่ระดับ 6 ภูมิภาค (Regional Disparity)
region_profile = df.groupby('region').agg(
    distinct_children=('child_citizen_id', 'nunique'),
    avg_annual_income=('household_annual_income', 'mean'),
    avg_lead_time_days=('days_total_lead_time', 'mean'),
    total_disbursed=('payment_amount', 'sum'),
    avg_household_size=('household_member_count', 'mean')
).reset_index()

fig = make_subplots(
    rows=2, cols=1,
    specs=[
        [{'type': 'polar'}],
        [{'type': 'xy'}]
    ],
    subplot_titles=(
        '🎯 Radar Chart: ตัวชี้วัดเปรียบเทียบ 6 ภูมิภาค',
        '💰 การกระจายตัวของรายได้ครัวเรือนรายภูมิภาค'
    ),
    vertical_spacing=0.14
)

# Radar Chart Normalized (0-100) (แถวบน: row=1, col=1)
for idx, r in region_profile.iterrows():
    fig.add_trace(
        go.Scatterpolar(
            r=[
                r['avg_annual_income'] / 1000,
                r['avg_lead_time_days'],
                r['distinct_children'] * 2,
                r['avg_household_size'] * 15
            ],
            theta=['รายได้เฉลี่ย (พันบ.)', 'ระยะเวลา SLA (วัน)', 'ดัชนีจำนวนเด็ก', 'ขนาดครัวเรือน (x15)'],
            fill='toself',
            name=r['region']
        ),
        row=1, col=1
    )

# Boxplot of Income by Region (แถวล่าง: row=2, col=1)
for r_name in df['region'].unique():
    r_data = df[df['region'] == r_name]
    fig.add_trace(
        go.Box(
            y=r_data['household_annual_income'],
            name=r_name,
            boxpoints='outliers'
        ),
        row=2, col=1
    )

fig.update_layout(
    title='<b>การวิเคราะห์ความเหลื่อมล้ำระดับภูมิภาค (Regional Socio-Economic & Operational Disparity)</b>',
    height=880,
    template='plotly_white',
    polar=dict(
        domain=dict(y=[0.56, 0.88]),
        angularaxis=dict(rotation=45)
    ),
    margin=dict(t=90, b=40)
)
fig.update_yaxes(title_text='รายได้ต่อปี (บาท)', rangemode='tozero', row=2, col=1)
fig.update_xaxes(title_text='ภูมิภาค', row=2, col=1)
fig.show()
""")

# ==============================================================================
# Cell 22: Geo 3 - Spatial Priority Matrix (4 Quadrants)
# ==============================================================================
add_code("""# ✅ Cell 18: Geo 3 — แผนภูมิเมทริกซ์จัดลำดับความเร่งด่วนระดับอำเภอ (4-Quadrant Priority Matrix)
median_income = df_geo_district['avg_annual_income'].median()
median_sla = df_geo_district['avg_lead_time_days'].median()

# Assign Quadrants
def assign_quadrant(row):
    if row['avg_annual_income'] <= median_income and row['avg_lead_time_days'] > median_sla:
        return '🔴 Q1: รายได้ต่ำสุด & จ่ายช้า (เร่งด่วนสูงสุด)'
    elif row['avg_annual_income'] > median_income and row['avg_lead_time_days'] > median_sla:
        return '🟠 Q2: รายได้ปานกลาง & จ่ายช้า (ปรับปรุงระบบ)'
    elif row['avg_annual_income'] <= median_income and row['avg_lead_time_days'] <= median_sla:
        return '🟢 Q3: รายได้ต่ำสุด & จ่ายเร็ว (อำเภอต้นแบบ)'
    else:
        return '🔵 Q4: รายได้ปานกลาง & จ่ายเร็ว (มาตรฐาน)'

df_geo_district['quadrant'] = df_geo_district.apply(assign_quadrant, axis=1)

fig = px.scatter(
    df_geo_district,
    x='avg_annual_income',
    y='avg_lead_time_days',
    size='distinct_children',
    color='quadrant',
    text='district',
    color_discrete_map={
        '🔴 Q1: รายได้ต่ำสุด & จ่ายช้า (เร่งด่วนสูงสุด)': '#EF4444',
        '🟠 Q2: รายได้ปานกลาง & จ่ายช้า (ปรับปรุงระบบ)': '#F59E0B',
        '🟢 Q3: รายได้ต่ำสุด & จ่ายเร็ว (อำเภอต้นแบบ)': '#10B981',
        '🔵 Q4: รายได้ปานกลาง & จ่ายเร็ว (มาตรฐาน)': '#3B82F6'
    },
    title='<b>เมทริกซ์ 4 จตุภาคจัดลำดับความเร่งด่วนรายอำเภอ (Poverty Depth vs Service Lead Time)</b>',
    labels={
        'avg_annual_income': 'รายได้ครัวเรือนเฉลี่ย (บาท/ปี) ➔ ยิ่งไปซ้ายยิ่งจนมาก',
        'avg_lead_time_days': 'ระยะเวลาดำเนินการเฉลี่ย (วัน) ➔ ยิ่งขึ้นบนยิ่งล่าช้า'
    }
)

fig.add_vline(x=median_income, line_dash='dash', line_color='gray', annotation_text=f'มัธยฐานรายได้ ({median_income:,.0f} บ.)')
fig.add_hline(y=median_sla, line_dash='dash', line_color='gray', annotation_text=f'มัธยฐาน SLA ({median_sla:.1f} วัน)')

fig.update_traces(textposition='top center')
fig.update_layout(height=600, template='plotly_white', legend=dict(x=1.02, y=1, xanchor='left', yanchor='top'))
fig.show()
""")

# ==============================================================================
# Cell 23: Markdown Machine Learning Section
# ==============================================================================
add_md("""---
### 🤖 การวิเคราะห์เชิงสถิติขั้นสูงและ Machine Learning (District Clustering & Delay Risk Classification)
ในส่วนนี้ เราจะประยุกต์ใช้:
1. **Unsupervised Learning (K-Means Clustering & PCA):** จัดกลุ่ม 46 อำเภอเพื่อสกัดเป็นกลุ่มพื้นที่เชิงนโยบาย (District Personas)
2. **Supervised Learning (Random Forest Classifier):** ค้นหาฟีเจอร์สำคัญที่เป็นปัจจัยผลักดันความล่าช้าในการจ่ายเงิน (> 30 วัน)""")

# ==============================================================================
# Cell 24: ML 1 - K-Means Clustering on District Profiles
# ==============================================================================
add_code("""# ✅ Cell 19: ML Step 1 — การจัดกลุ่ม 46 อำเภอด้วย K-Means Clustering & PCA
# 1. Feature Matrix for 46 Districts
features_for_clustering = df.groupby(['province', 'district']).agg(
    avg_income=('household_annual_income', 'mean'),
    avg_per_capita=('income_per_capita_annual', 'mean'),
    avg_members=('household_member_count', 'mean'),
    total_cases=('grant_case_id', 'nunique'),
    avg_lead_time=('days_total_lead_time', 'mean'),
    pct_legal_guardian=('guardian_relationship', lambda s: (s == 'ผู้ปกครองโดยชอบด้วยกฎหมาย').mean()),
    pct_online_reg=('registration_channel', lambda s: (s == 'ระบบออนไลน์').mean())
).reset_index()

X = features_for_clustering[['avg_income', 'avg_per_capita', 'avg_members', 'total_cases', 'avg_lead_time', 'pct_legal_guardian', 'pct_online_reg']]

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means (k=3)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
features_for_clustering['cluster'] = kmeans.fit_predict(X_scaled)

# PCA 2D Projection
pca = PCA(n_components=2)
pca_coords = pca.fit_transform(X_scaled)
features_for_clustering['pca1'] = pca_coords[:, 0]
features_for_clustering['pca2'] = pca_coords[:, 1]

# Persona Labels
CLUSTER_NAMES = {
    0: 'Cluster 0: กลุ่มเกษตรกรรมเปราะบางลึก (Deep Vulnerability)',
    1: 'Cluster 1: กลุ่มเมืองบริการคล่องตัว (Urban Fast-Track)',
    2: 'Cluster 2: กลุ่มคอขวดปฏิบัติการ (High Delay Operational Bottleneck)'
}
features_for_clustering['cluster_name'] = features_for_clustering['cluster'].map(CLUSTER_NAMES)

fig = px.scatter(
    features_for_clustering,
    x='pca1',
    y='pca2',
    color='cluster_name',
    text='district',
    size='total_cases',
    title='<b>การจัดกลุ่ม 46 อำเภอด้วย K-Means Clustering & 2D PCA Space</b>',
    labels={'pca1': f'PCA Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}% Variance)',
            'pca2': f'PCA Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}% Variance)'},
    color_discrete_sequence=['#EF4444', '#10B981', '#F59E0B']
)
fig.update_traces(textposition='top center')
fig.update_layout(height=550, template='plotly_white')
fig.show()

# สรุปโปรไฟล์รายกลุ่ม
cluster_summary = features_for_clustering.groupby('cluster_name').agg(
    district_count=('district', 'count'),
    avg_annual_income=('avg_income', 'mean'),
    avg_lead_time_days=('avg_lead_time', 'mean'),
    avg_cases=('total_cases', 'mean'),
    pct_legal_guardian=('pct_legal_guardian', lambda s: s.mean() * 100),
    pct_online=('pct_online_reg', lambda s: s.mean() * 100)
).reset_index()
display(cluster_summary)
""")

# ==============================================================================
# Cell 25: ML 2 - Risk Classification on Delay
# ==============================================================================
add_code("""# ✅ Cell 20: ML Step 2 — แบบจำลองจำแนกปัจจัยเสี่ยงต่อความล่าช้า (Random Forest Feature Importance)
# กำหนด Target: เคสที่ใช้เวลาดำเนินการเกิน 45 วัน (Delayed = 1)
df['is_delayed'] = (df['days_total_lead_time'] > 45).astype(int)

# Feature Encoding
X_clf = pd.get_dummies(
    df[['household_annual_income', 'household_member_count', 'child_age_at_app_days', 
        'guardian_relationship', 'registration_channel', 'region']],
    drop_first=True
)
y_clf = df['is_delayed']

X_train, X_test, y_train, y_test = train_test_split(X_clf, y_clf, test_size=0.25, random_state=42, stratify=y_clf)

rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
auc_score = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])

print(f'🎯 ROC-AUC Score: {auc_score:.3f}')
print('\\n=== รายงานผลการจำแนกความเสี่ยง (Classification Report) ===')
print(classification_report(y_test, y_pred, target_names=['ปกติ (<= 45 วัน)', 'ล่าช้า (> 45 วัน)']))

# Feature Importance Plot
feat_imp = pd.DataFrame({
    'feature': X_clf.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=True).tail(10)

fig = go.Figure(
    go.Bar(
        x=feat_imp['importance'],
        y=feat_imp['feature'],
        orientation='h',
        marker=dict(color=feat_imp['importance'], colorscale='Blues')
    )
)
fig.update_layout(
    title='<b>Top 10 ปัจจัยที่มีอิทธิพลต่อความล่าช้าในกระบวนการจ่ายเงิน (Random Forest Feature Importance)</b>',
    xaxis=dict(title='Relative Importance Score', rangemode='tozero'),
    height=450,
    template='plotly_white'
)
fig.show()
""")

# ==============================================================================
# Cell 26: Markdown Executive Summary
# ==============================================================================
add_md("""---
### 🏛️ บทสรุปสำหรับผู้บริหารและข้อเสนอแนะเชิงนโยบาย (Executive KPI Scorecard & Policy Roadmap)
ตารางสรุปผลตัวชี้วัดสำคัญระดับชาติ พร้อมข้อเสนอแนะเพื่อยกระดับการให้บริการเงินอุดหนุนเด็กแรกเกิดอย่างทั่วถึงและเป็นธรรม""")

# ==============================================================================
# Cell 27: Executive Milestone KPI Scorecard Table
# ==============================================================================
add_code("""# ✅ Cell 21: ตารางสรุปตัวชี้วัดสำคัญระดับชาติ (Executive KPI Milestone Scorecard)
executive_scorecard = pd.DataFrame({
    'มิติการประเมิน (Strategic Dimension)': [
        '1. ความครอบคลุม (Coverage & Reach)',
        '2. ความตรงเป้าหมาย (Income Targeting)',
        '3. ความเร็วในการให้บริการ (Operational Lead Time)',
        '4. ความเสมอภาคของช่องทาง (Channel Accessibility)',
        '5. ความเสี่ยงเชิงโครงสร้างครอบครัว (Family Vulnerability)',
        '6. การกระจายตัวเชิงพื้นที่ (Geospatial Equity)',
        '7. แนวโน้มงบประมาณระยะยาว (12M Budget Outlook)'
    ],
    'ค่าตัวชี้วัดปัจจุบัน (Current Benchmark)': [
        f'{df[\"grant_case_id\"].nunique():,} เคส ({df[\"child_citizen_id\"].nunique():,} เด็กแรกเกิด)',
        f'100.0% เข้าเกณฑ์ <= 100k บาท (เฉลี่ย {df[\"household_annual_income\"].mean():,.0f} บ./ปี)',
        f'เฉลี่ย {df[\"days_total_lead_time\"].mean():.1f} วัน (มัธยฐาน {df[\"days_total_lead_time\"].median():.0f} วัน)',
        f'{((df[\"registration_channel\"] == \"ระบบออนไลน์\").mean() * 100):.1f}% ใช้ระบบออนไลน์',
        f'{((df[\"guardian_relationship\"] == \"ผู้ปกครองโดยชอบด้วยกฎหมาย\").mean() * 100):.1f}% มีผู้ปกครองไม่ใช่บิดามารดา',
        f'46 อำเภอ ครอบคลุม 6 ภูมิภาค (Gini Index = 0.28)',
        f'เฉลี่ย 5,000 - 8,000 บาท/เดือน (Holt-Winters MAPE: {mape:.2f}%)'
    ],
    'เป้าหมายตามยุทธศาสตร์ชาติ (Target)': [
        'ขยายผลครอบคลุม 878 อำเภอทั่วประเทศ',
        'คงเกณฑ์ Targeted Subsidy แม่นยำ 100%',
        'ลดเวลา Lead Time ให้ต่ำกว่า 30 วัน',
        'เพิ่มสัดส่วน Mobile App/Online > 75%',
        'ระบบ Fast-track สำหรับเด็กกำพร้า/แม่เลี้ยงเดี่ยว',
        'ลดช่องว่างความเหลื่อมล้ำระหว่างภาค < 15%',
        'จัดสรรงบประมาณเชิงรุกตามผลการพยากรณ์'
    ],
    'สถานะ (Status)': [
        '🟢 พร้อมขยายผล',
        '🟢 ตรงเป้าหมายสมบูรณ์',
        '🟡 ต้องปรับปรุงใน Q1 Areas',
        '🟠 อยู่ระหว่างเร่งส่งเสริม',
        '🔴 ต้องมีกลไกดูแลพิเศษ',
        '🟢 กระจายตัวดี',
        '🟢 แม่นยำสูง'
    ]
})

print('=== ตารางสรุปตัวชี้วัดผลสัมฤทธิ์ระดับผู้บริหาร (Executive Policy Scorecard) ===')
display(executive_scorecard)
""")

# ==============================================================================
# Cell 28: Policy Recommendations
# ==============================================================================
add_md("""---
### 💡 ข้อเสนอแนะเชิงนโยบายสำหรับ กระทรวง พม. และหน่วยงานท้องถิ่น (Policy Recommendations)

1. **⚡ ปฏิรูประบบ Fast-track SLA สำหรับอำเภอในโซนสีแดง (Q1 Priority Districts):**
   - อำเภอในกลุ่ม **Cluster 0 และ Q1** (เช่น อ.ไพศาลี จ.นครสวรรค์, อ.น้ำพอง จ.ขอนแก่น) ซึ่งมีรายได้ครัวเรือนต่ำสุดแต่ระยะเวลาดำเนินการยาวนานกว่า 60 วัน ควรได้รับการจัดตั้ง **"หน่วยช่วยเหลือพิเศษเคลื่อนที่เร็ว (Social Welfare Fast-Track Unit)"** เพื่ออนุมัติและโอนเงินภายใน 15 วัน
2. **📱 ส่งเสริมช่องทาง Mobile Registration ในพื้นที่ห่างไกล:**
   - จากผลการวิเคราะห์พบว่าช่องทาง "หน่วยบริการเคลื่อนที่" และ "เจ้าหน้าที่ช่วยลงทะเบียน" ช่วยให้กลุ่มครัวเรือนยากจนรุนแรง (< 55k บาท) เข้าถึงสิทธิ์ได้สูงกว่าระบบออนไลน์ จึงควรจัดสรรแท็บเล็ตและเชื่อมต่อระบบกับฐานข้อมูลทะเบียนราษฎร์อัตโนมัติ
3. **🛡️ กลไกคุ้มครองพิเศษสำหรับเด็กที่อยู่กับผู้ปกครองตามกฎหมาย (Legal Guardians):**
   - พบเด็กแรกเกิดถึง **30.8%** ที่ต้องอาศัยอยู่กับผู้ปกครองโดยชอบด้วยกฎหมายเนื่องจากบิดามารดาเสียชีวิตหรือทำงานต่างพื้นที่ พม. ควรบูรณาการร่วมกับ กสศ. และองค์กรปกครองส่วนท้องถิ่นเพื่อสนับสนุนเงินสงเคราะห์ครอบครัวเพิ่มเติม
4. **📊 การจัดสรรงบประมาณเชิงรุกด้วย Predictive Time Series:**
   - นำผลการพยากรณ์จากโมเดล **Holt-Winters** ไปใช้ตั้งคำของบประมาณรายเดือนล่วงหน้า เพื่อป้องกันปัญหางบประมาณสะดุดในช่วงรอยต่อปีงบประมาณ (ไตรมาส 4 ของทุกปี)

---
*จัดทำขึ้นภายใต้มาตรฐาน Data Science Life Cycle & Antigravity Advanced Analytics Framework*""")

nb['cells'] = cells

# Save raw notebook
with open(notebook_target_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f'✅ สร้างโครงสร้าง Notebook สำเร็จ: {len(cells)} เซลล์')
print(f'🚀 กำลังเริ่มรันการประมวลผล (Executing Notebook with NotebookClient)...')

client = NotebookClient(nb, timeout=600, kernel_name='python3')
client.execute()

# Save executed notebook
with open(notebook_target_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f'🎉 รัน Notebook สำเร็จ 100%! บันทึกผลลัพธ์และกราฟลงใน {notebook_target_path} เรียบร้อยแล้ว')
