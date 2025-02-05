# **XRPL Token Development**

This project enables **XRPL token creation** using an **object-oriented approach**, providing a structured way to manage **wallets, transactions, trustlines, and token issuance**.

## **📌 Features**
- **🔹 Wallet Helper (`WalletHelperXRPL`)**  
  - Create and load **hot & cold wallets** securely.
  - Check **wallet balances** to ensure funding before issuing tokens.
  
- **🔹 XRPL Client (`XRPLCLIENT`)**  
  - Connect to **Testnet or Mainnet** via XRPL JSON-RPC.
  
- **🔹 XRPL Token Issuance (`XRPLToken`)**  
  - Configure **issuer & operational wallets** securely.
  - Establish a **trustline** between wallets.
  - Issue tokens and handle transactions **with retries & error handling**.

---

## **📂 Project Structure**
```
ripple_token_creator/
│── wallet_helper_xrpl.py      # Wallet management class
│── xrpl_client.py             # XRPL JSON-RPC client
│── xrpl_token.py              # Token creation and transaction management
│── main.py                    # Execution script with user input
│── README.md                  # Documentation
```

---

## **🔧 Setup & Installation**
### **1️⃣ Install Dependencies**
Make sure you have **Python 3.7+** installed.

```sh
pip install -r requirements.txt
```

### **2️⃣ Create an `.env` File**
Create a `.env` file to store your **XRPL Testnet/Mainnet RPC URLs**.

```ini
TESTNET_RPC=https://s.altnet.rippletest.net:51234
MAINNET_RPC=https://xrplcluster.com
```

---

## **🚀 Usage**
### **1️⃣ Run the Script**
Run the **main script** and enter required details.

```sh
python main.py
```

### **2️⃣ User Inputs**
You will be prompted to enter:
- **XRPL Network** (`testnet` or `mainnet`)
- **Wallets file** (e.g., `testnet_wallets.json`)
- **Currency Code** (e.g., `KKH`)
- **Total Supply** (e.g., `1000000`)
- **Token Domain** (e.g., `kryptokush.org`)

### **3️⃣ Wallet Creation & Balance Check**
If wallets do not exist, the script will **generate** and store them securely.

✅ **Check balances** before token creation:
- If wallets are **unfunded**, deposit XRP manually.

### **4️⃣ Token Configuration & Issuance**
Once the balance is sufficient, the script:
1. Configures **issuer & hot wallet settings**.
2. Establishes a **trustline**.
3. Issues **tokens to the hot wallet**.

---

## **🛠 Technical Breakdown**
### **1️⃣ Wallet Management (`wallet_helper_xrpl.py`)**
Handles **wallet creation & loading**.
```python
wallet_helper = WalletHelperXRPL("testnet_wallets.json")
cold_wallet, hot_wallet = wallet_helper.create_testnet_wallets(xrpl_client)
```

### **2️⃣ Check Wallet Balance**
Ensures wallets have enough **XRP funding**.
```python
balance = token.check_balance(cold_wallet)
```

### **3️⃣ Token Issuance (`xrpl_token.py`)**
Configures **issuer settings, trustlines, and token transfers**.
```python
token.configure_issuer()
token.configure_hot_wallet()
token.create_trustline()
token.issue_tokens()
```

---

## **💡 Improvements & Best Practices**
- ✅ **Error Handling**: Catches **transaction failures & retries** on errors.
- ✅ **Balance Verification**: Ensures **wallets have enough XRP** before issuing tokens.
- ✅ **OOP Structure**: Uses **modular classes** for easy **reusability & maintenance**.

---

## **📖 Resources**
- **XRPL Documentation**: [XRPL.org](https://xrpl.org)
- **XRPL Explorer**: [Testnet Explorer](https://testnet.xrpl.org)

---

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE.md](LICENSE.md) for details.

## 🤝 Contributing
Feel free to fork, submit issues, or create pull requests.