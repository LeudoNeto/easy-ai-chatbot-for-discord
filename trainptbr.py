#python3 train.py      no terminal
#tire os "#" do treinamento que você quer que o bot faça

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

chatbot = ChatBot('Nome do seu bot')

#trainamento pelo corpus (português):
#trainer = ChatterBotCorpusTrainer(chatbot)
#trainer.train("chatterbot.corpus.portuguese")

#treinamento personalziado com strings:
#trainer = ListTrainer(chatbot)
#trainer.train([
#  "Oi",
#  "Olá",
#])

trainer.export_for_training('./my_export.json')