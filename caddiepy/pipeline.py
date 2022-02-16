from .task import Task
from . import api


def pipeline(gene_list):

    # verify that genes exist in CADDIE
    caddie_gene_list = api.map_gene_id(gene_list).json()['genes']

    task = Task('drug-target', 'multi-steiner', [gene['graphId'] for gene in caddie_gene_list])
    # customize parameters
    task.set_parameter('result_size', 20)
    task.set_parameter('gene_interaction_datasets', ['BioGRID'])
    # start task
    task.run()
    # get result when task is finished, if task is still running wait until it is finished
    result_drug_targets = task.get_result()

    task = Task('drug', 'trustrank', result_drug_targets['network']['nodes'])
    # customize parameters
    task.set_parameter('result_size', 20)
    task.set_parameter('include_indirect_drugs', True)
    task.set_parameter('gene_interaction_datasets', ['IID'])
    task.set_parameter('drug_interaction_datasets', ['DrugBank'])
    # start task
    task.run()
    # get result when task is finished, if task is still running wait until it is finished
    result = task.get_result()

    return result