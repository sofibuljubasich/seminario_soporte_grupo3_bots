from ast import alias
import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        # Atributos para saber si está reproduciendo o pausado
        self.is_playing = False
        self.is_paused = False

        # Lista para guardar las canciones a reproducir
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

     # Buscar canción en youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # Tomar la primera URL
            m_url = self.music_queue[0][0]['source']

            # Remover el primer elemento, porque ya se está reproduciendo
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            # Conectarse al voice channel
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                # En caso de que no pueda conectarse
                if self.vc == None:
                    await ctx.send("Fallo al intentar conectar al canal")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            # Remover el primer elemento, porque ya se está reproduciendo
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing"], help="Reproduce una canción seleccionada de youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            # Necesita estar conectado a un canal
            await ctx.send("Conéctate a un canal!")
        # elif self.is_paused:
            # self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("La canción no pudo descargarse. Formato incorrecto (no se aceptan playlist y/o livestream)")
            else:
                await ctx.send("Canción añadida a la cola")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pausa la canción que se está reproduciendo actualmente")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        # elif self.is_paused:
            # self.is_paused = False
            # self.is_playing = True
            # self.vc.resume()
 
    @commands.command(name = "resume", aliases=["r"], help="Reanuda la canción pausada")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Saltea la canción actual")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            # Intenta reproducir la siguiente canción en cola
            await self.play_music()


    @commands.command(name="queue", aliases=["q"], help="Muestra las canciones que están en cola")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # Muestra las siguientes 5 canciones en cola
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No hay canciones en cola")

    @commands.command(name="clear", aliases=["c", "bin"], help="Limpia la lista de reproducción")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Cola borrada con éxito")

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Desconecta al bot del voice channel")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()