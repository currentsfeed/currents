#!/usr/bin/env python3
"""
Telegram Forwarder Bot for Currents Team
Forwards messages from @thecamel to Roy's chat with OpenClaw
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# Bot configuration
BOT_TOKEN = "8375579986:AAGXzK6fC7qLRlabth5SJPgqw5i0Sdkgv1k"
TARGET_CHAT_ID = "6472008941"  # Roy's Telegram ID (this chat)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    logger.info(f"Start command from user: {user.username} (ID: {user.id}, Chat ID: {chat_id})")
    
    await update.message.reply_text(
        f"👋 Currents Forwarder Bot Active!\n\n"
        f"Your Chat ID: `{chat_id}`\n"
        f"Your User ID: `{user.id}`\n\n"
        f"Send me any message and I'll forward it to Roy's chat with OpenClaw.\n\n"
        f"✅ Ready to forward messages!"
    )

async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /info command - show chat and user IDs"""
    user = update.effective_user
    chat = update.effective_chat
    
    info_text = (
        f"📊 Chat Information:\n\n"
        f"Chat ID: `{chat.id}`\n"
        f"Chat Type: {chat.type}\n"
        f"User ID: `{user.id}`\n"
        f"Username: @{user.username if user.username else 'none'}\n"
        f"First Name: {user.first_name}\n"
    )
    
    await update.message.reply_text(info_text)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward any message to target chat"""
    user = update.effective_user
    message = update.message
    
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
            chat_id=TARGET_CHAT_ID,
            text=forwarded_text
        )
        
        # Confirm to sender
        await update.message.reply_text("✅ Message forwarded to Roy!")
        
        logger.info(f"Forwarded message from {sender_username} (ID: {user.id}) to chat {TARGET_CHAT_ID}")
        
    except Exception as e:
        logger.error(f"Error forwarding message: {e}")
        await update.message.reply_text(f"❌ Error forwarding message: {str(e)}")

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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))
    application.add_error_handler(error_handler)
    
    # Start bot
    logger.info("🤖 Currents Forwarder Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
