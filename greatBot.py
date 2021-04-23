import asyncio
import os, re
import discord
from dotenv import load_dotenv
from discord.ext import commands
from time import time
from constants import *

from Controllers import *


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '%', case_insensitive = True, intents = intents)

factsRepo = FactsRepository(factsFile)
shuffledRepo = ShuffledFactsRepository(shuffledFile, factsRepo)
factsCtr = FactsController(factsRepo, shuffledRepo)

punishedUsersRepo = PunishedUsersRepository(punishedUsersFile)
punishedUsersCtr = PunishedUserController(punishedUsersRepo)

teasingInfoRepo = TeasingInfoRepository(teasingInfoFile)
teasedRepo = TeasedRepository(teasedFile)
teasingInfoCtr = TeasingInfoController(teasingInfoRepo)
teasedCtr = TeasedController(teasedRepo)

typingUsersRepo = TypingUsersRepository(typingUsersFile)
typingUsersCtr = TypingUsersController(typingUsersRepo)


@bot.command(name = 'fact', help = 'Generate a random fact')
async def randomFact(ctx):
    fact = factsCtr.getRandomFact()
    await ctx.send(fact)

@bot.command(name = 'add_fact', help = 'Add a fact. It will be shortly deleted if it has no relevance!')
async def addFact(ctx, *text):
    content = ''
    for word in text:
        content += (word + ' ')
    content = content[:-1]
    factsCtr.addFact(content, ctx.message.author.name)
    await ctx.send('l-am bagat in lista')

@bot.command(name = 'facts_ranking', help = 'Check the number of thumbs up and thumbs downs every fact has.')
async def factRankings(ctx):
    factsSorted = factsCtr.getDescendingSortedFacts()
    msg = ''
    for i, fact in enumerate(factsSorted, start = 1):
        msg += f'{i}.{fact}\n'
    await ctx.send(msg)

@bot.event
async def on_reaction_add(reaction, _):
    likeReaction = '👍'
    dislikeReaction = '👎'
    msg = reaction.message.content
    if not re.search('^.+\(added by:.+\); thumbsUp:[0-9]+; thumbsDown:[0-9]+$', msg):
        return
    for fact in factsCtr.factsIterate():
        factContent = str(fact).split(';')[0]
        msgContent = msg.split(';')[0]
        if msgContent == factContent:
            toUpdate = fact
            break
    if str(reaction.emoji) == likeReaction:
        factsCtr.updateThumbsUp(toUpdate.getText())
    elif str(reaction.emoji) == dislikeReaction:
        factsCtr.updateThumbsDown(toUpdate.getText())


@bot.command(name = 'punish', help = 'Punish a user by mentioning him after the command')
#@commands.has_any_role('KING', 'admin')
async def punish(ctx, curseType:int):
    #ToDo: punish those who try to punish the king
    #ToDo: punish all
    author = ctx.message.author
    punished = ctx.message.mentions[0]
    punishedRole = discord.utils.get(ctx.guild.roles, name='punished')
    initialChannel = author.voice.channel

    if curseType not in [1, 2]:
        await ctx.send(f'{author.mention}, tipul de punishment e 1 sau 2')
        return

    if punished.id == owner_id:
        await ctx.send(f'{author.mention}, tu chiar ai crezut?:)))))))))))))))))))))')
        return

    admin = author.id == owner_id
    allowed = True
    if not admin:
        user = punishedUsersCtr.getUserById(author.id)
        if user is not None:
            if time() - user.getTimer() < punishedTimer:
                allowed = False
                waitingTime = int(punishedTimer - (time() - user.getTimer()))
                await ctx.send(f'Ba {author.mention}, vezi ca mai ai de asteptat '
                               f'{waitingTime} secunde, nu ne grabim nicaieri.')
            else:
                punishedUsersCtr.removeUser(author.id)
    if allowed or admin:
        #ToDo: maybe punish even if the target is in another channel
        if punished not in initialChannel.members:
            await ctx.send(f'{punished.mention} nu-i aici, nu-l poti pedepsi nimic nu stii')
            return
        lastMsg = await ctx.send(f'{author.mention} il va pedepsi pe {punished.mention}')
        await lastMsg.add_reaction('😈')
        if not admin:
            punishedUsersCtr.addUser(author.id, time())

        if curseType == 1:
            try:
                roles = punished.roles
                timer = time()
                for role in roles:
                    if role.name != '@everyone':
                        await punished.remove_roles(role)
                await punished.add_roles(punishedRole)

                while time() - timer < punishDurationType1:
                    for channel in ctx.guild.voice_channels:
                        if time() - timer > punishDurationType1:
                            break
                        await punished.move_to(bot.get_channel(channel.id))
                        await asyncio.sleep(0.69)

                await punished.move_to(initialChannel)
            except discord.errors.HTTPException:
                await asyncio.sleep(punishDurationType1 - (time() - timer))

            await punished.remove_roles(punishedRole)
            for role in roles:
                if role.name != '@everyone':
                    await punished.add_roles(role)
            await punished.edit(mute = False)

        elif curseType == 2:
            await punished.move_to(bot.get_channel(punishedChannel))
            await punished.edit(mute = False)

            roles = punished.roles
            for role in roles:
                if role.name != '@everyone':
                    await punished.remove_roles(role)
            await punished.add_roles(punishedRole)

            await asyncio.sleep(punishDurationType2)

            await punished.remove_roles(punishedRole)
            for role in roles:
                if role.name != '@everyone':
                    await punished.add_roles(role)

            await punished.edit(mute = False)
            await punished.move_to(initialChannel)


@bot.command(name = 'clear_timers', help = 'Clean all timers for punishing')
@commands.has_role('KING')
async def clearTimers(ctx):
    if ctx.message.author.id == owner_id:
        punishedUsersCtr.clearData()
        teasedCtr.clearData()
        teasingInfoCtr.clearData()
        await ctx.send('Am curatat cronometrele cu succes!')

@bot.command(name = 'clear_timer', help = 'Clean timer for a specific user')
@commands.has_role('KING')
async def clearTimerFor(ctx):
    if ctx.message.author.id == owner_id:
        user = ctx.message.mentions[0]
        punishedUsersCtr.removeUser(user)
        await ctx.send(f'{user.mention} acuma esti curat frt')

@bot.command(name = 'tease', help = 'Mention someone you want to annoy')
async def tease(ctx, *text):

    author = ctx.message.author
    teased = ctx.message.mentions[0]

    key = ''
    for word in text:
        if word[0] != '<':
            key += word + ' '
    key = key[:-1]

    if teased.id == owner_id:
        await ctx.send(f'{ctx.message.author.mention}, te-ai gandit mult?')
        return

    admin = author.id == owner_id
    teasable = True

    #discord.utils.get(ctx.guild.roles, name="KING") not in ctx.message.author.roles:
    if not admin:
        teaseInfo = teasingInfoCtr.getTeaseByTeasedId(teased.id)
        if teaseInfo is not None:
            await ctx.send(f'{author.mention} lasa-l pe {teased.mention} ca are destule pe cap')
            teasable = False

        if teasable:
            teasedUser = teasedCtr.getTeasedUserById(teased.id)
            if teasedUser is not None and time() - teasedUser.getTimer() < teasedTimer:
                await ctx.send(f'lasa-l pe saracu {teased.mention}, mai are dreptul la liniste inca '
                               f'{int(teasedTimer - (time() - teasedUser.getTimer()))} secunde.')
                teasable = False

    if admin or teasable:
        await ctx.send(f'{teased.mention}, trb sa scrii "%r {key}" ca sa poti vb si auzi din nou')
        await teased.edit(mute=True, deafen=True)
        teasingInfoCtr.addTease(teased.id, author.id, key)

@bot.command(name = 'r', help = 'Use this to bypass the teased curse')
async def replyToTease(ctx, *text):

    author = ctx.message.author

    typed = ''
    for word in text:
        typed += word + ' '
    typed = typed[:-1]

    teaseInfo = teasingInfoCtr.getTeaseByTeasedId(author.id)
    if teaseInfo is not None:
        if teaseInfo.getKeyText() == typed:
            if not typingUsersCtr.isUserInRepo(author.id):
                await ctx.send(f'{ctx.message.author.mention}, cam suspicios de rapid, '
                               f'mai incearca o data fara copy paste :*')
            else:
                await asyncio.sleep(1.5)
                await author.edit(mute = False, deafen = False)
                teasingInfoCtr.removeTease(teaseInfo.getTeasedId())
                if teaseInfo.getTeaserId() != owner_id:
                    teasedCtr.addUser(author.id, time())

        typingUsersCtr.removeUser(author.id)

@bot.event
#ToDo random messages
async def on_member_join(member):
    for channel in member.guild.channels:
        if channel.name == 'general':
            await channel.send(f'salut pisto {member.mention}')
    role = discord.utils.get(channel.guild.roles, name = 'NoRole')
    await member.add_roles(role)

@bot.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if channel.name == 'general':
            await channel.send(f'te-am pupat pe portofel, {member.mention}')

@bot.event
async def on_typing(_, author, __):
    if teasingInfoCtr.getTeaseByTeasedId(author.id) is not None and not typingUsersCtr.isUserInRepo(author.id):
        typingUsersCtr.addUser(author.id)

@bot.event
async def on_message_delete(msg):
    async for message in msg.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
        deleted_by = message.user
    if deleted_by.id != owner_id:
        if deleted_by == msg.author:
            to_send = f'{msg.author.mention}, dc ai vrut sa iti stergi mesajul: {msg.content}?'
        else:
            to_send = f'{deleted_by.mention}, dc ai vrut sa stergi mesajul lui {msg.author.mention}:\n' \
                           f'{msg.content}?'
        await msg.channel.send(to_send)

#ToDo message when someone disconnect another user

#@bot.event
#async def on_message(msg):
    #ToDo implement random messages
    #if msg.content[0] != '%' and msg.author.id == david_id:
       # randomMsg = 'ti-am dat voie sa vorbesti?'
        #await msg.channel.send(f'{msg.author.mention} {randomMsg}')
    #await bot.process_commands(msg)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)


#ToDo: give warnings and at 3 warnings kick, smt like that
#ToDo: english lines integration