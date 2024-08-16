from pyrogram import Client, errors
from pyrogram.raw import functions
from urllib.parse import unquote
import logging
import os
import asyncio
import json
from colorama import init, Fore, Style
import shutil

# Initialize colorama
init()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set logging level for pyrogram to WARNING
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Ganti dengan path folder sesi
SESSIONS_FOLDER = 'sessions'
QUERY_FILE = "data.json"

# ASCII art with rainbow colors
ASCII_ART = r"""

 _______                          
|     __|.--.--.---.-.-----.---.-.
|__     ||  |  |  _  |-- __|  _  |
|_______||___  |___._|_____|___._|
         |_____|                  

"""

# Rainbow colors
RAINBOW_COLORS = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN
]

def print_ascii_art():
    """Print the ASCII art with rainbow colors centered."""
    # Split ASCII art into lines
    lines = ASCII_ART.strip().split('\n')
    
    # Get terminal width
    terminal_width = shutil.get_terminal_size().columns

    # Calculate maximum line length of ASCII art
    max_line_length = max(len(line) for line in lines)
    
    # Calculate padding to center the ASCII art
    padding = (terminal_width - max_line_length) // 2
    
    # Print each line with a different color and center-aligned
    for i, line in enumerate(lines):
        color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
        centered_line = ' ' * padding + line
        print(color + centered_line + Style.RESET_ALL)
    print()  # Print a newline after the ASCII art

async def generate_query(session_name, api_id, api_hash, bot_username, bot_url):
    """Mengambil query dari bot dan menyimpannya ke data.json"""
    try:
        async with Client(session_name, api_id=api_id, api_hash=api_hash) as client:
            if not client.is_connected:
                await client.start()
            
            # Resolve the peer for the bot
            peer = await client.resolve_peer(bot_username)
            
            # Request the webview
            webview = await client.invoke(functions.messages.RequestWebView(
                peer=peer,
                bot=peer,
                from_bot_menu=False,
                platform='Android',
                url=bot_url
            ))
            
            # Extract the query from the URL
            query = unquote(webview.url.split("&tgWebAppVersion=")[0].split("#tgWebAppData=")[1])
            
            # Load existing data from the JSON file
            if os.path.exists(QUERY_FILE):
                with open(QUERY_FILE, "r") as file:
                    data = json.load(file)
            else:
                data = {"accounts": []}
            
            # Append the new data
            data["accounts"].append({
                "name": session_name.split(os.path.sep)[-1],  # Extract the session name only
                "query": query
            })
            
            # Save the updated data back to the JSON file
            with open(QUERY_FILE, "w") as file:
                json.dump(data, file, indent=4)
            
            print(Fore.GREEN + f"Saved data for {session_name} to {QUERY_FILE}" + Style.RESET_ALL)
    
    except errors.FloodWait as e:
        logger.error(f"Flood wait error for {session_name}: {str(e)}")
    except Exception as e:
        print(Fore.RED + f"Failed to save data for {session_name} to {QUERY_FILE}" + Style.RESET_ALL)
        logger.error(f"Error retrieving query data for {session_name}: {str(e)}")

async def create_new_session(session_name, api_id, api_hash):
    """Membuat sesi baru dan menyimpannya ke dalam folder sesi"""
    try:
        async with Client(session_name, api_id=api_id, api_hash=api_hash) as client:
            # Tidak perlu memanggil client.start() di sini karena klien sudah terhubung secara otomatis
            logger.info(f"Created new session: {session_name}")
    except Exception as e:
        logger.error(f"Error creating new session {session_name}: {str(e)}")

async def add_session(api_id, api_hash):
    """Fungsi untuk menambahkan sesi baru"""
    session_name = input("Enter the name for the new session: ")
    await create_new_session(os.path.join(SESSIONS_FOLDER, session_name), api_id, api_hash)

async def generate_queries(api_id, api_hash, bot_username, bot_url):
    """Fungsi untuk menghasilkan query dari sesi yang ada"""
    while True:
        # Get all session files in the sessions folder
        sessions = [f[:-8] for f in os.listdir(SESSIONS_FOLDER) if f.endswith('.session')]
        
        # Clear the existing data.json file
        if os.path.exists(QUERY_FILE):
            os.remove(QUERY_FILE)
        
        tasks = []
        for session_name in sessions:
            # Generate queries for each existing session
            tasks.append(generate_query(os.path.join(SESSIONS_FOLDER, session_name), api_id, api_hash, bot_username, bot_url))
        
        await asyncio.gather(*tasks)
        
        # Wait for 6 hours before generating queries again
        print(Fore.YELLOW + "Waiting for 6 hours before the next query generation..." + Style.RESET_ALL)
        await asyncio.sleep(21600)  # 21600 seconds = 6 hours

async def main():
    """Main function to choose between adding a session or generating queries"""
    # Placeholder for API ID and API hash if needed
    api_id = 'YOUR_API_ID'  # Replace with actual API ID
    api_hash = 'YOUR_API_HASH'  # Replace with actual API hash

    # Create sessions folder if it doesn't exist
    if not os.path.exists(SESSIONS_FOLDER):
        os.makedirs(SESSIONS_FOLDER)

    print_ascii_art()

    print("Pilih opsi:")
    print("1. Tambah Sesi")
    print("2. Generate Query")
    choice = input("Masukkan pilihan (1 atau 2): ")

    if choice == '1':
        await add_session(api_id, api_hash)
    elif choice == '2':
        bot_username = input("Enter the bot username (e.g tabizoobot): ")
        bot_url = input("Request URL Header Bot(e.g https://app.tabibot.com): ")
        await generate_queries(api_id, api_hash, bot_username, bot_url)
    else:
        print("Pilihan tidak valid")

if __name__ == "__main__":
    asyncio.run(main())
