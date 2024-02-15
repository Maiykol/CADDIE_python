from enum import Enum
import json
import numpy as np

PATH_SOTRAGE = 'storage'

PALETTE_PAIRWISE = np.array([
    # green
    [105,206,132, 255],
    # grey
    [191, 191, 191, 255]
])/255

PALETTE_DRUG_INTERACTION_DATASETS = np.array([
    # blue
    [46, 134, 193, 255],
    # red
    [231, 76, 60, 255],
    # green
    [40, 180, 99, 255],
    # yellow
    [ 241, 196, 15, 255],
])/255

PALETTE_DATASET_COMBINATIONS = np.array([
    # blue
    [27, 79, 114, 255],
    [33, 97, 140, 255], 
    [46, 134, 193, 255],
    [93, 173, 226, 255],
    [133, 193, 233, 255],
    [199, 220, 240, 255],
    # red
    [ 120, 40, 31, 255],
    [148, 49, 38, 255],
    [ 176, 58, 46, 255 ],
    [231, 76, 60, 255],
    [ 241, 148, 138, 255],
    [ 250, 219, 216, 255],
    # green
    [ 20, 90, 50, 255 ],
    [29, 131, 72, 255],
    [40, 180, 99, 255],
    [ 46, 204, 113, 255],
    [ 125, 206, 160 , 255],
    [  212, 239, 223 , 255],
    # yellow
    [ 125, 102, 8, 255],
    [ 154, 125, 10, 255],
    [ 212, 172, 13, 255],
    [ 241, 196, 15, 255],
    [ 247, 220, 111, 255],
    [ 252, 243, 207, 255],
])/255

class Algorithm(str, Enum):
    TRUSTRANK = 'trustrank'
    DEGREE_CENTRALITY = 'degree_centrality'
    BETWEENNESS_CENTRALITY = 'betweenness_centrality'
    HARMONIC_CENTRALITY = 'harmonic_centrality'
    NETWORK_PROXIMITY = 'network_proximity'
    MUTLI_STEINER = 'multi-steiner'
    KEYPATHWAYMINER = 'keypathwayminer'

class CancerGeneDataset(str, Enum):
    NCG6 = 'NCG6'
    COSMIC = 'COSMIC'
    STRING = 'STRING'
    INTOGEN = 'IntOGen'
    CANCERGENESORG = 'cancer-genes.org'

class GeneInteractionDataset(str, Enum):
    REACTOME = 'REACTOME'
    BIOGRID = 'BioGRID'
    STRING = 'STRING'
    APID = 'APID'
    HTRIdb = 'HTRIdb'
    IID = 'IID'

class DrugInteractionDataset(str, Enum):
    DRUGBANK = 'DrugBank'
    BIOGRID = 'BioGRID'
    CHEMBL = 'ChEMBL'
    DGIDB = 'DGIdb'

class Target(str, Enum):
    DRUG = 'drug'
    DRUGTARGET = 'drug-target'

class DrugEffect(str, Enum):
    NONE = ''
    INHIBITOR = 'inhibitor'
    NOT_INHIBITOR = 'not_inhibitor'
    ACTIVATOR = 'activator'
    NOT_ACTIVATOR = 'not_activator'

class TaskParameters:
    def __init__(self) -> None:
        self.seeds = []
        self.cancer_dataset = CancerGeneDataset('NCG6')
        self.gene_interaction_datasets = [GeneInteractionDataset('IID')]
        self.drug_interaction_datasets = [DrugInteractionDataset('DrugBank')]
        self.cancer_types = []
        self.include_nutraceutical_drugs = True
        self.only_atc_l_drugs = False
        self.filter_paths = True
        self.mutation_cancer_type = None
        self.expression_cancer_type = None
        self.drug_target_action = None
        self.include_indirect_drugs = True
        self.include_non_approved_drugs = True
        self.ignore_non_seed_baits = True
        self.hub_penalty = 0
        self.result_size = 20
        self.available_drugs = None
        self.drug_target_action = DrugEffect('')
        self.cancer_type_names = []
        # multi steiner
        self.num_trees = 5
        self.tolerance = 10
        # trustrank
        self.damping_factor = 0.85
        # keypathwayminer
        self.k = 20


class TaskConfig:
    def __init__(self) -> None:
        # default parameter
        self.algorithm = Algorithm('trustrank')
        self.target = Target('drug')
        self.parameters = TaskParameters()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
DOMAIN = 'https://apps.cosy.bio/api-caddie/'

HEADERS_JSON = {
                'Content-type':'application/json', 
                'Accept':'application/json'
            }

class Endpoints:
    QUERY_NODES = 'query_nodes/'  # POST cancer_dataset, nodes, cancer_types
    TASK = 'task/'  # POST (start task), GET (get task information)
    TASK_RESULT = 'task_result/' # GET (get task result)
    DRUG_LOOKUP = 'drug_interaction_lookup/'
    GENE_DRUG_LOOKUP = 'gene_drug_interaction_lookup/'
    GENE_INTERACTION_DATASETS = 'interaction_gene_datasets/'
    DRUG_INTERACTION_DATASETS = 'interaction_drug_datasets/'
    TISSUES = 'tissues/'
    EXPRESSION_CANCER_TYPES = 'expression_cancer_types/'
    MUTATION_CANCER_TYPES = 'mutation_cancer_types/'
    DRUG_TARGET_ACTIONS = 'drug_target_actions/'
