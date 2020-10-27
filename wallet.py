import subprocess
import json
import os
from constants import BTC, ETH, BTCTEST
from web3 import Web3
from dotenv import load_dotenv
from eth_account import Account
load_dotenv() 
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

mnemonic = os.getenv("MNEMONIC")
priv_key = os.getenv("PRIVATE_KEY")

#i know i did this function incorrectly but i am not able to load web3 so i am having trouble figuring what i did wrong
def derive_wallets(coin, mnemonic, numderive):
    command = f"./derive -g --mnemonic='{mnemonic}'' --coin=btc --numderive=3 --format=json"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = p.communicate()
    
    keys = json.loads(output)
    return keys

derive_wallets(mnemonic, 'BTC', 2)

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

def create_tx(coin, account, recipient, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas({"from":account, "to":recipient, "value": amount})
        return {
        "from": account.address,
        "to": recipient,
        "value":amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address)}
    

    
        
def send_tx(coin, account, recipient, amount):
    tx = create_tx(coin, account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()

eth_acc = priv_key_to_account(ETH, '206cfff28db2ade68e81c02ccb2483449a20cd0147f8915efedbc12eaf43dfb9')

create_tx(BTCTEST,eth_acc,"0x94c21b954CcA25B292a387ddD9e0709b925454d7", 10)

send_tx(BTCTEST,eth_acc,"0xCEd13688851616CDE6C9f3A6f2393cFC24643A3E", 10) 

print(send_tx(ETH, "0x94c21b954CcA25B292a387ddD9e0709b925454d7", "0xCEd13688851616CDE6C9f3A6f2393cFC24643A3E", 10))



    








