import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime, timedelta

# Initialize a data dictionary to store user activities (for demo purposes)
user_data = {}

async def start(update: Update, context: CallbackContext) -> None:
    """Welcome message and initial interaction with the bot."""
    user = update.effective_user
    user_id = user.id
    username = user.username
    join_date = datetime.now().strftime('%Y-%m-%d')

    # Save user data if they are new
    if user_id not in user_data:
        user_data[user_id] = {
            "username": username,
            "join_date": join_date,
            "activity_time": 0,
            "last_active": datetime.now(),
            "commands_used": []
        }
        await update.message.reply_text(f"Welcome {username}! I've recorded your join date.")

async def get_info(update: Update, context: CallbackContext) -> None:
    """Send user details like join date, hours spent, etc."""
    user_id = update.effective_user.id
    
    if user_id in user_data:
        user_info = user_data[user_id]
        
        # Calculate hours spent on bot
        total_hours = user_info['activity_time'] / 3600

        # Check if user is currently online with a threshold
        last_active = user_info['last_active']
        is_online = (datetime.now() - last_active) < timedelta(minutes=5)

        # Display information to the user
        await update.message.reply_text(
            f"Username: {user_info['username']}\n"
            f"Join Date: {user_info['join_date']}\n"
            f"Commands Used: {', '.join(user_info['commands_used'])}\n"
            f"Hours Spent: {total_hours:.2f} hours\n"
            f"Online: {'Yes' if is_online else 'No'}"
        )
    else:
        await update.message.reply_text("I don’t have any information on you yet. Try interacting with me first!")

async def log_activity(update: Update, context: CallbackContext) -> None:
    """Logs each command used by the user as a mini-app."""
    user_id = update.effective_user.id
    command = update.message.text

    # Check if user data exists, then log the command and time
    if user_id in user_data:
        user_data[user_id]["commands_used"].append(command)
        user_data[user_id]["last_active"] = datetime.now()

        # Simulate time spent for demo purposes
        user_data[user_id]["activity_time"] += 300  # Adds 5 minutes per command (customizable)

def main():
    # Get the bot token from environment variable for security
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set.")

    # Initialize application with the bot token
    application = Application.builder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_info", get_info))
    application.add_handler(CommandHandler("log_activity", log_activity))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()