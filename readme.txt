---

# Discord NFT Ownership Verifier

This is a Discord bot that verifies ownership of NFTs (Non-Fungible Tokens) on a specified blockchain network and grants users a specific role upon successful verification.

## Features

- **NFT Ownership Verification**: Users can verify their ownership of NFTs by providing their wallet address.
- **Role Assignment**: Upon successful verification, users are assigned a specific role on the Discord server.
- **Customizable Parameters**: The bot allows customization of parameters such as the API endpoint, API key, Discord bot token, and more through environment variables.

## Installation

1. Clone the repository to your local machine:
   
2. Install the required dependencies:
pip install discord
pip install requests
pip install python-dotenv
pip install algosdk

3. Create a `.env` file in the root directory of the project and provide the following environment variables:

    ```
    API_KEY=your_api_key
    API_BASE_URL=your_api_base_url
    BOT_TOKEN=your_bot_token
    GUILD_ID=your_guild_id
    ```

    Make sure to replace `your_api_key`, `your_api_base_url`, `your_bot_token`, and `your_guild_id` with your actual values.

4. Edit the `bot.py` file and specify the desired collection name and the role name:

    ```
    # Specify the collection name to verify
    COLLECTION_NAME = "your_collection_name"  
    
    # Specify the role name to assign
    ROLE_NAME = "Tester"  
    ```

5. Run the bot:

    ```
    python bot.py
    ```

## Usage

To use the bot, invite it to your Discord server and use the `!verify` command followed by your wallet address.

Example:

```
!verify <wallet_address>
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
