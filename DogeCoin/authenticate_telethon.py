from telethon.sync import TelegramClient

# Replace these with your actual API ID and hash
api_id = 21353371
api_hash = '3cb76341be34a280b7dcbf3af309add7'
# Include your phone number with the country code
phone_number = '+85246785948'  # make sure to start with +

with TelegramClient('my_session', api_id, api_hash) as client:
    client.start(phone=phone_number)
