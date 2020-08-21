from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot(
    'Sakura',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter'
)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.chinese")
trainer.train("chatterbot.corpus.english")