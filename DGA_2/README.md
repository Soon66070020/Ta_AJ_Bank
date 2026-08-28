# 🇹🇭 DGA_2 — กรมสรรพากร & สถาบันมาตรวิทยาแห่งชาติ (Revenue & Metrology Data Science)

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![ML Library](https://img.shields.io/badge/library-scikit--learn-orange.svg)](https://scikit-learn.org/)
[![Visualization](https://img.shields.io/badge/visualization-plotly-cyan.svg)](https://plotly.com/)
[![Teaching](https://img.shields.io/badge/mode-exercise%20%2B%20solution-green.svg)](#-teaching-notebooks-ชุดสอน)
[![Git LFS](https://img.shields.io/badge/storage-git--lfs-red.svg)](https://git-lfs.com)

คลังข้อมูลชุดนี้รวบรวมตัวอย่างโครงงานวิทยาศาสตร์ข้อมูล (Data Science Showcase) และ **ชุดสอนสำหรับผู้เริ่มต้น (Teaching Notebooks)** ที่ประยุกต์ใช้ในการวิเคราะห์พฤติกรรมและการทำนายสถิติของหน่วยงานรัฐสองแห่ง ได้แก่ **กรมสรรพากร (Revenue Department — RD)** และ **สถาบันมาตรวิทยาแห่งชาติ (National Institute of Metrology — NIMT)**

> 📍 **ตำแหน่ง:** โฟลเดอร์นี้เป็นส่วนหนึ่งของ repo [`ZouWhatqq/Ta_AJ_Bank`](https://github.com/ZouWhatqq/Ta_AJ_Bank)
> working copy ต้นทางอยู่ที่ `E:\DGA_ALL\DGA_2` (remote แยก: `ZouWhatqq/DGA_2_example`)

---

## ⚡ เริ่มต้นใช้งาน (Quick Start)

```powershell
# 0. ติดตั้ง Git LFS ก่อน clone (จำเป็น — ไฟล์ CSV ทะเบียน VAT อยู่ใน LFS)
git lfs install
git clone https://github.com/ZouWhatqq/Ta_AJ_Bank.git

# 1. สร้าง virtual environment
cd Ta_AJ_Bank
python -m venv venv

# 2. ติดตั้งไลบรารีที่จำเป็นทั้งหมด
.\venv\Scripts\python.exe -m pip install pandas numpy scikit-learn plotly matplotlib seaborn openpyxl

# 3. (optional) XGBoost / LightGBM สำหรับ expert notebooks
.\venv\Scripts\python.exe -m pip install xgboost lightgbm

# 4. ลงทะเบียน kernel เข้า Jupyter
.\venv\Scripts\Activate.ps1
python -m ipykernel install --user --name=venv --display-name "Python 3.11 (venv)"
```

*ใน VS Code กด **Select Kernel** มุมขวาบน → เลือก **Python 3.11 (venv)***

**แก้ปัญหากราฟ Plotly ไม่แสดงผลใน VS Code (BUG-001)** — โค้ดใน notebook ตั้งค่าไว้แล้ว:

```python
import plotly.io as pio
pio.renderers.default = 'notebook'
```

---

## 📚 Teaching Notebooks (ชุดสอน)

ชุดสอนออกแบบตามสไตล์ **K-Means Template** ([`K_means_Clustering.ipynb`](K_means_Clustering.ipynb)) — แต่ละขั้นตอนมี markdown hint cell ด้านบน ตามด้วย blank code cell สำหรับนักเรียนเติม
Teaching notebooks follow the **K-Means Template** style — each step has a bilingual markdown hint above a blank code cell for students to fill in.

### 🔬 Metrology (NIMT) Teaching Notebooks — `Metrology_Department/for_final/`

| ไฟล์ / File | บทบาท / Role | หัวข้อ / Topics |
|---|---|---|
| [`nimt_eda_exercise.ipynb`](Metrology_Department/for_final/nimt_eda_exercise.ipynb) | 🎓 **นักเรียน / Student** | Blank cells to fill in |
| [`nimt_eda_solution.ipynb`](Metrology_Department/for_final/nimt_eda_solution.ipynb) | ✅ **ผู้สอน / Instructor** | Full working code |
| [`eda_data_metro.ipynb`](Metrology_Department/for_final/eda_data_metro.ipynb) | 📄 **ต้นฉบับ / Source** | Complete expert notebook |
| [`air_eda_data_metro.ipynb`](Metrology_Department/for_final/air_eda_data_metro.ipynb) | 🌬️ **เสริม / Extra** | Wind farm dataset variant |
| [`air2_eda_data_metro.ipynb`](Metrology_Department/for_final/air2_eda_data_metro.ipynb) | 🌬️ **เสริม / Extra** | Wind farm dataset variant 2 |

**ครอบคลุม 7 ส่วน / Covers 7 sections:**

| # | หัวข้อ / Topic |
|---|---|
| 0 | Import Libraries |
| 1 | Data Dictionary |
| 2 | Load & Explore (`shape`, `head`, `info`, `isna`, `describe`) |
| 3 | Data Cleaning — BUG-002 double-space fix, `SERVICE` normalization, `DESCRIPTION` standardization, date conversion |
| 4 | EDA — yearly revenue trend, department breakdown, service type distribution |
| 5 | Anomaly Detection — Revenue Leakage (`TOTALFEE=0` & `IN_OUT='OUT'`) + Turnaround Bottleneck (`PERIODDAY` outliers) |
| 6 | **K-Means + PCA** — `StandardScaler` → PCA 2D → Elbow Method → Silhouette Score → cluster labels + visualization |
| 7 | **Forecasting** — monthly revenue aggregation → Linear Regression → Random Forest Regressor → model comparison |

---

### 🏢 Revenue (VAT) Teaching Notebooks — `Revenue_Department/For_final/`

| ไฟล์ / File | บทบาท / Role | หัวข้อ / Topics |
|---|---|---|
| [`vat_teaching_exercise.ipynb`](Revenue_Department/For_final/vat_teaching_exercise.ipynb) | 🎓 **นักเรียน / Student** | Blank cells to fill in |
| [`vat_teaching_solution.ipynb`](Revenue_Department/For_final/vat_teaching_solution.ipynb) | ✅ **ผู้สอน / Instructor** | Full working code |
| [`vat_risk_analysis.ipynb`](Revenue_Department/For_final/vat_risk_analysis.ipynb) | 📄 **ต้นฉบับ / Source** | Complete expert notebook |
| [`eda_data_revenue.ipynb`](Revenue_Department/For_final/eda_data_revenue.ipynb) | 🔍 **เสริม / Extra** | Revenue dataset EDA |

**ครอบคลุม 7 ส่วน / Covers 7 sections:**

| # | หัวข้อ / Topic |
|---|---|
| 0 | Import Libraries |
| 1 | Load Data (multi-encoding: `tis-620` / `utf-8-sig`) |
| 2 | EDA — `head`, `info`, `isna`, `describe` |
| 3 | Data Cleaning — Buddhist Era (พ.ศ.) → CE date conversion, `business_age_years` calculation |
| 4 | Feature Engineering — `postcode_business_density`, 100k-row sampling |
| 5 | **PCA** — `StandardScaler` → `PCA(n_components=2)` → explained variance → 2D scatter |
| 6 | **K-Means Clustering** — Elbow Method + Silhouette Score → labels + PCA visualization + cluster summary |
| 7 | **Random Forest Classifier** — `high_risk` target, train/test split, `classification_report`, feature importance, risk % by cluster |

---

## 📁 1. กรมสรรพากร (Revenue Department) — Expert Analysis

**พยากรณ์ความเสี่ยงและสถานะกิจการในการยกเลิกจดทะเบียนภาษีมูลค่าเพิ่ม (VAT)**

📓 Notebook: [`Revenue_Department/For_final/vat_risk_analysis.ipynb`](Revenue_Department/For_final/vat_risk_analysis.ipynb)

### 🛠️ คุณลักษณะเชิงพื้นที่ (Geospatial Feature Engineering)

* **ความหนาแน่นของผู้เล่นในตลาด (Business Density):**
  * `postcode_business_density` : จำนวนธุรกิจจดทะเบียน VAT ในรหัสไปรษณีย์เดียวกัน
  * `district_business_density` : จำนวนธุรกิจจดทะเบียน VAT ในระดับอำเภอ/เขต
* **ชีพจรเศรษฐกิจในจังหวัด (Local Economic Trend):**
  * `prov_vat_trend_slope` : ความชันการเติบโต/หดตัวของยอดจัดเก็บภาษีมูลค่าเพิ่ม (ภ.พ.30) รายจังหวัดย้อนหลัง 4 ปี (2565–2568)
* **ข้อมูลอายุขัยธุรกิจ (Temporal Age):**
  * `business_age_years` : อายุการดำเนินการจริงของธุรกิจ (แปลงจากปี พ.ศ. เป็น ค.ศ.)

### 📊 โมเดลและการวิเคราะห์ (Modeling & Analysis)

| # | โมเดล | ผลลัพธ์ |
|---|---|---|
| 1 | **Business Longevity Regression** — Random Forest Regressor พยากรณ์อายุเฉลี่ยคงอยู่ของนิติบุคคลเชิงภูมิศาสตร์ | — |
| 2 | **High Risk Classification** — แยกกลุ่มธุรกิจจดใหม่เสี่ยงสูง | **ROC AUC = 0.9615** |
| 3 | **Geographic Risk Clustering** — K-Means แยกคลัสเตอร์ความเสี่ยงระดับอำเภอทั่วประเทศ | 3 กลุ่ม |

---

## 📁 2. สถาบันมาตรวิทยาแห่งชาติ (Metrology Department) — Expert Analysis

**การจำแนกประเภทฝ่ายงานสอบเทียบเครื่องมือวัดและการวิเคราะห์ข้อพิรุธในระบบ**

📓 Notebook: [`Metrology_Department/moc_data/metrology_data_science.ipynb`](Metrology_Department/moc_data/metrology_data_science.ipynb)

### 🛠️ คุณลักษณะข้อมูลเครื่องมือวัด (Metrological Features)

* **ค่าบริการสอบเทียบ (`TOTALFEE`):** วิเคราะห์และทำนายราคาและระยะเวลาดำเนินการ
* **ประเภทเครื่องมือวัด (`DESCRIPTION`):** ยุบรวมชื่อเครื่องมือที่สะกดต่างกันให้เป็นมาตรฐาน
* **ฝ่ายงานจริง (`ฝ่ายงานจริง (Actual Department)`):** ⚠️ มีช่องว่างซ้ำซ้อนฝังอยู่ 3 ชื่อ — ดู BUG-002

### 📊 โมเดลและการวิเคราะห์ (Modeling & Analysis)

| # | หัวข้อ | รายละเอียด |
|---|---|---|
| 1 | **Department Classification** | Random Forest / XGBoost / LightGBM จำแนกเครื่องมือไปยังฝ่ายงานสอบเทียบที่ถูกต้องอัตโนมัติ |
| 2 | **Fee Leakage Detection** | ค้นหางานลูกค้าภายนอก (`IN_OUT='OUT'`) ที่มีค่าธรรมเนียม 0 บาท |
| 3 | **Turnaround Bottleneck** | วิเคราะห์งานที่ใช้เวลาสอบเทียบนานผิดปกติ (สูงสุด **1,614 วัน**) |
| 4 | **Revenue Forecasting** | Linear Regression + Random Forest Regressor พยากรณ์รายได้รายเดือน |

---

## 📂 แผนผังโฟลเดอร์ (Repository Structure)

```text
DGA_2/
│
├── README.md                                   คำอธิบายโครงการนี้
├── CLAUDE.md                                   คู่มือ agent + bug log
├── K_means_Clustering.ipynb                    📐 Template ชุดสอน K-Means
│
├── Revenue_Department/                         🏢 กรมสรรพากร (RD)
│   ├── datasets_metadata.json                  metadata ชุดข้อมูลที่ดาวน์โหลดจาก data.go.th
│   ├── download_manifest.json                  บันทึกการดาวน์โหลด
│   │
│   ├── gdpublish-vat-taxpayeraddress/          ⚠️ Git LFS
│   │   ├── vat_taxpayeraddress_01.csv           60.28 MB — ทะเบียนผู้เสียภาษี กทม.
│   │   └── VAT_TaxpayerAddress_02.csv          243.75 MB — ทะเบียนผู้เสียภาษี ต่างจังหวัด
│   ├── gdpublish-ds-taxsumprov/                ยอดจัดเก็บภาษีรายจังหวัด
│   │   ├── taxsumprov_2565.csv                 ยอดเก็บภาษีปี 65
│   │   ├── taxsumprov_2566.csv                 ยอดเก็บภาษีปี 66
│   │   ├── -2567.csv                           ยอดเก็บภาษีปี 67
│   │   └── data2_2568.csv                      ยอดเก็บภาษีปี 68
│   ├── gdpublish-ds-taxsumyea/                 ยอดจัดเก็บภาษีรายปี 2565–2568
│   ├── gdpublish-tax/                          สถิติภาษีรวม
│   ├── gdpublish-taxchon1-2568/                ภาษีชลบุรี รายเดือน 2567–2569
│   ├── gdpublish-52-01/ · gdpublish-67-61/     ชุดข้อมูลรายได้และ dataset อื่น ๆ
│   ├── gdpublish-kpi_and_goals_12_02/          KPI และเป้าหมายหน่วยงาน
│   ├── gdpublish-rd-contact/ · rd-taxform/     ข้อมูลติดต่อ + แบบฟอร์มภาษี
│   ├── gdpublish-complaint*/ · fraud-risk*/    ข้อมูลร้องเรียนและความเสี่ยงทุจริต
│   ├── gdpublish-*/                            ชุดข้อมูลเปิด RD อื่น ๆ (รวม 21 โฟลเดอร์)
│   │
│   └── For_final/                           🎓 Teaching notebooks
│       ├── vat_teaching_exercise.ipynb         🎓 Student exercise (blank cells)
│       ├── vat_teaching_solution.ipynb         ✅ Instructor solution (full code)
│       ├── vat_risk_analysis.ipynb             📄 Source expert notebook
│       ├── eda_data_revenue.ipynb              🔍 Revenue EDA
│       └── data/
│           ├── salmon_head_datadic.csv         Data dictionary
│           └── ⚠️ dga306.csv                    (ไม่อยู่ใน repo — 13.87 MB)
│
└── Metrology_Department/                       🔬 สถาบันมาตรวิทยาแห่งชาติ (NIMT)
    ├── moc_data/                            📄 Expert analysis + ชุดข้อมูลหลัก
    │   ├── metrology_data_science.ipynb        ✅ Expert: NIMT full analysis
    │   ├── real_nimt_machine_learning.csv      ชุดข้อมูลจัดประเภทเครื่องมือ NIMT
    │   ├── real_nimt_machine_learning.xlsx
    │   ├── 1_หลักสูตรอบรมมาตรวิทยา_2569.csv
    │   ├── 2_ค่าธรรมเนียมสอบเทียบ_มาตรวิทยามิติ.csv
    │   ├── 3_ค่าธรรมเนียมสอบเทียบ_มาตรวิทยาไฟฟ้า.csv
    │   ├── 4_ค่าธรรมเนียมสอบเทียบ_มาตรวิทยาเชิงกล.csv
    │   ├── 5_ค่าธรรมเนียมสอบเทียบ_มาตรวิทยาเคมี.csv
    │   └── 6_ค่าธรรมเนียมสอบเทียบ_มาตรวิทยาอุณหภูมิ.csv
    │
    └── for_final/                           🎓 Teaching notebooks
        ├── nimt_eda_exercise.ipynb             🎓 Student exercise (blank cells)
        ├── nimt_eda_solution.ipynb             ✅ Instructor solution (full code)
        ├── eda_data_metro.ipynb                📄 Source expert notebook
        ├── air_eda_data_metro.ipynb
        ├── air2_eda_data_metro.ipynb
        └── data/
            ├── Datadic สถาบันมาตรวิทยาแห่งชาติ.csv   Data dictionary
            ├── wind_farm_data.csv
            ├── Record_Flow.csv
            ├── ขอข้อมูลแต่ละปี.csv
            └── ⚠️ ข้อมูลสถาบันมาตรวิทยาแห่งชาติ2.csv  (ไม่อยู่ใน repo — 8.44 MB)
```

---

## ⚠️ ไฟล์ข้อมูลขนาดใหญ่ (Large Data Files)

### ไฟล์ที่อยู่ใน Git LFS — ต้องติดตั้ง `git lfs` ก่อน clone

| ไฟล์ | ขนาด |
|---|---|
| `Revenue_Department/gdpublish-vat-taxpayeraddress/VAT_TaxpayerAddress_02.csv` | 243.75 MB |
| `Revenue_Department/gdpublish-vat-taxpayeraddress/vat_taxpayeraddress_01.csv` | 60.28 MB |

```powershell
git lfs install
git lfs pull          # ถ้า clone มาแล้วแต่ไฟล์เป็น pointer text
```

### ไฟล์ที่ **ไม่ได้** อยู่ใน repo — ต้องวางเองตาม path ที่ระบุ

| ไฟล์ | ขนาด | ที่ต้องวาง |
|---|---|---|
| `ข้อมูลสถาบันมาตรวิทยาแห่งชาติ2.csv` | 8.44 MB | `Metrology_Department/for_final/data/` |
| `dga306.csv` | 13.87 MB | `Revenue_Department/For_final/data/` |

> Large dataset files are **not included** in this repository due to size limits.
> Place them in the paths specified inside each notebook.

---

## 🐛 Known Issues & Lessons Learned

| Bug ID | อาการ / Symptom | แก้ไข / Fix |
|---|---|---|
| **BUG-001** | Plotly `'iframe'` renderer ไม่แสดงผลใน VS Code | เปลี่ยนเป็น `pio.renderers.default = 'notebook'` |
| **BUG-002** | Plotly Box Plot หายบางกล่องเมื่อชื่อ category มีช่องว่างซ้ำซ้อน | เพิ่ม `.str.replace(r'  +', ' ', regex=True)` หลัง `.str.strip()` |
| **BUG-003** | กราฟ Plotly ไม่แสดงบนหน้า GitHub preview | execute notebook ด้วย renderer `png` เพื่อฝังภาพนิ่งควบคู่ HTML |

รายละเอียดเต็มดูใน [`CLAUDE.md`](CLAUDE.md)

---

## 🌐 แหล่งข้อมูล (Data Sources)

| ชุดข้อมูล | หน่วยงาน | ลิงก์ |
|---|---|---|
| ทะเบียนผู้ประกอบการ VAT, ยอดจัดเก็บภาษีรายจังหวัด/รายปี | **กรมสรรพากร (RD)** กระทรวงการคลัง | [data.go.th](https://data.go.th) |
| สถิติการสอบเทียบเครื่องมือวัด, ค่าธรรมเนียม, หลักสูตรอบรม | **สถาบันมาตรวิทยาแห่งชาติ (NIMT)** กระทรวง อว. | [data.go.th](https://data.go.th) |
