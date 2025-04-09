
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from amlich_vi import convertSolar2Lunar
from tu_tru_module import tinh_tu_tru

# Map ngũ hành từ Can/Chi
ngu_hanh_map = {
    "Giáp": "Mộc", "Ất": "Mộc",
    "Bính": "Hỏa", "Đinh": "Hỏa",
    "Mậu": "Thổ", "Kỷ": "Thổ",
    "Canh": "Kim", "Tân": "Kim",
    "Nhâm": "Thủy", "Quý": "Thủy",
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc",
    "Thìn": "Thổ", "Tỵ": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ",
    "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"
}

canh_gio = {
    "Tý (23:00-01:00)": 23,
    "Sửu (01:00-03:00)": 1,
    "Dần (03:00-05:00)": 3,
    "Mão (05:00-07:00)": 5,
    "Thìn (07:00-09:00)": 7,
    "Tỵ (09:00-11:00)": 9,
    "Ngọ (11:00-13:00)": 11,
    "Mùi (13:00-15:00)": 13,
    "Thân (15:00-17:00)": 15,
    "Dậu (17:00-19:00)": 17,
    "Tuất (19:00-21:00)": 19,
    "Hợi (21:00-23:00)": 21
}

def pie_chart_nguhanh(data):
    fig, ax = plt.subplots()
    ax.pie(data.values(), labels=data.keys(), autopct="%1.1f%%", startangle=140)
    ax.axis("equal")
    st.pyplot(fig)

def bieu_do_vanhan(title, start_year, hanh_dai_van, color):
    years = list(range(start_year, start_year + len(hanh_dai_van) * 10, 10))
    diem = [8 if hanh in ["Mộc", "Hỏa"] else 5 if hanh == "Thổ" else 2 for hanh in hanh_dai_van]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(years, diem, color=color, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel("Năm")
    ax.set_ylabel("Điểm (thang 10)")
    ax.set_ylim(0, 10)
    ax.grid(True)
    st.pyplot(fig)

def tinh_dai_van(nam_sinh, thang_sinh, gioi_tinh):
    is_nam_am = nam_sinh % 2 != 0
    is_nam = gioi_tinh == "Nam"
    chieu_di = 1 if (is_nam and not is_nam_am) or (not is_nam and is_nam_am) else -1

    thang_can = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    thang_chi = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    can_index = (nam_sinh % 10 + 6) % 10
    chi_index = (thang_sinh - 1) % 12
    can_thang = thang_can[(can_index + thang_sinh - 1) % 10]
    chi_thang = thang_chi[chi_index]

    dai_van = []
    for i in range(10):
        can_i = (thang_can.index(can_thang) + chieu_di * i) % 10
        chi_i = (thang_chi.index(chi_thang) + chieu_di * i) % 12
        hanh = ngu_hanh_map[thang_can[can_i]]
        dai_van.append(hanh)
    return dai_van

st.set_page_config(layout="wide")
st.title("🔮 Xem Mệnh Khuyết & Đại Vận (Không cần thư viện ngoài!)")

st.sidebar.header("📅 Nhập Thông Tin")
ngay_dl = st.sidebar.number_input("Ngày sinh (dương lịch)", 1, 31, 23)
thang_dl = st.sidebar.number_input("Tháng sinh (dương lịch)", 1, 12, 4)
nam_dl = st.sidebar.number_input("Năm sinh (dương lịch)", 1900, 2100, 1992)
gio_sinh_label = st.sidebar.selectbox("Giờ sinh (canh giờ)", list(canh_gio.keys()))
gio_sinh = canh_gio[gio_sinh_label]
gioi_tinh = st.sidebar.radio("Giới tính", ["Nam", "Nữ"])

if st.sidebar.button("🔍 Xem Mệnh Khuyết"):
    try:
        lunar = convertSolar2Lunar(ngay_dl, thang_dl, nam_dl, 7.0)
        ngay_am, thang_am, nam_am = lunar

        tu_tru = tinh_tu_tru(ngay_am, thang_am, nam_am, gio_sinh)
        hanh_dai_van = tinh_dai_van(nam_am, thang_am, gioi_tinh)

        st.subheader("📜 Tứ Trụ Theo Ngày Giờ Sinh")
        st.write(f"**Dương lịch:** {ngay_dl}/{thang_dl}/{nam_dl} – Giờ {gio_sinh_label}")
        st.write(f"**Âm lịch:** {ngay_am}/{thang_am}/{nam_am}")
        for k, v in tu_tru.items():
            st.markdown(f"- **{k}**: {v}")

        ngu_hanh = {"Kim": 0, "Mộc": 0, "Thủy": 0, "Hỏa": 0, "Thổ": 0}
        for tru in tu_tru.values():
            can, chi = tru.split()
            ngu_hanh[ngu_hanh_map[can]] += 1
            ngu_hanh[ngu_hanh_map[chi]] += 1

        st.subheader("📊 Biểu Đồ Ngũ Hành Tứ Trụ")
        pie_chart_nguhanh(ngu_hanh)

        st.subheader("💰 Biểu Đồ Tài Lộc")
        bieu_do_vanhan("Tài Lộc", nam_am + 7, hanh_dai_van, "blue")

        st.subheader("📈 Sự Nghiệp")
        bieu_do_vanhan("Sự Nghiệp", nam_am + 7, hanh_dai_van[::-1], "green")

        st.subheader("❤️ Sức Khỏe")
        bieu_do_vanhan("Sức Khỏe", nam_am + 7, hanh_dai_van, "red")

        st.subheader("🏡 Gia Đạo")
        bieu_do_vanhan("Gia Đạo", nam_am + 7, hanh_dai_van[::-1], "purple")

        st.subheader("👥 Huynh Đệ")
        bieu_do_vanhan("Huynh Đệ", nam_am + 7, hanh_dai_van, "brown")

    except Exception as e:
        st.error(f"Lỗi: {e}")
