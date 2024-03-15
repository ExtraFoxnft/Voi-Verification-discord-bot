import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD_IDS = [int(guild_id) for guild_id in os.getenv("GUILD_IDS").split(",") if guild_id]  # Convert to list of integers

# Define intents with all available intents enabled
intents = discord.Intents.all()

# Create a new discord bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to get tokens owned by a user from the public indexer
def get_tokens_owned(user_address):
    try:
        # Query the account information
        response = requests.get(f"{API_BASE_URL}/nft-indexer/v1/tokens", headers={"x-api-key": API_KEY}, params={"owner": user_address})
        response.raise_for_status()
        return response.json().get('tokens', [])
    except Exception as e:
        return []

# Placeholder function for validating Voi addresses
def validate_address(address):
    return len(address) == 58 and address.isalnum()

# Define a function to handle bot commands
@bot.command()
async def verify(ctx, address: str):
    try:
        # Convert the short address to a public key
        public_key = address
        
        # Check if the address is a valid Voi address
        if not validate_address(public_key):
            await ctx.send("Please provide a valid Voi address.")
            return

        # Query the account information
        tokens_owned = get_tokens_owned(public_key)

        # Initialize count of occurrences
        count = 0

        # Check if any token has the desired name
        for token in tokens_owned:
            metadata_uri = token.get('metadataURI')
            if metadata_uri:
                metadata_response = requests.get(metadata_uri)
                if metadata_response.status_code == 200:
                    metadata = metadata_response.json()
                    name = metadata.get('name', '').lower()
                    # Increment count if name contains "gem3d"
                    if 'gem3d' in name:
                        count += 1

        if count > 0:
            # Add "tester" role to the user upon successful verification
            guild = ctx.guild
            if guild.id in GUILD_IDS:
                role = discord.utils.get(guild.roles, name="tester")
                if role:
                    await ctx.author.add_roles(role)
                    await ctx.send(f"NFT ownership verified. The user owns {count} NFT(s) with 'gem3d' in their name. Role 'tester' added.")
                else:
                    await ctx.send("Role 'tester' not found. Please make sure the role exists and try again.")
            else:
                await ctx.send("You can only verify in specific servers.")
        else:
            await ctx.send("You do not own any NFTs with 'gem3d' in their name from the specified wallet.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Run the bot with your bot token from environment variables
bot.run(BOT_TOKEN)
