
from datetime import datetime
from math import floor

# Danh sách Can Chi
THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# Can chi của năm
def can_chi_nam(nam):
    can = THIEN_CAN[(nam + 6) % 10]
    chi = DIA_CHI[(nam + 8) % 12]
    return f"{can} {chi}"

# Can chi của tháng theo Can năm và tháng âm lịch (dự kiến người dùng sẽ cung cấp tháng âm)
def can_chi_thang(nam_can_index, thang_am):
    can_index = (nam_can_index * 2 + thang_am - 2) % 10
    chi_index = (thang_am + 1) % 12
    return f"{THIEN_CAN[can_index]} {DIA_CHI[chi_index]}"

# Can chi của giờ dựa vào can ngày và giờ địa chi
def can_chi_gio(can_ngay_index, gio_chi_index):
    can_index = (can_ngay_index * 2 + gio_chi_index) % 10
    return f"{THIEN_CAN[can_index]} {DIA_CHI[gio_chi_index]}"

# Tính can chi của ngày (sử dụng thuật toán lịch vạn niên)
def jd_from_date(dd, mm, yy):
    a = int((14 - mm) / 12)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + int((153 * m + 2) / 5) + 365 * y + int(y / 4) - int(y / 100) + int(y / 400) - 32045
    return jd

def can_chi_ngay(dd, mm, yy):
    jd = jd_from_date(dd, mm, yy)
    can = THIEN_CAN[(jd + 9) % 10]
    chi = DIA_CHI[(jd + 1) % 12]
    return f"{can} {chi}", (jd + 9) % 10  # Trả thêm chỉ số Can để tính giờ

# Can Chi Giờ dựa vào giờ sinh
def gio_chi_index_from_hour(hour):
    gio_chi_ranges = [(23,1), (1,3), (3,5), (5,7), (7,9), (9,11), (11,13), (13,15), (15,17), (17,19), (19,21), (21,23)]
    for idx, (start, end) in enumerate(gio_chi_ranges):
        if start <= hour < end or (start == 23 and hour == 23):
            return idx
    return 0  # Default Tý

def tinh_tu_tru(ngay, thang, nam, gio):
    can_chi_n = can_chi_nam(nam)
    nam_can_index = (nam + 6) % 10
    thang_am = thang  # giả sử tháng âm trùng tháng dương
    can_chi_t = can_chi_thang(nam_can_index, thang_am)
    can_chi_d, can_ngay_index = can_chi_ngay(ngay, thang, nam)
    gio_chi_index = gio_chi_index_from_hour(gio)
    can_chi_g = can_chi_gio(can_ngay_index, gio_chi_index)
    return {
        "Năm": can_chi_n,
        "Tháng": can_chi_t,
        "Ngày": can_chi_d,
        "Giờ": can_chi_g
    }
