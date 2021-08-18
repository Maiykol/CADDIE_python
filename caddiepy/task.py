"""
Handles tasks and the corresponding parameter
"""
from . import settings
import caddiepy.api as api


class Task:
    def __init__(self, target, algorithm, seeds):
        self.config = settings.TaskConfig()
        self._set_target(target)
        self._set_algorithm(algorithm)
        self.set_parameter('seeds', seeds)

    def _set_algorithm(self, algorithm):
        self.config.algorithm = settings.Algorithm(algorithm)
    
    def _set_target(self, target):
        self.config.target = settings.Target(target)

    def _start_task(self):
        self.token = api.start_task(self.config.to_json())
    
    def _get_task(self):
        self.result = api.get_task(self.token)

    def get_result(self):
        return self.result

    def set_parameter(self, parameter, value):
        if parameter == 'geneInteractionDataset':
            setattr(self.config.parameters, parameter, settings.GeneInteractionDataset(value))
        elif parameter == 'drugInteractionDataset':
            setattr(self.config.parameters, parameter, settings.DrugInteractionDataset(value))
        elif parameter == 'cancerGeneDataset':
            setattr(self.config.parameters, parameter, settings.CancerGeneDataset(value))
        elif parameter == 'drugTargetAction':
            setattr(self.config.parameters, parameter, settings.DrugEffect(value))
        else:
            setattr(self.config.parameters, parameter, value)

    def run(self):
        self._start_task()
        self._get_task()