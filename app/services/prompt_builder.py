"""Prompt building service."""
from typing import Dict, List, Optional


class PromptBuilder:
    """Build and format prompts for LLM."""

    def __init__(self):
        """Initialize prompt builder."""
        self.system_prompt: Optional[str] = None
        self.template_vars: Dict[str, str] = {}

    def set_system_prompt(self, prompt: str) -> "PromptBuilder":
        """Set system prompt."""
        self.system_prompt = prompt
        return self

    def add_variables(self, variables: Dict[str, str]) -> "PromptBuilder":
        """Add template variables."""
        self.template_vars.update(variables)
        return self

    def build(self, user_prompt: str) -> str:
        """
        Build final prompt.

        Args:
            user_prompt: User input prompt

        Returns:
            Formatted prompt string
        """
        prompt = user_prompt

        # Substitute template variables
        for key, value in self.template_vars.items():
            prompt = prompt.replace(f"{{{key}}}", value)

        return prompt

    def build_quotation_prompt(self, data: dict) -> str:
        """
        Convert structured quotation JSON to a descriptive prompt.
        """
        customer = data.get("customer", {})
        pricing = data.get("pricing", {})
        quote = data.get("quote", {})
        context = data.get("context", {})
        sales = data.get("sales", {})

        prompt = f"""
Hãy đóng vai một chuyên gia phân tích kinh doanh cao cấp. Dựa trên dữ liệu dưới đây, hãy đánh giá tỷ lệ chốt đơn (Win Probability) và đưa ra các lời khuyên chiến lược.

### THÔNG TIN CHI TIẾT:

1. KHÁCH HÀNG:
- Loại khách: {'Khách cũ' if customer.get('isExisting') else 'Khách mới'}
- Tổng số đơn đã mua: {customer.get('totalOrders')} đơn
- Đơn cuối cùng: {customer.get('lastOrderDaysAgo')} ngày trước
- Giá trị đơn trung bình: {customer.get('avgOrderValue'):,} VNĐ
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
- Tổng số lượng sản phẩm: {sum([v for v in data.get('quote', {}).values() if isinstance(v, (int, float))])} (Lưu ý: Đối chiếu với Price Tiers)
- Có phương án thay thế: {'Có' if quote.get('hasAlternativeOptions') else 'Không'}
- Có bán kèm (Bundle): {'Có' if quote.get('hasBundle') else 'Không'}
- Độ phức tạp: {quote.get('complexity')}

4. BỐI CẢNH (CONTEXT):
- Độ khẩn cấp: {context.get('urgency')}
- Có đối thủ cạnh tranh: {'Có' if context.get('competition') else 'Không'}
- Khách chủ động yêu cầu: {'Có' if context.get('customerRequestedQuote') else 'Không'}
- Hạn chót cần chốt: {context.get('deadlineDays')} ngày

5. NHÂN VIÊN KINH DOANH:
- Kinh nghiệm: {sales.get('experienceYears')} năm
- Tỷ lệ chốt đơn TB: {sales.get('winRate') * 100}%
- Phong độ gần đây: {sales.get('recentPerformance')}

{'6. TIN NHẮN TỪ KHÁCH HÀNG: "' + data.get('customerMessage') + '"' if data.get('customerMessage') else ''}

### Yêu Cầu Phân Tích (Ngắn gọn & Trực diện):
1. Phân tích Negotiation Room dựa trên giá sàn.
2. Kiểm tra Price Tiers và tìm cơ hội Upsell.
3. Chỉ đưa ra tối đa 3 insight quan trọng nhất và 3 hành động thực tế nhất.
4. Tránh viết dài dòng, sử dụng ngôn ngữ quyết đoán.

Trả về JSON:
{{
  "win_probability": "0-100%",
  "risk_score": "low/medium/high",
  "negotiation_room": "ngắn gọn trong 1 câu",
  "upsell_opportunity": "ngắn gọn trong 1 câu (nếu có)",
  "key_insights": ["tối đa 3 ý cực ngắn"],
  "recommendations": ["tối đa 3 hành động cụ thể"],
  "suggested_next_step": "1 hành động duy nhất"
}}
"""
        return prompt.strip()
