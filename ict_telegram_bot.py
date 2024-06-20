import logging
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
import requests
import asyncio
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define your command handler. This usually takes the two arguments update and context.
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Hi! Send me a photo and I will forward it to the server."
    )


async def handle_photo(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    # file_path = "received_photo.jpg"
    # print("Downloading photo")
    # print(photo_file)
    # # await photo_file.download(file_path)
    # file_path = "received_photo.jpg"
    # await photo_file.download(file_path)
    fp = await photo_file.download_to_drive("received_photo.jpg")
    # fp = open(photo_file, "rb")
    # r = await photo_file.download_as_bytearray()

    # Now send this photo to your server
    with open(fp, "rb") as photo:
        # print(photo.)
        response = requests.post(
            "https://ict4dtiballiapp-production.up.railway.app/uploadimage/",
            files={"file": photo},
        )

    if response.status_code == 200:
        await update.message.reply_text(
            "Photo received and sent to the server successfully!"
        )
    else:
        print(response.status_code)
        print(response.text)
        await update.message.reply_text("Failed to send the photo to the server.")


async def nullop(update: Update, context: CallbackContext) -> None:
    print("nullop called")


if __name__ == "__main__":
    load_dotenv()

    # Retrieve the token from environment variables
    token = os.getenv("TOKEN")
    application = (
        ApplicationBuilder()
        .token("7405687726:AAHIoZX2VePOiYA0dECZ6qIX258hKs2y9tg")
        .build()
    )

    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(filters.PHOTO, handle_photo)
    application.add_handler(message_handler)

    application.run_polling()
