from xrpl.clients import JsonRpcClient
import os


class XRPLCLIENT:
    def __init__(self, network: str):
        """Initialize the XRPL Client with the given network (testnet/mainnet)"""
        
        # 🛠 Load RPC URLs from Environment Variables
        self.TESTNET_RPC = os.getenv("TESTNET_RPC", "https://s.altnet.rippletest.net:51234")  # Default Testnet URL
        self.MAINNET_RPC = os.getenv("MAINNET_RPC", "https://s1.ripple.com:51234")  # Default Mainnet URL
        
        # 🎯 Select Network
        network_url = {
            "testnet": self.TESTNET_RPC,  # Testnet URL
            "mainnet": self.MAINNET_RPC   # Mainnet URL
        }

        if network not in network_url:
            raise ValueError(f"❌ Invalid network '{network}'. Choose 'testnet' or 'mainnet'.")

        self.client = JsonRpcClient(network_url[network])
        print(f"✅ XRPL Client initialized for {network.upper()} at {network_url[network]}")

    def get_client(self):
        """Return the JSON-RPC Client"""
        return self.client
