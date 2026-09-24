<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Bill Calculator</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 20px;
            background: #f2f3f5;
            font-family: Arial, sans-serif;
        }

        .app {
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.1);
        }

        h1 {
            text-align: center;
            margin-top: 0;
            color: #e67e22;
        }

        .input-box {
            display: grid;
            grid-template-columns: 2fr 1fr 1.5fr 100px;
            gap: 10px;
            margin-bottom: 20px;
        }

        input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }

        button {
            border: none;
            border-radius: 8px;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 15px;
            font-weight: bold;
        }

        .add {
            background: #e67e22;
            color: white;
        }

        .add:hover {
            background: #d35400;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        th,
        td {
            padding: 12px 8px;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }

        th {
            background: #fff1e6;
            color: #d35400;
        }

        .delete {
            background: #ffdddd;
            color: #c0392b;
        }

        .summary {
            margin-top: 25px;
            background: #f8f8f8;
            padding: 20px;
            border-radius: 10px;
        }

        .row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 12px 0;
        }

        .row input {
            max-width: 150px;
        }

        .total {
            border-top: 2px solid #ddd;
            padding-top: 15px;
            font-size: 22px;
            font-weight: bold;
            color: #e67e22;
        }

        .change {
            color: #27ae60;
            font-weight: bold;
        }

        .print {
            width: 100%;
            margin-top: 20px;
            background: #2c3e50;
            color: white;
        }

        .empty {
            text-align: center;
            color: #999;
            padding: 25px;
        }

        @media (max-width: 650px) {

            .input-box {
                grid-template-columns: 1fr;
            }

            table {
                font-size: 13px;
            }

            th,
            td {
                padding: 8px 3px;
            }

            .summary {
                padding: 15px;
            }
        }

        @media print {

            body {
                background: white;
                padding: 0;
            }

            .app {
                box-shadow: none;
                max-width: 100%;
            }

            .no-print {
                display: none !important;
            }
        }
    </style>
</head>

<body>

<div class="app">

    <h1>🧾 HÓA ĐƠN</h1>

    <!-- NHẬP SẢN PHẨM -->
    <div class="input-box no-print">

        <input
            type="text"
            id="name"
            placeholder="Tên sản phẩm"
        >

        <input
            type="number"
            id="quantity"
            placeholder="Số lượng"
            value="1"
            min="1"
        >

        <input
            type="number"
            id="price"
            placeholder="Đơn giá"
            min="0"
        >

        <button class="add" onclick="addItem()">
            + Thêm
        </button>

    </div>


    <!-- BẢNG HÓA ĐƠN -->
    <table>

        <thead>
            <tr>
                <th>STT</th>
                <th>Sản phẩm</th>
                <th>SL</th>
                <th>Đơn giá</th>
                <th>Thành tiền</th>
                <th class="no-print">Xóa</th>
            </tr>
        </thead>

        <tbody id="bill">

            <tr>
                <td colspan="6" class="empty">
                    Chưa có sản phẩm
                </td>
            </tr>

        </tbody>

    </table>


    <!-- TÍNH TIỀN -->
    <div class="summary">

        <div class="row">
            <span>Tạm tính:</span>
            <strong id="subtotal">0 ₫</strong>
        </div>


        <div class="row no-print">
            <span>Giảm giá (%):</span>

            <input
                type="number"
                id="discount"
                value="0"
                min="0"
                max="100"
                oninput="calculate()"
            >
        </div>


        <div class="row">
            <span>Tiền giảm:</span>
            <strong id="discountMoney">0 ₫</strong>
        </div>


        <div class="row no-print">
            <span>VAT (%):</span>

            <input
                type="number"
                id="vat"
                value="0"
                min="0"
                oninput="calculate()"
            >
        </div>


        <div class="row">
            <span>Tiền VAT:</span>
            <strong id="vatMoney">0 ₫</strong>
        </div>


        <div class="row total">
            <span>TỔNG TIỀN:</span>

            <span id="total">
                0 ₫
            </span>
        </div>


        <!-- KHÁCH ĐƯA -->
        <div class="row no-print">

            <span>Khách đưa:</span>

            <input
                type="number"
                id="customer"
                placeholder="0"
                min="0"
                oninput="calculateChange()"
            >

        </div>


        <!-- TIỀN THỪA -->
        <div class="row">

            <span>Tiền thừa:</span>

            <span
                id="change"
                class="change"
            >
                0 ₫
            </span>

        </div>

    </div>


    <button
        class="print no-print"
        onclick="printBill()"
    >
        🖨️ IN HÓA ĐƠN
    </button>

</div>


<script>

    // ==========================
    // DỮ LIỆU HÓA ĐƠN
    // ==========================

    let items = [];

    let finalTotal = 0;


    // ==========================
    // FORMAT TIỀN
    // ==========================

    function money(number) {

        return Number(number).toLocaleString("vi-VN") + " ₫";

    }


    // ==========================
    // THÊM SẢN PHẨM
    // ==========================

    function addItem() {

        const name =
            document.getElementById("name").value.trim();

        const quantity =
            Number(document.getElementById("quantity").value);

        const price =
            Number(document.getElementById("price").value);


        if (name === "") {

            alert("Vui lòng nhập tên sản phẩm!");

            return;
        }


        if (!quantity || quantity <= 0) {

            alert("Số lượng không hợp lệ!");

            return;
        }


        if (price < 0 || isNaN(price)) {

            alert("Đơn giá không hợp lệ!");

            return;
        }


        items.push({

            name: name,

            quantity: quantity,

            price: price

        });


        // Reset ô nhập

        document.getElementById("name").value = "";

        document.getElementById("quantity").value = 1;

        document.getElementById("price").value = "";


        render();

    }


    // ==========================
    // HIỂN THỊ BILL
    // ==========================

    function render() {

        const bill =
            document.getElementById("bill");


        bill.innerHTML = "";


        if (items.length === 0) {

            bill.innerHTML = `
                <tr>
                    <td colspan="6" class="empty">
                        Chưa có sản phẩm
                    </td>
                </tr>
            `;

            calculate();

            return;
        }


        items.forEach((item, index) => {

            const itemTotal =
                item.quantity * item.price;


            const row =
                document.createElement("tr");


            row.innerHTML = `

                <td>
                    ${index + 1}
                </td>

                <td>
                    ${item.name}
                </td>

                <td>
                    ${item.quantity}
                </td>

                <td>
                    ${money(item.price)}
                </td>

                <td>
                    ${money(itemTotal)}
                </td>

                <td class="no-print">

                    <button
                        class="delete"
                        onclick="removeItem(${index})"
                    >
                        Xóa
                    </button>

                </td>

            `;


            bill.appendChild(row);

        });


        calculate();

    }


    // ==========================
    // XÓA SẢN PHẨM
    // ==========================

    function removeItem(index) {

        items.splice(index, 1);

        render();

    }


    // ==========================
    // TÍNH TỔNG
    // ==========================

    function calculate() {

        let subtotal = 0;


        // Tính tổng sản phẩm

        items.forEach(item => {

            subtotal +=
                item.quantity * item.price;

        });


        // Giảm giá

        let discount =
            Number(
                document.getElementById("discount").value
            ) || 0;


        // VAT

        let vat =
            Number(
                document.getElementById("vat").value
            ) || 0;


        const discountMoney =
            subtotal * discount / 100;


        const afterDiscount =
            subtotal - discountMoney;


        const vatMoney =
            afterDiscount * vat / 100;


        finalTotal =
            afterDiscount + vatMoney;


        // Hiển thị

        document.getElementById("subtotal").textContent =
            money(subtotal);


        document.getElementById("discountMoney").textContent =
            money(discountMoney);


        document.getElementById("vatMoney").textContent =
            money(vatMoney);


        document.getElementById("total").textContent =
            money(finalTotal);


        calculateChange();

    }


    // ==========================
    // TÍNH TIỀN THỪA
    // ==========================

    function calculateChange() {

        const customer =
            Number(
                document.getElementById("customer").value
            ) || 0;


        const change =
            customer - finalTotal;


        const changeElement =
            document.getElementById("change");


        if (customer === 0) {

            changeElement.textContent = "0 ₫";

            return;
        }


        if (change >= 0) {

            changeElement.textContent =
                money(change);

        } else {

            changeElement.textContent =
                "Thiếu " + money(Math.abs(change));

        }

    }


    // ==========================
    // IN HÓA ĐƠN
    // ==========================

    function printBill() {

        if (items.length === 0) {

            alert("Hóa đơn chưa có sản phẩm!");

            return;
        }


        window.print();

    }

</script>

</body>
</html>
