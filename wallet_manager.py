import tkinter as tk
from tkinter import scrolledtext, messagebox
from web3 import Web3
import threading
import time

# Initialize Web3 with your Infura project ID
infura_url = "https://mainnet.infura.io/v3/crypto-wallet-managerV1111"
web3 = Web3(Web3.HTTPProvider(infura_url))

class WalletManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Wallet Manager")

        self.wallets = []
        self.found_phrases = []
        self.active_chains = {
            'ETH': False
        }

        # Create UI Elements
        self.wallet_display = scrolledtext.ScrolledText(root, width=50, height=20)
        self.result_display = scrolledtext.ScrolledText(root, width=50, height=20)
        self.phrase_display = scrolledtext.ScrolledText(root, width=50, height=10)
        self.start_button = tk.Button(root, text="Start", command=self.start_search)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_search)
        self.copy_button = tk.Button(root, text="Copy Phrases", command=self.copy_phrases)

        # Blockchain Tiles
        self.eth_button = tk.Button(root, text="ETH", command=lambda: self.toggle_chain('ETH'), width=10)

        # Layout
        self.wallet_display.pack(side="left", fill="both", expand=True)
        self.result_display.pack(side="right", fill="both", expand=True)
        self.phrase_display.pack(side="bottom", fill="both", expand=True)
        self.eth_button.pack(side="left")
        self.start_button.pack(side="bottom")
        self.stop_button.pack(side="bottom")
        self.copy_button.pack(side="bottom")

        self.searching = False
        self.search_thread = None

    def toggle_chain(self, chain):
        self.active_chains[chain] = not self.active_chains[chain]
        button = self.eth_button
        if self.active_chains[chain]:
            button.config(bg="lightgreen")
        else:
            button.config(bg="SystemButtonFace")

    def add_wallet(self, wallet, phrase):
        self.wallets.append(wallet)
        self.found_phrases.append((wallet, phrase))
        self.wallet_display.insert(tk.END, f"Added Wallet: {wallet}\n")

    def start_search(self):
        if not self.searching:
            self.searching = True
            self.wallet_display.insert(tk.END, "Starting search...\n")
            self.search_thread = threading.Thread(target=self.search_wallets)
            self.search_thread.start()

    def stop_search(self):
        if self.searching:
            self.searching = False
            self.wallet_display.insert(tk.END, "Stopping search...\n")
            if self.search_thread and self.search_thread.is_alive():
                self.search_thread.join()

    def search_wallets(self):
        while self.searching:
            for wallet, phrase in self.found_phrases:
                if self.active_chains['ETH']:
                    balance = self.get_balance(wallet)
                    if balance > 1:
                        self.result_display.insert(tk.END, f"Wallet: {wallet}, Balance: {balance} ETH\n")
                        self.phrase_display.insert(tk.END, f"Wallet: {wallet}, Phrase: {phrase}\n")
            time.sleep(10)  # Check every 10 seconds

    def get_balance(self, wallet):
        balance = web3.eth.get_balance(wallet)
        return web3.fromWei(balance, 'ether')

    def copy_phrases(self):
        self.root.clipboard_clear()
        phrases = "\n".join([f"Wallet: {wallet}, Phrase: {phrase}" for wallet, phrase in self.found_phrases])
        self.root.clipboard_append(phrases)
        messagebox.showinfo("Info", "Phrases copied to clipboard")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WalletManagerApp(root)
    root.mainloop()
