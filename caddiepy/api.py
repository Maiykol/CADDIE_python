"""
Handles all communication with the CADDIE API
"""
import requests
import json
import time
from . import settings
import logging

requests.packages.urllib3.disable_warnings() 

logger = logging.getLogger(__name__)

def get_gene_interaction_datasets():
    query_url = f'{settings.DOMAIN}{settings.Endpoints.GENE_INTERACTION_DATASETS}'
    return requests.get(query_url, headers=settings.HEADERS_JSON, verify=False)

def get_drug_interaction_datasets():
    query_url = f'{settings.DOMAIN}{settings.Endpoints.DRUG_INTERACTION_DATASETS}'
    return requests.get(query_url, headers=settings.HEADERS_JSON, verify=False)

def get_tissues():
    query_url = f'{settings.DOMAIN}{settings.Endpoints.TISSUES}'
    return requests.get(query_url, headers=settings.HEADERS_JSON, verify=False)

def get_expression_cancer_types():
    query_url = f'{settings.DOMAIN}{settings.Endpoints.EXPRESSION_CANCER_TYPES}'
    return requests.get(query_url, headers=settings.HEADERS_JSON, verify=False)

def get_mutation_cancer_types():
    query_url = f'{settings.DOMAIN}{settings.Endpoints.MUTATION_CANCER_TYPES}'
    return requests.get(query_url, headers=settings.HEADERS_JSON, verify=False)

def get_drug_effects():
    query_url = f'{settings.DOMAIN}{settings.Endpoints.DRUG_TARGET_ACTIONS}'
    return requests.get(query_url, headers=settings.HEADERS_JSON, verify=False)

def gene_drug_lookup(search_string, dataset):
    query_url = f'{settings.DOMAIN}{settings.Endpoints.GENE_DRUG_LOOKUP}'
    payload = {
        'text': search_string,
        'dataset': dataset
    }
    return requests.get(query_url, params=payload, headers=settings.HEADERS_JSON, verify=False)

def drug_lookup(search_string, dataset):
    query_url = f'{settings.DOMAIN}{settings.Endpoints.DRUG_LOOKUP}'
    payload = {
        'text': search_string,
        'dataset': dataset
    }
    return requests.get(query_url, params=payload, headers=settings.HEADERS_JSON, verify=False)

def map_gene_id(genes):
    query_url = f'{settings.DOMAIN}{settings.Endpoints.QUERY_NODES}'
    payload = {
        'nodes': genes,
    }
    return requests.post(query_url, data=json.dumps(payload), headers=settings.HEADERS_JSON, verify=False)

def start_task(parameters):
    endpoint = f'{settings.DOMAIN}{settings.Endpoints.TASK}'
    response = requests.post(endpoint, data=parameters, headers=settings.HEADERS_JSON, verify=False)
    return response.json()['token']

def get_task(token, interval=1):
    while True:
        try:
            logger.debug(f'Waiting for task {token}')
            time.sleep(interval)
            
            endpoint_result = f'{settings.DOMAIN}{settings.Endpoints.TASK_RESULT}?token={token}'
            endpoint_task = f'{settings.DOMAIN}{settings.Endpoints.TASK}?token={token}'

            response_task = requests.get(endpoint_task, verify=False).json()
            if response_task['info']['failed']:
                logger.warning(f"task {token} failed due to {response_task['info']['status']}")
                return None
            if not response_task['info']['done']:
                logger.debug(f"task {token} not yet done: {response_task['info']['status']}")
                continue

            response = requests.get(endpoint_result, verify=False)
            # check here if task responded correctly
            if response.status_code != 200:
                logger.warning(f'Failed getting result for {token}')
                continue
            logger.debug(f'Got results for {token}')
            return response.json()
        except:
            logger.info(f'Task {token} is having connection issues, waiting before retrying')
            time.sleep(10)

