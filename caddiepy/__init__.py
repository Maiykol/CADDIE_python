"""
caddiepy.
"""

__version__ = "0.2.1"
__author__ = 'Michael Hartung'
__credits__ = """
Prof. Dr. Jan Baumbach, Chair of Computational Systems Biology (https://www.cosy.bio/), University of Hamburg ; 
Dr. Markus List, Head of the Research Group Big Data in BioMedicine (https://biomedical-big-data.de/), Technical University of Munich"""

from .utils.statistics import contingency_table, levenshtein
from .settings import PALETTE_DATASET_COMBINATIONS, PALETTE_PAIRWISE, PALETTE_DRUG_INTERACTION_DATASETS
from .task import Task