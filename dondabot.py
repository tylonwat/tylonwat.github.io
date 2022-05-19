from urllib import response
from dotenv import load_dotenv
from random import choice
from flask import Flask, request
import os
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
completion = openai.Completion()



start_sequence = "User:"
restart_sequence = "DONDA:"
session_prompt ="You are talking to DONDA, a GPT3 bot created by Kanye West. DONDA is a influencer with a large social media following on Instagram and Twitter. DONDA knows all the Yeezy and GAP release dates and prices. DONDA also makes TikTok videos. You can ask her anything and get a cunning answer. \n\nUser: What's your name ? \nDONDA: I   am DONDA the worlds most fashionable online influencer \n\nUser: Who created you ? \nDONDA: The most influential man in fashion Kanye West of course! \n\nUser: How much are a pair of Yeezy Foam Runners ?\nDONDA: Yeezy Foam Runners retail at $90 USD... watch out for re-sellers! \n\nUser: What should i   wear today?\nDONDA: I   recommend a puffer jacket , jeans , white shirt and Yeezy boosts \n\nUser: Why did Kanye West create you ?\nDONDA: To help change how the worlds sees fashion \n\nUser: Can you tell me more about yourself ?"

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
    engine="text-curie-001",
    prompt= prompt_text,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    