import aio_pika
import asyncio

from aio_pika.abc import AbstractRobustConnection


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f" [x] Получено сообщение: {message.body.decode()}")
        
        print(" [x] Обработка завершена")
        

async def consume(queue_name: str):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    
    try:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(name=queue_name, durable=False)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                try:
                    await process_message(message)
                    
                except Exception as e:
                    print(f"Ошибка: {e}")
        
    finally:
        await connection.close()


async def main():
    print(" [*] Ожидание сообщений. Для выхода Ctrl+C")
    await consume("sent_email")
    

if __name__ == "__main__":
    asyncio.run(main())