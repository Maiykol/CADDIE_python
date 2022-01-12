<p align="center">
  <img alt="CADDIE Logo" src="https://github.com/Maiykol/caddiepy/blob/main/caddie_logo.png?raw=true" />
</p>


# caddiepy

The python package to the <a href="https://exbio.wzw.tum.de/caddie/" target="_blank">Cancer Driver Drug Interaction Explorer (CADDIE)</a>. It  provides an interface for a variety of CADDIEs functionalities, giving the user the possibility to execute tasks on CADDIE programmatically without using the website. This allows to run a larger number of drug-target search or drug repurposing tasks and to implement CADDIE into your programs. For more information about CADDIE, visit the <a href="https://exbio.wzw.tum.de/caddie/documentation" target="_blank">documentation</a>.


# Working example

```
import caddiepy

gene_list = ['PTEN', 'MYC']

# verify that genes exist in CADDIE
caddie_gene_list = caddiepy.api.map_gene_id(gene_list).json()['genes']

task = caddiepy.Task('drug', 'network_proximity', [gene['graphId'] for gene in caddie_gene_list])
# customize parameters
task.set_parameter('result_size', 5)
task.set_parameter('include_indirect_drugs', True)
task.set_parameter('gene_interaction_datasets', ['IID'])
task.set_parameter('drug_interaction_datasets', ['DrugBank'])
# start task
task.run()
# get result when task is finished, if task is still running wait until it is finished
result = task.get_result()
```

# How to use

## Import
Import the module:
```
import caddiepy
```

## 2 Steps to repurpose drugs and find drug-targets
Step 1: Map genes to CADDIE gene IDs. This step is necessary to verify the genes exist in the CADDIE database. The gene objects returned contains a mapping to different IDs.
```
# gene list is a list of gene identifiers: entrez, uniprot ac or hugo
caddiepy.api.map_gene_id(gene_list)

# example to receive list of caddie IDs
caddie_gene_list = caddiepy.api.map_gene_id(gene_list).json()['genes']
caddie_gene_id_list = [gene['graphId'] for gene in caddie_gene_list]
```

Step 2: Use CADDIE IDs to find putative drug-targets or candidate drugs using one of CADDIEs algorithms

Drug-target algorithms: 
- multisteiner
- keypathwayminer
- trustrank
- harmonic_centraliy
- degree_centraliy
- betweenness_centraliy

Drug algorithms:
- trustrank
- harmonic_centraliy
- degree_centraliy
- network_proximity

```
# target is either 'drug' or 'drug-target'
# caddie_gene_id_list is a list of caddie gene IDs (like g123, g234, ...)
task = caddiepy.Task(target, algorithm, caddie_gene_id_list)
# set parameters like this (for a full list of parameters and the available datasets look below)
task.set_parameter('result_size', 50)
task.set_parameter('gene_interaction_datasets', [gene_interaction_dataset1, gene_interaction_dataset2, ...])
task.set_parameter('drug_interaction_datasets', [drug_interaction_dataset1, drug_interaction_dataset2, ...])
# start task
task.run()
# get result when task is finished, if task is still running wait until it is finished
result = task.get_result()
```

## Algorithm parameters

The full list of parameters for each algorithm (for an explanation, visit the <a href="https://exbio.wzw.tum.de/caddie/documentation" target="_blank">documentation</a>). For all available input options (dataset names, cancer-types) see below.

```
# multisteiner
task.set_parameter('num_trees', 5)
task.set_parameter('tolerance', 10)
task.set_parameter('hub_penalty', 0)
task.set_parameter('max_deg', sys.maxsize)
task.set_parameter('gene_interaction_datasets', gene_interaction_dataset_list)
task.set_parameter('mutation_cancer_type', mutation_cancer_type)
task.set_parameter('expression_cancer_type', expression_cancer_type)
task.set_parameter('tissue', tissue)

# keypathwayminer
task.set_parameter('k', 5)

# trustrank
task.set_parameter('damping_factor', 0.85)
task.set_parameter('hub_penalty', 0)
task.set_parameter('max_deg', sys.maxsize)
task.set_parameter('gene_interaction_datasets', gene_interaction_dataset_list)
task.set_parameter('drug_interaction_datasets', drug_interaction_dataset_list)
task.set_parameter('mutation_cancer_type', mutation_cancer_type)
task.set_parameter('expression_cancer_type', expression_cancer_type)
task.set_parameter('tissue', tissue)
task.set_parameter('include_nutraceutical_drugs', boolean)
task.set_parameter('only_atc_l_drugs', boolean)
task.set_parameter('include_indirect_drugs', boolean)
task.set_parameter('include_non_approved_drugs', boolean)
task.set_parameter('filter_paths', boolean)
task.set_parameter('available_drugs', available_drug_list)
# only avaibale if drug_interaction_dataset_list = ['drugbank']
task.set_parameter('drug_target_action', drug_effect)

# degree_centrality
task.set_parameter('hub_penalty', 0)
task.set_parameter('max_deg', sys.maxsize)
task.set_parameter('gene_interaction_datasets', gene_interaction_dataset_list)
task.set_parameter('drug_interaction_datasets', drug_interaction_dataset_list)
task.set_parameter('mutation_cancer_type', mutation_cancer_type)
task.set_parameter('expression_cancer_type', expression_cancer_type)
task.set_parameter('tissue', tissue)
task.set_parameter('include_nutraceutical_drugs', boolean)
task.set_parameter('only_atc_l_drugs', boolean)
task.set_parameter('include_indirect_drugs', boolean)
task.set_parameter('include_non_approved_drugs', boolean)
task.set_parameter('filter_paths', boolean)
task.set_parameter('available_drugs', available_drug_list)
# only avaibale if drug_interaction_dataset_list = ['drugbank']
task.set_parameter('drug_target_action', drug_effect)

# harmonic_centrality
task.set_parameter('hub_penalty', 0)
task.set_parameter('max_deg', sys.maxsize)
task.set_parameter('gene_interaction_datasets', gene_interaction_dataset_list)
task.set_parameter('drug_interaction_datasets', drug_interaction_dataset_list)
task.set_parameter('mutation_cancer_type', mutation_cancer_type)
task.set_parameter('expression_cancer_type', expression_cancer_type)
task.set_parameter('tissue', tissue)
task.set_parameter('include_nutraceutical_drugs', boolean)
task.set_parameter('only_atc_l_drugs', boolean)
task.set_parameter('include_indirect_drugs', boolean)
task.set_parameter('include_non_approved_drugs', boolean)
task.set_parameter('filter_paths', boolean)
task.set_parameter('available_drugs', available_drug_list)
# only avaibale if drug_interaction_dataset_list = ['drugbank']
task.set_parameter('drug_target_action', drug_effect)

# betweenness_centrality
task.set_parameter('hub_penalty', 0)
task.set_parameter('max_deg', sys.maxsize)
task.set_parameter('gene_interaction_datasets', gene_interaction_dataset_list)
task.set_parameter('mutation_cancer_type', mutation_cancer_type)
task.set_parameter('expression_cancer_type', expression_cancer_type)
task.set_parameter('tissue', tissue)
task.set_parameter('filter_paths', boolean)

# network_proximity
task.set_parameter('hub_penalty', 0)
task.set_parameter('max_deg', sys.maxsize)
task.set_parameter('gene_interaction_datasets', gene_interaction_dataset_list)
task.set_parameter('drug_interaction_datasets', drug_interaction_dataset_list)
task.set_parameter('mutation_cancer_type', mutation_cancer_type)
task.set_parameter('expression_cancer_type', expression_cancer_type)
task.set_parameter('tissue', tissue)
task.set_parameter('include_nutraceutical_drugs', boolean)
task.set_parameter('only_atc_l_drugs', boolean)
task.set_parameter('include_indirect_drugs', boolean)
task.set_parameter('include_non_approved_drugs', boolean)
task.set_parameter('filter_paths', boolean)
task.set_parameter('available_drugs', available_drug_list)
# only avaibale if drug_interaction_dataset_list = ['drugbank']
task.set_parameter('drug_target_action', drug_effect)
```

## List all available datasets

List all available gene interaction datasets:
```
caddiepy.api.get_gene_interaction_datasets().json()
```

List all available drug interaction datasets:
```
caddiepy.api.get_drug_interaction_datasets().json()
```

List all available tissues:
```
caddiepy.api.get_tissues().json()
```

List all available expression cancer types:
```
caddiepy.api.get_expression_cancer_types().json()
```

List all available mutation cancer types:
```
caddiepy.api.get_mutation_cancer_types().json()
```

List all available drug effects (only relevant when working with DrugBank):
```
caddiepy.api.get_drug_effects().json()
```

Look up drugs in the CADDIE database and their interactions with genes:
```
caddiepy.api.drug_lookup(search_string, database_name)
```



## Logging
Configure the logging level like this:
```
import logging
logging.basicConfig(level=logging.DEBUG)
```