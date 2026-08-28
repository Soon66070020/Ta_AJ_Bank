# CLAUDE.md — DGA_3 (Economic Index & Social Welfare)

> **ขั้นตอนแรกเสมอ:** ทุกครั้งที่เริ่ม session ใหม่ agent / AI model **ต้องอ่านไฟล์นี้ก่อน** เพื่อเข้าใจข้อจำกัดของโครงการ การตั้งค่า environment และกฎการแปลงข้อมูล
> ดูคู่มือระดับ workspace ที่ [`../../CLAUDE.md`](../../CLAUDE.md) และคู่มือระดับ repo ที่ [`../CLAUDE.md`](../CLAUDE.md)

---

## 📌 บริบทของโฟลเดอร์นี้ (Context)

โฟลเดอร์นี้เป็น **สำเนาที่คัดกรองแล้ว** ของโครงการ DGA_3 ซึ่งถูกเพิ่มเข้ามาเป็นโฟลเดอร์ย่อยของ repo [`ZouWhatqq/Ta_AJ_Bank`](https://github.com/ZouWhatqq/Ta_AJ_Bank)

| | |
|---|---|
| **Working copy ต้นทาง** | `E:\DGA_ALL\DGA_3` (ไม่มี git ของตัวเอง) |
| **โฟลเดอร์นี้** | `E:\DGA_ALL\Ta_AJ_Bank\DGA_3` |
| **Sync** | ❌ ไม่มีระบบอัตโนมัติ — ถ้าแก้ที่ต้นทางต้อง copy กลับมาเอง |

---

## ⚠️ ISSUE-A: ชื่อโฟลเดอร์ `G3_` / `G5_` สลับกับเนื้อหา

**นี่คือกับดักที่ทำให้คนอ่านผิดบ่อยที่สุดในโครงการนี้**

| โฟลเดอร์บนดิสก์ | เนื้อหาจริง | README ภายในเรียกว่า |
|---|---|---|
| `G3_เศรษฐกิจอุตสาหกรรม_นโยบายและยุทธศาสตร์การค้า/` | **สวัสดิการสังคม (พม.) + วัฒนธรรม (วธ.)** | `group_6/` |
| `G5_วัฒนธรรม_การพัฒนาสังคมและความมั่นคงของมนุษย์/` | **PPI (สนค.) + Shipment Index (สศอ.)** | `group_5/` |

**ยังไม่เปลี่ยนชื่อ** เพราะ path ใน notebook และสคริปต์ทั้งหมดอ้างชื่อปัจจุบันอยู่
ถ้าจะแก้ ต้องแก้พร้อมกันทั้ง: ชื่อโฟลเดอร์ + path ใน notebook ทุกไฟล์ + path ใน `scripts/*.py` + README ทั้ง 3 ระดับ

---

## 🐍 Python Environment & Dependencies

1. **Virtual Environment**
   - ใช้ venv ของโครงการเสมอ — **ห้ามใช้ global python หรือแก้ package ระดับระบบ**
   - Python: `.\venv\Scripts\python.exe`
   - Pip: `.\venv\Scripts\python.exe -m pip install <package>`
   - venv ต้นทาง: `E:\DGA_ALL\DGA_3\venv`

2. **Core Libraries**
   - `pandas`, `numpy`, `openpyxl` — data pipeline
   - `scikit-learn` — K-Means, PCA, Regression, Classification
   - `plotly`, `matplotlib`, `seaborn` — visualization
   - `statsmodels` — Holt-Winters / time-series forecasting

---

## 🎯 Project Overview & Objective

โครงการนี้อ่านไฟล์ Excel (`.xlsx`) ที่ **จัดรูปแบบมาเพื่อให้คนอ่าน** — merged cell, multi-row header, แถวสรุป, เชิงอรรถ, ข้อความไทย, ปี พ.ศ. — แล้วแปลงเป็น **CSV มาตรฐานที่เครื่องอ่านได้** ก่อนต่อยอดเป็น EDA + Machine Learning + ข้อเสนอแนะเชิงนโยบาย

### โครงสร้างงาน

| Path | เนื้อหา |
|---|---|
| `scripts/` | Data pipeline ทั้งหมด (ย้ายมาจาก root เดิม) |
| `G5_*/raw/` · `G5_*/clean_csv/` | PPI + Shipment — ดิบ / สะอาด |
| `G3_*/raw/` · `G3_*/clean/` | สวัสดิการ พม. + วัฒนธรรม วธ. — ดิบ / สะอาด |
| `G3_*/process_clean_csv.py` | pipeline เฉพาะกลุ่ม `group_6` (ยังอยู่ในโฟลเดอร์ตัวเอง) |

> ⚠️ **path เปลี่ยนจากเวอร์ชันเดิม:** สคริปต์ `process_price_index.py`, `process_shipment.py`,
> `validate_output.py`, `validate_shipment.py`, `execute_notebook.py`, `build_*.py`, `update_goal_notebook.py`
> ย้ายจาก root ของ `DGA_3/` ไปอยู่ที่ `DGA_3/scripts/` แล้ว
> → คำสั่งรันเปลี่ยนจาก `python process_price_index.py` เป็น `python scripts\process_price_index.py`
> → ตัวสคริปต์ยังอ้าง path ข้อมูลแบบ relative จาก **root ของ `DGA_3/`** อยู่ ดังนั้น **ต้อง `cd DGA_3` ก่อนรันเสมอ**

### สคริปต์ที่ถูกตัดออก (throwaway จากตอน debug)

`inspect_goal_nb.py` · `inspect_notebooks.py` · `inspect_ppi.py` · `inspect_top_divisions.py` ·
`test_cell9_legend.py` · `test_new_cells.py` · `test_perfect_radar.py` · `test_*.html` · `test_font_prompt_barchart.ipynb`

---

## 📐 Data Transformation & Cleaning Standards

1. **Encoding** — บันทึก CSV ที่มีภาษาไทยด้วย `utf-8-sig` (UTF-8 with BOM) เสมอ เพื่อให้เปิดใน Excel และเครื่องมือประมวลผลข้อมูลได้ถูกต้อง
2. **Header Normalization**
   - ยุบ multi-level / merged header เป็นชื่อคอลัมน์ที่ชัดเจนและกระชับ (snake_case หรือชื่อมาตรฐาน)
   - ลบ header ซ้ำ เชิงอรรถ และ title block ออกจากแถวข้อมูล
3. **Data Integrity & Types**
   - ฟิลด์ตัวเลข (ดัชนี, เปอร์เซ็นต์, ปริมาณ, มูลค่า) ต้อง parse เป็น numeric — ตัด `,` ออก, จัดการ `-`, `N/A`, ช่องว่าง → NaN หรือ 0 ตาม schema
   - ฟิลด์วันที่ / เดือน / ปี ต้องแปลงเป็นมาตรฐาน — ปี พ.ศ. `2569` หรือ `69` → `year_be` + `year_ce` และ `period_ym` แบบ ISO `YYYY-MM`
4. **Hierarchical / Category Unpivoting** — แตกหมวดหมู่ที่ merge หรือ indent เป็นคอลัมน์ category / sub-category ที่ชัดเจน (`category_level`, `level_type`, `*_code`, `*_name`)
5. **No Loss of Metadata** — เก็บ metadata ของไฟล์ต้นทาง (`source_file`, `source_agency`, `base_year`, รอบรายงาน) ไว้เป็นคอลัมน์เสมอ
6. **Validation** — ทุก pipeline ต้องมีสคริปต์ตรวจสอบเทียบทุกแถวและทุกตัวเลขกับ Excel ต้นฉบับแบบ 1:1

---

## 🐛 Known Issues & Lessons Learned

### BUG-001: Plotly `'iframe'` renderer ไม่แสดงผลใน VS Code

- **อาการ:** กราฟ Plotly ไม่แสดงผลใน VS Code Jupyter — cell output ว่างเปล่า
- **สาเหตุ:** Renderer `'iframe'` สร้างไฟล์ HTML แยกใน `iframe_figures/` แล้วใส่ `<iframe src="iframe_figures/...">` ใน output แต่ VS Code Jupyter WebView มี Content Security Policy (CSP) ที่บล็อก local `file://` path จาก iframe
- **แก้ไข:** เปลี่ยน renderer เป็น `'notebook'` ซึ่งฝัง HTML โดยตรงใน cell output

  ```python
  import plotly.io as pio
  pio.renderers.default = 'notebook'
  ```

---

### BUG-002: Plotly Box / Scatter Plot ไม่แสดงผลหรือ Data Mismatch จากช่องว่างซ้ำซ้อนและ Data Type

- **อาการ:** Plotly ไม่แสดงกราฟ หรือเกิด `ValueError: Value of 'x' is not the name of a column in 'data_frame'` จากการรวมข้อมูลที่ว่างเปล่า
- **สาเหตุ:**
  1. ชื่อหมวดหมู่มีช่องว่างซ้ำซ้อน (`  +`) ทำให้ string comparison ระหว่างหมวดหมู่ไม่ตรงกัน
  2. รหัสหมวดหมู่ (เช่น TSIC Code) ถูกอ่านเป็น Float (`10.0`) ในขณะที่ตารางแมปเป็น String (`'10'`)
- **แก้ไข:**

  ```python
  # กำจัดช่องว่างซ้ำซ้อนในชื่อ Category
  df['category_name'] = df['category_name'].astype(str).str.strip().str.replace(r'  +', ' ', regex=True)
  # จัดการรหัสหมวดให้เป็น String 2 หลักมาตรฐาน
  df['tsic_code_str'] = df['tsic_division_code'].dropna().astype(int).astype(str).str.zfill(2)
  ```

- **บทเรียน:** ก่อน merge หรือใช้ `color=` บน categorical column ให้ตรวจด้วย `df[col].unique()` และ `repr()` เสมอ

---

### BUG-003: matplotlib แสดงภาษาไทยเป็นสี่เหลี่ยม (tofu)

- **อาการ:** กราฟ matplotlib แสดงข้อความไทยเป็น `□□□□`
- **สาเหตุ:** ฟอนต์ default ของ matplotlib (DejaVu Sans) ไม่มี glyph ภาษาไทย
- **แก้ไข:** โหลดฟอนต์ Prompt จากไฟล์ TTF ในเครื่อง

  ```python
  from matplotlib import font_manager
  from pathlib import Path
  font_dir = Path('./fonts/Prompt')          # 18 ไฟล์ TTF
  for f in font_dir.glob('*.ttf'):
      font_manager.fontManager.addfont(str(f))
  plt.rcParams['font.family'] = 'Prompt'
  ```

- **ไฟล์ที่ใช้:** `G5_*/shipment_goal_analysis.ipynb`
- **หมายเหตุ:** `fonts/Prompt/` ถูก commit ไว้ใน repo แล้ว (2.93 MB, ลิขสิทธิ์ SIL OFL)
  **ห้ามลบ** — notebook จะแสดงภาษาไทยไม่ได้
  Plotly ใช้ Google Fonts CDN ได้เลย ไม่ต้องโหลด TTF

---

## ✅ Checklist ก่อน commit

- [ ] ไม่มี `venv/`, `__pycache__/`, `.ipynb_checkpoints/` ติดไปด้วย
- [ ] ไม่มี `test_*.html`, `*.zip`, `*.rar`, `*.pdf` หลุดเข้ามา (มีใน `.gitignore` แล้ว)
- [ ] notebook ตั้ง `pio.renderers.default` แล้ว
- [ ] CSV ภาษาไทยบันทึกด้วย `utf-8-sig`
- [ ] รัน `scripts\validate_output.py` และ `scripts\validate_shipment.py` ผ่านทั้งคู่
- [ ] `README.md` ตรงกับไฟล์จริงในโฟลเดอร์
