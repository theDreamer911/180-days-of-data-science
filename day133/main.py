from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer

chatBot = ChatBot("Hand")

# Create a new trainer for the chatBot
trainer = ChatterBotCorpusTrainer(chatBot)

# Train chatBot based english corpus
trainer.train("chatterbot.corpus.english")

# Get response from input statement
# print(chatBot.get_response("Hello"))
# print(chatBot.get_response("What is AI?"))

print("Hi, I am Hand your friend")
while True:
    query = input(">>>")
    print(chatBot.get_response(Statement(text=query, search_text=query)))