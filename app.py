import streamlit as st
from datetime import datetime

# =========================
# CẤU HÌNH APP
# =========================

st.set_page_config(
    page_title="Tính tiền hóa đơn",
    page_icon="🧾",
    layout="centered"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #e67e22;
    margin-bottom: 25px;
}

.total-box {
    background: #fff3e8;
    border-radius: 12px;
    padding: 20px;
    margin-top: 15px;
    text-align: center;
}

.total-label {
    font-size: 16px;
    color: #555;
}

.total-money {
    font-size: 30px;
    font-weight: bold;
    color: #d35400;
}

.change-box {
    background: #eafaf1;
    border-radius: 12px;
    padding: 15px;
    margin-top: 15px;
    text-align: center;
}

.change-money {
    font-size: 24px;
    font-weight: bold;
    color: #27ae60;
}

</style>
""", unsafe_allow_html=True)


# =========================
# TIÊU ĐỀ
# =========================

st.markdown(
    '<div class="main-title">🧾 TÍNH TIỀN HÓA ĐƠN</div>',
    unsafe_allow_html=True
)


# =========================
# KHỞI TẠO DỮ LIỆU
# =========================

if "products" not in st.session_state:
    st.session_state.products = []


# =========================
# THÊM SẢN PHẨM
# =========================

st.subheader("➕ Thêm sản phẩm")

col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input(
        "Tên sản phẩm",
        placeholder="Ví dụ: Cà phê sữa"
    )

with col2:
    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        value=1,
        step=1
    )

price = st.number_input(
    "Đơn giá (VNĐ)",
    min_value=0,
    value=0,
    step=1000
)


if st.button("➕ THÊM SẢN PHẨM", use_container_width=True):

    if product_name.strip() == "":
        st.error("⚠️ Vui lòng nhập tên sản phẩm.")

    elif price <= 0:
        st.error("⚠️ Vui lòng nhập đơn giá.")

    else:

        st.session_state.products.append({
            "name": product_name.strip(),
            "quantity": quantity,
            "price": price
        })

        st.success("✅ Đã thêm sản phẩm!")

        st.rerun()


# =========================
# DANH SÁCH SẢN PHẨM
# =========================

st.subheader("🛒 Danh sách sản phẩm")


if len(st.session_state.products) == 0:

    st.info("Chưa có sản phẩm nào.")

else:

    for index, product in enumerate(st.session_state.products):

        item_total = (
            product["quantity"] *
            product["price"]
        )

        col1, col2, col3, col4, col5 = st.columns(
            [0.5, 2, 0.8, 1.5, 0.8]
        )

        with col1:
            st.write(index + 1)

        with col2:
            st.write(product["name"])

        with col3:
            st.write(product["quantity"])

        with col4:
            st.write(
                f"{item_total:,.0f} VNĐ"
            )

        with col5:

            if st.button(
                "🗑️",
                key=f"delete_{index}"
            ):

                st.session_state.products.pop(index)

                st.rerun()


# =========================
# TÍNH TIỀN
# =========================

subtotal = 0

for product in st.session_state.products:

    subtotal += (
        product["quantity"] *
        product["price"]
    )


st.divider()


# =========================
# GIẢM GIÁ + VAT
# =========================

col1, col2 = st.columns(2)

with col1:

    discount_percent = st.number_input(
        "Giảm giá (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

with col2:

    vat_percent = st.number_input(
        "VAT (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )


# =========================
# TÍNH TOÁN
# =========================

discount_money = (
    subtotal *
    discount_percent /
    100
)

after_discount = (
    subtotal -
    discount_money
)

vat_money = (
    after_discount *
    vat_percent /
    100
)

total = (
    after_discount +
    vat_money
)


# =========================
# HIỂN THỊ TỔNG
# =========================

st.write(
    f"**Tạm tính:** {subtotal:,.0f} VNĐ"
)

st.write(
    f"**Tiền giảm:** {discount_money:,.0f} VNĐ"
)

st.write(
    f"**Tiền VAT:** {vat_money:,.0f} VNĐ"
)


st.markdown(
    f"""
    <div class="total-box">

        <div class="total-label">
            TỔNG THANH TOÁN
        </div>

        <div class="total-money">
            {total:,.0f} VNĐ
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# THANH TOÁN
# =========================

st.subheader("💵 Thanh toán")

customer_money = st.number_input(
    "Tiền khách đưa (VNĐ)",
    min_value=0,
    value=0,
    step=1000
)


change = customer_money - total


if customer_money > 0:

    if change >= 0:

        st.markdown(
            f"""
            <div class="change-box">

                <div>
                    TIỀN THỪA
                </div>

                <div class="change-money">
                    {change:,.0f} VNĐ
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.error(
            f"❌ Khách còn thiếu "
            f"{abs(change):,.0f} VNĐ"
        )


# =========================
# NÚT XÓA HÓA ĐƠN
# =========================

st.divider()

if st.button(
    "🗑️ XÓA TOÀN BỘ HÓA ĐƠN",
    use_container_width=True
):

    st.session_state.products = []

    st.rerun()


# =========================
# THÔNG TIN HÓA ĐƠN
# =========================

st.caption(
    "Thời gian: "
    + datetime.now().strftime(
        "%d/%m/%Y - %H:%M"
    )
)
