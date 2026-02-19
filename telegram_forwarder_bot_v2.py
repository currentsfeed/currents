#!/usr/bin/env python3
"""
Telegram Forwarder Bot for Currents Team - v2
Forwards messages from @thecamel to Roy's chat with OpenClaw
Allows dynamic target chat configuration
"""

import logging
import os
import json
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# Bot configuration
BOT_TOKEN = "8375579986:AAGXzK6fC7qLRlabth5SJPgqw5i0Sdkgv1k"
CONFIG_FILE = "/home/ubuntu/.openclaw/workspace/currents-full-local/forwarder_config.json"

# Default target (Roy's user ID)
DEFAULT_TARGET = "6472008941"

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def load_config():
    """Load target chat ID from config file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('target_chat_id', DEFAULT_TARGET)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
    return DEFAULT_TARGET

def save_config(target_chat_id):
    """Save target chat ID to config file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'target_chat_id': target_chat_id}, f)
        logger.info(f"Saved target chat ID: {target_chat_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    logger.info(f"Start command from user: {user.username} (ID: {user.id}, Chat ID: {chat_id})")
    
    current_target = load_config()
    
    await update.message.reply_text(
        f"👋 Currents Forwarder Bot Active!\n\n"
        f"Your Chat ID: `{chat_id}`\n"
        f"Your User ID: `{user.id}`\n"
        f"Current target: `{current_target}`\n\n"
        f"Commands:\n"
        f"/settarget <chat_id> - Set forwarding destination\n"
        f"/info - Show current settings\n\n"
        f"Send any message to forward it!"
    )

async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /info command - show chat and user IDs"""
    user = update.effective_user
    chat = update.effective_chat
    current_target = load_config()
    
    info_text = (
        f"📊 Bot Information:\n\n"
        f"This Chat ID: `{chat.id}`\n"
        f"Chat Type: {chat.type}\n"
        f"Your User ID: `{user.id}`\n"
        f"Your Username: @{user.username if user.username else 'none'}\n"
        f"Your Name: {user.first_name}\n\n"
        f"Current Target: `{current_target}`\n\n"
        f"💡 To change target:\n"
        f"/settarget <chat_id>"
    )
    
    await update.message.reply_text(info_text)

async def set_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set the target chat ID for forwarding"""
    user = update.effective_user
    
    # Check if user is Roy (only Roy can change target)
    if str(user.id) != "6472008941":
        await update.message.reply_text("❌ Only Roy can change the target chat.")
        return
    
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "Usage: /settarget <chat_id>\n\n"
            "Example: /settarget -1001234567890"
        )
        return
    
    new_target = context.args[0]
    
    if save_config(new_target):
        await update.message.reply_text(
            f"✅ Target chat updated!\n\n"
            f"New target: `{new_target}`\n\n"
            f"All messages will now be forwarded there."
        )
    else:
        await update.message.reply_text("❌ Error saving new target.")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward any message to target chat"""
    user = update.effective_user
    message = update.message
    target_chat_id = load_config()
    
    # Get sender info
    sender_name = user.first_name
    sender_username = f"@{user.username}" if user.username else "no username"
    
    # Build forwarded message
    if message.text:
        forwarded_text = (
            f"📨 [From {sender_name} ({sender_username})]\n\n"
            f"{message.text}"
        )
    else:
        forwarded_text = f"📨 [From {sender_name} ({sender_username})]\n\n[Non-text message]"
    
    try:
        # Send to target chat
        await context.bot.send_message(
            chat_id=target_chat_id,
            text=forwarded_text
        )
        
        # Confirm to sender
        await update.message.reply_text(
            f"✅ Forwarded to chat `{target_chat_id}`"
        )
        
        logger.info(f"Forwarded message from {sender_username} (ID: {user.id}) to chat {target_chat_id}")
        
    except Exception as e:
        logger.error(f"Error forwarding message: {e}")
        await update.message.reply_text(
            f"❌ Error forwarding message:\n{str(e)}\n\n"
            f"Current target: `{target_chat_id}`\n"
            f"Use /settarget to change."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", get_info))
    application.add_handler(CommandHandler("settarget", set_target))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))
    application.add_error_handler(error_handler)
    
    # Start bot
    logger.info("🤖 Currents Forwarder Bot v2 starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
