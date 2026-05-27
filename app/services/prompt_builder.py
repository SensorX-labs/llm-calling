# xay dung mau prompt cho AI
class PromptBuilder:
    def _format_number(self, value):
        """Ham ho tro ep kieu va dinh dang so an toan"""
        try:
            if value is None:
                return "0"
            return f"{float(value):,.0f}"
        except (ValueError, TypeError):
            return str(value)

    def build_quotation_prompt(self, data: dict) -> str:
        customer = data.get("customer", {})
        staff = data.get("staff", {})
        quote = data.get("quote", {})
        items = quote.get("items", [])

        total_quotes = customer.get("totalQuotes", 0)
        accepted_quotes = customer.get("acceptedQuotes", 0)
        customer_win_rate = (accepted_quotes / total_quotes * 100) if total_quotes > 0 else 0

        tiers_info = []
        for item in items:
            product_name = item.get("productName", "San pham")
            tiers = item.get("priceTiers", [])
            if tiers:
                tiers_info.append(f"  - {product_name}:")
                for tier in tiers:
                    min_qty = tier.get("minQuantity", 0)
                    price = self._format_number(tier.get("price", 0))
                    tiers_info.append(f"    + SL >= {min_qty}: {price} VND")

        tiers_str = "\n".join(tiers_info) if tiers_info else "  (Khong co thong tin tiers)"

        items_detail = []
        for item in items:
            qty = item.get("quantity", 0)
            quoted_price = item.get("quotedUnitPrice", 0)
            suggested = item.get("suggestedPrice", 0)
            floor = item.get("floorPrice", 0)

            items_detail.append(
                f"  - {item.get('productName')} (Ma: {item.get('productCode')})\n"
                f"    So luong: {qty} {item.get('unit')}\n"
                f"    Gia dang chao: {self._format_number(quoted_price)} VND\n"
                f"    Gia de xuat: {self._format_number(suggested)} VND\n"
                f"    Gia san: {self._format_number(floor)} VND"
            )

        prompt = f"""
Ban la chuyen gia phan tich bao gia B2B.
Muc tieu: danh gia nhanh muc do deal va de xuat hanh dong ngan gon, thuc dung.

QUY TAC BAT BUOC VE DO DAI:
- reasoning toi da 320 ky tu.
- strategy toi da 320 ky tu.
- Moi truong chi viet ngan gon, uu tien 2-3 y chinh.
- Khong viet doan van dai.
- Khong danh so nhieu tang.
- Khong lap lai du lieu da co.

DU LIEU BAO GIA:

1. KHACH HANG
- Ten cong ty: {customer.get('companyName')}
- Nguoi nhan: {customer.get('recipientName') or 'Khong co'}
- Da nhan {total_quotes} bao gia, da chot {accepted_quotes} don
- Ty le chot trong qua khu: {customer_win_rate:.1f}%

2. TONG QUAN BAO GIA
- Ma bao gia: {data.get('quoteCode')}
- Tong gia tri dang chao: {self._format_number(quote.get('totalAmount'))} VND
- Tong so luong san pham: {quote.get('totalQuantity')}
- So loai san pham: {quote.get('itemCount')}
- Ghi chu: {quote.get('note') or 'Khong co'}

3. CHI TIET SAN PHAM VA GIA
{chr(10).join(items_detail)}

4. PRICE TIERS
{tiers_str}

5. NHAN VIEN PHU TRACH
- Ten: {staff.get('staffName')}
- Bo phan: {staff.get('department')}
- Kinh nghiem: {staff.get('tenureYears', 0)} nam

YEU CAU PHAN TICH:
- Chon 1 deal_status:
  - "An toan": gia dang chao >= gia de xuat
  - "Tiem nang": gia dang chao nam giua gia de xuat va gia san
  - "Rui ro": gia sat gia san hoac khach co ty le chot thap
  - "Canh bao": gia dang chao duoi gia san
  - "Upsell": co co hoi day them theo price tier
- reasoning: tom tat 2-3 nguyen nhan quan trong nhat.
- strategy: 2-3 hanh dong ngan, co the lam ngay.

TRA VE DUNG JSON, KHONG GIAI THICH THEM:
- Khong dung markdown.
- Khong them text truoc hoac sau JSON.
- Neu trong reasoning hoac strategy co dau ngoac kep, hay escape dung JSON.
{{
  "deal_status": "An toan | Tiem nang | Rui ro | Canh bao | Upsell",
  "reasoning": "Toi da 320 ky tu, ngan gon va truc tiep.",
  "strategy": "Toi da 320 ky tu, hanh dong ro rang va ngan gon."
}}
"""
        return prompt.strip()
