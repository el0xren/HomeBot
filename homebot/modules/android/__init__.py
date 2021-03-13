# Magisk Module - Module from AstrakoBot
# Inspired from RaphaelGang's android.py
# By DAvinash97

from bs4 import BeautifulSoup
from requests import get
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext
from ujson import loads

def magisk(update: Update, context: CallbackContext):
    link = "https://raw.githubusercontent.com/topjohnwu/magisk_files/"
    bot = context.bot
    magisk_dict = {
        "*Stable*": "master/stable.json",
        "\n" "*Canary*": "canary/canary.json",
    }.items()
    releases = "*Latest Magisk Releases:*\n\n"
    for magisk_type, release_url in magisk_dict:
        canary = "https://github.com/topjohnwu/magisk_files/raw/canary/" if "Canary" in magisk_type else ""
        data = get(link + release_url).json()
        releases += (
            f"{magisk_type}:\n"
            f'• Manager - [{data["app"]["version"]} ({data["app"]["versionCode"]})]({canary + data["app"]["link"]}) \n'
            f'• Uninstaller - [Uninstaller {data["magisk"]["version"]} ({data["magisk"]["versionCode"]})]({canary + data["uninstaller"]["link"]}) \n'
        )
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=releases,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    
def orangefox(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    device = " ".join(args)
    link = get(f"https://api.orangefox.download/v3/releases/?codename={device}&sort=date_desc&limit=1")
    if not device:
        update.effective_message.reply_text("Error: use /ofox codename")
        return
    elif link.status_code == 404:
        message = f"OrangeFox currently is not avaliable for {device}"
    else:
        page = loads(link.content)
        file_id = page["data"][0]["_id"]
        link = get(f"https://api.orangefox.download/v3/devices/get?codename={device}")
        page = loads(link.content)
        oem = page["oem_name"]
        model = page["model_name"]
        full_name = page["full_name"]
        link = get(f"https://api.orangefox.download/v3/releases/get?_id={file_id}")
        page = loads(link.content)
        dl_file = page["filename"]
        build_type = page["type"]
        version = page["version"]
        changelog = page["changelog"][0]
        size = page["size"]
        dl_link = page["mirrors"]["DL"]
        date = page["date"]
        md5 = page["md5"]
        message = f"<b>Latest OrangeFox Recovery for the {full_name}</b>\n\n"
        message += f"• Manufacturer: {oem}\n"
        message += f"• Model: {model}\n"
        message += f"• Codename: {device}\n"
        message += f"• Release type: official\n"
        message += f"• Build type: {build_type}\n"
        message += f"• Version: {version}\n"
        message += f"• Changelog: {changelog}\n"
        message += f"• Size: {size}\n"
        message += f"• Date: {date}\n"
        message += f"• File: {dl_file}\n"
        message += f"• MD5: {md5}\n\n"
        message += f"• <b>Download:</b> {dl_link}\n"
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

def twrp(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    device = " ".join(args)
    link = get(f"https://eu.dl.twrp.me/{device}")
    if not device:
        update.effective_message.reply_text("Error: use /twrp codename")
        return
    elif link.status_code == 404:
        message = f"TWRP currently is not avaliable for {device}"
    else:
        page = BeautifulSoup(link.content, "lxml")
        download = page.find("table").find("tr").find("a")
        dl_link = f"https://eu.dl.twrp.me{download['href']}"
        dl_file = download.text
        size = page.find("span", {"class": "filesize"}).text
        date = page.find("em").text.strip()
        message = f"<b>Latest TWRP for the {device}</b>\n\n"
        message += f"• Release type: official\n"
        message += f"• Size: {size}\n"
        message += f"• Date: {date}\n"
        message += f"• File: {dl_file}\n\n"
        message += f"• <b>Download:</b> {dl_link}\n"
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    
commands = {
    magisk : ['magisk', 'root', 'su'],
    orangefox : ['ofox'],
    twrp : ['twrp']
}
