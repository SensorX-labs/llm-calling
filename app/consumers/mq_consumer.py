import asyncio
import json
import os
import sys
import time
from urllib.parse import urlparse

import pika
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.config import settings
from app.services.analysis_service import AnalysisService

load_dotenv()

_loop = None
_analysis_service = None


def get_service():
    global _analysis_service
    if _analysis_service is None:
        _analysis_service = AnalysisService()
    return _analysis_service


def on_message_received(ch, method, properties, body):
    try:
        print(f"\n[MQ] Nhan duoc tin nhan tu RabbitMQ: {body.decode('utf-8')[:500]}...")
        raw_data = json.loads(body)
        bundle = raw_data.get("message", {})
        print(f"[MQ] Du lieu sau khi boc tach: {json.dumps(bundle, indent=2, ensure_ascii=False)}")

        quote_id = bundle.get("quoteId")
        if not quote_id:
            print(" [!] Bo qua tin nhan: khong tim thay quoteId")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        print(f" [AI] Dang tien hanh phan tich qua LLM cho Quote ID: {quote_id}...")

        service = get_service()
        result = _loop.run_until_complete(service.process_quotation(bundle))

        if result.get("status") == "success":
            print(f" [ok] Phan tich va luu database hoan tat cho ID: {quote_id}")
        else:
            print(f" [x] Phan tich that bai cho ID {quote_id}: {result.get('message')}")

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f" [!] Loi xu ly tin nhan: {e!r}")
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    global _loop
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)

    exchange_name = "quote-analysis-bundle"
    queue_name = "ai_service_analysis_queue"
    retry_seconds = 5

    while True:
        try:
            rabbitmq_url = settings.RABBITMQ_URL
            parameters = pika.URLParameters(rabbitmq_url)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            channel.exchange_declare(exchange=exchange_name, exchange_type="fanout", durable=True)
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(exchange=exchange_name, queue=queue_name)

            print(" [*] Background Consumer da san sang va dang doi tin nhan...")

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=queue_name, on_message_callback=on_message_received)
            channel.start_consuming()
        except Exception as e:
            host = urlparse(settings.RABBITMQ_URL).hostname or "unknown"
            print(
                f" [!] RabbitMQ host '{host}' chua san sang hoac bi ngat ket noi: {e!r}. "
                f"Thu lai sau {retry_seconds} giay..."
            )
            time.sleep(retry_seconds)


if __name__ == "__main__":
    try:
        start_consumer()
    except KeyboardInterrupt:
        print(" [*] Dang dung consumer...")
        sys.exit(0)
