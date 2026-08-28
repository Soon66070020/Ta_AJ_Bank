import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, json, re, html
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# 1. Standard Reference Tables (77 Provinces & Centroids)
# ---------------------------------------------------------
PROVINCE_REF = {
    1: {'th': 'กรุงเทพมหานคร', 'en': 'Bangkok', 'region': 'ภาคกลาง', 'lat': 13.7563, 'lng': 100.5018},
    2: {'th': 'สมุทรปราการ', 'en': 'Samut Prakan', 'region': 'ภาคกลาง', 'lat': 13.5991, 'lng': 100.5998},
    3: {'th': 'นนทบุรี', 'en': 'Nonthaburi', 'region': 'ภาคกลาง', 'lat': 13.8621, 'lng': 100.5144},
    4: {'th': 'ปทุมธานี', 'en': 'Pathum Thani', 'region': 'ภาคกลาง', 'lat': 14.0208, 'lng': 100.5250},
    5: {'th': 'พระนครศรีอยุธยา', 'en': 'Phra Nakhon Si Ayutthaya', 'region': 'ภาคกลาง', 'lat': 14.3532, 'lng': 100.5684},
    6: {'th': 'อ่างทอง', 'en': 'Ang Thong', 'region': 'ภาคกลาง', 'lat': 14.5896, 'lng': 100.4550},
    7: {'th': 'ลพบุรี', 'en': 'Lop Buri', 'region': 'ภาคกลาง', 'lat': 14.7995, 'lng': 100.6534},
    8: {'th': 'สิงห์บุรี', 'en': 'Sing Buri', 'region': 'ภาคกลาง', 'lat': 14.8936, 'lng': 100.4018},
    9: {'th': 'ชัยนาท', 'en': 'Chai Nat', 'region': 'ภาคกลาง', 'lat': 15.1852, 'lng': 100.1252},
    10: {'th': 'สระบุรี', 'en': 'Saraburi', 'region': 'ภาคกลาง', 'lat': 14.5289, 'lng': 100.9108},
    11: {'th': 'ชลบุรี', 'en': 'Chon Buri', 'region': 'ภาคตะวันออก', 'lat': 13.3611, 'lng': 100.9847},
    12: {'th': 'ระยอง', 'en': 'Rayong', 'region': 'ภาคตะวันออก', 'lat': 12.6814, 'lng': 101.2816},
    13: {'th': 'จันทบุรี', 'en': 'Chanthaburi', 'region': 'ภาคตะวันออก', 'lat': 12.6114, 'lng': 102.1039},
    14: {'th': 'ตราด', 'en': 'Trat', 'region': 'ภาคตะวันออก', 'lat': 12.2428, 'lng': 102.5175},
    15: {'th': 'ฉะเชิงเทรา', 'en': 'Chachoengsao', 'region': 'ภาคตะวันออก', 'lat': 13.6904, 'lng': 101.0780},
    16: {'th': 'ปราจีนบุรี', 'en': 'Prachin Buri', 'region': 'ภาคตะวันออก', 'lat': 14.0509, 'lng': 101.3716},
    17: {'th': 'นครนายก', 'en': 'Nakhon Nayok', 'region': 'ภาคกลาง', 'lat': 14.2069, 'lng': 101.2131},
    18: {'th': 'สระแก้ว', 'en': 'Sa Kaeo', 'region': 'ภาคตะวันออก', 'lat': 13.8140, 'lng': 102.0718},
    19: {'th': 'นครราชสีมา', 'en': 'Nakhon Ratchasima', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 14.9707, 'lng': 102.0978},
    20: {'th': 'บุรีรัมย์', 'en': 'Buri Ram', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 14.9930, 'lng': 103.1029},
    21: {'th': 'สุรินทร์', 'en': 'Surin', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 14.8818, 'lng': 103.4936},
    22: {'th': 'ศรีสะเกษ', 'en': 'Si Sa Ket', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 15.1186, 'lng': 104.3220},
    23: {'th': 'อุบลราชธานี', 'en': 'Ubon Ratchathani', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 15.2448, 'lng': 104.8473},
    24: {'th': 'ยโสธร', 'en': 'Yasothon', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 15.7926, 'lng': 104.1453},
    25: {'th': 'ชัยภูมิ', 'en': 'Chaiyaphum', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 15.8063, 'lng': 102.0315},
    26: {'th': 'อำนาจเจริญ', 'en': 'Amnat Charoen', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 15.8657, 'lng': 104.6258},
    27: {'th': 'บึงกาฬ', 'en': 'Bueng Kan', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 18.3609, 'lng': 103.6465},
    28: {'th': 'หนองบัวลำภู', 'en': 'Nong Bua Lam Phu', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 17.2044, 'lng': 102.4407},
    29: {'th': 'ขอนแก่น', 'en': 'Khon Kaen', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 16.4419, 'lng': 102.8360},
    30: {'th': 'อุดรธานี', 'en': 'Udon Thani', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 17.4157, 'lng': 102.7872},
    31: {'th': 'เลย', 'en': 'Loei', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 17.4860, 'lng': 101.7223},
    32: {'th': 'หนองคาย', 'en': 'Nong Khai', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 17.8783, 'lng': 102.7420},
    33: {'th': 'มหาสารคาม', 'en': 'Maha Sarakham', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 16.1851, 'lng': 103.3007},
    34: {'th': 'ร้อยเอ็ด', 'en': 'Roi Et', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 16.0538, 'lng': 103.6520},
    35: {'th': 'กาฬสินธุ์', 'en': 'Kalasin', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 16.4322, 'lng': 103.5061},
    36: {'th': 'สกลนคร', 'en': 'Sakon Nakhon', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 17.1612, 'lng': 104.1486},
    37: {'th': 'นครพนม', 'en': 'Nakhon Phanom', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 17.3976, 'lng': 104.7816},
    38: {'th': 'มุกดาหาร', 'en': 'Mukdahan', 'region': 'ภาคตะวันออกเฉียงเหนือ', 'lat': 16.5436, 'lng': 104.7235},
    39: {'th': 'เชียงใหม่', 'en': 'Chiang Mai', 'region': 'ภาคเหนือ', 'lat': 18.7883, 'lng': 98.9853},
    40: {'th': 'ลำพูน', 'en': 'Lamphun', 'region': 'ภาคเหนือ', 'lat': 18.5745, 'lng': 99.0087},
    41: {'th': 'ลำปาง', 'en': 'Lampang', 'region': 'ภาคเหนือ', 'lat': 18.2888, 'lng': 99.4928},
    42: {'th': 'อุตรดิตถ์', 'en': 'Uttaradit', 'region': 'ภาคเหนือ', 'lat': 17.6201, 'lng': 100.0993},
    43: {'th': 'แพร่', 'en': 'Phrae', 'region': 'ภาคเหนือ', 'lat': 18.1446, 'lng': 100.1410},
    44: {'th': 'น่าน', 'en': 'Nan', 'region': 'ภาคเหนือ', 'lat': 18.7838, 'lng': 100.7782},
    45: {'th': 'พะเยา', 'en': 'Phayao', 'region': 'ภาคเหนือ', 'lat': 19.1670, 'lng': 99.9022},
    46: {'th': 'เชียงราย', 'en': 'Chiang Rai', 'region': 'ภาคเหนือ', 'lat': 19.9072, 'lng': 99.8325},
    47: {'th': 'แม่ฮ่องสอน', 'en': 'Mae Hong Son', 'region': 'ภาคเหนือ', 'lat': 19.3020, 'lng': 97.9654},
    48: {'th': 'นครสวรรค์', 'en': 'Nakhon Sawan', 'region': 'ภาคกลาง', 'lat': 15.6987, 'lng': 100.1199},
    49: {'th': 'อุทัยธานี', 'en': 'Uthai Thani', 'region': 'ภาคกลาง', 'lat': 15.3835, 'lng': 100.0246},
    50: {'th': 'กำแพงเพชร', 'en': 'Kamphaeng Phet', 'region': 'ภาคกลาง', 'lat': 16.4828, 'lng': 99.5227},
    51: {'th': 'ตาก', 'en': 'Tak', 'region': 'ภาคเหนือ', 'lat': 16.8840, 'lng': 99.1258},
    52: {'th': 'สุโขทัย', 'en': 'Sukhothai', 'region': 'ภาคกลาง', 'lat': 17.0078, 'lng': 99.8235},
    53: {'th': 'พิษณุโลก', 'en': 'Phitsanulok', 'region': 'ภาคกลาง', 'lat': 16.8211, 'lng': 100.2659},
    54: {'th': 'พิจิตร', 'en': 'Phichit', 'region': 'ภาคกลาง', 'lat': 16.4429, 'lng': 100.3488},
    55: {'th': 'เพชรบูรณ์', 'en': 'Phetchabun', 'region': 'ภาคกลาง', 'lat': 16.4190, 'lng': 101.1567},
    56: {'th': 'ราชบุรี', 'en': 'Ratchaburi', 'region': 'ภาคตะวันตก', 'lat': 13.5283, 'lng': 99.8134},
    57: {'th': 'กาญจนบุรี', 'en': 'Kanchanaburi', 'region': 'ภาคตะวันตก', 'lat': 14.0228, 'lng': 99.5328},
    58: {'th': 'สุพรรณบุรี', 'en': 'Suphan Buri', 'region': 'ภาคกลาง', 'lat': 14.4745, 'lng': 100.1177},
    59: {'th': 'นครปฐม', 'en': 'Nakhon Pathom', 'region': 'ภาคกลาง', 'lat': 13.8196, 'lng': 100.0601},
    60: {'th': 'สมุทรสาคร', 'en': 'Samut Sakhon', 'region': 'ภาคกลาง', 'lat': 13.5475, 'lng': 100.2744},
    61: {'th': 'สมุทรสงคราม', 'en': 'Samut Songkhram', 'region': 'ภาคกลาง', 'lat': 13.4098, 'lng': 99.9999},
    62: {'th': 'เพชรบุรี', 'en': 'Phetchaburi', 'region': 'ภาคตะวันตก', 'lat': 13.1114, 'lng': 99.9398},
    63: {'th': 'ประจวบคีรีขันธ์', 'en': 'Prachuap Khiri Khan', 'region': 'ภาคตะวันตก', 'lat': 11.8124, 'lng': 99.7973},
    64: {'th': 'นครศรีธรรมราช', 'en': 'Nakhon Si Thammarat', 'region': 'ภาคใต้', 'lat': 8.4325, 'lng': 99.9631},
    65: {'th': 'กระบี่', 'en': 'Krabi', 'region': 'ภาคใต้', 'lat': 8.0863, 'lng': 98.9063},
    66: {'th': 'พังงา', 'en': 'Phangnga', 'region': 'ภาคใต้', 'lat': 8.4501, 'lng': 98.5255},
    67: {'th': 'ภูเก็ต', 'en': 'Phuket', 'region': 'ภาคใต้', 'lat': 7.8804, 'lng': 98.3923},
    68: {'th': 'สุราษฎร์ธานี', 'en': 'Surat Thani', 'region': 'ภาคใต้', 'lat': 9.1382, 'lng': 99.3215},
    69: {'th': 'ระนอง', 'en': 'Ranong', 'region': 'ภาคใต้', 'lat': 9.9529, 'lng': 98.6348},
    70: {'th': 'ชุมพร', 'en': 'Chumphon', 'region': 'ภาคใต้', 'lat': 10.4930, 'lng': 99.1800},
    71: {'th': 'สงขลา', 'en': 'Songkhla', 'region': 'ภาคใต้', 'lat': 7.1898, 'lng': 100.5954},
    72: {'th': 'สตูล', 'en': 'Satun', 'region': 'ภาคใต้', 'lat': 6.6238, 'lng': 100.0674},
    73: {'th': 'ตรัง', 'en': 'Trang', 'region': 'ภาคใต้', 'lat': 7.5594, 'lng': 99.6114},
    74: {'th': 'พัทลุง', 'en': 'Phatthalung', 'region': 'ภาคใต้', 'lat': 7.6167, 'lng': 100.0740},
    75: {'th': 'ปัตตานี', 'en': 'Pattani', 'region': 'ภาคใต้', 'lat': 6.8677, 'lng': 101.2501},
    76: {'th': 'ยะลา', 'en': 'Yala', 'region': 'ภาคใต้', 'lat': 6.5411, 'lng': 101.2804},
    77: {'th': 'นราธิวาส', 'en': 'Narathiwat', 'region': 'ภาคใต้', 'lat': 6.4255, 'lng': 101.8253}
}

PROV_TH_TO_REGION = {v['th']: v['region'] for v in PROVINCE_REF.values()}
PROV_TH_TO_EN = {v['th']: v['en'] for v in PROVINCE_REF.values()}
PROV_TH_TO_ID = {v['th']: k for k, v in PROVINCE_REF.items()}
PROV_TH_TO_CENTROID = {v['th']: (v['lat'], v['lng']) for v in PROVINCE_REF.values()}

CATEGORY_REF = {
    '2': 'ดนตรีและการแสดง',
    '3': 'ภาพยนตร์และสื่อสร้างสรรค์',
    '4': 'เทศกาลและงานประจำปี',
    '5': 'เทศกาลอาหารและวิถีชีวิต',
    '6': 'ศิลปวัฒนธรรมและชาติพันธุ์',
    '7': 'ประเพณีและศาสนา',
    '8': 'นิทรรศการและตลาดวัฒนธรรม',
    '10': 'ศิลปะร่วมสมัยและการถ่ายภาพ',
    '11': 'ศาสนพิธีและการปฏิบัติธรรม',
    '12': 'วรรณกรรม ประวัติศาสตร์และตำนาน',
    '13': 'มรดกภูมิปัญญาทางวัฒนธรรมและประเพณีท้องถิ่น'
}

def clean_html_text(raw_html):
    if not raw_html or pd.isna(raw_html):
        return ''
    # Unescape HTML entities
    text = html.unescape(str(raw_html))
    # Replace <br>, <br/>, <p> with spaces/newlines
    text = re.sub(r'<(br|br\s*/|/p|/div)>', '\n', text, flags=re.IGNORECASE)
    # Strip remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize whitespaces
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join([line for line in lines if line])
    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')
    return text.strip()

def get_age_group(age):
    if pd.isna(age):
        return 'ไม่ระบุ'
    if age < 18:
        return 'เด็กและเยาวชน (<18)'
    elif age <= 35:
        return 'วัยแรงงานตอนต้น (18-35)'
    elif age <= 59:
        return 'วัยแรงงานตอนกลาง (36-59)'
    else:
        return 'ผู้สูงอายุ (60+)'

def get_thai_season(month):
    if month in [3, 4, 5]:
        return 'ฤดูร้อน'
    elif month in [6, 7, 8, 9, 10]:
        return 'ฤดูฝน'
    else:
        return 'ฤดูหนาว'

raw_dir = r'e:\DGA_ALL\DGA_3\group_6\raw'
clean_dir = r'e:\DGA_ALL\DGA_3\group_6\clean'
os.makedirs(clean_dir, exist_ok=True)

print('=== 1. CLEANING SOCIAL CASES ASSISTED ===')
p_cases = os.path.join(raw_dir, 'ผู้ประสบปัญหาทางสังคมที่ได้รับความช่วยเหลือ', 'mso_social_cases_assisted_500.csv')
df_cases = pd.read_csv(p_cases, encoding='utf-8-sig')

# Temporal & SLA derivations
df_cases['birth_date'] = pd.to_datetime(df_cases['birth_date'])
df_cases['request_date'] = pd.to_datetime(df_cases['request_date'])
df_cases['assistance_date'] = pd.to_datetime(df_cases['assistance_date'])
df_cases['close_date'] = pd.to_datetime(df_cases['close_date'])

df_cases['request_year'] = df_cases['request_date'].dt.year
df_cases['request_month'] = df_cases['request_date'].dt.month
df_cases['request_ym'] = df_cases['request_date'].dt.strftime('%Y-%m')

df_cases['assistance_year'] = df_cases['assistance_date'].dt.year
df_cases['assistance_month'] = df_cases['assistance_date'].dt.month
df_cases['assistance_ym'] = df_cases['assistance_date'].dt.strftime('%Y-%m')

df_cases['close_year'] = df_cases['close_date'].dt.year
df_cases['close_month'] = df_cases['close_date'].dt.month
df_cases['close_ym'] = df_cases['close_date'].dt.strftime('%Y-%m')

df_cases['days_to_assistance'] = (df_cases['assistance_date'] - df_cases['request_date']).dt.days
df_cases['days_to_close'] = (df_cases['close_date'] - df_cases['request_date']).dt.days
df_cases['assistance_to_close_days'] = (df_cases['close_date'] - df_cases['assistance_date']).dt.days

# Age & Demographics
df_cases['age_at_request'] = ((df_cases['request_date'] - df_cases['birth_date']).dt.days / 365.25).astype(int)
df_cases['age_group'] = df_cases['age_at_request'].apply(get_age_group)

# Geography
df_cases['region'] = df_cases['province'].map(PROV_TH_TO_REGION).fillna('ไม่ระบุ')
df_cases['province_en'] = df_cases['province'].map(PROV_TH_TO_EN)
df_cases['province_id'] = df_cases['province'].map(PROV_TH_TO_ID)

# Format dates back to standard ISO string
for dcol in ['birth_date', 'request_date', 'assistance_date', 'close_date']:
    df_cases[dcol] = df_cases[dcol].dt.strftime('%Y-%m-%d')

out_cases = os.path.join(clean_dir, 'clean_mso_social_cases.csv')
df_cases.to_csv(out_cases, index=False, encoding='utf-8-sig')
print(f'Saved: {out_cases} (shape: {df_cases.shape})')


print('\n=== 2. CLEANING WELFARE PAYMENTS ===')
p_pay = os.path.join(raw_dir, 'การช่วยเหลือเงินสงเคราะห์', 'mso_welfare_payments_500.csv')
df_pay = pd.read_csv(p_pay, encoding='utf-8-sig')

df_pay['birth_date'] = pd.to_datetime(df_pay['birth_date'])
df_pay['request_date'] = pd.to_datetime(df_pay['request_date'])
df_pay['approval_date'] = pd.to_datetime(df_pay['approval_date'])
df_pay['payment_date'] = pd.to_datetime(df_pay['payment_date'])

df_pay['request_year'] = df_pay['request_date'].dt.year
df_pay['request_month'] = df_pay['request_date'].dt.month
df_pay['request_ym'] = df_pay['request_date'].dt.strftime('%Y-%m')

df_pay['approval_year'] = df_pay['approval_date'].dt.year
df_pay['approval_month'] = df_pay['approval_date'].dt.month
df_pay['approval_ym'] = df_pay['approval_date'].dt.strftime('%Y-%m')

df_pay['payment_year'] = df_pay['payment_date'].dt.year
df_pay['payment_month'] = df_pay['payment_date'].dt.month
df_pay['payment_ym'] = df_pay['payment_date'].dt.strftime('%Y-%m')

df_pay['days_to_approval'] = (df_pay['approval_date'] - df_pay['request_date']).dt.days
df_pay['days_to_payment'] = (df_pay['payment_date'] - df_pay['request_date']).dt.days
df_pay['approval_to_payment_days'] = (df_pay['payment_date'] - df_pay['approval_date']).dt.days

df_pay['age_at_request'] = ((df_pay['request_date'] - df_pay['birth_date']).dt.days / 365.25).astype(int)
df_pay['age_group'] = df_pay['age_at_request'].apply(get_age_group)

# Financial metrics
df_pay['payment_pct'] = np.round((df_pay['paid_amount'] / df_pay['approved_amount']) * 100, 2)
df_pay['unpaid_amount'] = df_pay['approved_amount'] - df_pay['paid_amount']

df_pay['region'] = df_pay['province'].map(PROV_TH_TO_REGION).fillna('ไม่ระบุ')
df_pay['province_en'] = df_pay['province'].map(PROV_TH_TO_EN)
df_pay['province_id'] = df_pay['province'].map(PROV_TH_TO_ID)

for dcol in ['birth_date', 'request_date', 'approval_date', 'payment_date']:
    df_pay[dcol] = df_pay[dcol].dt.strftime('%Y-%m-%d')

out_pay = os.path.join(clean_dir, 'clean_mso_welfare_payments.csv')
df_pay.to_csv(out_pay, index=False, encoding='utf-8-sig')
print(f'Saved: {out_pay} (shape: {df_pay.shape})')


print('\n=== 3. CLEANING NEWBORN CHILD GRANTS ===')
p_grant = os.path.join(raw_dir, 'เด็กแรกเกิด - การจ่ายเงินอุดหนุนเด็กแรกเกิด', 'mso_newborn_child_grant_500.csv')
df_grant = pd.read_csv(p_grant, encoding='utf-8-sig')

df_grant['child_birth_date'] = pd.to_datetime(df_grant['child_birth_date'])
df_grant['application_date'] = pd.to_datetime(df_grant['application_date'])
df_grant['approval_date'] = pd.to_datetime(df_grant['approval_date'])
df_grant['entitlement_start_date'] = pd.to_datetime(df_grant['entitlement_start_date'])
df_grant['payment_date'] = pd.to_datetime(df_grant['payment_date'])

df_grant['child_birth_year'] = df_grant['child_birth_date'].dt.year
df_grant['child_birth_month'] = df_grant['child_birth_date'].dt.month

df_grant['application_year'] = df_grant['application_date'].dt.year
df_grant['application_month'] = df_grant['application_date'].dt.month
df_grant['application_ym'] = df_grant['application_date'].dt.strftime('%Y-%m')

df_grant['payment_year'] = df_grant['payment_date'].dt.year
df_grant['payment_month'] = df_grant['payment_date'].dt.month
df_grant['payment_ym'] = df_grant['payment_date'].dt.strftime('%Y-%m')

df_grant['days_app_to_approval'] = (df_grant['approval_date'] - df_grant['application_date']).dt.days
df_grant['days_app_to_payment'] = (df_grant['payment_date'] - df_grant['application_date']).dt.days
df_grant['child_age_at_application_days'] = (df_grant['application_date'] - df_grant['child_birth_date']).dt.days
df_grant['child_age_at_payment_months'] = np.round((df_grant['payment_date'] - df_grant['child_birth_date']).dt.days / 30.4375, 1)

# Household economics
df_grant['household_total_monthly_income'] = df_grant['household_income_per_capita'] * df_grant['household_member_count']
df_grant['income_bracket'] = pd.cut(
    df_grant['household_income_per_capita'],
    bins=[0, 3000, 6000, 10000, np.inf],
    labels=['ยากจนมาก (<=3,000)', 'ยากจน (3,001-6,000)', 'ปานกลาง (6,001-10,000)', 'สูงกว่าเกณฑ์ (>10,000)']
)

df_grant['region'] = df_grant['province'].map(PROV_TH_TO_REGION).fillna('ไม่ระบุ')
df_grant['province_en'] = df_grant['province'].map(PROV_TH_TO_EN)
df_grant['province_id'] = df_grant['province'].map(PROV_TH_TO_ID)

for dcol in ['child_birth_date', 'application_date', 'approval_date', 'entitlement_start_date', 'payment_date']:
    df_grant[dcol] = df_grant[dcol].dt.strftime('%Y-%m-%d')

out_grant = os.path.join(clean_dir, 'clean_mso_newborn_grants.csv')
df_grant.to_csv(out_grant, index=False, encoding='utf-8-sig')
print(f'Saved: {out_grant} (shape: {df_grant.shape})')


print('\n=== 4. CREATING CITIZEN 360 MASTER PROFILE ===')
# Build 360 view from all citizens across df_cases, df_pay, df_grant
cit_cases = df_cases[['citizen_id', 'first_name', 'last_name', 'gender', 'birth_date', 'province', 'region']].drop_duplicates(subset=['citizen_id'])
cit_pay = df_pay[['citizen_id', 'first_name', 'last_name', 'gender', 'birth_date', 'province', 'region']].drop_duplicates(subset=['citizen_id'])

# Aggregate assistance from cases
cases_agg = df_cases.groupby('citizen_id').agg(
    total_social_cases=('case_id', 'count'),
    problem_types_list=('problem_type', lambda s: '; '.join(sorted(set(s)))),
    target_groups_list=('target_group', lambda s: '; '.join(sorted(set(s)))),
    channels_used=('channel', lambda s: '; '.join(sorted(set(s)))),
    has_emergency_case=('urgency_level', lambda s: int('ฉุกเฉิน' in set(s) or 'เร่งด่วน' in set(s))),
    latest_case_date=('request_date', 'max')
).reset_index()

# Aggregate payments from welfare
pay_agg = df_pay.groupby('citizen_id').agg(
    total_welfare_transactions=('payment_id', 'count'),
    total_approved_amount=('approved_amount', 'sum'),
    total_paid_amount=('paid_amount', 'sum'),
    welfare_types_list=('welfare_type', lambda s: '; '.join(sorted(set(s)))),
    latest_payment_date=('payment_date', 'max')
).reset_index()

# Aggregate guardian roles
guard_agg = df_grant.groupby('guardian_citizen_id').agg(
    total_child_grants_managed=('grant_case_id', 'nunique'),
    total_child_grant_paid=('payment_amount', 'sum'),
    children_count=('child_citizen_id', 'nunique')
).reset_index().rename(columns={'guardian_citizen_id': 'citizen_id'})

# Merge all citizens
base_citizens = pd.concat([cit_cases, cit_pay], ignore_index=True).drop_duplicates(subset=['citizen_id'])
df_c360 = base_citizens.merge(cases_agg, on='citizen_id', how='left')
df_c360 = df_c360.merge(pay_agg, on='citizen_id', how='left')
df_c360 = df_c360.merge(guard_agg, on='citizen_id', how='left')

df_c360['total_social_cases'] = df_c360['total_social_cases'].fillna(0).astype(int)
df_c360['total_welfare_transactions'] = df_c360['total_welfare_transactions'].fillna(0).astype(int)
df_c360['total_approved_amount'] = df_c360['total_approved_amount'].fillna(0)
df_c360['total_paid_amount'] = df_c360['total_paid_amount'].fillna(0)
df_c360['total_child_grants_managed'] = df_c360['total_child_grants_managed'].fillna(0).astype(int)
df_c360['total_child_grant_paid'] = df_c360['total_child_grant_paid'].fillna(0)

# Vulnerability composite index
df_c360['total_aid_received'] = df_c360['total_paid_amount'] + df_c360['total_child_grant_paid']
df_c360['is_multi_program_beneficiary'] = ((df_c360['total_paid_amount'] > 0) & (df_c360['total_child_grant_paid'] > 0)).astype(int)

out_c360 = os.path.join(clean_dir, 'clean_mso_citizen_360.csv')
df_c360.to_csv(out_c360, index=False, encoding='utf-8-sig')
print(f'Saved: {out_c360} (shape: {df_c360.shape})')


print('\n=== 5. CLEANING CULTURE EVENTS (วธ. OPEN DATA) ===')
p_events = os.path.join(raw_dir, 'events.json')
with open(p_events, 'r', encoding='utf-8') as f:
    events_raw = json.load(f)['data']

clean_events = []
DEFAULT_LAT = 13.766913
DEFAULT_LNG = 100.576203

for ev in events_raw:
    pid = int(ev['event_province_id'])
    pref = PROVINCE_REF.get(pid, {'th': 'ไม่ระบุ', 'en': 'Unknown', 'region': 'ไม่ระบุ', 'lat': DEFAULT_LAT, 'lng': DEFAULT_LNG})
    
    cat_ids = [c.strip() for c in str(ev['event_category']).split(',') if c.strip()]
    cat_names = [CATEGORY_REF.get(c, f'หมวด {c}') for c in cat_ids]
    primary_cat = cat_names[0] if cat_names else 'อื่นๆ'
    
    # Dates
    dt_start = pd.to_datetime(ev['event_start'])
    dt_end = pd.to_datetime(ev['event_end'])
    duration = (dt_end - dt_start).total_seconds() / 86400.0
    
    # Coordinates check
    raw_lat = float(ev['event_lat'])
    raw_lng = float(ev['event_lng'])
    is_default = (abs(raw_lat - DEFAULT_LAT) < 0.0001 and abs(raw_lng - DEFAULT_LNG) < 0.0001)
    
    if is_default:
        clean_lat = pref['lat']
        clean_lng = pref['lng']
        coord_source = 'Provincial Centroid (Imputed from Fallback)'
    else:
        clean_lat = raw_lat
        clean_lng = raw_lng
        coord_source = 'Original API Coordinates'
        
    # Text cleaning
    name_th = clean_html_text(ev['event_name_th'])
    name_en = clean_html_text(ev['event_name_en'])
    detail_th = clean_html_text(ev['event_detail_th'])
    detail_en = clean_html_text(ev['event_detail_en'])
    addr_clean = clean_html_text(ev['event_address'])
    ref_clean = clean_html_text(ev['event_ref'])
    
    # Count images
    img_list = [ev.get('event_image'), ev.get('event_image_1'), ev.get('event_image_2'), ev.get('event_image_3'), ev.get('event_image_4'), ev.get('event_image_5')]
    total_imgs = sum(1 for img in img_list if img and pd.notna(img))
    
    clean_events.append({
        'event_id': ev['event_id'],
        'event_category_ids': ','.join(cat_ids),
        'event_categories_th': '; '.join(cat_names),
        'primary_category_th': primary_cat,
        'event_start': ev['event_start'],
        'event_start_date': dt_start.strftime('%Y-%m-%d'),
        'event_start_time': dt_start.strftime('%H:%M:%S'),
        'start_year': dt_start.year,
        'start_month': dt_start.month,
        'start_ym': dt_start.strftime('%Y-%m'),
        'season_th': get_thai_season(dt_start.month),
        'event_end': ev['event_end'],
        'event_end_date': dt_end.strftime('%Y-%m-%d'),
        'event_end_time': dt_end.strftime('%H:%M:%S'),
        'end_year': dt_end.year,
        'end_month': dt_end.month,
        'end_ym': dt_end.strftime('%Y-%m'),
        'duration_days': round(duration, 2),
        'event_ref': ref_clean,
        'event_name_th': name_th,
        'event_name_en': name_en,
        'event_detail_th': detail_th,
        'event_detail_en': detail_en,
        'event_address': addr_clean,
        'event_province_id': pid,
        'province_th': pref['th'],
        'province_en': pref['en'],
        'region': pref['region'],
        'raw_lat': raw_lat,
        'raw_lng': raw_lng,
        'is_default_coords': int(is_default),
        'clean_lat': clean_lat,
        'clean_lng': clean_lng,
        'coord_source': coord_source,
        'active': ev.get('active', '1'),
        'event_image_url': ev.get('event_image', ''),
        'total_images': total_imgs
    })

df_clean_events = pd.DataFrame(clean_events)
out_events = os.path.join(clean_dir, 'clean_culture_events.csv')
df_clean_events.to_csv(out_events, index=False, encoding='utf-8-sig')
print(f'Saved: {out_events} (shape: {df_clean_events.shape})')


print('\n=== 6. BUILDING PROVINCIAL INTEGRATED MASTER ===')
# Aggregate all 77 provinces
records = []
for pid, pref in PROVINCE_REF.items():
    pname = pref['th']
    
    # MSDHS metrics
    p_cases = df_cases[df_cases['province'] == pname]
    p_pay = df_pay[df_pay['province'] == pname]
    p_grant = df_grant[df_grant['province'] == pname]
    p_events = df_clean_events[df_clean_events['province_th'] == pname]
    
    records.append({
        'province_id': pid,
        'province_th': pname,
        'province_en': pref['en'],
        'region': pref['region'],
        'centroid_lat': pref['lat'],
        'centroid_lng': pref['lng'],
        
        # Social Cases
        'total_social_cases': len(p_cases),
        'emergency_cases': len(p_cases[p_cases['urgency_level'].isin(['ฉุกเฉิน', 'เร่งด่วน'])]),
        'avg_days_to_close_case': round(p_cases['days_to_close'].mean(), 1) if len(p_cases) > 0 else np.nan,
        
        # Welfare Payments
        'welfare_payment_count': len(p_pay),
        'total_welfare_approved_amount': p_pay['approved_amount'].sum() if len(p_pay) > 0 else 0,
        'total_welfare_paid_amount': p_pay['paid_amount'].sum() if len(p_pay) > 0 else 0,
        'avg_payment_days': round(p_pay['days_to_payment'].mean(), 1) if len(p_pay) > 0 else np.nan,
        
        # Newborn Grants
        'newborn_grant_count': len(p_grant),
        'total_newborn_grant_paid': p_grant['payment_amount'].sum() if len(p_grant) > 0 else 0,
        'avg_household_income_per_capita': round(p_grant['household_income_per_capita'].mean(), 1) if len(p_grant) > 0 else np.nan,
        'avg_household_members': round(p_grant['household_member_count'].mean(), 1) if len(p_grant) > 0 else np.nan,
        
        # Combined Social Aid
        'total_combined_social_aid': (p_pay['paid_amount'].sum() if len(p_pay) > 0 else 0) + (p_grant['payment_amount'].sum() if len(p_grant) > 0 else 0),
        
        # Culture Events
        'total_culture_events': len(p_events),
        'total_event_days': round(p_events['duration_days'].sum(), 1) if len(p_events) > 0 else 0,
        'has_cultural_events': int(len(p_events) > 0)
    })

df_prov_master = pd.DataFrame(records)
out_prov_master = os.path.join(clean_dir, 'provincial_integrated_master.csv')
df_prov_master.to_csv(out_prov_master, index=False, encoding='utf-8-sig')
print(f'Saved: {out_prov_master} (shape: {df_prov_master.shape})')

print('\nALL 6 CLEAN CSV FILES PRODUCED SUCCESSFULLY!')
