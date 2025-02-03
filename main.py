import xrpl
from xrpl.wallet import generate_faucet_wallet
from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import AccountSet, TrustSet, Payment
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.transaction import submit_and_wait
from xrpl.models.requests import AccountLines, GatewayBalances

# 🎯 Select Network
network_url = {
    "testnet": "https://s.altnet.rippletest.net:51234",  # Testnet URL
    "mainnet": "https://xrplcluster.com"  # Mainnet URL
}

# 🔥 Set Network (Change this to "mainnet" for real transactions)
NETWORK = "testnet"  # Change to "mainnet" for production
client = JsonRpcClient(network_url[NETWORK])

# 🏦 Step 1: Generate Wallets (For Testnet)
print("🔹 Generating wallets...")
cold_wallet = generate_faucet_wallet(client, debug=True)  # Issuer
hot_wallet = generate_faucet_wallet(client, debug=True)  # Operational Wallet

# If using Mainnet, replace with pre-funded wallet seeds:
# cold_wallet = xrpl.wallet.Wallet.from_seed("seed")
# hot_wallet =xrpl.wallet.Wallet.from_seed("seed")

# 🏦 Step 2: Configure Cold Wallet (Issuer Account Settings)
cold_settings_tx = AccountSet(
    account=cold_wallet.address,
    transfer_rate=1001000000,  # 0.1% Transfer Fee
    tick_size=5,
    domain=bytes.hex("kryptokush.org".encode("ASCII")),  # Token's domain
    set_flag=8  # Enable Default Ripple (ASF_DEFAULT_RIPPLE)
)

print("🔹 Configuring Issuer (Cold) Wallet...")
submit_and_wait(cold_settings_tx, client, cold_wallet)

# 🔥 Step 3: Configure Hot Wallet (Requires Authorization)
hot_settings_tx = AccountSet(
    account=hot_wallet.address,
    set_flag=2  # Require Authorization for trust lines (ASF_REQUIRE_AUTH)
)

print("🔹 Configuring Operational (Hot) Wallet...")
submit_and_wait(hot_settings_tx, client, hot_wallet)

# 📜 Step 4: Create Trust Line (Hot → Cold)
TOKEN_CODE = "KKH"
trust_set_tx = TrustSet(
    account=hot_wallet.address,
    limit_amount=IssuedCurrencyAmount(
        currency=TOKEN_CODE,
        issuer=cold_wallet.address,
        value="10000000000"  # Large limit for demonstration
    )
)

print(f"🔹 Creating Trust Line for {TOKEN_CODE} from Hot Wallet to Issuer...")
submit_and_wait(trust_set_tx, client, hot_wallet)

# 🎁 Step 5: Issue Token (Cold → Hot)
issue_quantity = "5000"  # Number of KKH tokens to issue
send_token_tx = Payment(
    account=cold_wallet.address,
    destination=hot_wallet.address,
    amount=IssuedCurrencyAmount(
        currency=TOKEN_CODE,
        issuer=cold_wallet.address,
        value=issue_quantity
    )
)

print(f"🔹 Issuing {issue_quantity} {TOKEN_CODE} to Hot Wallet...")
submit_and_wait(send_token_tx, client, cold_wallet)

# 📊 Step 6: Check Balances
print("🔹 Checking Hot Wallet Token Balances...")
hot_balance_response = client.request(AccountLines(account=hot_wallet.address))
print(hot_balance_response.result)

print("🔹 Checking Issuer Token Balances...")
issuer_balance_response = client.request(GatewayBalances(
    account=cold_wallet.address,
    hotwallet=[hot_wallet.address]
))
print(issuer_balance_response.result)

# 🎉 Done
print(f"✅ {TOKEN_CODE} Token Created Successfully on {NETWORK.upper()}!")
print(f"🔹 Issuer Wallet (Cold): {cold_wallet.address}")
print(f"🔹 Operational Wallet (Hot): {hot_wallet.address}")
