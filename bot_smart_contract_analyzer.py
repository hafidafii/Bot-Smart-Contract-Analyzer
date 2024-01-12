"""
ARWallet

ETHERSCAN_API_KEY = 'XG9FUHR74C3SYWC5YA5CJQX4VJBDEB2YU6'  # Ganti dengan API key Anda dari Etherscan
TELEGRAM_BOT_TOKEN = '969681382:AAFzz6k6TbUkW8f0er0lCEdzT-nTx8bHTbk'  # Ganti dengan token bot Telegram Anda

"""

import re
import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from web3 import Web3, EthereumTesterProvider
from eth_tester import EthereumTester
import requests
import json
import datetime
from eth_utils import to_checksum_address 
from eth_account import Account

API_TOKEN = '5984964979:AAHWZsQmwOJhBN8VAlLUO-YKzREDReGdhlM'
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# @dp.message_handler()
@dp.message_handler()
async def on_message(message: types.Message):
    text = message.text

    contract_address_pattern = re.compile(r'^(0x)?[0-9a-fA-F]{40}$')

    contract_match = contract_address_pattern.match(text)
    w3_bsc = Web3(Web3.HTTPProvider('https://bsc-dataseed4.ninicoin.io'))

    print(contract_match.group(0))
    contract_address = str(contract_match.group(0))
    api_bsc = f"https://api.bscscan.com/api?module=contract&action=getabi&address={contract_address}&apikey=EJYGGZAFHAZUC1SBUE7GHY161T7J5BVDBM"
    response = requests.get(api_bsc)
    data_bsc = response.json()
    abi_bsc = data_bsc['result']
    try:
        ca_bsc = w3_bsc.to_checksum_address(contract_address)
        contract = w3_bsc.eth.contract(address=ca_bsc, abi=abi_bsc)
        decimal = contract.functions.decimals().call()
        supply = int(contract.functions.totalSupply().call() / 10**decimal)
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        owner = contract.functions.owner().call() 
        if contract_match:
            # await message.reply(f"Coba")
            keyboard = InlineKeyboardMarkup()
            bscscan = f"https://bscscan.com/token/{ca_bsc}"
            button = InlineKeyboardButton('🔸 BSCScan', url=bscscan)
            keyboard.add(button)
            await message.reply(f"[@ARWallet_bot | Scanner | BSC]\nVerified ✅ \n\nContract Name : {name}\nSupply : {supply}\nSymbol : {symbol} \nOwner : {owner}", reply_markup=keyboard)
    except Exception as e:
        if str(e) == "Could not format invalid value 'Contract source code not verified' as field 'abi'":
            w3_eth = Web3(Web3.HTTPProvider('https://ethereum.publicnode.com'))
            api_eth = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey=XG9FUHR74C3SYWC5YA5CJQX4VJBDEB2YU6"
            response = requests.get(api_eth)
            data_eth = response.json()
            abi_eth = data_eth['result']
            ca_eth = w3_eth.to_checksum_address(contract_address)
            contract = w3_eth.eth.contract(address=ca_eth, abi=abi_eth)
            decimal = contract.functions.decimals().call()
            supply = int(contract.functions.totalSupply().call() / 10**decimal)
            name = contract.functions.name().call()
            symbol = contract.functions.symbol().call()
            owner = contract.functions.owner().call() 
            keyboard = InlineKeyboardMarkup()
            etherscan = f"https://etherscan.io/token/{ca_eth}"
            button = InlineKeyboardButton('🔹 Etherscan', url=etherscan)
            keyboard.add(button)
            if str(owner) == "0x000000000000000000000000000000000000dEaD" or str(owner) == "0x0000000000000000000000000000000000000000":
                await message.reply(f"[@ARWallet_bot | Scanner | ETH]\nVerified ✅ \n\nContract Name : {name}\nSupply : {supply}\nSymbol : {symbol} \nOwner : **Renounced**", reply_markup=keyboard)
            else:
                await message.reply(f"[@ARWallet_bot | Scanner | ETH]\nVerified ✅ \n\nContract Name : {name}\nSupply : {supply}\nSymbol : {symbol} \nOwner : {owner}", reply_markup=keyboard)
        else:
            await message.reply(f"{str(e)}")
            await message.reply(f"Belum verif")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
