# CLAUDE.md — Ta_AJ_Bank

> **ขั้นตอนแรกเสมอ:** อ่านไฟล์นี้ก่อนเริ่มงานใน repo นี้ทุกครั้ง
> คู่มือระดับ workspace (ครอบทุก repo): [`../CLAUDE.md`](../CLAUDE.md)

---

## 📌 Repository นี้คืออะไร

**คลังวิเคราะห์ข้อมูลเปิดภาครัฐไทย (Thailand Open Government Data Analytics Portfolio)**
รวม 5 โครงการที่ใช้ข้อมูลจาก [data.go.th](https://data.go.th) และหน่วยงานภาครัฐ แล้วทำ
Clean CSV → EDA → Machine Learning → ข้อเสนอแนะเชิงนโยบาย

| | |
|---|---|
| **Remote** | https://github.com/ZouWhatqq/Ta_AJ_Bank.git |
| **Branch หลัก** | `main` |
| **Local path** | `E:\DGA_ALL\Ta_AJ_Bank` |

### 5 โครงการ

| โฟลเดอร์ | หน่วยงาน | เนื้อหา | คู่มือย่อย |
|---|---|---|---|
| `กรมส่งเสริมการเกษตร/` | DOAE | พยากรณ์พื้นที่เกษตร + งบเยียวยาภัยพิบัติ (Folium Choropleth, GBR log-target) | — |
| `เกษตรกรรม/` | DLD | พยากรณ์กำลังผลิตแปรรูปเนื้อสัตว์รายจังหวัด (GBR + Huber Loss) | — |
| `ควบคุมโรค/` | DDC | พยากรณ์ผู้ป่วยโรคติดต่อนำโดยแมลง (Lag features, Recursive, XGB/LGBM) | — |
| `DGA_2/` | RD · NIMT | ความเสี่ยงยกเลิก VAT + จำแนกฝ่ายงานสอบเทียบ + ชุดสอน | [`DGA_2/CLAUDE.md`](DGA_2/CLAUDE.md) |
| `DGA_3/` | สนค. · สศอ. · พม. · วธ. | ดัชนี PPI/Shipment + สวัสดิการสังคมและวัฒนธรรม | [`DGA_3/CLAUDE.md`](DGA_3/CLAUDE.md) |

### โฟลเดอร์ที่สร้างอัตโนมัติ (Generated — อย่าแก้ด้วยมือ)

| Path | คืออะไร |
|---|---|
| `graphs/` | คลังกราฟ 192 ชิ้นจากทุก notebook แยกโฟลเดอร์ตามกลุ่ม — **สร้างจากสคริปต์ ห้ามแก้ตรง ๆ** |
| `tools/export_graphs.py` | ตัวสร้าง `graphs/` — รันใหม่ทุกครั้งที่ notebook เปลี่ยน |

```powershell
.\venv\Scripts\python.exe tools\export_graphs.py
```

**ทำไมต้องมีสคริปต์นี้:** Plotly renderer `'notebook'` ฝังไลบรารี plotly.js (4.85 MB) ลงในทุก cell output
ถ้าบันทึกกราฟตรง ๆ 125 กราฟจะกินพื้นที่ ~650 MB สคริปต์จึงดึงเฉพาะ `<div class="plotly-graph-div">`
กับ `Plotly.newPlot(...)` แล้วประกอบหน้า HTML ใหม่ที่โหลด plotly.js จาก CDN — เหลือรวม **15.1 MB**

*หมายเหตุ:* notebook บางไฟล์รันด้วย renderer `'notebook_connected'` ซึ่ง inject `<script src="cdn.plot.ly/...">`
เข้ามาเองตอนรัน (42 จาก 125 กราฟ) สคริปต์จะตรวจเจอแล้ว **ไม่ใส่ CDN tag ซ้ำ** เพื่อไม่ให้โหลด plotly สองรอบ

---

## ⚠️ กฎสำคัญเรื่อง Git

1. **`DGA_2/` และ `DGA_3/` เป็นสำเนา ไม่ใช่ submodule** — ไม่มี `.git` ของตัวเอง
   - Working copy ต้นทาง: `E:\DGA_ALL\DGA_2` (มี remote แยก `ZouWhatqq/DGA_2_example`) และ `E:\DGA_ALL\DGA_3` (ไม่มี git)
   - **ไม่มีระบบ sync อัตโนมัติ** — แก้ที่ไหนต้อง copy ไปอีกที่เอง
2. **ต้องติดตั้ง Git LFS** ก่อน clone หรือก่อน commit ไฟล์ข้อมูลใหญ่

   ```powershell
   git lfs install
   git lfs ls-files        # ตรวจว่าไฟล์ VAT ทั้ง 2 อยู่ใน LFS จริง
   git lfs pull            # ถ้า clone มาแล้วไฟล์เป็น pointer text
   ```

3. **อย่าใช้ `git add -A` แบบไม่ดู** — `git status` ก่อนเสมอ ข้อมูลดิบและ venv ใหญ่มาก
4. `.gitignore` และ `.gitattributes` ที่ root ควบคุมทั้ง repo รวมถึง `DGA_2/` และ `DGA_3/`

### ไฟล์ที่อยู่ใน Git LFS

```
DGA_2/Revenue_Department/gdpublish-vat-taxpayeraddress/VAT_TaxpayerAddress_02.csv   243.75 MB
DGA_2/Revenue_Department/gdpublish-vat-taxpayeraddress/vat_taxpayeraddress_01.csv    60.28 MB
```

> โควตา GitHub LFS ฟรี = 1 GiB storage / 1 GiB bandwidth ต่อเดือน **ต่อบัญชี**
> ไฟล์ชุดนี้อยู่ใน repo `DGA_2_example` ด้วย → เก็บซ้ำสองที่กินโควตาราว 600 MB

---

## 🐍 Python Environment

รัน Python จาก virtual environment ที่ `venv` เสมอ — **ห้ามใช้ global Python**

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install pandas numpy scikit-learn plotly matplotlib seaborn openpyxl
.\venv\Scripts\python.exe -m pip install xgboost lightgbm statsmodels folium    # เสริม

# ลงทะเบียน kernel เข้า Jupyter
.\venv\Scripts\Activate.ps1
python -m ipykernel install --user --name=venv --display-name "Python 3.11 (venv)"
```

`venv/` อยู่ใน `.gitignore` — ห้าม commit

---

## 🐛 Known Issues

### BUG-001: Plotly Rendering in VS Code Jupyter Notebooks

**Issue** — เมื่อแสดงกราฟ Plotly ใน `.ipynb` ภายใน VS Code จะขึ้น warning/error:
`No renderer could be found for mimetype "application/vnd.plotly.v1+json", but one might be available on the Marketplace.`
หรือ cell output ว่างเปล่าไปเลย

**Cause** — โดย default Plotly ส่ง output ผ่าน renderer `plotly_mimetype` (mimetype `application/vnd.plotly.v1+json`)
ซึ่ง VS Code Jupyter editor เรนเดอร์เองไม่ได้ถ้าไม่ได้ติดตั้ง extension เพิ่ม
ส่วน renderer `'iframe'` ก็ใช้ไม่ได้เช่นกัน เพราะมันเขียน HTML แยกไว้ใน `iframe_figures/`
แล้วอ้างผ่าน `<iframe src="file://...">` ซึ่งโดน Content Security Policy ของ VS Code WebView บล็อก

**Solution** — บังคับให้ Plotly ส่ง `text/html` มาตรฐาน ใส่ในเซลล์ import/setup ของทุก notebook:

```python
import plotly.io as pio
pio.renderers.default = "notebook_connected"
```

| renderer | ใช้เมื่อ |
|---|---|
| `'notebook_connected'` | ดึง plotly.js จาก CDN — ไฟล์ `.ipynb` เล็ก แต่ต้องต่อเน็ต (**ค่ามาตรฐานของ repo นี้**) |
| `'notebook'` | ฝัง plotly.js ในไฟล์ (~3 MB) — offline ได้ แต่ไฟล์ใหญ่ (DGA_2 / DGA_3 ใช้ตัวนี้) |
| `'notebook_connected+png'` | ฝัง `image/png` ด้วย เพื่อให้ GitHub preview เห็นกราฟเป็นภาพนิ่ง |

---

### BUG-002: Plotly category หายหรือ mismatch จากช่องว่างซ้ำซ้อน / data type

**อาการ** — box/bar หายบางกลุ่มโดยไม่มี error หรือ `ValueError: Value of 'x' is not the name of a column in 'data_frame'`

**สาเหตุ**
1. ชื่อ category มีช่องว่างสองช่องฝังอยู่ (เช่น `'Electrical  Metrology Department'`) → trace name ≠ axis label
2. รหัสหมวดถูกอ่านเป็น float (`10.0`) ขณะที่ตารางแมปเป็น string (`'10'`)

**แก้**

```python
df[col] = df[col].astype(str).str.strip().str.replace(r'  +', ' ', regex=True)
df['tsic_code_str'] = df['tsic_division_code'].dropna().astype(int).astype(str).str.zfill(2)
```

**บทเรียน** — ก่อนใช้ `color=` บน categorical column ให้ตรวจด้วย `df[col].unique()` และ `repr()` เสมอ

---

### BUG-003: matplotlib แสดงภาษาไทยเป็นสี่เหลี่ยม (tofu)

**แก้** — โหลดฟอนต์ Prompt จาก TTF ในเครื่อง (มีอยู่ที่ `DGA_3/G5_*/fonts/Prompt/`)

```python
from matplotlib import font_manager
from pathlib import Path
for f in Path('./fonts/Prompt').glob('*.ttf'):
    font_manager.fontManager.addfont(str(f))
plt.rcParams['font.family'] = 'Prompt'
```

Plotly ใช้ Google Fonts CDN ได้เลย ไม่ต้องโหลด TTF

---

## 📐 มาตรฐานข้อมูล (Data Standards)

1. **Encoding** — บันทึก CSV ภาษาไทยด้วย `utf-8-sig` เสมอ; ตอนอ่านไฟล์ราชการเก่าลอง `tis-620` แล้ว fallback เป็น `utf-8-sig`
2. **Header** — ยุบ multi-level / merged header เป็น snake_case ชั้นเดียว ตัด footnote และ title block ออก
3. **ชนิดข้อมูล** — ตัวเลข parse เป็น numeric (ตัด `,`, จัดการ `-`, `N/A`, ช่องว่าง)
4. **ปี พ.ศ. → ค.ศ.** — เก็บทั้ง `year_be` / `year_ce` และ `period_ym` แบบ ISO `YYYY-MM`
5. **Hierarchy** — แตกหมวดที่ merge/indent เป็นคอลัมน์ (`category_level`, `level_type`, `*_code`, `*_name`)
6. **Metadata** — เก็บ `source_file`, `source_agency`, `base_year` เป็นคอลัมน์ทุกครั้ง
7. **Validation** — ทุก pipeline ต้องมีสคริปต์ตรวจสอบเทียบ 1:1 กับต้นฉบับ (ดู `DGA_3/scripts/validate_*.py`)

---

## ✅ Checklist ก่อน commit

- [ ] `git status` ตรวจแล้ว — ไม่มี `venv/`, `__pycache__/`, `.ipynb_checkpoints/`, `iframe_figures/`
- [ ] `git lfs ls-files` แสดงไฟล์ VAT ทั้ง 2 ไฟล์
- [ ] ไม่มีไฟล์ > 100 MB ที่ไม่ได้อยู่ใน LFS
- [ ] notebook ตั้ง `pio.renderers.default` แล้ว
- [ ] CSV ภาษาไทยบันทึกด้วย `utf-8-sig`
- [ ] README ของโฟลเดอร์ที่แก้ อัปเดตให้ตรงกับไฟล์จริงแล้ว
