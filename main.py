import discord
from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import asyncio

chatbot = ChatBot('Your bot name')   #u can put whatever you want here, including nothing

bot_prefix = "ai-"   #change here your bot prefix
bot = commands.Bot(command_prefix=bot_prefix)

def check_channel(channel):   #checks if the channel is on the database
  archive = open('channels.txt','rt+')
  if f'{channel}\n' in archive.readlines():
    archive.close()
    return True
  else:
    archive.close()
    return False


@bot.command(help="Enable chatting with the bot in this text channel", name="enable") #for adding the channel id to the database
async def enable(ctx: commands.Context):
  if not check_channel(ctx.message.channel.id):
    archive = open('channels.txt','at')
    archive.write(f'{ctx.message.channel.id}\n')
    archive.close()
    await ctx.send('This channel is now enabled for chatting with the bot')
  else:
    await ctx.send('This channel was already enabled for chatting with the bot')

@bot.command(help="Disable chatting with the bot in this text channel", name="disable") #for removing the channel id from the database
async def disable(ctx: commands.Context):
  if check_channel(ctx.message.channel.id):
    archive = open('channels.txt','r')
    lines = archive.readlines()
    pos = lines.index(f'{ctx.message.channel.id}\n')
    newarchive = open('channels.txt','w')
    for num,line in enumerate(lines):
        if num != pos:
            newarchive.write(line)
    await ctx.send('This channel has been disabled for chatting with the bot')
  else:
    await ctx.send('This channel was already disabled for chatting with the bot')

@bot.event
async def on_ready():   #print the bot user when its fully online
  print(f'Connected as {bot.user}')
  await bot.change_presence(activity=discord.Game(name=f'{bot_prefix}help | 🤖💬'))   #set the bot presence


#on message: Quando receber qualquer mensagem, retornará o usuário que mandou e a própria mensagem.
@bot.listen()   #prints every user and message the bot can read
async def on_message(message):
  print(f'Mensagem de {message.author}: {message.content}')
  
  messages = await message.channel.history(limit=2).flatten()   #for not getting an answer when teaching it
  em = discord.Embed(title=f"Thanks,  i think i learned this", color = message.author.color)
  for pos,msg in enumerate(messages):
    if msg.content == 'I have no ideia, please teach me:' and messages[pos+1].author == message.author:
      return
      
  if check_channel(message.channel.id) and not message.author.bot and message.content not in [f'{bot_prefix}disable',f'{bot_prefix}enable'] and not message.content.startswith(f'{bot_prefix}ignore'):   #ignoring certain conditions, note that if you send the "command" [prefix]ignore the bot will not answer
    speak = message.content
    answer = chatbot.get_response(speak)
    if float(answer.confidence) > 0.1:     #make the bot learn if the answer confidence is lower than 10%
      em = discord.Embed(title=answer, color = message.author.color)
      em.set_footer(text=f"The confidence of this answer was {float(answer.confidence)*100}%")
      await message.channel.send(embed=em)
    else:
      await message.channel.send('I have no ideia, please teach me:')  #when the bot says it, you can send the message you want its to say when someone sends your previous message

      def is_correct(m):
        return m.author == message.author and m.channel == message.channel
        
      try:
        teach = await bot.wait_for('message', check=is_correct, timeout=30.0)
      except asyncio.TimeoutError:
        return await message.channel.send('You took so long to answer')

      trainer = ListTrainer(chatbot)
      trainer.train([
      str(message.content),
      str(teach.content),
])
      trainer.export_for_training('./my_export.json')

      em = discord.Embed(title=f"Thanks,  i think i learned this", color = message.author.color)
      await message.channel.send(embed=em)
    
#autenticação
bot.run('Token')