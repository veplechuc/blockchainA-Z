import datetime
import hashlib
import json
from flask import Flask, jsonify

#building Blockchain

PROOF = 1
INITIAL_HASH = '0'

class Blockchain:
    
    def __init__(self):
        self.chain = []
        #create gensis block
        self.create_block(proof=PROOF, previous_hash=INITIAL_HASH)

    def create_block(self, proof, previous_hash):
        block = {'index':len(self.chan)+1,
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'previous_hash': previous_hash
                }
        self.chain.append(block)
        return block
