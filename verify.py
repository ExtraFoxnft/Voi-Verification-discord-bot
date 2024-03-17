import os
import discord
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv

load_dotenv()

# Get the environment variables
API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))  # Convert to integer
CREATOR_WALLETS = os.getenv("CREATOR_WALLETS").split(",")  # List of creator wallets
CREATOR_ROLES = os.getenv("CREATOR_ROLES").split(",")  # List of creator roles

# Define intents with all available intents enabled
intents = discord.Intents.all()

# Create a new discord bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Define a dictionary to store user IDs and their associated wallet addresses
user_wallets = {}

# Define a function to fetch all tokens created by the creator wallets
async def fetch_creator_tokens():
    creator_tokens = {}
    async with aiohttp.ClientSession() as session:
        try:
            for index, creator_wallet in enumerate(CREATOR_WALLETS):
                async with session.get(f"{API_BASE_URL}/nft-indexer/v1/collections", headers={"x-api-key": API_KEY}, params={"creator": creator_wallet}) as response:
                    response.raise_for_status()
                    data = await response.json()
                    # Map 'contractId' to the index of the creator wallet
                    tokens = {collection['contractId']: index for collection in data.get('collections', [])}
                    creator_tokens.update(tokens)
        except aiohttp.ClientResponseError as e:
            print(f"Error fetching tokens created by creator wallets: {e}")
    return creator_tokens

# Define a function to get tokens owned by a user
async def get_tokens_owned(owner_address):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE_URL}/nft-indexer/v1/tokens", headers={"x-api-key": API_KEY}, params={"owner": owner_address}) as response:
                response.raise_for_status()
                data = await response.json()
                return {token['contractId'] for token in data.get('tokens', [])}
        except aiohttp.ClientResponseError as e:
            print(f"Error fetching tokens owned by {owner_address}: {e}")
            return set()

# Placeholder function for validating Voi addresses
def validate_address(address):
    return len(address) == 58 and address.isalnum()

# Define a function to handle bot startup
@bot.event
async def on_ready():
    print('Bot is ready!')
    # Fetch creator tokens and store them in bot instance
    bot.creator_tokens = await fetch_creator_tokens()

# Define a function to handle the verify command
@bot.command()
async def verify(ctx, address: str):
    try:
        # Check if the address is a valid Voi address
        if not validate_address(address):
            await ctx.send("Please provide a valid Voi address.")
            return

        # Update the user's wallet address in the library
        user_wallets[ctx.author.id] = address

        # Fetch all tokens owned by the user
        user_tokens = await get_tokens_owned(address)

        # Initialize a list to store the roles to be assigned
        roles_to_assign = []

        # Check tokens owned by the user and map to corresponding roles
        for token_contract_id in user_tokens:
            if token_contract_id in bot.creator_tokens:
                # Get the index of the creator wallet
                creator_wallet_index = bot.creator_tokens[token_contract_id]
                # Map the index to the corresponding role
                role_name = CREATOR_ROLES[creator_wallet_index]
                roles_to_assign.append(role_name)

        # Get the guild and the member
        guild = bot.get_guild(GUILD_ID)
        member = guild.get_member(ctx.author.id)

        # Roles to remove are those that are not in roles_to_assign
        roles_to_remove = [role for role in member.roles if role.name in CREATOR_ROLES and role.name not in roles_to_assign]

        # Remove roles that the user should no longer have
        for role in roles_to_remove:
            await member.remove_roles(role)

        # Assign the corresponding roles
        for role_name in set(roles_to_assign):  # Use a set to avoid duplicate roles
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.add_roles(role)

        # Send a message based on the roles assigned and removed
        assigned_roles = ', '.join(set(roles_to_assign))
        removed_roles = ', '.join([role.name for role in roles_to_remove])
        response_message = f"Updated roles based on the NFTs you own."
        if assigned_roles:
            response_message += f"\nYou have been assigned the role(s): {assigned_roles}"
        if removed_roles:
            response_message += f"\nYou have been removed from the role(s): {removed_roles}"
        await ctx.send(response_message)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Run the bot with your bot token from environment variables
bot.run(BOT_TOKEN)
