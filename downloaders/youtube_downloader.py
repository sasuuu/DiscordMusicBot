import yt_dlp
import asyncio

YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

async def get_info_from_url(url, *, loop=None):
    loop = loop or asyncio.get_event_loop()
    ytdl = yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS)
    try:
        return await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
    except:
        return None