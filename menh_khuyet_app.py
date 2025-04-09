
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from tu_tru_module import tinh_tu_tru
from lunardate import LunarDate

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

def pie_chart_nguhanh(data):
    fig, ax = plt.subplots()
    ax.pie(data.values(), labels=data.keys(), autopct="%1.1f%%", startangle=140)
    ax.axis("equal")
    st.pyplot(fig)

def bieu_do_vanhan(title, start_year, hanh_dai_van, color):
    years = list(range(start_year + 7, start_year + 103))
    diem = []
    for hanh in hanh_dai_van:
        if hanh in ["Mộc", "Hỏa"]:
            diem.append(8)
        elif hanh == "Thổ":
            diem.append(5)
        else:
            diem.append(2)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(years, diem, color=color, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel("Năm")
    ax.set_ylabel("Điểm (thang 10)")
    ax.set_ylim(0, 10)
    ax.grid(True)
    st.pyplot(fig)

st.set_page_config(layout="wide")
st.title("🔮 Xem Mệnh Khuyết & Lá Số Tứ Trụ (Âm Lịch CHUẨN)")

st.sidebar.header("📅 Nhập Thông Tin")
ngay_dl = st.sidebar.number_input("Ngày sinh (dương lịch)", 1, 31, 21)
thang_dl = st.sidebar.number_input("Tháng sinh (dương lịch)", 1, 12, 9)
nam_dl = st.sidebar.number_input("Năm sinh (dương lịch)", 1900, 2100, 1999)
gio_sinh = st.sidebar.slider("Giờ sinh (24h)", 0, 23, 14)

if st.sidebar.button("🔍 Xem Mệnh Khuyết"):
    # Chuyển dương lịch ➜ âm lịch
    try:
        lunar = LunarDate.fromSolarDate(nam_dl, thang_dl, ngay_dl)
        ngay_am, thang_am, nam_am = lunar.day, lunar.month, lunar.year

        tu_tru = tinh_tu_tru(ngay_am, thang_am, nam_am, gio_sinh)

        st.subheader("📜 Tứ Trụ Theo Ngày Giờ Sinh (Âm lịch)")
        st.write(f"**Dương lịch:** {ngay_dl}/{thang_dl}/{nam_dl} – Giờ {gio_sinh}:00")
        st.write(f"**Âm lịch:** {ngay_am}/{thang_am}/{nam_am}")
        for k, v in tu_tru.items():
            st.markdown(f"- **{k}**: {v}")

        # Phân tích ngũ hành
        ngu_hanh = {"Kim": 0, "Mộc": 0, "Thủy": 0, "Hỏa": 0, "Thổ": 0}
        for tru in tu_tru.values():
            can, chi = tru.split()
            ngu_hanh[ngu_hanh_map[can]] += 1
            ngu_hanh[ngu_hanh_map[chi]] += 1

        st.subheader("📊 Biểu Đồ Ngũ Hành Tứ Trụ")
        pie_chart_nguhanh(ngu_hanh)

        hanh_van = ["Mộc"]*20 + ["Hỏa"]*20 + ["Thổ"]*20 + ["Kim"]*20 + ["Thủy"]*16

        st.subheader("💰 Biểu Đồ Tài Lộc (theo năm sinh)")
        bieu_do_vanhan("Tài Lộc", nam_am, hanh_van, "blue")

        st.subheader("📈 Sự Nghiệp")
        bieu_do_vanhan("Sự Nghiệp", nam_am, hanh_van, "green")

        st.subheader("❤️ Sức Khỏe")
        bieu_do_vanhan("Sức Khỏe", nam_am, hanh_van, "red")

        st.subheader("🏡 Gia Đạo")
        bieu_do_vanhan("Gia Đạo", nam_am, hanh_van, "purple")

        st.subheader("👥 Huynh Đệ")
        bieu_do_vanhan("Huynh Đệ", nam_am, hanh_van, "brown")
    except Exception as e:
        st.error(f"Lỗi chuyển đổi âm lịch: {e}")
