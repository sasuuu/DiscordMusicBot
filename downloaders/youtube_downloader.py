import youtube_dl
import asyncio

YTDL_FORMAT_OPTIONS_BASE = {
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

async def get_url_info(url, *, loop=None):
    loop = loop or asyncio.get_event_loop()
    ytdl = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS_BASE)
    return await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

async def download_from_url(url, *, loop=None):
    loop = loop or asyncio.get_event_loop()
    ytdl_format_options = YTDL_FORMAT_OPTIONS_BASE | {'outtmpl': 'downloaded_songs/%(title)s.%(ext)s'}
    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
    if 'entires' in data:
        data = data['entries'][0]
    filename = ytdl.prepare_filename(data)
    print(f'YoutubeDownloader: Starting song downloading for url: {url}')
    ytdl.download([url])
    print(f'YoutubeDownloader: Song for url: {url} downloaded')
    return filename