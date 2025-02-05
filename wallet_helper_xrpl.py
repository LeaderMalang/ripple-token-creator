import xrpl.wallet
from xrpl.wallet import generate_faucet_wallet
import json
import os


class WalletHelperXRPL:
    def __init__(self,file_name:str):
            self.file_name=file_name
            self.cold_wallet=None
            self.hot_wallet=None

    def create_testnet_wallets(self,client):
        """Generate cold (issuer) and hot (operational) wallets for XRPL Testnet"""
        if not os.path.exists(self.file_name):
            print("🔹 Wallets file not found. Creating new wallets...")
            # 🏦 Step 1: Generate Wallets (For Testnet)
            print("🔹 Generating wallets...")
            self.cold_wallet = generate_faucet_wallet(client, debug=True)  # Issuer
            self.hot_wallet = generate_faucet_wallet(client, debug=True)  # Operational Wallet
            try:
                # Structure wallet data
                cold_wallet_data = {
                    "address": self.cold_wallet.address,
                    "seed": self.cold_wallet.seed,
                    "public_key": self.cold_wallet.public_key,
                    "private_key": self.cold_wallet.private_key
                }

                
            
                hot_wallet_data = {
                    "address": self.hot_wallet.address,
                    "seed": self.hot_wallet.seed,
                    "public_key": self.hot_wallet.public_key,
                    "private_key": self.hot_wallet.private_key
                }

                # Save wallets to a JSON file
                with open(self.file_name, "w") as f:
                    json.dump({"cold_wallet": cold_wallet_data, "hot_wallet": hot_wallet_data}, f, indent=4)

                print(f"✅ Wallets generated and stored securely in {self.file_name}")
                return self.hot_wallet,self.cold_wallet
            except Exception as e:
                print(f"❌ Error in wallet generation:{e}")
                return None,None
            
        else:
            print("🔹 Wallets filefound. loading a existing wallets...")
            return self.load_wallets()
        

    def create_wallets(self):
        """Generate cold (issuer) and hot (operational) wallets for XRPL Mainnet"""
        if os.path.exists(self.file_name):
            print("🔹 Wallets file found. Loading existing wallets...")
            return self.load_wallets()
        try:
            # Generate Cold (Issuer) Wallet
            cold_wallet = xrpl.wallet.Wallet.create()
            cold_wallet_data = {
                "address": cold_wallet.address,
                "seed": cold_wallet.seed,
                "public_key": cold_wallet.public_key,
                "private_key": cold_wallet.private_key
            }

            # Generate Hot Wallet
            hot_wallet = xrpl.wallet.Wallet.create()
            hot_wallet_data = {
                "address": hot_wallet.address,
                "seed": hot_wallet.seed,
                "public_key": hot_wallet.public_key,
                "private_key": hot_wallet.private_key
            }

            # Save wallets to a JSON file
            with open(self.file_name, "w") as f:
                json.dump({"cold_wallet": cold_wallet_data, "hot_wallet": hot_wallet_data}, f, indent=4)

            print(f"✅ Wallets generated and stored securely in  {self.file_name}")
        except Exception as e:
            print(f"❌ Error in wallet generation: {e}")
            return None, None
        return self.cold_wallet, self.hot_wallet


    def load_wallets(self):
        """Load wallets from JSON file"""
        
        try:
            with open(self.file_name, "r") as f:
                wallets = json.load(f)

            self.cold_wallet = xrpl.wallet.Wallet(
                public_key=wallets["cold_wallet"]["public_key"],
                private_key=wallets["cold_wallet"]["private_key"]
            )
            self.hot_wallet = xrpl.wallet.Wallet(
                public_key=wallets["hot_wallet"]["public_key"],
                private_key=wallets["hot_wallet"]["private_key"]
            )

            print(f"✅ Cold Wallet Loaded: {self.cold_wallet.address}")
            print(f"✅ Hot Wallet Loaded: {self.hot_wallet.address}")
            return self.cold_wallet,self.hot_wallet
        except FileNotFoundError:
            print(f"❌ Wallet file '{self.file_name}' not found!")
            return None, None
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON format in '{self.file_name}'!")
            return None, None    
        except Exception as e:
            print(f"❌ Error while reading wallet file: {e}")
            return None, None
        
        


