# CLAUDE.md — DGA_2 (Revenue & Metrology)

> **ขั้นตอนแรกเสมอ:** อ่านไฟล์นี้ก่อนเริ่มงานในโฟลเดอร์ `DGA_2/` ทุกครั้ง
> ดูคู่มือระดับ workspace ที่ [`../../CLAUDE.md`](../../CLAUDE.md) และคู่มือระดับ repo ที่ [`../CLAUDE.md`](../CLAUDE.md)

---

## 📌 บริบทของโฟลเดอร์นี้ (Context)

โฟลเดอร์นี้เป็น **สำเนาที่คัดกรองแล้ว** ของโครงการ DGA_2 ซึ่งถูกเพิ่มเข้ามาเป็นโฟลเดอร์ย่อยของ repo [`ZouWhatqq/Ta_AJ_Bank`](https://github.com/ZouWhatqq/Ta_AJ_Bank)

| | |
|---|---|
| **Working copy ต้นทาง** | `E:\DGA_ALL\DGA_2` (remote แยก: `ZouWhatqq/DGA_2_example`) |
| **โฟลเดอร์นี้** | `E:\DGA_ALL\Ta_AJ_Bank\DGA_2` — ไม่มี `.git` ของตัวเอง |
| **Sync** | ❌ ไม่มีระบบอัตโนมัติ — ถ้าแก้ที่ต้นทางต้อง copy กลับมาเอง |

---

## 🐍 Python Environment

โครงการนี้ใช้ virtual environment แยก **ห้ามใช้ global Python หรือแก้ package ระดับระบบ**

| | path |
|---|---|
| venv (ต้นทาง) | `E:\DGA_ALL\DGA_2\venv` |
| venv (repo นี้) | `E:\DGA_ALL\Ta_AJ_Bank\venv` — สร้างเอง ไม่ได้ commit |

```powershell
.\venv\Scripts\python.exe <script.py>
.\venv\Scripts\python.exe -m pip install <package>
```

**ไลบรารีหลัก:** `pandas`, `numpy`, `scikit-learn`, `plotly`, `matplotlib`, `seaborn`, `openpyxl`
**เสริม:** `xgboost`, `lightgbm`

---

## 📂 Project Structure

| Path | เนื้อหา |
|---|---|
| `Revenue_Department/gdpublish-*/` | ชุดข้อมูลเปิดกรมสรรพากรจาก data.go.th (21 โฟลเดอร์) |
| `Revenue_Department/For_final/` | ชุดสอน VAT (exercise / solution / expert source) |
| `Metrology_Department/moc_data/` | ชุดข้อมูล NIMT + notebook expert หลัก |
| `Metrology_Department/for_final/` | ชุดสอน NIMT (exercise / solution / expert source) |
| `K_means_Clustering.ipynb` | template รูปแบบชุดสอนที่ notebook ทั้งหมดยึดตาม |

> ⚠️ **path เปลี่ยนจากเวอร์ชันเดิม:** `metrology_data_science.ipynb` และ `real_nimt_machine_learning.csv`
> ย้ายจาก `Metrology_Department/` (และเวอร์ชันเก่ากว่านั้นคือ `meter/`) มาอยู่ที่ `Metrology_Department/moc_data/` แล้ว
> เช่นเดียวกับ `vat_risk_analysis.ipynb` ที่ย้ายไป `Revenue_Department/For_final/`

---

## 💾 Git LFS — ต้องรู้ก่อนแก้ไฟล์ข้อมูล

ไฟล์สองไฟล์นี้ถูก track ด้วย Git LFS (ตั้งค่าใน [`../.gitattributes`](../.gitattributes)):

```
Revenue_Department/gdpublish-vat-taxpayeraddress/VAT_TaxpayerAddress_02.csv   243.75 MB
Revenue_Department/gdpublish-vat-taxpayeraddress/vat_taxpayeraddress_01.csv    60.28 MB
```

- ถ้า `git lfs install` ยังไม่ได้รัน ไฟล์ที่ clone มาจะเป็น **pointer text ไม่กี่บรรทัด** ไม่ใช่ CSV จริง
  → notebook จะพังตอน `pd.read_csv` ด้วย error แปลก ๆ (เช่น column ไม่ครบ) ให้เช็ค `git lfs ls-files` ก่อนเสมอ
- โควตา GitHub LFS ฟรี = 1 GiB storage / 1 GiB bandwidth ต่อเดือน **ต่อบัญชี**
  ไฟล์ชุดนี้อยู่ใน repo `DGA_2_example` ด้วย → เก็บซ้ำสองที่กินโควตาราว 600 MB

---

## 📐 มาตรฐานการอ่านข้อมูล (Data Loading Standards)

```python
# ข้อมูลราชการไทยเก่ามักเป็น tis-620 — ลองก่อนแล้ว fallback
for enc in ('tis-620', 'utf-8-sig', 'cp874'):
    try:
        df = pd.read_csv(path, encoding=enc)
        break
    except UnicodeDecodeError:
        continue

# ปี พ.ศ. → ค.ศ.
df['year_ce'] = df['year_be'] - 543

# บันทึก CSV ภาษาไทยด้วย utf-8-sig เสมอ (Excel เปิดแล้วไม่เพี้ยน)
df.to_csv(out_path, index=False, encoding='utf-8-sig')
```

---

## 🐛 Known Issues & Lessons Learned

### BUG-001: Plotly `'iframe'` renderer ไม่แสดงผลใน VS Code

- **อาการ:** กราฟ Plotly ไม่แสดงผลใน VS Code Jupyter — cell output ว่างเปล่า
- **สาเหตุ:** Renderer `'iframe'` สร้างไฟล์ HTML แยกใน `iframe_figures/` แล้วใส่ `<iframe src="iframe_figures/...">` ใน output แต่ VS Code Jupyter WebView มี Content Security Policy (CSP) ที่บล็อก local `file://` path จาก iframe
- **แก้ไข:** เปลี่ยน renderer เป็น `'notebook'` ซึ่งฝัง HTML โดยตรงใน cell output

  ```python
  # ❌ ใช้ไม่ได้ใน VS Code
  pio.renderers.default = 'iframe'

  # ✅ ถูกต้อง — ฝัง HTML ตรงใน cell output
  pio.renderers.default = 'notebook'
  ```

- **ไฟล์ที่แก้:** เซลล์ import แรกของทุก notebook ในโครงการ

---

### BUG-002: Plotly Box Plot ไม่แสดงผลเมื่อชื่อ category มีช่องว่างซ้ำซ้อน

- **อาการ:** `px.box(..., color='ฝ่ายงานจริง (Actual Department)')` ไม่แสดง box บางกล่อง (แสดงเพียงบางฝ่ายงาน) — **ไม่มี error message**
- **สาเหตุ:** ข้อมูลใน column `'ฝ่ายงานจริง (Actual Department)'` มีช่องว่างสองช่องฝังอยู่ใน 3 ชื่อฝ่ายงาน:
  - `'Electrical  Metrology Department'` (double space)
  - `'Mechanical  Metrology Department'` (double space)
  - `'Chemical Metrology  Department'` (double space)

  เมื่อใช้ `color=` พร้อมกับ `y=` บน column เดียวกัน Plotly สร้าง 1 trace ต่อ category โดยใช้ชื่อเป็น trace name และ y-axis label พร้อมกัน ชื่อที่มี double space ทำให้ trace name ≠ y-axis label → box หายไปจาก plot

- **แก้ไข:** เพิ่มการ normalize ช่องว่างในขั้นตอน Data Cleaning ทันทีหลัง `.str.strip()`

  ```python
  df['ฝ่ายงานจริง (Actual Department)'] = df['ฝ่ายงานจริง (Actual Department)'].str.strip()
  # ✅ เพิ่มบรรทัดนี้ — กำจัดช่องว่างซ้ำซ้อนในชื่อ category
  df['ฝ่ายงานจริง (Actual Department)'] = df['ฝ่ายงานจริง (Actual Department)'].str.replace(r'  +', ' ', regex=True)
  ```

- **บทเรียน:** ก่อนใช้ `color=` บน categorical column ควรตรวจสอบด้วย `df[col].unique()` และ `repr()` เพื่อดูช่องว่างซ่อน
- **ไฟล์ที่แก้:** `Metrology_Department/moc_data/metrology_data_science.ipynb` เซลล์ Data Cleaning (เซลล์ที่ 3)

---

### BUG-003: กราฟ Plotly ไม่แสดงบนหน้า GitHub preview

- **อาการ:** เปิด `.ipynb` บน GitHub แล้วเห็นแต่ที่ว่าง ทั้งที่ใน VS Code แสดงปกติ
- **สาเหตุ:** GitHub เลือก mimetype ที่มี priority สูงสุดใน output ซึ่งคือ `application/vnd.plotly.v1+json` แต่ GitHub เรนเดอร์ mimetype นี้ไม่ได้
- **แก้ไข:** execute notebook ด้วย renderer `png` (หรือ `notebook_connected+png`) เพื่อให้มี `image/png` ฝังอยู่ใน output ด้วย GitHub จะ fallback มาแสดงภาพนิ่งแทน

  ```python
  pio.renderers.default = 'notebook_connected+png'
  ```

- **ข้อแลกเปลี่ยน:** ไฟล์ `.ipynb` ใหญ่ขึ้น และกราฟบน GitHub จะกดโต้ตอบไม่ได้ (แต่ใน VS Code ยัง interactive ปกติ)

---

## ✅ Checklist ก่อน commit

- [ ] `git lfs ls-files` แสดงไฟล์ VAT ทั้ง 2 ไฟล์ (ไม่ใช่ commit เป็น blob ธรรมดา)
- [ ] ไม่มี `venv/`, `__pycache__/`, `.ipynb_checkpoints/`, `iframe_figures/` ติดไปด้วย
- [ ] notebook ตั้ง `pio.renderers.default` แล้ว
- [ ] `README.md` ตรงกับไฟล์จริงในโฟลเดอร์
