#!/usr/bin/env python3
# (c) tonyironman

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# the PTB
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, DispatcherHandlerStop, run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity, ChatAction

import subprocess
import math
import requests
import os
import json

from telethon import TelegramClient
from telethon.errors import (
    RPCError, BrokenAuthKeyError, ServerError,
    FloodWaitError, FloodTestPhoneWaitError, FileMigrateError,
    TypeNotFoundError, UnauthorizedError, PhoneMigrateError,
    NetworkMigrateError, UserMigrateError, SessionPasswordNeededError
)
from telethon.utils import get_display_name
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo


# the secret configuration specific things
from config import Config
# the Strings used for this "thing"
from translation import Translation

# the Telegram trackings
from chatbase import Message
ABUSIVE_SPAM = []

def TRChatBase(chat_id, message_text, intent):
    msg = Message(api_key=Config.CHAT_BASE_TOKEN,
              platform="Telegram",
              version="1.3",
              user_id=chat_id,
              message=message_text,
              intent=intent)
    resp = msg.send()


def DownLoadFile(url, file_name):
    if not os.path.exists(file_name):
        r = requests.get(url, allow_redirects=True, stream=True)
        with open(file_name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=Config.CHUNK_SIZE):
                fd.write(chunk)
    return file_name


def humanbytes(size):
    # http
