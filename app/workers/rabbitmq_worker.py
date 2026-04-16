import json
import asyncio
import aio_pika
from app.core.config import settings
from app.services.analysis_service import AnalysisService

async def start_worker():
    # lắng nghe rabbitmq để xử lý tự động
    analysis_service = AnalysisService()
    
    # kết nối broker
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    
    async with connection:
        channel = await connection.channel()
        # khai báo queue nhận tin
        queue = await channel.declare_queue(settings.RABBITMQ_QUEUE, durable=True)
        
        print(f" [*] lắng nghe trên: {settings.RABBITMQ_QUEUE}")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        print(f" [v] nhận dữ liệu mới...")
                        data = json.loads(message.body.decode())
                        
                        # gọi service phân tích
                        result = await analysis_service.process_quotation(data)
                        
                        if result["status"] == "success":
                            print(f" [ok] hoàn thành id: {data.get('quoteId')}")
                        else:
                            print(f" [error] lỗi: {result.get('message')}")
                            
                    except Exception as e:
                        print(f" [!] lỗi message: {str(e)}")

if __name__ == "__main__":
    asyncio.run(start_worker())
