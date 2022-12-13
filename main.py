import os
import re
import discord
import random
from dotenv import load_dotenv

prepared_answers  = [
    "Woof-woof, I came here to bark and remind you to send the ss58 public key (node address). As you can see, I barked.",
    "Do you know why chainflip lab members call me a good boy? I am not greedy to send a ss58 public key (node address) in this chat.",
    "I was also so cocky in my youth and did not send a ss58 public key (node address) when I asked for tokens, but after that I was taken to the vet. Don't repeat my mistakes.",
    "I always try to be a good boy, but when someone doesn't send here a ss58 public key (node address) in this chat, I want to call someone a bad boy.",
    "There was a rumor that everyone who sends a ss58 public key (node address) is called a good boy. But for now, these are just rumors.",
    "May I borrow your ss58 public key (node address)? I have paws, I can hardly generate it myself."
]

class MyClient(discord.Client):
    async def on_message(self, message):
        # Bot's messages ignoring
        if message.author == client.user:
            return

        # Parsing a string for an array of words
        message_substr_arr = ''.join(char if char.isalnum() else " " for char in message.content).split(" ")
        # Cleaning empty strings cause ':','!' and etc symbols
        cleaned_substr_arr = [current_word for current_word in message_substr_arr if len(current_word) != 0] 
        
        check_metamask, check_pubkey = None, None 
        regex_metamask = re.compile(r"^0x[0-9a-zA-Z]{40,40}$") # the metamask wallet is 42 characters long
        regex_pubkey = re.compile(r"^cF[0-9a-zA-Z]{47,47}$") # 49 long
        
        for current_word in cleaned_substr_arr:
            word_len = len(current_word)
            if word_len == 42 and not check_metamask:
                check_metamask = regex_metamask.search(current_word)
            elif word_len == 49 and not check_pubkey:
                check_pubkey = regex_pubkey.search(current_word)

        if check_metamask and check_pubkey:
            await message.add_reaction('\U0001F496')    
            return

        if not (check_metamask and not check_pubkey):
            return  
        
        await message.channel.send(random.choice(prepared_answers), reference=message)


if __name__ == "__main__":
    load_dotenv()
    discord_token = os.getenv("discord")
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(discord_token)