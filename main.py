import asyncio
import traceback
import yaml
from random import randint

from pyrogram import *
from pyrogram.raw.functions.messages import StartBot
from pyrogram.types import *
import sqlite3

try:
    userbotspammer = sqlite3.connect("userbot.db")
    userbotspammer.cursor().execute("CREATE TABLE IF NOT EXISTS gruppi (chatid INT)")
except:
    pass

def LoadScadenza():
    with open('Scadenza.yml', 'r') as Message:
        return yaml.safe_load(Message)

api_id = 2699748
api_hash = "b8bd204c463de7e163fcf7b3e57a94d7"

spamcheck = False
Scadenza = LoadScadenza()

Spammer = Client("userbots", api_id, api_hash, lang_code="IT")

@Spammer.on_message(filters.user("self") & filters.command("addgroup", "."))
async def groupadd(_, message):
    try:
        print(message.chat.type)
        if str(message.chat.type) == "ChatType.GROUP":
            print("yee")
            group = message.chat.id
            gruppo = await Spammer.get_chat(group)
            userbotspammer.cursor().execute("INSERT INTO gruppi (chatid) VALUES (?)", [gruppo.id])
            userbotspammer.commit()
            try:
                await Spammer.join_chat(gruppo)
            except:
                pass
            await message.edit(f"<b>✅ | Il Gruppo {gruppo.title} è stato aggiunto!</b>")
        else:
            group = message.text.split(" ")[1]
            gruppo = await Spammer.get_chat(group)
            userbotspammer.cursor().execute("INSERT INTO gruppi (chatid) VALUES (?)", [gruppo.id])
            userbotspammer.commit()
            try:
                await Spammer.join_chat(group)
            except:
                pass
            await message.edit(f"<b>✅ | Il Gruppo {gruppo.title} è stato aggiunto!</b>")
    except:
        traceback.print_exc()
        await message.edit("❌ | Errore in .addgroup!")

@Spammer.on_message(filters.user("self") & filters.command("remgroup", "."))
async def rimuovigruppo(_, message):
    try:
        count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]
        if count == 0:
            await message.edit("❌ | Non ci sono Gruppi!")
        else:
            group = await Spammer.get_chat(message.text.split(" ")[1])
            userbotspammer.cursor().execute("DELETE FROM gruppi WHERE chatid = ?", [group.id])
            userbotspammer.commit()
            await message.edit(f"✅ | Gruppo {group.title} è stato rimosso!")
    except:
        group = await Spammer.get_chat(message.text.split(" ")[1])
        await message.edit(f"❌ | Errore in .remgroup {group.title}")

@Spammer.on_message(filters.user("self") & filters.command("info", "."))
async def Info(client, message):
    await message.delete()
    bot = ""
    file_id = None
    if message.reply_to_message:
        info = await client.get_users(message.reply_to_message.from_user.id)
        if info.is_bot:
            bot += "✅"
        else:
            bot += "❌"
        try:
            async for photo in client.get_chat_photos(message.reply_to_message.from_user.id):
                file_id = photo.file_id
            await client.send_photo(message.chat.id, file_id, caption=f"""
**🔎 Informazioni utente

• 💭 Nome: {info.first_name}
• 🏷 Cognome: {info.last_name}
• 💡 ID: {info.id}
• ⚙️ Username: @{info.username}**
• 🤖 Bot: {bot}
• 📡 DataCenter: {info.dc_id}

• 🔗 PermaLink: [{info.first_name}](tg://user?id={info.id})
   """)
        except:
            await client.send_message(message.chat.id, f"""
**🔎 Informazioni utente

• 💭 Nome: {info.first_name}
• 🏷 Cognome: {info.last_name}
• 💡 ID: {info.id}
• ⚙️ Username: @{info.username}**
• 🤖 Bot: {bot}
• 📡DataCenter: {info.dc_id}

• 🔗 PermaLink: [{info.first_name}](tg://user?id={info.id})
    """)
    else:
        idusers = message.text.split(" ")[1]
        info = await client.get_users(idusers)
        if info.is_bot:
            bot += "✅"
        else:
            bot += "❌"
        try:
            async for photo in client.get_chat_photos(message.reply_to_message.from_user.id):
                file_id = photo.file_id
            await client.send_photo(message.chat.id, file_id, caption=f"""
**🔎 Informazioni utente

• 💭 Nome: {info.first_name}
• 🏷 Cognome: {info.last_name}
• 💡 ID: {info.id}
• ⚙️ Username: @{info.username}**
• 🤖 Bot: {bot}
• 📡DataCenter: {info.dc_id}

• 🔗 PermaLink: [{info.first_name}](tg://user?id={info.id})
""")
        except:
            await client.send_message(message.chat.id, f"""
**🔎 Informazioni utente

• 💭 Nome: {info.first_name}
• 🏷 Cognome: {info.last_name}
• 💡 ID: {info.id}
• ⚙️ Username: @{info.username}**
• 🤖 Bot: {bot}
• 📡DataCenter: {info.dc_id}

• 🔗 PermaLink: [{info.first_name}](tg://user?id={info.id})
 """)

@Spammer.on_message(filters.user("self") & filters.command("expiry", "."))
async def expiry(_, message):
    await message.edit("Lo spammer ti scade il " + Scadenza["time"])

@Spammer.on_message(filters.user("self") & filters.command("grouplist", "."))
async def listagruppi(_, message):
    count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]
    if count == 0:
        await message.edit("❌ | Non ci sono Gruppi!")
    else:
        gruppimsg = ""
        for gruppi, in userbotspammer.cursor().execute("SELECT chatid FROM gruppi").fetchall():
            gruppimsg += f"➥ {(await Spammer.get_chat(gruppi)).title} | <code>{(await Spammer.get_chat(gruppi)).id}</code>\n\n"
        await message.edit(f"<b>🗯 » Lista Gruppi:</b>\n\n{gruppimsg}")

timespam = None
messaggio = ""

@Spammer.on_message(filters.user("self") & filters.command("time", "."))
async def tempo(_, message):
    global timespam
    minuti = message.text.split(" ")[1]
    if len(message.text.split(" ")) > 1:
        try:
            int(minuti)
            if int(minuti) >= 300:
                timespam = int(minuti)
                await message.edit(f"Tempo impostato su {timespam} secondi")
                pass
            else:
                await message.edit("❌ | Il minimo sono 300 secondi")
                return
        except:
            return await message.edit("❌ | Specifica il tempo in secondi")

@Spammer.on_message(filters.user("self") & filters.command("setmex", "."))
async def setmex(_, message):
    global messaggio
    try:
        messaggio = message.text.replace(f".setmex", "")
        await message.edit(f"✅ | Messaggio impostato\n\n <code>{messaggio}</code>")
    except:
        await message.edit("❌ | Formato non corretto, .setmex Messaggio")

@Spammer.on_message(filters.user("self") & filters.command("spam", "."))
async def spamavviato(_, message):
    global spamcheck
    count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]
    if count == 0:
        await message.edit("❌ | Non ci sono Gruppi!")
    else:
        if not spamcheck:
            spamcheck = True
            await message.edit(f"✅ | Spam iniziato. Sto spammando in {count} gruppi")
            while spamcheck:
                for gruppi, in userbotspammer.cursor().execute("SELECT chatid FROM gruppi").fetchall():
                    try:
                        await Spammer.send_message(gruppi, messaggio)
                        await asyncio.sleep(0.5)
                    except:
                         await asyncio.sleep(0.5)
                await asyncio.sleep(int(timespam))
        else:
            await message.edit("❌ | Formato non corretto, .spam")

@Spammer.on_message(filters.user("self") & filters.command("elimina_lista", "."))
async def elimina_lista(_, message):
    userbotspammer.cursor().execute("DELETE FROM gruppi")
    userbotspammer.commit()
    await message.edit("✅ | Lista Gruppi cancellata")

@Spammer.on_message(filters.user("self") & filters.command("stop", "."))
async def stopspam(_, message):
    global spamcheck
    if spamcheck:
        spamcheck = False
        await message.edit("❌ | Spam terminato")
    else:
        await message.edit("⚠️ | Spam non avviato")

@Spammer.on_message(filters.user("self") & filters.command("verify", "."))
async def verifys(client, message):
    resolved = await Spammer.resolve_peer("@spambot")
    await Spammer.invoke(StartBot(bot=resolved, peer=resolved, random_id=randint(1000, 9999), start_param="e"))
    await asyncio.sleep(1)
    async for messagess in Spammer.get_chat_history("@spambot", 1):
        msg = messagess.text
    if msg.find("Good news") > -1 or msg.find("Buone notizie") > -1:
        await message.edit("**✅ | Non sei limitato**")
    else:
        await message.edit("**❌ | Sei limitato**")

@Spammer.on_message(filters.user("self") & filters.command(["hmm"], "."))
async def HMM(_, message):
    minuti = message.text.split(" ")[1]
    total = int(minuti) * 60
    await message.edit(f"✅ | {minuti} Minuti in secondi sono: {total}")

@Spammer.on_message(filters.user("self") & filters.command(["cmd", "help"], "."))
async def ai(_, message):
    await message.edit("**__🤖 Comandi:__** __[Press Here](https://telegra.ph/Comandi-UserBot-Spammer-08-01)__", disable_web_page_preview=True)



Spammer.run()

