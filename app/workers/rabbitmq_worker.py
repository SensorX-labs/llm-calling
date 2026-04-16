import json
import asyncio
import aio_pika
from app.core.config import settings
from app.services.analysis_service import AnalysisService

async def start_worker():
    """
    Worker lắng nghe RabbitMQ để tự động phân tích báo giá.
    """
    analysis_service = AnalysisService()
    
    # 1. Kết nối RabbitMQ
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    
    async with connection:
        # 2. Tạo channel
        channel = await connection.channel()
        
        # 3. Khai báo Queue
        queue = await channel.declare_queue(settings.RABBITMQ_QUEUE, durable=True)
        
        print(f" [*] Đang lắng nghe trên queue: {settings.RABBITMQ_QUEUE}")

        # 4. Callback khi có tin nhắn
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        print(f" [v] Nhận được yêu cầu phân tích mới...")
                        data = json.loads(message.body.decode())
                        
                        # Gọi Service xử lý (Đã bao gồm lưu DB)
                        result = await analysis_service.process_quotation(data)
                        
                        if result["status"] == "success":
                            print(f" [ok] Đã phân tích xong cho Quote ID: {data.get('quoteId')}")
                        else:
                            print(f" [error] Lỗi: {result.get('message')}")
                            
                    except Exception as e:
                        print(f" [!] Lỗi xử lý message: {str(e)}")

if __name__ == "__main__":
    asyncio.run(start_worker())
