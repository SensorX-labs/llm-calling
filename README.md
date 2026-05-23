# 🚀 Quote Analysis Service (LLM-Based)

Dịch vụ phân tích báo giá thông minh sử dụng **9router** theo chuẩn **OpenAI-compatible API**. Hệ thống sử dụng phương pháp **Feature Engineering for LLMs** để đánh giá tỷ lệ chốt đơn (Win Probability) và đưa ra các chỉ dẫn chiến lược cho bộ phận Sales.

## 🛠 Tech Stack
- **Backend:** FastAPI (Python)
- **LLM Gateway:** 9router
- **Validation:** Pydantic V2
- **Config:** Pydantic Settings

## 📥 Cài đặt & Chạy ứng dụng

1. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Cấu hình 9router:**
   Mở file `.env` và cấu hình endpoint 9router:
   ```env
   LLM_API_KEY=your_key_here
   LLM_MODEL=auto
   LLM_API_BASE=http://localhost:3001
   ```

3. **Khởi chạy Server:**
   ```bash
   python -m app.main
   ```
   Server sẽ chạy tại: `http://127.0.0.1:8000`

## 📡 API Endpoints

### 1. Phân tích báo giá chuyên sâu
- **Endpoint:** `POST /api/v1/analyze-quote`
- **Mục tiêu:** Nhận dữ liệu đặc trưng (Features) của báo giá và trả về phân tích từ AI.

#### Request Body (Dữ liệu đầu vào):
Hệ thống yêu cầu 5 nhóm dữ liệu chính:
- **`customer`**: Thông tin hành vi và lịch sử khách hàng.
- **`pricing`**: Các chỉ số về giá, lợi nhuận và tính cạnh tranh.
- **`quote`**: Cấu trúc và độ phức tạp của báo giá.
- **`context`**: Bối cảnh mục tiêu (độ gấp, đối thủ).
- **`sales`**: Năng lực và phong độ của nhân viên kinh doanh.

#### Ví dụ Request:
```json
{
  "customer": {
    "isExisting": true,
    "totalOrders": 12,
    "lastOrderDaysAgo": 30,
    "avgOrderValue": 12000000,
    "paymentBehavior": "on_time",
    "relationshipLevel": "medium"
  },
  "pricing": {
    "totalAmount": 15000000,
    "discountPercent": 5,
    "avgMargin": 12,
    "priceCompetitiveness": "medium"
  },
  "quote": {
    "itemCount": 5,
    "hasAlternativeOptions": true,
    "hasBundle": false,
    "complexity": "low"
  },
  "context": {
    "urgency": "high",
    "competition": true,
    "customerRequestedQuote": true,
    "deadlineDays": 2
  },
  "sales": {
    "experienceYears": 3,
    "winRate": 0.4,
    "recentPerformance": "stable"
  },
  "customerMessage": "Sếp mình đang cần gấp trong tuần!"
}
```

#### Response (Kết quả từ AI):
```json
{
  "status": "success",
  "analysis": {
    "win_probability": "75%",
    "risk_score": "medium",
    "key_insights": ["..."],
    "recommendations": ["..."],
    "suggested_next_step": "..."
  }
}
```

## 🧠 Nguyên tắc Feature cho LLM
Dự án áp dụng nguyên tắc **Semantic Labels**:
- Ưu tiên các nhãn có nghĩa (`high`, `medium`, `low`) thay vì các chỉ số thuần túy.
- Tập trung vào dữ liệu mà AI có thể suy luận logic (Reasoning).
- Loại bỏ các ID và dữ liệu rác không đóng góp vào phân tích.

---
*Created by Antigravity AI Assistant.*
