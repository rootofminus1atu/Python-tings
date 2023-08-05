from colorama import Fore, Style, Back
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

def print_report(text):
    rn = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    print(f"{Fore.LIGHTBLACK_EX}[{rn}]{Fore.RESET} {text}")

def see_colors():
    for color in Fore.__dict__.keys():
        if color[0] != "_":
            print(f"{getattr(Fore, color)}{color}{Fore.RESET}")

from xata.client import XataClient

client = XataClient(db_url=os.getenv('XATA_DATABASE_URL'), api_key=os.getenv('XATA_API_KEY'))
print(client.db_name)