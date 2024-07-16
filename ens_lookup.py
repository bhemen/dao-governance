"""
    Lookp ENS names corresponding to addresses on ENS
"""

from bs4 import BeautifulSoup
import pandas as pd
import time
import progressbar

#Selenium library for scraping data from Etherscan
#Etherscan doesn't seem to like requests
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
opts = FirefoxOptions()
opts.add_argument("--headless")
driver = webdriver.Firefox(options=opts)

#Web3 for getting data directly from the chain
from web3 import Web3
from web3.providers.rpc import HTTPProvider
from ens import ENS

api_url = "" #Need to supply an API provider (we've used nownodes)
provider = HTTPProvider(api_url)
web3 = Web3(provider)
ns = ENS(provider)

def lookup_name( addr, method="ns" ):
	if method == 'etherscan':
		try:
			url=f"https://etherscan.io/enslookup-search?search={eth_addr}"
			driver.get(url)
			html = driver.page_source
			soup = BeautifulSoup(html, "lxml")
		except Exception as e:
			raise e

		try:
			d = soup.find('div', attrs={'class':'card-body'})
			if d is not None:
				links = d.find_all('a')
				prefix = "enslookup-search?search="

				for a in links:
					if a['href'].find(prefix) == 0:
						ethname = a['href'][len(prefix):]
						return ethname
			else:
				print( html )
		except Exception as e:
			raise e

	if method == 'ns':
		ethname = ns.name(addr)
		if addr != ns.address(ethname): #https://docs.ens.domains/dapp-developer-guide/resolving-names#reverse-resolution
			if ethname is not None:
				print( f"Name mismatch! {ethname} -/-> {addr}" )
			ethname = None
		return ethname

	print( f"Error method '{method}' not in ['ns','etherscan']" )

#eth_addresses = pd.read_csv('addresses.csv',header=None)

method = "ns"

eth_addresses = pd.read_csv('data/voters.csv')
eth_addresses = set(eth_addresses['address'].unique())

known_address_file = f"data/ens_names_{method}.csv"

try:
	df = pd.read_csv(known_address_file)
	df = df.dropna(axis=0,subset=['address']) #This is potentially dangerous if there are other columns you care about
except Exception as e:
	print( e )
	df = pd.DataFrame(columns=["address","name"])

print( f"{df.shape[0]} addresses already known" )
print( f"Looking up names for {len(eth_addresses)} addresses" )
eth_addresses = list( eth_addresses.difference(df['address']) )
print( f"Looking up names for {len(eth_addresses)} addresses" )

#import sys
#sys.exit(1)

current_wait = base_wait = 1
max_wait = 300
i = 0

with progressbar.ProgressBar(max_value=len(eth_addresses)) as bar:
	while i < len(eth_addresses):
		eth_addr = eth_addresses[i]

		try:
			ethname = lookup_name(eth_addr,method=method)
		except Exception as e:
			print( e )
			time.sleep(current_wait)
			current_wait *= 2
			continue

		if ethname is not None:
			df = df.append( {'address':eth_addr,'name':ethname},ignore_index=True )

		current_wait = base_wait
		i += 1
		bar.update(i)
		
		if i%10 == 0:
			df.to_csv(known_address_file,index=False)

df.to_csv(known_address_file,index=False)
