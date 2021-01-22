# Cryptofinance Assignments

The assignements are as follow:
1. Simulation of Satoshi's original attack on Bitcoin
2. Simulation of the selfish mining attack on Bitcoin and Bcash

Before starting to explain the simulation processes; let us give a brief introduction on what is a blockchain and what are these attacks strategies. 


# What is a Blockchain?

Blockchain is a decentralized data structure that can be defined by a list of records, also called blocks, that can contain data from any type and that are linked by means of cryptographic references. [[1]](#1)

In 2008 Satoshi Nakamoto published the article 'Bitcoin: A Peer-to-Peer Electronic Cash System', which uses blockchain as a central part of the proposed implementation of the Bitcoin cryptocurrency. [[1]](#1)

Actually the Bitcoin cryptocurrency records its transactions in a public log which is the blockchain. [[3]](#3)

As we said it earlier, bitcoin blockchain consists of blocks. Each block can contain number of transaction. The following figure shows the bitcoin blocks structure.

![1](https://user-images.githubusercontent.com/72521500/105473700-adc63100-5c9d-11eb-839f-84c9fe7371f2.JPG)


All transactions must be broadcast to the network and to be validated through a process called mining. Mining is a distributed consensus system that is used to validate transactions by including them in the block chain. It enforces a chronological order in the block chain, and allows different nodes to agree on the state of the system. [[2]](#2)

Thus, to ensure transactions, blocks need to be mined. That's achieved resolving a cryptopuzzle with increasing complexity, requiring computer resources as Proof of Work.

Proof of Work is a technique in that the network participant must perform hard computational work to be able to insert the new block on the chain with two specific properties: the difficulty and the nonce.

The difficulty is a property used to regulate the speed that blocks are added to the chain. And the nonce must be changed in order to generate new hash results until the hash function reaches the expected result by the network.

This work is computationally intense and tends to get more difficult with the increased computational capacity of network participants [[1]](#1). But what are the miners incentives to perform such an intense computation?

Actually mining is the process by which new bitcoin is added to the money supply. Miners provide processing power to the bitcoin network in exchange for the opportunity to be rewarded bitcoin. [[4]](#4)

Miners receive two types of rewards for mining: new coins created with each new block, and transaction fees from all the transactions included in the block. To earn this reward, the miners compete to solve a difficult mathematical problem based on a cryptographic hash algorithm which is the proof of work. [[4]](#4)

The amount of newly created bitcoin a miner can add to a block decreases approximately every four years (or precisely every 210,000 blocks). It started at 50 bitcoin per block in January of 2009 and until approximately the year 2140, no new bitcoins will be issued. [[4]](#4)

Bitcoin miners also earn fees from transactions. Every transaction may include a transaction fee. The winning bitcoin miner gets to “keep the change” on the transactions included in the winning block. However, as the reward decreases over time and the number of transactions per block increases, a greater proportion of bitcoin mining earnings will come from fees. [[4]](#4) 

Now that we briefly introduce block chain and how it is a shared public ledger on which the entire Bitcoin network relies. We want to describe the strategies behind double spend attack and selfish mining attack. 

# Double Spend Attack
As Nakamato says it is the situation where a malicious miner makes a payment, then in the secret tries to validate a second conflicting transaction in a new block, from the same address, but to a new address that he controls, which allows him to recover the funds. [[5]](#5) 

Once the first transaction has been validated in a block in the official blockchain and the vendor delivered the goods (the vendor will not deliver unless some confirmations are visible), the only possibility consists in rewriting the blockchain from that block. [[5]](#5) 

If the attacker controls a majority of hash rate <sup>[1](#myfootnote1)</sup>, that is, if his relative hash rate q be greater than 1\2, then he is able to mine faster that the rest of the network so he can rewrite the last end of the block chain as he desires. This is the reason why a decentralized mining is necessary so that no one can control more than half of the mining power. [[5]](#5) 

Now if the attacker hash rate be 0<q<1\2 , even by this hash rate the attacker can attempt a double spend and will succeed with a non zero probability. [[5]](#5) 

We simulated this attack on Bitcoin. The following plot shows the revenue of a double spend attack based on the attacker hash rate.

![2](https://user-images.githubusercontent.com/72521500/105473781-c7677880-5c9d-11eb-9ae8-d70adf2dde0a.jpeg)

# Selfish Mining Attack

Here miner instead of publishing a new block, keeps the block secret and tries to build a longer blockchain increasing its advantage. [[5]](#5)  

And when he makes his blockchain public, he will orphan the last mined honest block and will recap the rewards.

To be precise the attack cycles are defined as follows: [[5]](#5) 
1. The miner starts mining a block on top of the official blockchain.
2. If an honest miner finds a block first then the cycles ends and he starts over.
3. Otherwise; when he is first to find a block, he keeps mining on top of it and keeping it a secret.
4. If before he mines a second block the honest network mines one public block, then he publish his block immediately; thus trying to get the maximal proportion 0<\gamma<1 <sup>[2](#myfootnote2)</sup> of honest miners adopting his block.
5. A competition follows, and if the next block is mined on top of the honest block, then the selfish miner losses the rewards of his block and the attack cycle ends.
6. And if the attacker or his allied honest miners, mine the next block, then they publish it, and the attack cycle ends again.

Also we simulated this attack on both Bitcoin and BCash. Following plots show the revenue plot of selfish mining attack based on attacker hash rate.	 

![3](https://user-images.githubusercontent.com/72521500/105478939-25975a00-5ca4-11eb-9cb9-ce2c0efcd389.jpeg)

Note that the green line is the theoretical line that represents the minimum hash rate before the attack becomes profitable given the connectivity.

![4](https://user-images.githubusercontent.com/72521500/105478965-30ea8580-5ca4-11eb-8ce1-c286da5d3668.jpeg)


<a name="myfootnote1">1</a>: The number of attempts made per second by miner to vary the nonce is called hash rate or hash power.

<a name="myfootnote2">2</a>: The efficiency depends on the new parameter <img src="http://www.sciweavers.org/tex2img.php?eq=%5Cgamma&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt="\gamma" width="17" height="17" /> which represents attacker's good connectivity to the network

## References
<a id="1">[1]</a> 
Medium: A Technical Introduction to Blockchain,
[Medium website] (https://medium.com/better-programming/a-technical-introduction-to-blockchain)

<a id="2">[2]</a>
Bitcoin: How does Bitcoin work?,
(https://bitcoin.org/en/how-it-works)

<a id="3">[3]</a>
Eyal, Ittay and Sirer, Emin Gun, *Majority is Not Enough: Bitcoin Mining is Vulnerable*, Commun.ACM 61, (2018) 95–102.

<a id="4">[4]</a>
Andreas M.Antonopoulos, *Mastering Bitcoin*, O'Reilly Media, Inc, (2014) chapter 8.


<a id="5">[5]</a>
Grunspan, Cyril & Pérez-Marco, Ricardo, *The mathematics of Bitcoin*, (2020). 
