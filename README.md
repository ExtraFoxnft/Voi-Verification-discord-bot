# Discord NFT Verification Bot

This Discord bot verifies the ownership of NFTs stored in a user's wallet and grants users a specified role on Discord upon successful verification. It provides feedback to users through Discord messages and is customizable through environment variables.

## Features

- **NFT Ownership Verification**: Users can verify their ownership of NFTs by providing their wallet address.
- **Role Assignment**: Upon successful verification, users are assigned a specific role on the Discord server.
- **Role Management**: The bot can add or remove roles based on the current NFT holdings of the user.
- **User-Wallet Mapping**: Maintains a record of users and their associated wallet addresses to prevent multiple role assignments.

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies.
3. Create a `.env` file in the root directory of the project and provide the necessary environment variables:

    ```plaintext
    # .env file
    API_KEY=your_api_key_here
    API_BASE_URL=https://api.example.com
    BOT_TOKEN=your_discord_bot_token_here
    GUILD_ID=your_discord_guild_id_here
    CREATOR_WALLETS=wallet1,wallet2,wallet3
    CREATOR_ROLES=role1,role2,role3
    ```

    Replace the placeholders with your actual values:
    - `your_api_key_here`: Your API key for the NFT indexer service.
    - `https://api.example.com`: The base URL of the NFT indexer API.
    - `your_discord_bot_token_here`: Your Discord bot token.
    - `your_discord_guild_id_here`: The ID of your Discord server (guild).
    - `wallet1,wallet2,wallet3`: The wallets associated with the creator roles, separated by commas.
    - `role1,role2,role3`: The Discord roles to assign to users, corresponding to the creator wallets, separated by commas.

4. Run the bot using the command `python bot.py`.

## Usage

Invite the bot to your Discord server and use the `!verify` command followed by your wallet address to verify NFT ownership.

Example:

!verify <wallet_address>


## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
