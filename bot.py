import telegram
import asyncio

def mens_telegram(message_text):
    api_token = '6051737713:AAExOZfgQOU3UgeYu9bP7w3Jv7pzED2PQ9k'

    bot = telegram.Bot(api_token)

    chat_id = '-1001748518612'
    # message_text = 'Olá, este é um teste de mensagem enviada pelo bot do Telegram!'


    async def enviar_mensagem():
        await bot.send_message(chat_id=chat_id, text=message_text)

    asyncio.run(enviar_mensagem())
