import discord
from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import asyncio

chatbot = ChatBot('Nome do seu bot')

bot_prefix = "ai-"
bot = commands.Bot(command_prefix=bot_prefix)

def check_channel(channel):
  arquivo = open('canais.txt','rt+')
  if f'{channel}\n' in arquivo.readlines():
    arquivo.close()
    return True
  else:
    arquivo.close()
    return False


@bot.command(help="Habilita a conversa com o bot nesse canal de texto", name="habilitar")
async def habilitar(ctx: commands.Context):
  if not check_channel(ctx.message.channel.id):
    arquivo = open('canais.txt','at')
    arquivo.write(f'{ctx.message.channel.id}\n')
    arquivo.close()
    await ctx.send('Esse canal agora está habilitado para conversa')
    await ctx.send('Se você mandar qualquer um desses no começo da mensagem:')
    await ctx.send('. , - _ > < = : ; + / ~')
    await ctx.send("Eu não vou considerar a mensagem")
  else:
    await ctx.send('Esse canal já estava habilitado para conversa')

@bot.command(help="Desabilita a conversa com o bot nesse canal de texto", name="desabilitar")
async def desabilitar(ctx: commands.Context):
  if check_channel(ctx.message.channel.id):
    arquivo = open('canais.txt','r')
    linhas = arquivo.readlines()
    pos = linhas.index(f'{ctx.message.channel.id}\n')
    novoarquivo = open('canais.txt','w')
    for numero,linha in enumerate(linhas):
        if numero != pos:
            novoarquivo.write(linha)
    await ctx.send('Esse canal foi desabilitado para conversa')
  else:
    await ctx.send('Esse canal já não estava habilitado para conversa')

@bot.event
async def on_ready():
  print(f'Fui conectado como {bot.user}')
  await bot.change_presence(activity=discord.Game(name=f'{bot_prefix}help | 🤖💬'))


#on message: Quando receber qualquer mensagem, retornará o usuário que mandou e a própria mensagem.
@bot.listen()
async def on_message(message):
  print(f'Mensagem de {message.author}: {message.content}')
  
  messages = await message.channel.history(limit=2).flatten()
  em = discord.Embed(title=f"Obrigada, acho que aprendi", color = message.author.color)
  for pos,msg in enumerate(messages):
    if msg.content == 'Não faço ideia, me ensine:' and messages[pos+1].author == message.author:
      return
      
  if check_channel(message.channel.id) and not message.author.bot and message.content not in [f'{bot_prefix}habilitar',f'{bot_prefix}habilitar'] and message.content[0] not in ['.',',','-','>','<','=','_',':',';','+','/','~']:
    fala = message.content
    resposta = chatbot.get_response(fala)
    if float(resposta.confidence) > 0.1:
      em = discord.Embed(title=resposta, color = message.author.color)
      em.set_footer(text=f"A certeza dessa resposta foi de {float(resposta.confidence)*100}%")
      await message.reply(embed=em)
    else:
      await message.reply('Não faço ideia, me ensine:')

      def is_correct(m):
        return m.author == message.author and m.channel == message.channel
        
      try:
        ensinar = await bot.wait_for('message', check=is_correct, timeout=30.0)
      except asyncio.TimeoutError:
        return await message.channel.send('Você demorou demais para responder.')

      trainer = ListTrainer(chatbot)
      trainer.train([
      str(message.content),
      str(ensinar.content),
])
      trainer.export_for_training('./my_export.json')

      em = discord.Embed(title=f"Obrigada, acho que aprendi", color = message.author.color)
      await message.channel.send(embed=em)
    
#autenticação
bot.run('Token')