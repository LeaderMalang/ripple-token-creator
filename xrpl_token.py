import xrpl
from xrpl.models.transactions import AccountSet, TrustSet, Payment
from xrpl.transaction import submit_and_wait
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.clients import JsonRpcClient
from xrpl.core.binarycodec.exceptions import XRPLBinaryCodecException
from xrpl.models.exceptions import XRPLModelException
from xrpl.transaction import XRPLReliableSubmissionException
from xrpl.clients import JsonRpcClient
from xrpl.models.requests.account_info import AccountInfo
import time
import os


class XRPLToken:
    def __init__(self, client: JsonRpcClient, cold_wallet, hot_wallet, currency_code: str, domain: str, total_supply: int):
        """Initialize the XRPL Token Issuance."""
        self.client = client
        self.cold_wallet = cold_wallet
        self.hot_wallet = hot_wallet
        self.currency_code = currency_code.upper()
        self.total_supply = total_supply
        self.domain = domain
        self.debug = os.getenv("DEBUG_MODE", "False").lower() == "true"  # Enable debug via env variable

    def log(self, message: str, error=False):
        """Centralized logging with error handling."""
        prefix = "❌" if error else "✅"
        print(f"{prefix} {message}")


   

    def check_balance(self,address: str):
        try:
            account_info_request = AccountInfo(account=address, ledger_index="validated")
            response = self.client.request(account_info_request)
            
            if "error" in response.result:
                print(f"⚠️ Error fetching balance: {response.result['error']}")
                return None

            return response.result["account_data"]["Balance"]  # Balance is in drops (1 XRP = 1,000,000 drops)
        except Exception as e:
            print(f"❌ Failed to fetch balance: {e}")
            return None
   

    def submit_transaction(self, transaction, wallet, retries=3, delay=3):
        """Handles transaction submission with retries and error handling."""
        for attempt in range(retries):
            try:
                response = submit_and_wait(transaction, self.client, wallet)
                if response.is_successful():
                    self.log(f"Transaction successful: {response.result}")
                    return response
                else:
                    self.log(f"Transaction failed: {response.result}", error=True)
            except (XRPLReliableSubmissionException, XRPLModelException, XRPLBinaryCodecException) as e:
                self.log(f"XRPL Exception: {e}", error=True)
            except Exception as e:
                self.log(f"Unexpected error: {e}", error=True)

            if attempt < retries - 1:
                self.log(f"Retrying transaction... ({attempt + 1}/{retries})")
                time.sleep(delay)

        self.log("Transaction failed after multiple attempts.", error=True)
        return None

    def configure_issuer(self):
        """Configures the issuer (cold wallet) settings with proper error handling."""
        # if not self.ensure_funded():
        #     return

        try:
            cold_settings_tx = AccountSet(
                account=self.cold_wallet.address,
                set_flag=2,
            )

            self.log("Configuring cold wallet as the issuer...")
            response = self.submit_transaction(cold_settings_tx, self.cold_wallet)
            if response:
                self.log("Issuer wallet successfully configured.")
            else:
                self.log("Failed to configure issuer wallet.", error=True)
        except Exception as e:
            self.log(f"Error configuring issuer: {e}", error=True)

    def configure_hot_wallet(self):
        """Configures the hot wallet settings safely."""
        # if not self.ensure_funded():
        #     return

        try:
             #📜 Step 4: Create Trust Line (Hot → Cold)
            TOKEN_CODE = self.currency_code
            trust_set_tx = TrustSet(
                account=self.hot_wallet.address,
                limit_amount=IssuedCurrencyAmount(
                    currency=TOKEN_CODE,
                    issuer=self.cold_wallet.address,
                    value=self.total_supply  # Large limit for demonstration
                )
            )

            self.log("Configuring hot wallet settings...")
            response = self.submit_transaction(trust_set_tx, self.hot_wallet)
            if response:
                self.log("Hot wallet successfully configured.")
            else:
                self.log("Failed to configure hot wallet.", error=True)
        except Exception as e:
            self.log(f"Error configuring hot wallet: {e}", error=True)

    def create_trustline(self):
        """Creates a trustline between hot and cold wallet with error handling."""
        # if not self.ensure_funded():
        #     return

        try:
            trust_set_tx = TrustSet(
                account=self.hot_wallet.address,
                limit_amount=IssuedCurrencyAmount(
                    currency=self.currency_code,
                    issuer=self.cold_wallet.address,
                    value=str(self.total_supply),
                ),
            )

            self.log("Establishing trustline between hot and cold wallet...")
            response = self.submit_transaction(trust_set_tx, self.hot_wallet)
            if response:
                self.log("Trustline successfully established.")
            else:
                self.log("Trustline creation failed.", error=True)
        except Exception as e:
            self.log(f"Error establishing trustline: {e}", error=True)

    def issue_tokens(self):
        """Issues tokens from cold wallet to hot wallet with retries."""
        # if not self.ensure_funded():
        #     return

        retries = 3
        for attempt in range(retries):
            try:
                issue_tx = Payment(
                    account=self.cold_wallet.address,
                    amount=IssuedCurrencyAmount(
                        currency=self.currency_code,
                        issuer=self.cold_wallet.address,
                        value=str(self.total_supply),
                    ),
                    destination=self.hot_wallet.address,
                )

                self.log(f"Issuing {self.total_supply} {self.currency_code} tokens...")
                response = self.submit_transaction(issue_tx, self.cold_wallet)

                if response:
                    self.log(f"Successfully issued {self.total_supply} {self.currency_code} tokens.")
                    return
                else:
                    self.log(f"Attempt {attempt + 1}/{retries} failed. Retrying...")
                    time.sleep(3)

            except Exception as e:
                self.log(f"Error issuing tokens (Attempt {attempt + 1}/{retries}): {e}", error=True)

        self.log("Token issuance failed after multiple attempts.", error=True)
