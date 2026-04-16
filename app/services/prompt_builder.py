# xây dựng mẫu prompt cho AI
class PromptBuilder:
    def build_quotation_prompt(self, data: dict) -> str:
        customer = data.get('customer', {})
        pricing = data.get('pricing', {})
        quote = data.get('quote', {})
        context = data.get('context', {})
        sales = data.get('sales', {})

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
          - Tổng giá trị báo giá (đang chào): {pricing.get('totalAmount'):,} VNĐ
          - Giá đề xuất hệ thống: {pricing.get('suggestedPrice'):,} VNĐ
          - Giá sàn tuyệt đối (Floor): {pricing.get('floorPrice'):,} VNĐ
          - Các mức giá theo số lượng (Price Tiers):
          {chr(10).join([f"  + Số lượng >= {t.get('quantity')}: {t.get('price'):,} VNĐ" for t in pricing.get('priceTiers', [])])}
          - Tỷ lệ chiết khấu: {pricing.get('discountPercent')}%
          - Biên lợi nhuận dự kiến: {pricing.get('avgMargin')}%
          - Khả năng cạnh tranh về giá: {pricing.get('priceCompetitiveness')}

          3. CẤU TRÚC BÁO GIÁ:
          - Số lượng hạng mục: {quote.get('itemCount')} mục
          - Tổng số lượng sản phẩm: {sum([v for v in data.get('quote', {}).values() if isinstance(v, (int, float))])}
          - Có phương án thay thế: {'Có' if quote.get('hasAlternativeOptions') else 'Không'}
          - Có bán kèm (Bundle): {'Có' if quote.get('hasBundle') else 'Không'}
          - Độ phức tạp: {quote.get('complexity')}

          4. NGỮ CẢNH THƯƠNG VỤ:
          - Độ khẩn cấp: {context.get('urgency')}
          - Có đối thủ cạnh tranh: {'Có' if context.get('competition') else 'Không'}
          - Deadline chốt đơn: {context.get('deadlineDays')} ngày

          5. NHÂN VIÊN KINH DOANH (SALES):
          - Kinh nghiệm: {sales.get('experienceYears')} năm
          - Tỷ lệ chốt đơn trung bình: {sales.get('winRate') * 100}%
          - Phong độ gần đây: {sales.get('recentPerformance')}

          {'6. TIN NHẮN TỪ KHÁCH HÀNG: "' + data.get('customerMessage') + '"' if data.get('customerMessage') else ''}

          ### Yêu Cầu Phân Tích (Sắc bén & Logic):
          1. Phân loại thương vụ (deal_status) vào 1 trong 4 mốc: An toàn | Rủi ro | Lỗ | Tiềm năng Upsell.
          2. Reasoning: Giải thích ngắn gọn và thuyết phục tại sao lại chọn trạng thái đó (dựa trên biên lợi nhuận, giá sàn, lịch sử khách hàng hoặc đối thủ).
          3. Strategy: Đưa ra chiến lược đàm phán và cơ hội bán thêm (upsell) tối ưu nhất để Sales tham khảo.

          Trả về JSON:
          {{
            "deal_status": "An toàn | Rủi ro | Lỗ | Tiềm năng Upsell",
            "reasoning": "đoạn lập luận giải thích nguyên nhân dẫn đến status trên",
            "strategy": "chiến lược đàm phán và upsell"
          }}
          """
        return prompt.strip()
