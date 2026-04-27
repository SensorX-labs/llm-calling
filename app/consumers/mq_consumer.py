import pika
import json
import asyncio
import sys
import os
from dotenv import load_dotenv

# Thêm root dự án vào sys.path để có thể import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.analysis_service import AnalysisService

# Load biến môi trường từ .env
load_dotenv()

# Biến toàn cục để giữ loop và service
_loop = None
_analysis_service = None

def get_service():
    """Đảm bảo service được khởi tạo đúng trong loop hiện tại"""
    global _analysis_service
    if _analysis_service is None:
        _analysis_service = AnalysisService()
    return _analysis_service

def on_message_received(ch, method, properties, body):
    # 1. Giải mã JSON từ RabbitMQ
    try:
        print(f"\n[MQ] Nhận được tin nhắn thô từ RabbitMQ: {body.decode('utf-8')[:500]}...") 
        raw_data = json.loads(body)
        
        # 2. Lấy dữ liệu thực tế (MassTransit wrap dữ liệu trong field "message")
        bundle = raw_data.get("message", {})
        print(f"[MQ] Dữ liệu thực tế bóc tách (Bundle): {json.dumps(bundle, indent=2, ensure_ascii=False)}")
        
        quote_id = bundle.get("quoteId")
        if not quote_id:
            print(" [!] Bỏ qua tin nhắn: Không tìm thấy quoteId")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        print(f" [AI] Đang tiến hành phân tích qua LLM cho Quote ID: {quote_id}...")
        
        # Sử dụng loop duy nhất đã khởi tạo ở start_consumer
        service = get_service()
        result = _loop.run_until_complete(service.process_quotation(bundle))
        
        if result.get("status") == "success":
            print(f" [ok] Phân tích và lưu database hoàn tất cho ID: {quote_id}")
        else:
            print(f" [x] Phân tích thất bại cho ID {quote_id}: {result.get('message')}")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f" [!] Lỗi xử lý tin nhắn: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    global _loop
    # Khởi tạo một asyncio loop duy nhất cho thread này
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)

    # Cấu hình kết nối RabbitMQ
    try:
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        EXCHANGE_NAME = 'quote-analysis-bundle'
        QUEUE_NAME = 'ai_service_analysis_queue'

        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout', durable=True)
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME)

        print(' [*] Background Consumer đã sẵn sàng và đang đợi tin nhắn...')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message_received)
        channel.start_consuming()
    except Exception as e:
        print(f" [!] Không thể khởi động Consumer: {e}")

if __name__ == "__main__":
    try:
        start_consumer()
    except KeyboardInterrupt:
        print(' [*] Đang dừng consumer...')
        sys.exit(0)
