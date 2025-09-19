import os
from dotenv import load_dotenv
from telethon import TelegramClient, events  # <- IMPORTANTE

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
group_id = int(os.getenv("GROUP_ID"))

# Inicializa el cliente
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    print("🔄 Iniciando...")

    try:
        await client.start(phone_number)
        print("✅ Cliente activo.")
    except Exception as e:
        print(f"❌ Error al iniciar: {e}")
        return

    @client.on(events.NewMessage(chats=group_id))
    async def moderar(event):
        # Captura robusta del texto, ya sea mensaje normal o caption
        text = event.raw_text.lower() if event.raw_text else ""

        if not text:
            return

        try:
            if "[⚠️] importante ➩" in text:
                await event.delete()
                print("🗑 Borrado: mensaje con IMPORTANTE")

            elif "comando no está incluido en tu plan" in text:
                await event.delete()
                await event.respond(
                    "⚠️ Mejora tu plan para usar este comando.\nEscribe /buy para más información."
                )
                print("💬 Respuesta enviada: mejora de plan")

            elif "no tienes suficientes monedas o una suscripción." in text:
                await event.delete()
                await event.respond(
                    "⚠️ No tienes un plan activo.\nEscribe /buy para ver los disponibles."
                )
                print("💬 Respuesta enviada: sin monedas o suscripción")

        except Exception as e:
            print(f"⚠️ Error moderando mensaje: {e}")

    print("📡 Moderando mensajes...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
