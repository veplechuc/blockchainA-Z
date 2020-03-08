import datetime
import hashlib
import json
from flask import Flask, jsonify

#building Blockchain

PROOF = 1
INITIAL_HASH = '0'

LEADING_ZEROS = '0000'

class Blockchain:
    
    def __init__(self):
        self.chain = []
        #create gensis block
        self.create_block(proof=PROOF, previous_hash=INITIAL_HASH)

    def create_block(self, proof, previous_hash):
        block = {'index':len(self.chain)+1,
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'previous_hash': previous_hash
                }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == LEADING_ZEROS:
                check_proof =True
            else:
                new_proof +=1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        #first check the hash of the current block is = to the hash of the previous block
        #genesis block
        previous_block = chain[0]
        block_index = 1 #value for index that is in the block
        while block_index < len(chain):
            current_block = chain[block_index]
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

#definig the mining
#create the flask app
app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'Great block created',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof' : block['proof'],
                'previous_hash': block['previous_hash']}

    return jsonify(response) , 200

