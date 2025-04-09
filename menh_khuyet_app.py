
# menh_khuyet_app.py (phiên bản có nút Submit và cập nhật động)
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
st.title("🔮 Phần Mềm Xem Mệnh Khuyết & Biểu Đồ Vận Hạn 96 Năm")

# --- Nhập liệu
st.sidebar.header("📅 Nhập Thông Tin Ngày Giờ Sinh")
ngay = st.sidebar.number_input("Ngày sinh", 1, 31, 21)
thang = st.sidebar.number_input("Tháng sinh", 1, 12, 9)
nam = st.sidebar.number_input("Năm sinh", 1900, 2100, 1999)
gio = st.sidebar.selectbox("Giờ sinh", 
    ["Tý (23h-1h)", "Sửu (1h-3h)", "Dần (3h-5h)", "Mão (5h-7h)", "Thìn (7h-9h)",
     "Tỵ (9h-11h)", "Ngọ (11h-13h)", "Mùi (13h-15h)", "Thân (15h-17h)", "Dậu (17h-19h)", 
     "Tuất (19h-21h)", "Hợi (21h-23h)"])
gioi_tinh = st.sidebar.radio("Giới tính", ["Nam", "Nữ"])

if st.sidebar.button("🔍 Xem Mệnh Khuyết"):
    # --- Ngũ hành giả lập từ ngày giờ năm sinh
    ngu_hanh = {
        "Kim": 1,
        "Mộc": 2,
        "Thủy": 2,
        "Hỏa": 1,
        "Thổ": 2
    }

    # --- Biểu đồ Pie Ngũ Hành
    def pie_chart_nguhanh(data):
        fig, ax = plt.subplots()
        ax.pie(data.values(), labels=data.keys(), autopct="%1.1f%%", startangle=140)
        ax.axis("equal")
        st.pyplot(fig)

    # --- Biểu đồ vận hạn theo năm
    def bieu_do_vanhan(title, hanh_dai_van, color):
        years = list(range(2006, 2102))
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

    # --- Hành đại diện theo từng năm từ 2006–2101 (96 năm)
    hanh_van = ["Mộc"]*20 + ["Hỏa"]*20 + ["Thổ"]*20 + ["Kim"]*20 + ["Thủy"]*16

    # --- PHÂN TÍCH TỔNG QUAN
    st.header("🔎 Phân Tích Tổng Quan Mệnh Khuyết")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Tứ Trụ Giả Lập (Can Chi từ dữ liệu mẫu)")
        st.write(f"**Ngày sinh:** {ngay}/{thang}/{nam}")
        st.write(f"**Giờ sinh:** {gio}")
        st.write("**Năm:** Kỷ Mão (Thổ – Mộc)")
        st.write("**Tháng:** Quý Dậu (Thủy – Kim)")
        st.write("**Ngày:** Bính Tí (Hỏa – Thủy)")
        st.write("**Giờ:** Ất Mùi (Mộc – Thổ)")
    with col2:
        st.markdown("### Mệnh Khuyết & Dụng Thần")
        st.write("🔺 **Dụng Thần:** Hỏa")
        st.write("🌿 **Hỷ Thần:** Mộc")
        st.write("⛔ **Nên tránh:** Kim và Thủy")
        st.write("🎨 **Màu hợp:** Đỏ, cam, hồng, tím, xanh lá")
        st.write("🧭 **Hướng tốt:** Nam, Đông Nam")

    st.markdown("---")
    st.subheader("📊 Biểu Đồ Pie Ngũ Hành Tứ Trụ")
    pie_chart_nguhanh(ngu_hanh)

    st.markdown("---")
    st.subheader("💰 Biểu Đồ Tài Lộc (96 năm)")
    bieu_do_vanhan("Tài Lộc Từng Năm", hanh_van, "blue")

    st.subheader("📈 Biểu Đồ Sự Nghiệp (96 năm)")
    bieu_do_vanhan("Sự Nghiệp Từng Năm", hanh_van, "green")

    st.subheader("❤️ Biểu Đồ Sức Khỏe (96 năm)")
    bieu_do_vanhan("Sức Khỏe Từng Năm", hanh_van, "red")

    st.subheader("🏠 Biểu Đồ Gia Đạo (96 năm)")
    bieu_do_vanhan("Gia Đạo Từng Năm", hanh_van, "purple")

    st.subheader("👥 Biểu Đồ Huynh Đệ (96 năm)")
    bieu_do_vanhan("Huynh Đệ Từng Năm", hanh_van, "brown")
