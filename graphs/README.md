# 📊 คลังกราฟรวมทุกกลุ่ม (Graph Gallery)

กราฟทั้งหมดที่ดึงออกมาจาก notebook ในโครงการนี้ รวบรวมไว้ที่เดียว
แยกโฟลเดอร์ตามกลุ่มงาน เพื่อให้เปิดดูได้โดยไม่ต้องรัน notebook

| รวมทั้งหมด | 192 กราฟ |
|---|---|
| Plotly (interactive `.html`) | 125 |
| ภาพนิ่ง (`.png`) | 67 |

> ⚠️ ไฟล์ `.html` โหลด plotly.js จาก CDN — **ต้องต่ออินเทอร์เน็ตตอนเปิด**
> และ GitHub ไม่เรนเดอร์ HTML ในหน้า preview ให้ดาวน์โหลดไปเปิดในเบราว์เซอร์
> หรือดูผ่าน [htmlpreview.github.io](https://htmlpreview.github.io)

สร้างใหม่ได้ด้วย:

```powershell
.\venv\Scripts\python.exe tools\export_graphs.py
```

---

## กลุ่มงาน (Groups)

| กลุ่ม | จำนวนกราฟ | ดัชนี |
|---|---:|---|
| 🌾 กรมส่งเสริมการเกษตร (DOAE) | 15 | [`กรมส่งเสริมการเกษตร/`](กรมส่งเสริมการเกษตร/README.md) |
| 🐃 เกษตรกรรม / ปศุสัตว์ (DLD) | 16 | [`เกษตรกรรม/`](เกษตรกรรม/README.md) |
| 🦟 ควบคุมโรค (DDC) | 52 | [`ควบคุมโรค/`](ควบคุมโรค/README.md) |
| 🏢 DGA_2 — กรมสรรพากร & มาตรวิทยา | 38 | [`DGA_2/`](DGA_2/README.md) |
| 📈 DGA_3 — ดัชนีเศรษฐกิจ & สวัสดิการสังคม | 71 | [`DGA_3/`](DGA_3/README.md) |

---

## ⚠️ notebook ที่อ่านไม่ได้ (ข้ามไป)

| ไฟล์ | ปัญหา |
|---|---|
| `DGA_2/Revenue_Department/For_final/eda_data_revenue.ipynb` | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
