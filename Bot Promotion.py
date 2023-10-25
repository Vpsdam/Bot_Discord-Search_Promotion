import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

Service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=Service)
load_dotenv('.env.txt')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='*', intents=intents)
senha = os.getenv('DISCORD_TOKEN')

def livros(link):
    navegador.get(link)

    lista_de_produtos = []

    for p in range(3):
        time.sleep(2)
        search_nomes = navegador.find_elements('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "a-color-base", " " )) and contains(concat( " ", @class, " " ), concat( " ", "a-text-normal", " " ))]')
        search_precos = navegador.find_elements('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "puis-price-instructions-style", " " ))]')

        if len(search_nomes) != len(search_precos):
            print("Erro: número de nomes e preços não corresponde")
            break

        for i in range(len(search_nomes)):
            nome = search_nomes[i].text
            preco_element = search_precos[i].text

            produto_dict = {'nome': nome, 'preco': preco_element}
            lista_de_produtos.append(produto_dict)

        time.sleep(2)
        try:
            navegador.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "s-pagination-next", " " ))]').click()
        except:
            print('acabou a página')
            break

    return lista_de_produtos

async def Top_Vendas(link):  # Adicione "async" aqui para torná-la assíncrona
    navegador.get(link)

    lista_produto = []
    Search_name = navegador.find_elements('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "a-link-normal", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y", " " ))]')
    Search_Price = navegador.find_elements('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "_cDEzb_p13n-sc-price_3mJ9Z", " " ))]')
    Search_position = navegador.find_elements('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "zg-bdg-text", " " ))]')

    for i in range(len(Search_position)):
        nome = Search_name[i].text
        price = Search_Price[i].text
        position = Search_position[i].text
        produto_dict = {'nome': nome, 'preco' : price, 'rank' : position}
        lista_produto.append(produto_dict)
    
    return lista_produto

@bot.command()
async def Top_AudiBook(ctx):
    await ctx.send("Iniciando a procura de Audio livros...")
    link = 'https://www.amazon.com.br/gp/bestsellers/audible/ref=zg_mw_tab_t_audible_bs'
    data = await Top_Vendas(link)  # Aguarde a função assíncrona
    if data:
        for produto in data:
            message = f"**{produto['rank']}** - {produto['nome']} - {produto['preco']}"
            time.sleep(1)
            await ctx.send(message)

@bot.command()
async def invert(ctx, message):
    await ctx.send(message[::-1])

@bot.command()
async def Promo_fantasy(ctx):
    await ctx.send("Iniciando a procura de livros...")
    link = 'https://www.amazon.com.br/s?i=stripbooks&rh=n%3A7841775011&fs=true&qid=1698114157&ref=sr_pg_1'
    livro_data = livros(link)
    if livro_data:
        for produto in livro_data:
            preco_formatado = produto['preco'].replace('\n', ',').replace('De:,', 'De: ').replace('Capa Comum,', 'Capa Comum ')
            message = f"**{produto['nome']}** - Preço: {preco_formatado}\n"
            time.sleep(1)
            await ctx.author.send(message)
    else:
        await ctx.send("Não foi possível obter os dados dos livros.")

@bot.command()
async def Promo_Book(ctx):
    await ctx.send("Iniciando a procura de livros...")
    link = 'https://www.amazon.com.br/s?i=stripbooks&bbn=13130368011&rh=n%3A6740748011&dc&ds=v1%3AovzadTvUg1XqGen%2BVjefPKMUW1en5Ly9zs9aTtD3qqc&qid=1698111785&ref=sr_ex_n_1'
    livro_data = livros(link)
    if livro_data:
        for produto in livro_data:
            preco_formatado = produto['preco'].replace('\n', ',').replace('De:,', 'De: ').replace('Capa Comum,', 'Capa Comum ')
            message = f"**{produto['nome']}** - Preço: {preco_formatado}\n"
            time.sleep(1)
            await ctx.author.send(message)
    else:
        await ctx.send("Não foi possível obter os dados dos livros.")

@bot.command()
async def Promo_Medo(ctx):
    await ctx.send("Iniciando a procura de livros...")
    link = 'https://www.amazon.com.br/s?i=stripbooks&bbn=13130368011&rh=n%3A6740748011%2Cn%3A13130368011%2Cn%3A7841775011%2Cn%3A7872746011&dc&ds=v1%3AdLvQO3XVgD%2Fml9iIbPBgZTMKiftfo4KFqsN1TfyePPo&qid=1698114903&rnid=6740748011&ref=sr_nr_n_4'
    livro_data = livros(link)
    if livro_data:
        for produto in livro_data:
            preco_formatado = produto['preco'].replace('\n', ',').replace('De:,', 'De: ').replace('Capa Comum,', 'Capa Comum ')
            message = f"**{produto['nome']}** - Preço: {preco_formatado}\n"
            time.sleep(1)
            await ctx.author.send(message)
    else:
        await ctx.send("Não foi possível obter os dados dos livros.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('oi'):
        await message.channel.send('Hello')

    if message.content.startswith('good'):
        await message.channel.send('Bye')

    await bot.process_commands(message)

bot.run(senha)
