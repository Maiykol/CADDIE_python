from enum import Enum
import json


PATH_SOTRAGE = '.temp'

class Algorithm(str, Enum):
    TRUSTRANK = 'trustrank'
    DEGREE_CENTRALITY = 'degree_centrality'
    BETWEENNESS_CENTRALITY = 'betweenness_centrality'
    HARMONIC_CENTRALITY = 'harmonic_centrality'
    NETWORK_PROXIMITY = 'network_proximity'
    MUTLI_STEINER = 'multi_steiner'
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

class Target(str, Enum):
    DRUG = 'drug'
    DRUGTARGET = 'drug-target'

class DrugEffect(str, Enum):
    NONE = ''
    INHIBITOR = 'inhibitor'
    ACTIVATOR = 'activator'

class TaskParameters:
    def __init__(self) -> None:
        self.seeds = []
        self.cancerDataset = CancerGeneDataset('NCG6')
        self.geneInteractionDataset = GeneInteractionDataset('IID')
        self.drugInteractionDataset = DrugInteractionDataset('DrugBank')
        self.cancerTypes = [72]
        self.includeNutraceuticalDrugs = False
        self.onlyAtcLDrugs = False
        self.filterPaths = True
        self.mutationCancerType = None
        self.expressionCancerType = None
        self.drugTargetAction = None
        self.dampingFactor = 0.85
        self.includeIndirectDrugs = True
        self.includeNonApprovedDrugs = True
        self.ignoreNonSeedBaits = True
        self.hubPenalty = 0
        self.resultSize = 20
        self.drugTargetAction = DrugEffect('inhibitor')
        self.cancerTypeNames = ['acute lymphoblastic leukemia']

class TaskConfig:
    def __init__(self) -> None:
        self.algorithm = Algorithm('trustrank')
        self.target = Target('drug')
        self.parameters = TaskParameters()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    

DOMAIN = 'http://10.162.163.20:8000/' # DEV API

HEADERS_JSON = {
                'Content-type':'application/json', 
                'Accept':'application/json'
            }

class Endpoints:
    QUERY_NODES = 'query_nodes/'  # POST cancer_dataset, nodes, cancer_types
    TASK = 'task/'  # POST (start task), GET (get task information)
    TASK_RESULT = 'task_result/' # GET (get task result)
    DRUG_LOOKUP = 'drug_interaction_lookup/'