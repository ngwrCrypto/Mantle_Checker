import asyncio
import aiohttp

async def fetch_wallet_amount(session, wallet, index):
    url = f"https://mdi-quests-api-preprod.up.railway.app/reward-claim/active-pools/status?walletAddress={wallet}"
    async with session.get(url) as response:
        while True:
            if response.status == 200:
                result = await response.json()
                if result:
                    amount = float(result[0]["amount"])
                    print(f'{index+1}. {wallet} = {amount}')
                    return amount
                else:
                    print(f'{index+1}. {wallet} = 0')
                    return 0
            else:
                await asyncio.sleep(1)

async def main():
    wallets = read_txt("wallets.txt")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_wallet_amount(session, wallet, i) for i, wallet in enumerate(wallets)]
        amounts = await asyncio.gather(*tasks)

    print(f'\n{sum(amounts)}')

    time.sleep(10)

def read_txt(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

if name == "__main__":
    asyncio.run(main())
