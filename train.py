#python3 train.py      on shell
#delete the "#" from the train you want the bot to do

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

chatbot = ChatBot('Your bot name')

#train from corpus:
#trainer = ChatterBotCorpusTrainer(chatbot)
#trainer.train("chatterbot.corpus.english")

#custom training with strings:
#trainer = ListTrainer(chatbot)
#trainer.train([
#  "Hi",
#  "Hey",
#])

trainer.export_for_training('./my_export.json')