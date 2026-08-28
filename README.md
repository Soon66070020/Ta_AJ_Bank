# 📊 คลังวิเคราะห์ข้อมูลเปิดภาครัฐไทย (Thailand Open Government Data Analytics Portfolio)

คลังข้อมูลเชิงลึก (Data Analytics) และโมเดลทำนายอัจฉริยะ (Machine Learning Models) สำหรับงานสาธารณสุข ควบคุมโรคระบาด การวางแผนงบประมาณเกษตรกรรม การจัดเก็บภาษี มาตรวิทยา ดัชนีเศรษฐกิจอุตสาหกรรม และสวัสดิการสังคมในประเทศไทย โดยใช้ข้อมูลเปิดของภาครัฐ (Open Government Data)

📦 **GitHub Repository**: https://github.com/ZouWhatqq/Ta_AJ_Bank.git

> ⚠️ **ต้องติดตั้ง [Git LFS](https://git-lfs.com) ก่อน clone** — repo นี้เก็บ CSV ทะเบียนผู้เสียภาษี VAT ขนาด 243 MB และ 60 MB ผ่าน Git LFS
> ```powershell
> git lfs install
> git clone https://github.com/ZouWhatqq/Ta_AJ_Bank.git
> ```

---

## 🗺️ ภาพรวม 5 โครงการ (Portfolio at a Glance)

| # | โฟลเดอร์ | หน่วยงาน | โจทย์หลัก |
|---|---|---|---|
| 1 | [`กรมส่งเสริมการเกษตร/`](#1--กรมส่งเสริมการเกษตร-department-of-agricultural-extension---doae) | DOAE | พยากรณ์พื้นที่เกษตรและงบเยียวยาภัยพิบัติ |
| 2 | [`เกษตรกรรม/`](#2--เกษตรกรรม-livestock-development---dld) | DLD | พยากรณ์กำลังการผลิตแปรรูปเนื้อสัตว์รายจังหวัด |
| 3 | [`ควบคุมโรค/`](#3--ควบคุมโรค-disease-control---ddc) | DDC | พยากรณ์ยอดผู้ป่วยโรคติดต่อนำโดยแมลง |
| 4 | [`DGA_2/`](DGA_2/README.md) | RD · NIMT | ความเสี่ยงยกเลิกจดทะเบียน VAT + จำแนกฝ่ายงานสอบเทียบ |
| 5 | [`DGA_3/`](DGA_3/README.md) | สนค. · สศอ. · พม. · วธ. | ดัชนี PPI/Shipment + สวัสดิการสังคมและวัฒนธรรม |

📘 คู่มือระดับ workspace (โครงสร้าง, environment, bug ที่เจอบ่อย): [`../CLAUDE.md`](../CLAUDE.md) · คู่มือระดับ repo: [`CLAUDE.md`](CLAUDE.md)

---

## 📂 โครงสร้างและเนื้อหาโดยละเอียดของแต่ละหมวดหมู่ (Project Details)

3 หมวดหมู่แรกแบ่งตามหน่วยงานภาครัฐผู้รับผิดชอบข้อมูล:

### 1. 🌾 กรมส่งเสริมการเกษตร (Department of Agricultural Extension - DOAE)
โฟลเดอร์นี้เกี่ยวข้องกับการจัดเตรียมข้อมูลเกษตรกรและพื้นที่เกษตรกรรมของจังหวัดเพชรบูรณ์ เพื่อเป็นฐานข้อมูลสำหรับการวางแผนงบประมาณเยียวยาเกษตรกรที่ประสบภัยพิบัติธรรมชาติ (เช่น อุทกภัย ภัยแล้ง) ล่วงหน้า

*   **ข้อมูลนำเข้า (`การขึ้นทะเบียนเกษตรกร.csv`)**:
    *   รวบรวมสถิติรายอำเภอ (11 อำเภอในเพชรบูรณ์) ตั้งแต่ปี 2561 ถึง 2568
    *   ฟิลด์ข้อมูล: `ปี` (ปีงบประมาณ พ.ศ.), `อำเภอ` (พื้นที่ปกครอง), `จำนวนครัวเรือน` (ครัวเรือนเกษตรกรที่ลงทะเบียน), `จำนวนแปลง` (พื้นที่เป็นแปลง), `เนื้อที่(ไร่)` (พื้นที่ทำกินทั้งหมด)
*   **[disaster_risk_map_eda.ipynb](กรมส่งเสริมการเกษตร/disaster_risk_map_eda.ipynb) (การสำรวจข้อมูลแผนที่ปฏิสัมพันธ์)**:
    *   รวบรวมประวัติความเสียหายและเงินช่วยเหลือเกษตรกรรายตำบล
    *   พล็อตแผนที่เชิงพื้นที่ด้วย **Folium** แบบแบ่งระดับสี (Choropleth Map) โดยใช้โครงสร้าง `thailand_tambon.geojson` ในการตรวจสอบความหนาแน่นของผู้ได้รับผลกระทบรายตำบล
    *   แสดงแนวโน้มด้วยกราฟ Plotly แบบอินเตอร์แอคทีฟ
*   **[disaster_forecast.ipynb](กรมส่งเสริมการเกษตร/disaster_forecast.ipynb) (โมเดลพยากรณ์ระดับฐาน - Baseline)**:
    *   โมเดลทำนายพื้นที่เกษตรและเกษตรกรปี 2569 และ 2570
    *   ใช้โมเดล **Linear Regression** และ **Gradient Boosting** ฝึกสอนบนสเกลข้อมูลปกติ
    *   ประเมินผลลัพธ์บนปี 2568: Linear Regression ทำคะแนน $R^2$ สูงสุดที่ **$0.7337$** (MAE: 41,113 ไร่)
*   **[disaster_forecast_imbalance.ipynb](กรมส่งเสริมการเกษตร/disaster_forecast_imbalance.ipynb) (โมเดลรองรับการกระจายข้อมูลที่ไม่สมดุล)**:
    *   *ปัญหาหลัก (The Scale Imbalance Problem)*: แต่ละอำเภอมีขนาดต่างกันมาก (หนองไผ่ ~ 400,000 ไร่ ในขณะที่เขาค้อ ~ 20,000 ไร่) การเทรนด้วยโมเดลปกติจะถูกชี้นำโดยอำเภอขนาดใหญ่
    *   *แนวทางแก้ไข*: ใช้เทคนิค **Target Log-Transformation** แปลงค่าเป้าหมายให้อยู่ในรูป $y' = \log(y + 1)$ ในช่วงการฝึกสอน เพื่อให้น้ำหนักการเรียนรู้ในระดับเปอร์เซ็นต์มีความเท่าเทียมกันทุกขนาดพื้นที่ และแปลงผลลัพธ์กลับด้วย $y = \exp(y') - 1$
    *   *ผลลัพธ์*: **Gradient Boosting (Log)** ทำคะแนน $R^2$ สูงขึ้นเป็น **$0.7633$** และช่วยลดค่าเฉลี่ยความคลาดเคลื่อน (MAE) ลงเหลือ **30,823 ไร่** (ลดลงถึง 23% จากรุ่นเดิม)

---

### 2. 🐃 เกษตรกรรม (Livestock Development - DLD)
โฟลเดอร์นี้เกี่ยวกับการสำรวจการปศุสัตว์ และการพยากรณ์ขีดความสามารถการผลิตเนื้อสัตว์ของแต่ละจังหวัด โดยอ้างอิงจากสถิติการอนุญาตฆ่าสัตว์เพื่อบริโภครายปี

*   **ข้อมูลนำเข้า (`total_*.csv`, `animal_can_kill.csv`)**:
    *   ข้อมูลประชากรสัตว์เลี้ยงและจำนวนเกษตรกร (ปี 2564 - 2568) แยกตามสัตว์ 6 ชนิด (ไก่, เป็ด, สุกร, โคเนื้อ, โคนม, กระบือ)
    *   ข้อมูลสถิติการฆ่าสัตว์เพื่อบริโภครายจังหวัด (`animal_can_kill.csv` ปี 2560 - 2568) ประกอบด้วย โค, กระบือ และสุกร
*   **[animal_eda.ipynb](เกษตรกรรม/animal_eda.ipynb) (การสำรวจการกระจายตัวปศุสัตว์)**:
    *   เปรียบเทียบขนาดประชากรสัตว์เลี้ยงของประเทศ (พบว่าไก่และเป็ดมีจำนวนหลักร้อยล้านตัว จึงปรับปรุงการนำเสนอด้วย Log-Scale)
    *   วิเคราะห์มูลค่าทางเศรษฐกิจรายปีจาก `Profit_Livestock.csv`
    *   สร้างแผนที่ความหนาแน่นของผู้เลี้ยงสัตว์ด้วย Plotly Choropleth Map ร่วมกับข้อมูลพิกัดภูมิศาสตร์
*   **[animal_slaughter_prediction.ipynb](เกษตรกรรม/animal_slaughter_prediction.ipynb) (โมเดลแก้ปัญหาข้อมูลเบ้ - Optimised GBR)**:
    *   พยากรณ์กำลังการผลิตแปรรูปเนื้อสัตว์รายจังหวัด
    *   ประยุกต์ใช้ **Target Log-Transformation** ร่วมกับ **Gradient Boosting Regressor (Huber Loss)** เพื่อลดน้ำหนักของจังหวัดที่มีโรงฆ่าสัตว์ขนาดใหญ่ผิดปกติ (Outliers/Skewness) เช่น ปทุมธานี นครปฐม
    *   *ประสิทธิภาพสุกร*: ได้คะแนน $R^2$ สูงถึง **$0.7067$** บนข้อมูลทดสอบปี 2568 (ในขณะที่ Random Forest รุ่นเดิมทำได้เพียง $0.2183$)
*   **[animal_slaughter_prediction_rf.ipynb](เกษตรกรรม/animal_slaughter_prediction_rf.ipynb) (โมเดลเปรียบเทียบ - Random Forest)**:
    *   ใช้ **Random Forest Regressor** ฝึกสอนบนค่าจริงของสเปกตรัมปกติ เพื่อแสดงประสิทธิภาพและเปรียบเทียบข้อแตกต่างของอัลกอริทึมให้ผู้เรียนเห็นภาพอย่างชัดเจน

---

### 3. 🦟 ควบคุมโรค (Disease Control - DDC)
วิเคราะห์สถิติจำนวนผู้ป่วยโรคระบาดติดต่อนำโดยแมลง เพื่อคาดการณ์ความเสี่ยงในการแพร่ระบาดล่วงหน้า

*   **[Diease_forcast.ipynb](ควบคุมโรค/Diease_forcast.ipynb) (พยากรณ์ยอดผู้ป่วยสะสม)**:
    *   โหลดและเชื่อมโยงชุดข้อมูลประวัติผู้ป่วยโรคระบาดติดต่อนำโดยแมลง (2015 - 2025) เช่น ไข้เลือดออก (Dengue), ไวรัสซิกา (Zika), ไข้ปวดข้อยุงลาย (Chikungunya), และมาลาเรีย (Malaria)
    *   **Feature Engineering**: สร้างฟีเจอร์ย้อนหลัง (Lag Features) ได้แก่ ย้อนหลัง 1 เดือน (`lag_1`), ย้อนหลัง 2 เดือน (`lag_2`) และย้อนหลัง 12 เดือน (`lag_12` เพื่อเป็นตัวแทนความเป็นฤดูกาลรายปี เช่น ยอดฝนระบาดช่วงฤดูฝนเดิม)
    *   **Recursive Time-Series Forecasting**: ใช้โมเดลพยากรณ์ล่วงหน้า 6 เดือนด้วยวิธีการทำนายแบบวนซ้ำ (Recursive)
    *   เปรียบเทียบประสิทธิภาพระหว่าง **Linear Regression** และ **Random Forest** แสดงผลแบบเส้นทำนายสัญจรโดย Plotly

---

### 4. 🏢 DGA_2 — กรมสรรพากร (RD) & สถาบันมาตรวิทยาแห่งชาติ (NIMT)

📄 **รายละเอียดเต็ม: [`DGA_2/README.md`](DGA_2/README.md)**

โครงงาน Data Science Showcase พร้อม **ชุดสอนสำหรับผู้เริ่มต้น (Teaching Notebooks)** แบบ exercise + solution สองภาษา

* **[`DGA_2/Revenue_Department/`](DGA_2/Revenue_Department/) — ความเสี่ยงการยกเลิกจดทะเบียน VAT**
  * Feature Engineering เชิงพื้นที่: `postcode_business_density`, `district_business_density`, `prov_vat_trend_slope` (ความชันยอดจัดเก็บ ภ.พ.30 รายจังหวัด 2565–2568), `business_age_years`
  * **High Risk Classification** แยกกลุ่มธุรกิจจดใหม่เสี่ยงสูง — **ROC AUC = 0.9615**
  * **Geographic Risk Clustering** ด้วย K-Means แยกความเสี่ยงระดับอำเภอทั่วประเทศเป็น 3 กลุ่ม
  * ⚠️ ชุดข้อมูล `VAT_TaxpayerAddress_02.csv` (243.75 MB) และ `vat_taxpayeraddress_01.csv` (60.28 MB) เก็บผ่าน **Git LFS**
* **[`DGA_2/Metrology_Department/`](DGA_2/Metrology_Department/) — จำแนกฝ่ายงานสอบเทียบเครื่องมือวัด**
  * **Department Classification** ด้วย Random Forest / XGBoost / LightGBM
  * **Fee Leakage Detection** ค้นงานลูกค้าภายนอก (`IN_OUT='OUT'`) ที่มีค่าธรรมเนียม 0 บาท
  * **Turnaround Bottleneck** วิเคราะห์งานที่ใช้เวลาสอบเทียบนานผิดปกติ (สูงสุด **1,614 วัน**)
  * **Revenue Forecasting** Linear Regression + Random Forest พยากรณ์รายได้รายเดือน
* **ชุดสอน 7 ส่วน** ทั้งสองหน่วยงาน: Import → Data Dictionary → Load & Explore → Cleaning → EDA → **K-Means + PCA** → Forecasting / Classification

---

### 5. 📈 DGA_3 — ดัชนีเศรษฐกิจอุตสาหกรรม & สวัสดิการสังคม

📄 **รายละเอียดเต็ม: [`DGA_3/README.md`](DGA_3/README.md)**

แปลงรายงาน Excel ที่จัดรูปแบบมาให้คนอ่าน (merged cell, multi-row header, ปี พ.ศ.) เป็น Clean CSV มาตรฐาน `utf-8-sig` แล้วต่อยอดเป็น EDA + ML + ข้อเสนอแนะเชิงนโยบาย

* **`DGA_3/G5_*/` — ดัชนีราคาผู้ผลิต (PPI) + ดัชนีการส่งสินค้า (Shipment Index)**
  * PPI จาก **สนค. กระทรวงพาณิชย์** (มาตรฐาน CPA, ปีฐาน 2564 = 100) · Shipment จาก **สศอ. กระทรวงอุตสาหกรรม** (มาตรฐาน TSIC 2552, ปีฐาน 2559 = 100)
  * ถอดโครงสร้างลำดับชั้น TSIC 5 ระดับ (`TOTAL` → `DIVISION_2DIGIT` → `GROUP_4DIGIT` → `CLASS_5DIGIT` → `PRODUCT_ITEM`) ครอบคลุม **66 เดือน (ม.ค. 2564 – มิ.ย. 2569)**
  * ผลลัพธ์: `shipment_index_tidy_timeseries.csv` **34,518 แถว × 22 คอลัมน์** พร้อมทำ BI / Forecasting
  * Notebooks: PPI Life Cycle + K-Means/PCA · PPI Lag-Feature ML · Shipment + Holt-Winters · เจาะลึกอิเล็กทรอนิกส์ TSIC 26 · PPI ⟷ Shipment 4-Quadrant
  * 📑 สอบทานกับคู่มือ TSIC 2552 ของ สสช. 2 เล่ม (1,007 หน้า) — ยืนยันถูกต้อง **100% ทุกระดับชั้น**
* **`DGA_3/G3_*/` — สวัสดิการสังคม (พม.) + ปฏิทินวัฒนธรรม (วธ.)**
  * 6 ชุดข้อมูล clean: เคสช่วยเหลือ (500×36) · เงินสงเคราะห์ (500×41) · เงินอุดหนุนเด็กแรกเกิด (500×42) · **Citizen 360** (420×23) · ปฏิทินเทศกาล (200 กิจกรรม×37) · **บูรณาการ 77 จังหวัด** (77×21)
  * โจทย์ 3 มิติ: ⚡ SLA Optimization · 👥 Citizen 360 Persona Clustering (K-Means) · 🗺️ Geospatial พม. × วธ.
  * แก้คุณภาพข้อมูลต้นทาง: clean HTML entities, impute พิกัดที่เป็นค่า default กทม. ~58% ด้วย Provincial Centroid
* ⚠️ **ชื่อโฟลเดอร์ `G3_` / `G5_` สลับกับเนื้อหา** — อ่านคำเตือนใน [`DGA_3/README.md`](DGA_3/README.md) ก่อนใช้งาน

---

## 📂 แผนผัง Repository (Repository Structure)

```text
Ta_AJ_Bank/
├── README.md                              ไฟล์นี้
├── CLAUDE.md                              คู่มือ agent ระดับ repo
├── .gitignore                             ควบคุมขอบเขตไฟล์ที่ขึ้น GitHub
├── .gitattributes                         ตั้งค่า Git LFS สำหรับ CSV ขนาดใหญ่
│
├── กรมส่งเสริมการเกษตร/                    🌾 DOAE — พยากรณ์ภัยพิบัติเกษตร
│   ├── data/                                  ข้อมูลเปิด 151 ไฟล์ + thailand_tambon.geojson
│   ├── eda_output/
│   ├── disaster_risk_map_eda.ipynb            แผนที่ Folium Choropleth รายตำบล
│   ├── disaster_forecast.ipynb                Baseline (R² = 0.7337)
│   └── disaster_forecast_imbalance.ipynb      Log-transform GBR (R² = 0.7633)
│
├── เกษตรกรรม/                              🐃 DLD — ปศุสัตว์และการฆ่าสัตว์
│   ├── Animal/
│   ├── animal_eda.ipynb
│   ├── animal_slaughter_prediction.ipynb      GBR + Huber + log-target (สุกร R² = 0.7067)
│   └── animal_slaughter_prediction_rf.ipynb   Random Forest (R² = 0.2183)
│
├── ควบคุมโรค/                              🦟 DDC — พยากรณ์โรคระบาด
│   ├── Diseases/
│   ├── Disease_eda.ipynb
│   ├── Diease_forcast.ipynb                   Lag features + Recursive forecast
│   ├── Diease_forcast_sincos.ipynb            Cyclical encoding (sin/cos)
│   └── Diease_forcast_xgb_lgb.ipynb           XGBoost + LightGBM
│
├── DGA_2/                                  🏢 กรมสรรพากร + สถาบันมาตรวิทยา
│   ├── Revenue_Department/                    VAT risk + ชุดสอน (For_final/)
│   ├── Metrology_Department/                  NIMT classification + ชุดสอน (for_final/)
│   ├── K_means_Clustering.ipynb               Template ชุดสอน
│   ├── README.md · CLAUDE.md
│
└── DGA_3/                                  📈 ดัชนีเศรษฐกิจ + สวัสดิการสังคม
    ├── scripts/                               Data pipeline + validation
    ├── G5_.../                                PPI + Shipment  (เนื้อหาจริง = group_5)
    ├── G3_.../                                พม. + วธ.        (เนื้อหาจริง = group_6)
    ├── DATA_REVIEW_FEEDBACK_CHAT.txt
    └── README.md · CLAUDE.md
```

---

## 🌐 แหล่งข้อมูลอ้างอิงของภาครัฐ (Data Sources & Credits)

ข้อมูลวิเคราะห์และโครงสร้างโมเดลทั้งหมดอ้างอิงจากคลังข้อมูลเปิดของภาครัฐ ประเทศไทย (Open Government Data of Thailand) และหน่วยงานหลักดังนี้:

1.  **สถิติการเกษตรและการขึ้นทะเบียนที่ทำกิน**:
    *   *หน่วยงานรับผิดชอบ*: กรมส่งเสริมการเกษตร (DOAE) กระทรวงเกษตรและสหกรณ์
    *   *ลิงก์คลังข้อมูล*: [data.go.th](https://data.go.th)
2.  **ข้อมูลปศุสัตว์และปริมาณการอนุมัติการฆ่าสัตว์**:
    *   *หน่วยงานรับผิดชอบ*: กรมปศุสัตว์ (DLD) กระทรวงเกษตรและสหกรณ์
    *   *ลิงก์คลังข้อมูล*: [data.go.th](https://data.go.th)
3.  **สถิติโรคระบาดและโรคติดต่อนำโดยแมลง**:
    *   *หน่วยงานรับผิดชอบ*: กรมควบคุมโรค (DDC) กระทรวงสาธารณสุข
    *   *ลิงก์คลังข้อมูล*: [data.go.th](https://data.go.th)
4.  **ขอบเขตข้อมูลแผนที่ประเทศไทย (GeoJSON)**:
    *   *หน่วยงานรับผิดชอบ*: Humanitarian Data Exchange (HDX)
    *   *ลิงก์คลังข้อมูล*: [data.humdata.org](https://data.humdata.org)
5.  **ทะเบียนผู้ประกอบการ VAT และยอดจัดเก็บภาษีรายจังหวัด/รายปี** *(DGA_2)*:
    *   *หน่วยงานรับผิดชอบ*: กรมสรรพากร (RD) กระทรวงการคลัง
    *   *ลิงก์คลังข้อมูล*: [data.go.th](https://data.go.th)
6.  **สถิติการสอบเทียบเครื่องมือวัด ค่าธรรมเนียม และหลักสูตรอบรม** *(DGA_2)*:
    *   *หน่วยงานรับผิดชอบ*: สถาบันมาตรวิทยาแห่งชาติ (NIMT) กระทรวง อว.
    *   *ลิงก์คลังข้อมูล*: [data.go.th](https://data.go.th)
7.  **ดัชนีราคาผู้ผลิต (PPI)** *(DGA_3)*:
    *   *หน่วยงานรับผิดชอบ*: สำนักงานนโยบายและยุทธศาสตร์การค้า (สนค.) กระทรวงพาณิชย์
    *   *ลิงก์คลังข้อมูล*: [tpso.go.th](https://www.tpso.go.th) · [data.go.th](https://data.go.th)
8.  **ดัชนีการส่งสินค้า (Shipment Index)** *(DGA_3)*:
    *   *หน่วยงานรับผิดชอบ*: สำนักงานเศรษฐกิจอุตสาหกรรม (สศอ.) กระทรวงอุตสาหกรรม
    *   *ลิงก์คลังข้อมูล*: [oie.go.th](https://www.oie.go.th) · [data.go.th](https://data.go.th)
9.  **มาตรฐานการจัดประเภทอุตสาหกรรม TSIC 2552** *(DGA_3)*:
    *   *หน่วยงานรับผิดชอบ*: สำนักงานสถิติแห่งชาติ (สสช.)
    *   *ลิงก์คลังข้อมูล*: [nso.go.th](https://www.nso.go.th)
10. **ข้อมูลสวัสดิการสังคม (Synthetic Data) และปฏิทินเทศกาลประเพณี (Real Open Data)** *(DGA_3)*:
    *   *หน่วยงานรับผิดชอบ*: กระทรวงการพัฒนาสังคมและความมั่นคงของมนุษย์ (พม.) และ กระทรวงวัฒนธรรม (วธ.)
    *   *ลิงก์คลังข้อมูล*: [m-society.go.th](https://www.m-society.go.th) · [m-culture.go.th](https://www.m-culture.go.th) · [data.go.th](https://data.go.th)

---

## 🛠️ คู่มือระบบการติดตั้งและการรันโครงงาน (Setup & Execution Guide)

### 1. การเตรียมสภาพแวดล้อมระบบ (System Prerequisites)
*   **Python**: แนะนำเวอร์ชัน 3.11 หรือใหม่กว่า (แนะนำ Python 3.11.9 ตามระบบของโครงงาน)
*   **Virtual Environment**: ติดตั้งไลบรารีทั้งหมดในโฟลเดอร์ `venv` ประจำโปรเจกต์ เพื่อไม่ให้เกิดปัญหารุ่นของแพ็กเกจชนกัน

### 2. การสร้างและเชื่อมโยง Jupyter Kernel
เปิดคอมมานด์ไลน์ (Terminal) ภายในพื้นที่โฟลเดอร์โครงการ จากนั้นรันคำสั่งเหล่านี้เพื่อสร้างและเชื่อมโยง Kernel:
```bash
# 1. เรียกใช้งาน virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 2. ติดตั้งและลงทะเบียน venv เข้าในระบบ Jupyter
python -m ipykernel install --user --name=venv --display-name "Python 3.11 (venv)"
```
*หลังจากทำรายการเสร็จสิ้น เมื่อเปิดหน้าต่างวิเคราะห์โค้ดใน VS Code ให้คลิกปุ่ม **Select Kernel** ที่มุมขวาบนของหน้าจอ แล้วเลือกตัวเลือก **Python 3.11 (venv)** เป็นหลัก*

### 3. วิธีการรันเซลล์ Plotly โดยไม่พบบั๊ก Mimetype บน VS Code
โดยปกติ VS Code จะมีปัญหาแจ้งเตือน `No renderer could be found for mimetype "application/vnd.plotly.v1+json"` ซึ่งทำให้ไม่เห็นกราฟ

**แนวทางแก้ไขที่เราตั้งค่าไว้ในทุกไฟล์**:
เราได้กำหนดตัวแสดงผลเริ่มต้นให้ดึงรหัสประมวลผลผ่านเว็บเบราว์เซอร์ (`notebook_connected`) ไว้ที่ตอนต้นของทุกๆ โค้ดชีท:
```python
import plotly.io as pio
pio.renderers.default = "notebook_connected"
```
*ข้อกำหนดนี้ทำให้การนำเสนอสามารถรันกราฟแบบ 3D, แผนที่ Choropleth หรือแผนภูมิแท่งแบบ Interactive ตอบสนองการทำงานผ่าน VS Code ได้ทันทีอย่างไร้รอยต่อ*
