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
        quote = data.get('quote', {})
        context = data.get('context', {})
        sales = data.get('sales', {})

        # Xử lý price tiers - từ trong items
        tiers_list = []
        items = quote.get('items', [])
        if items:
            # Lấy price tiers từ item đầu tiên (hoặc có thể loop tất cả items)
            for item in items:
                policy = item.get('policy', {})
                tiers = policy.get('tiers', [])
                for t in tiers:
                    qty = t.get('quantity', 0)
                    price = self._format_number(t.get('price', 0))
                    tiers_list.append(f"  + Số lượng >= {qty}: {price} VNĐ")
        
        tiers_str = chr(10).join(tiers_list) if tiers_list else "  (Không có thông tin tiers)"

        prompt = f"""
          Hãy đóng vai một chuyên gia phân tích kinh doanh cao cấp và cố vấn chiến lược bán hàng. 
          Nhiệm vụ của bạn là phân tích bản báo giá dưới đây và đưa ra dự báo về khả năng thành công (Win Probability) cũng như các lời khuyên thực chiến.

          DỮ LIỆU BÁO GIÁ:

          1. KHÁCH HÀNG:
          - Khách hàng cũ: {'Có' if customer.get('isExisting') else 'Không'}
          - Tổng số đơn đã đặt: {customer.get('totalOrders')} đơn
          - Hành vi thanh toán: {customer.get('paymentBehavior')}
          - Mức độ thân thiết: {customer.get('relationshipLevel')}

          2. GIÁ CẢ & LỢI NHUẬN:
          - Tổng giá trị báo giá (đang chào): {self._format_number(quote.get('totalAmount'))} VNĐ
          - Giá đề xuất hệ thống: {self._format_number(quote.get('totalSuggestedPrice'))} VNĐ
          - Giá sàn tuyệt đối (Floor): {self._format_number(quote.get('totalFloorPrice'))} VNĐ
          - Các mức giá theo số lượng (Price Tiers):
          {tiers_str}
          - Biên lợi nhuận dự kiến: {quote.get('avgMargin')}%
          - Tổng số sản phẩm: {quote.get('totalItemCount')} sản phẩm

          3. CẤU TRÚC BÁO GIÁ:
          - Số lượng hạng mục: {quote.get('itemCount')} mục
          - Độ phức tạp: {quote.get('complexity')}
          - Danh sách sản phẩm:
          {chr(10).join([f"  • {item.get('productName')} x{item.get('quantity')} @ {self._format_number(item.get('quotedPrice'))} VNĐ (lợi nhuận: {item.get('margin')}%)" for item in items])}

          4. NGỮ CẢNH THƯƠNG VỤ:
          - Độ khẩn cấp: {context.get('urgency')}
          - Có đối thủ cạnh tranh: {'Có' if context.get('competition') else 'Không'}
          - Deadline chốt đơn: {context.get('deadlineDays')} ngày
          - Khách hàng yêu cầu báo giá: {'Có' if context.get('customerRequestedQuote') else 'Không'}

          5. NHÂN VIÊN KINH DOANH (SALES):
          - Kinh nghiệm: {sales.get('experienceYears')} năm
          - Tỷ lệ chốt đơn trung bình: {sales.get('winRate') * 100}%
          - Phong độ gần đây: {sales.get('recentPerformance')}

          {'6. TIN NHẮN TỪ KHÁCH HÀNG: "' + data.get('customerMessage') + '"' if data.get('customerMessage') else ''}

          ### Yêu Cầu Phân Tích (Sắc bén & Logic):
          1. Phân loại thương vụ (deal_status) vào 1 trong 4 mốc: An toàn | Rủi ro | Lỗ | Tiềm năng Upsell.
          2. Reasoning: Giải thích ngắn gọn và thuyết phục tại sao lại chọn trạng thái đó (dựa trên: biên lợi nhuận, giá sàn, lịch sử khách hàng, áp lực thời gian, đối thủ cạnh tranh).
          3. Strategy: Đưa ra chiến lược đàm phán cụ thể và cơ hội bán thêm (upsell/bundle) tối ưu nhất để Sales tham khảo.

          Trả về JSON hợp lệ:
          {{
            "deal_status": "An toàn | Rủi ro | Lỗ | Tiềm năng Upsell",
            "reasoning": "đoạn lập luận giải thích nguyên nhân dẫn đến status trên",
            "strategy": "chiến lược đàm phán và upsell"
          }}
          """
        return prompt.strip()
