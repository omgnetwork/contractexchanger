#!/usr/local/bin/python3

# Copyright 2019 OmiseGO Pte Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import namedtuple
import json
import logging

from flask import Flask
from flask import request


app = Flask(__name__)


class ContractExchanger:
    ''' Module for updating and retrieving smart contract data that has been
    deployed on a private Ethereum network or via geth --dev for Plasma MVP.
    This service should be instantiated once per laptop or once per cluster as
    there's no data persistence at the moment.

    This data is set and retrieved from the Childchain and Watcher services.
    '''
    ContractData = namedtuple(
        'ContractExchanger', 'contract_addr txhash_contract authority_addr'
    )
    Contract = None

    def __init__(self):
        logging.info('ContractExchanger data class instantiated')

    def set_contract_data(self, data: dict):
        ''' Set the contract data
        '''
        logging.critical(data)
        ContractExchanger.Contract = ContractExchanger.ContractData(
            data['contract_addr'],
            data['txhash_contract'],
            data['authority_addr']

        )
        logging.info(
            'Contract data set: {}'.format(ContractExchanger.Contract)
        )

    def get_contract_data(self) -> dict:
        ''' Get the contract data
        '''
        data = {}
        data['contract_addr'] = ContractExchanger.Contract.contract_addr
        data['txhash_contract'] = ContractExchanger.Contract.txhash_contract
        data['authority_addr'] = ContractExchanger.Contract.authority_addr
        logging.info('Contract data retrieved: {}'.format(data))
        return data


@app.route('/set_contract', methods=['POST', 'GET'])
def set_contract() -> str:
    ''' Sets the contract details

    Post to this API via:
    request = requests.post(
        'http://localhost:5000/set_contract',
        data=json.dumps({
            'contract_addr': '"0x071dadebbfd03e2895f3ee0eec602263c12eb9b2f"',
            'txhash_contract': '"0x501fde66462faca83f1b3b27d280300c8b9ad7cf141cc9e8f22fe8ac24286827"', # noqa E501
            'authority_addr': '"0xba8b150f1db94c13ba8b57a670b6884e643bc696"'
        })
    )
    '''
    contract_exchanger = ContractExchanger()
    if request.method == 'GET':
        return 'This API only accepts HTTP POST requests'

    if not request.data:
        return 'No data provided in API call'

    contract_exchanger.set_contract_data(json.loads(request.data))
    return 'Contract information set'


@app.route('/get_contract', methods=['POST', 'GET'])
def get_contract() -> dict:
    ''' Returns the contract details
    '''
    contract_exchanger = ContractExchanger()
    if request.method == 'POST':
        return 'This API only accepts HTTP GET requests'

    return json.dumps(contract_exchanger.get_contract_data())


def set_logger(log_level: str = 'INFO'):
    ''' Sets the logging module parameters
    '''
    root = logging.getLogger('')
    for handler in root.handlers:
        root.removeHandler(handler)
    format = '%(asctime)s %(levelname)-8s:%(message)s'
    logging.basicConfig(format=format, level=log_level)



if __name__ == "__main__":
    set_logger()
    app.run(host='0.0.0.0')
