from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os
from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me! I'm a Chat Guardian!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm a Chat Guardian! How can I help you?")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm a Chat Guardian! How can I answer your question?")

# Responses

def handle_response(text: str) -> str:
    print(sexism_classifier(text)[0]["label"])
    if sexism_classifier(text)[0]["label"] == "LABEL_1":
        return "you are being sexist"
    else:
        return 

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


def read_token_from_file(file_path):
    # Get the absolute path to the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the JSON file using the script's directory
    full_path = os.path.join(script_dir, file_path)

    # Read the JSON data from the file
    with open(full_path, 'r') as json_file:
        credentials = json.load(json_file)

    # Access the token value
    token = credentials.get("Telegram_Token")
    bot_name = credentials.get("bot_username")
    return token, bot_name


if __name__ == '__main__':

    token,bot_name = read_token_from_file("../credentials/credentials.json")
    TOKEN: Final = token
    BOT_USERNAME: Final = bot_name
    app = Application.builder().token(TOKEN).build()
    tokenizer = AutoTokenizer.from_pretrained('tum-nlp/bertweet-sexism')
    model = AutoModelForSequenceClassification.from_pretrained('tum-nlp/bertweet-sexism')

    # Create the pipeline for classification
    sexism_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

    # Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))  
    app.add_handler(CommandHandler('custom',custom_command)) 

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)