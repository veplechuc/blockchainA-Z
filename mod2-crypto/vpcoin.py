import datetime
import hashlib
import json
from flask import request
import requests
from uuid import uuid4
from urllib.parse import urlparse
 

#building Blockchain

PROOF = 1
INITIAL_HASH = '0'

LEADING_ZEROS = '0000'

class Blockchain:
    
    def __init__(self):
        self.chain = []
        #first create a transaction before a block creation
        self.transations = []
        #create gensis block
        self.create_block(proof=PROOF, previous_hash=INITIAL_HASH)
        #handles all the nodes 
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {'index':len(self.chain)+1,
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'data': f'this fild just show some extra data, like index={len(self.chain)+1} and prev-hash={previous_hash}',
                'previous_hash': previous_hash,
                'transactions': self.transations
                }
        self.transations = []        
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            #need to use encode required by sha256
            # hexdigest returns hexadecimal value 
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == LEADING_ZEROS:
                check_proof =True
            else:
                new_proof +=1
        return new_proof

    def hash(self, block):
        #need to use encode required by sha256 
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        #first check the hash of the current block is = to the hash of the previous block
        #remember always to check the entire chain
        #genesis block
        previous_block = chain[0]
        block_index = 1 #value for index that is in the block
        while block_index < len(chain):
            current_block = chain[block_index]
            #first check equality on hashes
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            proof_previous_block = previous_block['proof']
            proof_current_block = current_block['proof']
            hash_operation = hashlib.sha256(str(proof_current_block **2 - proof_previous_block**2).encode()).hexdigest()
            #second check proof is valid
            if hash_operation[:4] != LEADING_ZEROS:
                return False
            previous_block = current_block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transations.append({
            'sender': sender,
            'receiver' : receiver,
            'amount' : amount
        })
        #return the index of the block = previous block +1
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
#concesus resolver -- replace the chain with the longest one
    def replace_chain(self):
        net = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        #for eac node in the net we requests the  lenght of the chain
        for node in net:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                node_chain_length = response.json['length']
                node_chain = response.json['chain']
                if node_chain_length > max_length and self.is_chain_valid(node_chain):
                    max_length = node_chain_length
                    longest_chain = node_chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

