<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Tính Tiền Hóa Đơn</title>

    <style>
        * {
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            margin: 0;
            background: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        h1 {
            text-align: center;
            color: #e67e22;
            margin-bottom: 25px;
        }

        .form-row {
            display: grid;
            grid-template-columns: 2fr 1fr 1.5fr auto;
            gap: 10px;
            margin-bottom: 15px;
        }

        input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 15px;
        }

        button {
            border: none;
            padding: 12px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }

        .btn-add {
            background: #e67e22;
            color: white;
        }

        .btn-add:hover {
            background: #d35400;
        }

        .btn-delete {
            background: #ffeded;
            color: #e74c3c;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 12px;
            border-bottom: 1px solid #eee;
            text-align: center;
        }

        th {
            background: #fff3e8;
            color: #d35400;
        }

        .summary {
            margin-top: 25px;
            padding: 20px;
            background: #fafafa;
            border-radius: 10px;
        }

        .summary-row {
            display: flex;
            justify-content: space-between;
            margin: 12px 0;
            font-size: 16px;
        }

        .total {
            font-size: 22px;
            font-weight: bold;
            color: #e67e22;
            border-top: 2px solid #ddd;
            padding-top: 15px;
        }

        .payment {
            margin-top: 20px;
        }

        .payment label {
            display: block;
            margin-bottom: 7px;
            font-weight: bold;
        }

        .change {
            color: #27ae60;
            font-weight: bold;
            font-size: 18px;
        }

        .btn-print {
            width: 100%;
            margin-top: 20px;
            background: #2c3e50;
            color: white;
            font-size: 16px;
        }

        .btn-print:hover {
            background: #1f2d3a;
        }

        @media (max-width: 600px) {
            .form-row {
                grid-template-columns: 1fr;
            }

            table {
                font-size: 13px;
            }

            th, td {
                padding: 8px 4px;
            }
        }

        @media print {
            .no-print {
                display: none;
            }

            body {
                background: white;
                padding: 0;
            }

            .container {
                box-shadow: none;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <h1>🧾 HÓA ĐƠN THANH TOÁN</h1>

    <!-- Nhập sản phẩm -->
    <div class="form-row no-print">

        <input
            type="text"
            id="productName"
            placeholder="Tên sản phẩm"
        >

        <input
            type="number"
            id="quantity"
            placeholder="Số lượng"
            min="1"
            value="1"
        >

        <input
            type="number"
            id="price"
            placeholder="Đơn giá"
            min="0"
        >

        <button class="btn-add" onclick="addProduct()">
            + Thêm
        </button>

    </div>

    <!-- Danh sách sản phẩm -->
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

        <tbody id="billBody">
        </tbody>
    </table>

    <!-- Tổng tiền -->
    <div class="summary">

        <div class="summary-row">
            <span>Tạm tính:</span>
            <strong id="subtotal">0 ₫</strong>
        </div>

        <div class="summary-row no-print">
            <label>
                Giảm giá (%):
                <input
                    type="number"
                    id="discount"
                    value="0"
                    min="0"
                    max="100"
                    oninput="calculateTotal()"
                >
            </label>
        </div>

        <div class="summary-row">
            <span>Tiền giảm:</span>
            <strong id="discountMoney">0 ₫</strong>
        </div>

        <div class="summary-row no-print">
            <label>
                VAT (%):
                <input
                    type="number"
                    id="vat"
                    value="0"
                    min="0"
                    oninput="calculateTotal()"
                >
            </label>
        </div>

        <div class="summary-row">
            <span>Tiền VAT:</span>
            <strong id="vatMoney">0 ₫</strong>
        </div>

        <div class="summary-row total">
            <span>TỔNG TIỀN:</span>
            <span id="total">0 ₫</span>
        </div>

        <!-- Thanh toán -->
        <div class="payment no-print">

            <label>Tiền khách đưa:</label>

            <input
                type="number"
                id="customerMoney"
                placeholder="Nhập số tiền khách đưa"
                min="0"
                oninput="calculateChange()"
            >

            <div class="summary-row">
                <span>Tiền thừa:</span>
                <span class="change" id="change">
                    0 ₫
                </span>
            </div>

        </div>

    </div>

    <button class="btn-print no-print" onclick="printBill()">
        🖨️ In hóa đơn
    </button>

</div>


<script>

    // Danh sách sản phẩm
    let products = [];


    // Thêm sản phẩm
    function addProduct() {

        const name = document.getElementById("productName").value.trim();

        const quantity =
            Number(document.getElementById("quantity").value);

        const price =
            Number(document.getElementById("price").value);


        if (name === "") {
            alert("Vui lòng nhập tên sản phẩm!");
            return;
        }

        if (quantity <= 0) {
            alert("Số lượng phải lớn hơn 0!");
            return;
        }

        if (price < 0) {
            alert("Đơn giá không hợp lệ!");
            return;
        }


        products.push({
            name: name,
            quantity: quantity,
            price: price
        });


        // Xóa ô nhập
        document.getElementById("productName").value = "";
        document.getElementById("quantity").value = 1;
        document.getElementById("price").value = "";


        renderBill();
    }


    // Hiển thị hóa đơn
    function renderBill() {

        const billBody =
            document.getElementById("billBody");

        billBody.innerHTML = "";


        products.forEach((product, index) => {

            const total =
                product.quantity * product.price;


            const row = document.createElement("tr");


            row.innerHTML = `
                <td>${index + 1}</td>

                <td>${product.name}</td>

                <td>${product.quantity}</td>

                <td>${formatMoney(product.price)}</td>

                <td>${formatMoney(total)}</td>

                <td class="no-print">
                    <button
                        class="btn-delete"
                        onclick="deleteProduct(${index})">
                        Xóa
                    </button>
                </td>
            `;


            billBody.appendChild(row);

        });


        calculateTotal();
    }


    // Xóa sản phẩm
    function deleteProduct(index) {

        products.splice(index, 1);

        renderBill();
    }


    // Tính tổng
    function calculateTotal() {

        let subtotal = 0;


        products.forEach(product => {

            subtotal +=
                product.quantity * product.price;

        });


        const discountPercent =
            Number(document.getElementById("discount").value) || 0;


        const vatPercent =
            Number(document.getElementById("vat").value) || 0;


        // Tiền giảm
        const discountMoney =
            subtotal * discountPercent / 100;


        // Sau giảm giá
        const afterDiscount =
            subtotal - discountMoney;


        // VAT
        const vatMoney =
            afterDiscount * vatPercent / 100;


        // Tổng cuối
        const total =
            afterDiscount + vatMoney;


        document.getElementById("subtotal").innerText =
            formatMoney(subtotal);


        document.getElementById("discountMoney").innerText =
            formatMoney(discountMoney);


        document.getElementById("vatMoney").innerText =
            formatMoney(vatMoney);


        document.getElementById("total").innerText =
            formatMoney(total);


        calculateChange();
    }


    // Tính tiền thừa
    function calculateChange() {

        const totalText =
            document.getElementById("total").innerText
                .replace(/[^\d]/g, "");


        const total =
            Number(totalText) || 0;


        const customerMoney =
            Number(
                document.getElementById("customerMoney").value
            ) || 0;


        const change =
            customerMoney - total;


        if (change >= 0) {

            document.getElementById("change").innerText =
                formatMoney(change);

        } else {

            document.getElementById("change").innerText =
                "Thiếu " + formatMoney(Math.abs(change));

        }

    }


    // Định dạng tiền Việt Nam
    function formatMoney(number) {

        return new Intl.NumberFormat("vi-VN", {
            style: "currency",
            currency: "VND"
        }).format(number);

    }


    // In hóa đơn
    function printBill() {

        if (products.length === 0) {

            alert("Chưa có sản phẩm trong hóa đơn!");

            return;
        }

        window.print();
    }

</script>

</body>
</html>
