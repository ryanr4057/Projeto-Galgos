import telegram
import asyncio

def mens_telegram(message_text):
    api_token = '6051737713:AAExOZfgQOU3UgeYu9bP7w3Jv7pzED2PQ9k'

    bot = telegram.Bot(api_token)

    chat_id = '-1001725044307'
    # message_text = 'Olá, este é um teste de mensagem enviada pelo bot do Telegram!'


    async def enviar_mensagem():
        await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='Markdown')

    asyncio.run(enviar_mensagem())
