import telegram
import asyncio
import f_busca as fbd
import funções_ as f
from tabulate import tabulate
tabulate.PRESERVE_WHITESPACE = True
from texttable import Texttable
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import io


def mens_telegram(message_text):
    api_token = '6051737713:AAExOZfgQOU3UgeYu9bP7w3Jv7pzED2PQ9k'

    bot = telegram.Bot(api_token)

    chat_id = '-1001725044307'
    # message_text = 'Olá, este é um teste de mensagem enviada pelo bot do Telegram!'


    async def enviar_mensagem():
        await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='Markdown')

    asyncio.run(enviar_mensagem())

def mens_telegram_ia(message_text):
    api_token = '6051737713:AAExOZfgQOU3UgeYu9bP7w3Jv7pzED2PQ9k'

    bot = telegram.Bot(api_token)

    chat_id = '-1001896788559'
    # message_text = 'Olá, este é um teste de mensagem enviada pelo bot do Telegram!'


    async def enviar_mensagem():
        await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='Markdown')

    asyncio.run(enviar_mensagem())

def mens_telegram_ia_ft(buffer,text):
    api_token = '6051737713:AAExOZfgQOU3UgeYu9bP7w3Jv7pzED2PQ9k'

    bot = telegram.Bot(api_token)

    chat_id = '-1001896788559'
    # message_text = 'Olá, este é um teste de mensagem enviada pelo bot do Telegram!'


    async def enviar_mensagem():
        await bot.send_photo(chat_id=chat_id, photo=buffer.getvalue(),caption=text, parse_mode='Markdown')

    asyncio.run(enviar_mensagem())



def cria_mens(odd, vencedor, risco, a, b, race_id):
    d_dogs_a, d_dogs_b, venc = f.compara_av(race_id, a, b)

    horario = fbd.buscar_race_h(race_id[0])
    nome = fbd.buscar_race_nome(race_id[0])
    pista_id = fbd.buscar_race_pis(race_id[0])
    pista_nome = fbd.buscar_pista_nome(pista_id[0])
    r_dist = fbd.buscar_race_dist(race_id)
    r_cat = fbd.buscar_race_cat(race_id)


    dados_race = f"RR TIPS - AvB:  \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m"

    if vencedor == 0:
        t_vencedor = f"*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})*"
        t_perdedor = f"TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})"
    elif vencedor == 1:
        t_perdedor = f"TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})"
        t_vencedor = f"*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})*"

    if risco == 0:
        risc = "PADRÃO"
    elif risco == 1:
        risc = "ARRISCADA"


    comp1 = f"dias sem correr: {d_dogs_a[2]}    {abs(d_dogs_a[2] - d_dogs_b[2])}    {d_dogs_b[2]}"
    comp2 = f"peso: {d_dogs_a[3]}    {abs(d_dogs_a[3] - d_dogs_b[3])}    {d_dogs_b[3]}"
    comp3 = f"media split: {d_dogs_a[4]}    {abs(d_dogs_a[4] - d_dogs_b[4])}    {d_dogs_b[4]}"
    comp4 = f"media 1º bend: {d_dogs_a[5]}    {abs(d_dogs_a[5] - d_dogs_b[5])}    {d_dogs_b[5]}"
    comp5 = f"media finalização: {d_dogs_a[6]}    {abs(d_dogs_a[6] - d_dogs_b[6])}    {d_dogs_b[6]}"
    comp6 = f"media de tempo: {d_dogs_a[7]}    {abs(d_dogs_a[7] - d_dogs_b[7])}    {d_dogs_b[7]}"
    comp7 = f"variação med de tempo: {d_dogs_a[8]}    {abs(d_dogs_a[8] - d_dogs_b[8])}    {d_dogs_b[8]}"
    comp8 = f"velocidade media: {d_dogs_a[9]}    {abs(d_dogs_a[9] - d_dogs_b[9])}    {d_dogs_b[9]}"
    comp9 = f"recupera / cansa: {d_dogs_a[10]}    {abs(d_dogs_a[10] - d_dogs_b[10])}    {d_dogs_b[10]}"
    comp10 = f"media split final: {d_dogs_a[11]}    {abs(d_dogs_a[11] - d_dogs_b[11])}    {d_dogs_b[11]}"
    comp11 = f"status da cat: {d_dogs_a[12]}    {abs(d_dogs_a[12] - d_dogs_b[12])}    {d_dogs_b[12]}"
    comp12 = f"n races com dist: {d_dogs_a[15]}    {abs(d_dogs_a[15] - d_dogs_b[15])}    {d_dogs_b[15]}"
    comp13 = f"cat ultima race: {d_dogs_a[16]}    -------------    {d_dogs_b[16]}"
    comp14 = f"odds: @{odd[0]}    -------------    @{odd[1]}"
    metodo_a =f"metodo dog A: {venc[13]}"
    metodo_b =f"metodo dog B: {venc[14]}"

    table = [
             ["dias s correr:", d_dogs_a[2], round(abs(d_dogs_a[2] - d_dogs_b[2]),2), d_dogs_b[2]],
             ["peso:", d_dogs_a[3], round(abs(d_dogs_a[3] - d_dogs_b[3]),2), d_dogs_b[3]],
             ["med split:", d_dogs_a[4], round(abs(d_dogs_a[4] - d_dogs_b[4]),2), d_dogs_b[4]],
             ["med 1º bend:", d_dogs_a[5], round(abs(d_dogs_a[5] - d_dogs_b[5]),2), d_dogs_b[5]],
             ["med finalz:", d_dogs_a[6], round(abs(d_dogs_a[6] - d_dogs_b[6]),2), d_dogs_b[6]],
             ["med de tempo:", d_dogs_a[7], round(abs(d_dogs_a[7] - d_dogs_b[7]),2), d_dogs_b[7]],
             ["var med  tempo:", d_dogs_a[8], round(abs(d_dogs_a[8] - d_dogs_b[8]),2), d_dogs_b[8]],
             ["veloc media:", d_dogs_a[9], round(abs(d_dogs_a[9] - d_dogs_b[9]),2), d_dogs_b[9]],
             ["rec / cansa:", d_dogs_a[10], round(abs(d_dogs_a[10] - d_dogs_b[10]),2), d_dogs_b[10]],
             ["med split fin:", d_dogs_a[11], round(abs(d_dogs_a[11] - d_dogs_b[11]),2), d_dogs_b[11]],
             ["stts da cat:", d_dogs_a[12], round(abs(d_dogs_a[12] - d_dogs_b[12]),2), d_dogs_b[12]],
             ["n races c/ dist:", d_dogs_a[15], round(abs(d_dogs_a[15] - d_dogs_b[15]),2), d_dogs_b[15]],
             ["cat ult race:", d_dogs_a[16], "---", d_dogs_b[16]],
             ["odds:", odd[0], "---", odd[1]]]

    table_str = tabulate(table, headers=["", "A", "DIF", "B"], tablefmt="grid", colalign=("left","center","center","center") )

    print(table_str)

    mens = f"{dados_race} \n\n{metodo_a}\n{metodo_b}\n \n{t_vencedor}\nVENCE\n{t_perdedor}\n{risc}\nLink:aaaaaa"


    largura = 1600
    altura = 2000

    # Criar uma nova imagem em memória
    imagem = Image.new("RGB", (largura, altura), color="black")

    # Criar um objeto draw para desenhar na imagem
    draw = ImageDraw.Draw(imagem)

    # Definir a fonte e o tamanho do texto
    fonte = ImageFont.truetype("consola.ttf", size=40)

    # Desenhar a tabela na imagem
    draw.text((10, 10), mens, font=fonte, fill=(255, 255, 255))

    # Criar um objeto BytesIO em memória
    buffer = BytesIO()

    # Salvar a imagem no objeto BytesIO em formato jpg
    imagem.save(buffer, format="JPEG")

    mensagem = f"{dados_race} \n{comp1}\n{comp2}\n{comp3}\n{comp4}\n{comp5}\n{comp6}\n{comp7}\n{comp8}\n{comp9}\n{comp10}\n{comp11}\n{comp12}\n{comp13}\n{comp14}\n{metodo_a}\n{metodo_b}\n \n{t_vencedor}\nVENCE\n{t_perdedor}\n{risc}\nLink:aaaaaa"

    return buffer

def bot_mensagem_av(odd, vencedor, risco, a, b, race_id, link):
    d_dogs_a, d_dogs_b, venc = f.compara_av(race_id, a, b)

    horario = fbd.buscar_race_h(race_id[0])
    nome = fbd.buscar_race_nome(race_id[0])
    pista_id = fbd.buscar_race_pis(race_id[0])
    pista_nome = fbd.buscar_pista_nome(pista_id[0])
    r_dist = fbd.buscar_race_dist(race_id)
    r_cat = fbd.buscar_race_cat(race_id)


    dados_race = f"RR TIPS - AvB:  🐕‍🦺  \n{pista_nome[0]} {horario[0]} - ({nome[0]}) - {r_cat[0]} - {r_dist[0]}m"

    if vencedor == 0:
        t_vencedor = f"🥇*TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})*"
        t_perdedor = f"TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})"
    elif vencedor == 1:
        t_perdedor = f"TRAP: {d_dogs_a[0]}- {d_dogs_a[1]} ({venc[11]})"
        t_vencedor = f"🥇*TRAP: {d_dogs_b[0]}- {d_dogs_b[1]} ({venc[12]})*"

    if risco == 0:
        risc = "PADRÃO"
    elif risco == 1:
        risc = "ARRISCADA"

    metodo_a =f"metodo dog A: {venc[13]}"
    metodo_b =f"metodo dog B: {venc[14]}"

    table = [["TRAP:", d_dogs_a[0], "---", d_dogs_b[0]],
             ["dias s correr:", d_dogs_a[2], round(abs(d_dogs_a[2] - d_dogs_b[2]),2), d_dogs_b[2]],
             ["peso:", d_dogs_a[3], round(abs(d_dogs_a[3] - d_dogs_b[3]),2), d_dogs_b[3]],
             ["m/ split:", d_dogs_a[4], round(abs(d_dogs_a[4] - d_dogs_b[4]),2), d_dogs_b[4]],
             ["m/ 1º bend:", d_dogs_a[5], round(abs(d_dogs_a[5] - d_dogs_b[5]),2), d_dogs_b[5]],
             ["m/ finalização:", d_dogs_a[6], round(abs(d_dogs_a[6] - d_dogs_b[6]),2), d_dogs_b[6]],
             ["m/ de tempo:", d_dogs_a[7], round(abs(d_dogs_a[7] - d_dogs_b[7]),2), d_dogs_b[7]],
             ["variação m/ tempo:", d_dogs_a[8], round(abs(d_dogs_a[8] - d_dogs_b[8]),2), d_dogs_b[8]],
             ["velocidade media:", d_dogs_a[9], round(abs(d_dogs_a[9] - d_dogs_b[9]),2), d_dogs_b[9]],
             ["recup / cansa:", d_dogs_a[10], round(abs(d_dogs_a[10] - d_dogs_b[10]),2), d_dogs_b[10]],
             ["m/ split final:", d_dogs_a[11], round(abs(d_dogs_a[11] - d_dogs_b[11]),2), d_dogs_b[11]],
             ["status da cat:", d_dogs_a[12], "---", d_dogs_b[12]],
             ["n races c/ dist:", d_dogs_a[15], "---", d_dogs_b[15]],
             ["cats anteriores:", d_dogs_a[16], "---", d_dogs_b[16]],
             ["odds:", odd[0], "---", odd[1]]]

    table_str = tabulate(table, headers=["", "A", "DIF", "B"], tablefmt="grid", colalign=("left","center","center","center") )

    print(table_str)

    text = f"{dados_race}\n \n{t_vencedor}\nVENCE\n{t_perdedor}\n \n{metodo_a}\n{metodo_b}\nENTRADA {risc}\nLink:{link}"


    largura = 1600
    altura = 1300

    # Criar uma nova imagem em memória
    imagem = Image.new("RGB", (largura, altura), color="black")

    # Criar um objeto draw para desenhar na imagem
    draw = ImageDraw.Draw(imagem)

    # Definir a fonte e o tamanho do texto
    fonte = ImageFont.truetype("consola.ttf", size=44)

    # Desenhar a tabela na imagem
    draw.text((10, 10), table_str, font=fonte, fill=(255, 255, 255))

    # Criar um objeto BytesIO em memória
    buffer = BytesIO()

    # Salvar a imagem no objeto BytesIO em formato jpg
    imagem.save(buffer, format="JPEG")

    mens_telegram_ia_ft(buffer,text)



# a = 'Crystal Wild'
# b = 'Borna Bee'
# race_id = fbd.buscar_dog_rid(a)

# odds = [1.75,2.00]
# link = "aaaaa"

# bot_mensagem_av(odds,0,0,a,b,race_id, link)


# mens_telegram_ia_ft(ft,link)
# mens_telegram_ia(men)

# cria_mens(odds,0,0,a,b,race_id)
