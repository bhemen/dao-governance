# Overview

This repository contains source code for scraping blockchain votes from five popular Ethereum DAOs

* [Aave](https://app.aave.com/governance/)
* [Compound](https://compound.finance/governance)
* [Lido](https://lido.fi/governance)
* [MKR](https://vote.makerdao.com)
* [Uniswap](https://uniswap.org/governance)

The scripts connect directly to an Ethereum node and scrape the events emitted by the governance contracts.

The data can be found in the [data](data) folder.

The Python notebook [analysis/data_viz.ipynb] can be used to recreate all the analyses and figures 
in [Blockchain Governance: An Empirical Analysis of User Engagement on DAOs](https://arxiv.org/abs/2407.10945)

