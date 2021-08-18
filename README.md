<p align="center">
  <img alt="CADDIE Logo" src="https://github.com/Maiykol/caddiepy/blob/main/caddie_logo.png?raw=true" />
</p>


# caddiepy

The python package to the Cancer Driver Drug Interaction Explorer (CADDIE). It  provides an interface for a variety of CADDIE functionalities, giving the user the possibility to execute tasks on CADDIE programmatically without using the website.


# How to use

## Import
Import the module:
```
import caddiepy
```

## Examples
N.B.: Required datasets for the examples will be downloaded upon execution and stored in the folder '.temp'.

- Run the comparison of the CADDIE results against the Drug Sensitivity ranking of GDSC2 (https://www.cancerrxgene.org/) (this may take up to 5 hours):
```
caddiepy.examples.GDSC_study.run(algorithm, gene_interaction_dataset, output_folder)
```

## Logging
Configure the logging level like this:
```
import logging
logging.basicConfig(level=logging.INFO)
```