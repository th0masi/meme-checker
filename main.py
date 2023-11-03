import time
from web3 import Web3


# ---SETTINGS--- #
rpc = "https://rpc.ankr.com/eth"
filename = "wallets"
# ---SETTINGS--- #


w3 = Web3(Web3.HTTPProvider(rpc))
_type = [0, 4]
contract_address = w3.to_checksum_address("0xb1911d8ffcc2d8ca6c5ea4f4f18be6ea675c1ce7")
abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "userAddress", "type": "address"},
            {"internalType": "enum ClaimType", "name": "claimType", "type": "uint8"},
        ],
        "name": "usersClaimData",
        "outputs": [
            {"internalType": "uint128", "name": "totalClaimable", "type": "uint128"},
            {"internalType": "uint128", "name": "claimed", "type": "uint128"},
        ],
        "stateMutability": "view",
        "type": "function",
    }
]


def is_valid_address(address_wallet):
    return w3.is_address(address_wallet) and w3.is_checksum_address(address_wallet)


def counter(address_wallet):
    contract = w3.eth.contract(address=contract_address, abi=abi)
    total = 0
    for claim_type in _type:
        claim_data = contract.functions.usersClaimData(
            address_wallet, claim_type
        ).call()
        avalible_claim = float(claim_data[0] / 10**18)
        total += avalible_claim

    return total


if __name__ == "__main__":
    with open(f"{filename}.txt", "r") as file:
        address_list = [line.strip() for line in file]
    print(f"Total wallets: {len(address_list)}")

    total_all = 0
    for address in address_list:
        if not is_valid_address(address):
            print(f"Error: address {address} not found")
            continue
        total_for_address = counter(address)
        print(address, round(total_for_address, 2))
        total_all += total_for_address
        time.sleep(0.4)

    print(f"Total: {round(total_all, 2)}")
