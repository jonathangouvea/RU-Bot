import discord
import os
import urllib.request

from keep_alive import keep_alive

client = discord.Client()

def FindAlmoco(texto):
    inicio = texto.find("ALMOÇO")
    fim = texto.find("JANTAR", inicio)
    textoAlmoco = texto[inicio:fim]
    almoco = []
    C2 = 0
    for i in range(0, 6):
        C1 = textoAlmoco.find("<span>", C2)
        C2 = textoAlmoco.find("</span>", C1)
        almoco.append(textoAlmoco[C1+6:C2])
    return almoco
 
def FindJantar(texto):
    inicio = texto.find("JANTAR")
    fim = texto.find("</article>", inicio)
    textoAlmoco = texto[inicio:fim]
    almoco = []
    C2 = 0
    for i in range(0, 6):
        C1 = textoAlmoco.find("<span>", C2)
        C2 = textoAlmoco.find("</span>", C1)
        almoco.append(textoAlmoco[C1+6:C2])
    return almoco

def decorador(refeicao):
    textao = ''
    textos = ['**Prato Principal**', '**Prato Vegetariano**', '**Guarnição**', '**Arroz**', '**Feijão**', '**Saladas**', '**Sobremesa**']

    emojis = [' :poultry_leg: ', ' :cooking: ', ' :potato: ', ' :curry: ', ' :curry: ', ' :salad: ', ' :apple: ']

    i = 0
    for r in refeicao:
      if i == 0:
        C = r.find("/")
        textao += "{2}{0}: {1}\n".format(textos[i], r[0:C], emojis[i])
        i += 1
        textao += "{2}{0}: {1}\n".format(textos[i], r[C+2::], emojis[i])
      else:
        textao += "{2}{0}: {1}\n".format(textos[i], r, emojis[i])
      i += 1
    textao += '\n'
    return textao

@client.event
async def on_ready():
    print('\N{hot beverage}')
    print(client.user)

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content == '!RU':
          print("TESTE")
          pagina = urllib.request.urlopen('http://www2.ufscar.br/estudante/restaurantes-universitario')
          texto = pagina.read().decode("utf-8")      

          almoco =  ':fork_and_knife: **ALMOÇO** :fork_and_knife:\n' + decorador(FindAlmoco(texto))
          await client.send_message(message.channel, almoco)

          jantar = ':fork_and_knife: **JANTAR** :fork_and_knife:\n' + decorador(FindAlmoco(texto))
          await client.send_message(message.channel, jantar)

        elif message.content.lower() == '!almoco' or message.content.lower() == '!almoço':
          print("TESTE")
          pagina = urllib.request.urlopen('http://www2.ufscar.br/estudante/restaurantes-universitario')
          texto = pagina.read().decode("utf-8")      

          almoco =  ':fork_and_knife: **ALMOÇO** :fork_and_knife:\n' + decorador(FindAlmoco(texto))
          await client.send_message(message.channel, almoco)

        elif message.content.lower() == '!jantar':
          print("TESTE")
          pagina = urllib.request.urlopen('http://www2.ufscar.br/estudante/restaurantes-universitario')
          texto = pagina.read().decode("utf-8")      

          jantar = ':fork_and_knife: **JANTAR** :fork_and_knife:\n' + decorador(FindJantar(texto))
          await client.send_message(message.channel, jantar)

        elif message.content.lower() == '!ajuda':
          embed = discord.Embed(title="Ajuda do **RU Bot**", colour=discord.Colour(0xd0021b), url="https://github.com/jonathangouvea/RU-Bot", description="Estou aqui para te ajudar a saber 'o que tem no RU'! Consigo mostrar o cardápio do dia, só do almoço ou do jantar...\n\nPara usar essas funções basta digitar:")

          embed.set_author(name="Criado por Jonathan Gouvea", url="https://github.com/jonathangouvea/RU-Bot")
          embed.set_footer(text="Imagine emojis de guaxinim aqui")

          embed.add_field(name="!RU", value="Assim você pode ver o cardápio do dia inteiro", inline=False)
          embed.add_field(name="!Almoço :fork_and_knife:", value="Assim para apenas o almoço", inline=True)
          embed.add_field(name="!Jantar :fork_and_knife:", value="E assim para o jantar\n\n", inline=True)
          embed.add_field(name="Parou de funcionar :thinking:", value="Bem, o problema pode ser no site [da UFSCar](https://www2.ufscar.br/estudante/restaurantes-universitario) que parou, ou algum problema no meu código, ~~a falta de Try-Catchs é real~~.")
          embed.add_field(name="Código no GitHub", value="[**Aqui**](https://github.com/jonathangouvea/RU-Bot), sinta-se livre para contribuir... Qualquer coisa só gritar quem me fez!")

          await client.send_message(message.channel,embed=embed)

        #else:
        #  print(message.content)

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)