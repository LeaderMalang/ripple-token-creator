from wallet_helper_xrpl import WalletHelperXRPL
from xrpl_client import XRPLCLIENT
from xrpl_token import XRPLToken
import sys


def get_valid_input(prompt, validator=lambda x: x.strip()):
    """Prompts the user for input and validates it."""
    while True:
        try:
            value = validator(input(prompt))
            if value:
                return value
        except ValueError:
            print("❌ Invalid input. Please try again.")

            
def validate_network(value):
    """Ensures the network input is valid."""
    value = value.strip().lower()
    if value not in ["testnet", "mainnet"]:
        raise ValueError("Invalid network. Choose 'testnet' or 'mainnet'.")
    return value


def validate_total_supply(value):
    """Ensures total supply is a valid integer."""
    total = int(value.strip())
    if total <= 0:
        raise ValueError("Total supply must be a positive number.")
    return total


# 📌 User Inputs with Validation
network = get_valid_input("Select XRPL network (e.g., testnet or mainnet): ", validate_network)
wallets_file = get_valid_input("Enter XRPL wallet file name (e.g., testnet_wallets.json or mainnet_wallets.json): ")
currency_code = get_valid_input("Enter the token currency code (e.g., 'KKH'): ").upper()
total_supply = get_valid_input("Enter the total supply of tokens: ", validate_total_supply)
domain = get_valid_input("Enter the issuing domain (e.g., 'kryptokush.org'): ")

# 🛠 Initialize XRPL Client
xrpl_client = XRPLCLIENT(network).get_client()

# 🔑 Wallet Helper
wallet_helper = WalletHelperXRPL(wallets_file)

# ✅ Load or Create Wallets
cold_wallet, hot_wallet = wallet_helper.load_wallets()
if not cold_wallet or not hot_wallet:
    print("🔹 Wallets not found. Creating new ones...")
    cold_wallet, hot_wallet = wallet_helper.create_testnet_wallets(xrpl_client)

# 🏦 Initialize XRPL Token
token = XRPLToken(
    client=xrpl_client,
    cold_wallet=cold_wallet,
    hot_wallet=hot_wallet,
    currency_code=currency_code,
    domain=domain,
    total_supply=total_supply
)

# 🚀 Ensure Wallets Are Funded Before Proceeding
cold_wallet_balance = token.check_balance(cold_wallet.address)
hot_wallet_balance = token.check_balance(hot_wallet.address)

if cold_wallet_balance is None or hot_wallet_balance is None:
    print("❌ Failed to retrieve wallet balances. Exiting...")
    sys.exit(1)

if int(cold_wallet_balance) < 20 or int(hot_wallet_balance) < 20:
    print("⚠️ Wallets are underfunded! Please deposit at least 20 XRP in each wallet.")
    sys.exit(1)

# 🏗️ Execute Token Setup
token.configure_issuer()
token.configure_hot_wallet()
token.create_trustline()
token.issue_tokens()

print("🎉 Token creation process completed successfully!")
