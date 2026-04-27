# xây dựng mẫu prompt cho AI
class PromptBuilder:
    def _format_number(self, value):
        """Hàm hỗ trợ ép kiểu và định dạng số an toàn"""
        try:
            if value is None: return "0"
            return f"{float(value):,.0f}"
        except (ValueError, TypeError):
            return str(value)

    def build_quotation_prompt(self, data: dict) -> str:
        customer = data.get('customer', {})
        staff = data.get('staff', {})
        quote = data.get('quote', {})
        items = quote.get('items', [])

        # Tính toán Win Rate của khách hàng dựa trên lịch sử
        total_quotes = customer.get('totalQuotes', 0)
        accepted_quotes = customer.get('acceptedQuotes', 0)
        customer_win_rate = (accepted_quotes / total_quotes * 100) if total_quotes > 0 else 0

        # Xử lý price tiers từ items
        tiers_info = []
        for item in items:
            p_name = item.get('productName', 'Sản phẩm')
            tiers = item.get('priceTiers', [])
            if tiers:
                tiers_info.append(f"  • {p_name}:")
                for t in tiers:
                    min_qty = t.get('minQuantity', 0)
                    price = self._format_number(t.get('price', 0))
                    tiers_info.append(f"    + SL >= {min_qty}: {price} VNĐ")
        
        tiers_str = "\n".join(tiers_info) if tiers_info else "  (Không có thông tin Tiers)"

        # Danh sách sản phẩm chi tiết
        items_detail = []
        for item in items:
            qty = item.get('quantity', 0)
            quoted_price = item.get('quotedUnitPrice', 0)
            suggested = item.get('suggestedPrice', 0)
            floor = item.get('floorPrice', 0)
            
            items_detail.append(
                f"  • {item.get('productName')} (Mã: {item.get('productCode')})\n"
                f"    - Số lượng: {qty} {item.get('unit')}\n"
                f"    - Giá đang chào: {self._format_number(quoted_price)} VNĐ\n"
                f"    - Giá đề xuất: {self._format_number(suggested)} VNĐ\n"
                f"    - Giá sàn: {self._format_number(floor)} VNĐ"
            )

        prompt = f"""
          Hãy đóng vai một chuyên gia phân tích kinh doanh (Business Analyst) và cố vấn chiến lược bán hàng. 
          Nhiệm vụ của bạn là phân tích bản báo giá dưới đây và đưa ra dự báo về khả năng chốt đơn thành công cũng như các lời khuyên thực chiến.

          DỮ LIỆU BÁO GIÁ CHI TIẾT:

          1. THÔNG TIN KHÁCH HÀNG:
          - Tên: {customer.get('companyName')} (Người nhận: {customer.get('recipientName')})
          - Lịch sử giao dịch: Đã nhận {total_quotes} báo giá, đã chốt {accepted_quotes} đơn.
          - Tỷ lệ chốt đơn trong quá khứ: {customer_win_rate:.1f}%

          2. TỔNG QUAN BÁO GIÁ:
          - Mã báo giá: {data.get('quoteCode')}
          - Tổng giá trị (đang chào): {self._format_number(quote.get('totalAmount'))} VNĐ
          - Tổng số lượng sản phẩm: {quote.get('totalQuantity')}
          - Số loại sản phẩm: {quote.get('itemCount')} mục
          - Ghi chú: {quote.get('note') or "Không có"}

          3. CHI TIẾT SẢN PHẨM & GIÁ:
          {chr(10).join(items_detail)}

          4. CHÍNH SÁCH GIÁ THEO SỐ LƯỢNG (PRICE TIERS):
          {tiers_str}

          5. NHÂN VIÊN PHỤ TRÁCH:
          - Tên: {staff.get('staffName')}
          - Bộ phận: {staff.get('department')}
          - Kinh nghiệm: {staff.get('tenureYears', 0)} năm

          ### YÊU CẦU PHÂN TÍCH:
          Dựa trên sự chênh lệch giữa "Giá đang chào" so với "Giá đề xuất" và "Giá sàn", cùng với lịch sử của khách hàng, hãy thực hiện:

          1. Phân loại trạng thái (deal_status):
             - "An toàn": Giá đang chào >= Giá đề xuất.
             - "Tiềm năng": Giá đang chào nằm giữa Giá đề xuất và Giá sàn.
             - "Rủi ro": Giá đang chào sát Giá sàn hoặc khách hàng có tỷ lệ chốt đơn thấp.
             - "Cảnh báo": Giá đang chào dưới Giá sàn.
             - "Upsell": Nếu khách hàng mua số lượng lớn nhưng chưa đạt mức Tier tiếp theo.

          2. Reasoning (Lập luận): Giải thích lý do chọn trạng thái trên (phân tích sâu về giá và biên độ an toàn).
          3. Strategy (Chiến lược): 
             - Nếu giá cao: Cách thuyết phục khách hàng về giá trị.
             - Nếu giá thấp: Cách bảo vệ biên lợi nhuận.
             - Gợi ý Upsell/Cross-sell dựa trên Price Tiers nếu khả thi.

          TRẢ VỀ KẾT QUẢ DƯỚI ĐỊNH DẠNG JSON:
          {{
            "deal_status": "An toàn | Tiềm năng | Rủi ro | Cảnh báo | Upsell",
            "reasoning": "Chuỗi văn bản giải thích...",
            "strategy": "Chuỗi văn bản gợi ý hành động cụ thể..."
          }}
          """
        return prompt.strip()
