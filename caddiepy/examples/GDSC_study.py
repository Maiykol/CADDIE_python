from caddiepy.file_utils.download_file import download_file_ftp, unzip
from caddiepy.file_utils.load_file import load_csv, load_xlsx
from caddiepy import api as api
from caddiepy.task import Task
from pathlib import Path
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import logging

logger = logging.getLogger(__name__)

GDSC2_DATASET = 'ftp://ftp.sanger.ac.uk/pub/project/cancerrxgene/releases/current_release/GDSC2_fitted_dose_response_25Feb20.csv'
GDSC2_DATASET_FILENAME = 'GDSC2_fitted_dose_response_25Feb20.csv'

GDSC2_CELL_LINES = 'ftp://ftp.sanger.ac.uk/pub/project/cancerrxgene/releases/current_release/Cell_Lines_Details.xlsx'
GDSC2_CELL_LINES_FILENAME = 'Cell_Lines_Details.xlsx'

GDSC2_CELL_LINE_DATA = 'ftp://ftp.sanger.ac.uk/pub/project/cancerrxgene/releases/current_release/GDSCtools_mobems.zip'
GDSC2_CELL_LINE_DATA_FILENAME = 'GDSCtools_mobems.zip'
GDSC2_CELL_LINE_DATA_PANCAN_FILENAME = GDSC2_CELL_LINE_DATA_FILENAME[:-4] + '/GF_PANCAN_nomedia_mobem.csv'


def load_data():
    download_file_ftp(GDSC2_DATASET_FILENAME, GDSC2_DATASET)
    df_gdsc2_reponse = load_csv(GDSC2_DATASET_FILENAME)

    download_file_ftp(GDSC2_CELL_LINES_FILENAME, GDSC2_CELL_LINES)
    df_gdsc2_cell_lines = load_xlsx(GDSC2_CELL_LINES_FILENAME, sheet='COSMIC tissue classification')

    download_file_ftp(GDSC2_CELL_LINE_DATA_FILENAME, GDSC2_CELL_LINE_DATA)
    unzip(GDSC2_CELL_LINE_DATA_FILENAME)
    df_gdsc2_pancan = load_csv(GDSC2_CELL_LINE_DATA_PANCAN_FILENAME)
    return df_gdsc2_pancan, df_gdsc2_cell_lines, df_gdsc2_reponse

def preprocess_data(df_gdsc2_pancan, df_gdsc2_cell_lines):
    cell_line_col = []
    for i, row in df_gdsc2_pancan.iterrows():
        cosmic_id = row['COSMIC_ID']
        filtered_cell_line_row = df_gdsc2_cell_lines[df_gdsc2_cell_lines['COSMIC_ID']==cosmic_id]
        if len(filtered_cell_line_row) != 1:
            logger.debug(f'could not fetch cell line for cosmic_id {cosmic_id}')
            cell_line_col.append(None)
        else:
            cell_line_col.append(filtered_cell_line_row.iloc[0]['Line'])
    df_gdsc2_pancan['cell_line'] = cell_line_col

    dict_cosmic_to_cancer = df_gdsc2_cell_lines.set_index('COSMIC_ID')['Histology'].to_dict()
    df_gdsc2_pancan['cancer'] = df_gdsc2_pancan['COSMIC_ID'].map(dict_cosmic_to_cancer)
    return df_gdsc2_pancan

def find_common_drugs(df_gdsc2_reponse):
    found = []
    not_found = []
    for drug in df_gdsc2_reponse['DRUG_NAME'].unique():
        response = api.drug_lookup(drug, 'DrugBank').json()
        if response['found']:
            found.append(response['drug'][0]['name'])
            logger.debug(f"found {response['drug'][0]['name']}")
        else:
            logger.debug(f'not found {drug}')
            not_found.append(drug)
    return found, not_found


def calculate_cell_line_candidates(df_gdsc2_pancan):
    # maps genes of cell lines to caddie gene objects, which can be used as task input
    # returns cell lines with genes for futher analysis and filtered out cell lines
    genes_mutated_columns = [col for col in df_gdsc2_pancan.columns if '_mut' in col]
    filtered_out = {}
    to_compare = {}

    for cell_id, row in df_gdsc2_pancan.set_index('COSMIC_ID').iterrows():
        # only mutated gene data
        cell_gene_info = row[genes_mutated_columns]
        if not cell_gene_info.sum():
            # no mutated genes, might be interesting for later but filter out now
            filtered_out[row['cell_line']] = 'No mutated genes'
            continue
            
        # only mutated genes
        genes_mut = cell_gene_info[cell_gene_info==1]
        genes = [key.split('_')[0] for key in genes_mut.keys()]
        caddie_gene_objects = api.map_gene_id(genes).json()['genes']
        to_compare[row['cell_line']] = caddie_gene_objects
    return to_compare, filtered_out


def get_drugs_for_cell_line_with_caddie(genes, algorithm, gene_interaction_dataset):
    caddie_gene_ids = [g['graphId'] for g in genes]
    task = Task('drug', algorithm, caddie_gene_ids)
    task.set_parameter('resultSize', 99999999)
    task.set_parameter('geneInteractionDataset', gene_interaction_dataset)
    task.set_parameter('drugInteractionDataset', 'DrugBank')
    task.set_parameter('drug_target_action', 'not_activator')
    task.run()
    return task.get_result()

def find_drugs_for_cell_lines(cell_line_dict, algorithm, gene_interaction_dataset):
    drug_dict = {}
    for cell_line, genes in cell_line_dict.items():
        if not len(genes):
            logger.debug(f'Skipping cell line {cell_line} because of no seeds')
            continue
        response = get_drugs_for_cell_line_with_caddie(genes, algorithm, gene_interaction_dataset)
        if response is None:
            logger.debug(f'ERROR for cell line {cell_line}')
            continue
        drug_dict[cell_line] = [(x['name'], x['score']) for x in response['drugObjects']]

    return drug_dict

def compare_study_and_caddie(df_drug_response, cell_line_dict, caddie_drug_dict, found_drugs):

    overlap_dict = {}
    spearman_cor_dict = {}
    for cell_line, genes in cell_line_dict.items():
        
        df_study_drug_and_auc = df_drug_response[df_drug_response['CELL_LINE_NAME']==cell_line][['DRUG_NAME', 'AUC']]
        # filter out drugs that are not included in CADDIE
        df_study_drug_and_auc = df_study_drug_and_auc[df_study_drug_and_auc['DRUG_NAME'].isin(found_drugs)]
        df_study_drug_and_auc = df_study_drug_and_auc.sort_values('AUC', ascending=False)
        if len(df_study_drug_and_auc) == 0:
            logger.debug(f'No study data for {cell_line}. Skipping')
            continue

        # get CADDIE results from dict
        if cell_line not in caddie_drug_dict:
            logger.debug(f'No CADDIE data for {cell_line}. Skipping')
            continue
        caddie_drugs = caddie_drug_dict[cell_line]
        df_caddie_drug_score = pd.DataFrame(caddie_drugs, columns=['DRUG_NAME', 'score'])
        df_caddie_drug_score = df_caddie_drug_score.sort_values('score', ascending=False)
        if len(df_caddie_drug_score) == 0:
            logger.debug(f'No CADDIE data for {cell_line}. Skipping')
            continue

        # clean ddrug names
        df_study_drug_and_auc['DRUG_NAME'] = df_study_drug_and_auc['DRUG_NAME'].map(lambda x: x.lower().strip())
        df_caddie_drug_score['DRUG_NAME'] = df_caddie_drug_score['DRUG_NAME'].map(lambda x: x.lower().strip())

        # compare against CADDIE results
        df_overlap = pd.merge(df_study_drug_and_auc, df_caddie_drug_score, how='inner', on=['DRUG_NAME'])
        n_overlap = len(df_overlap)
        overlap_dict[cell_line] = n_overlap
        
        # spearman rank correlation
        drug_list_study = df_study_drug_and_auc[df_study_drug_and_auc['DRUG_NAME'].isin(df_overlap['DRUG_NAME'])]['DRUG_NAME']
        drug_list_caddie = df_caddie_drug_score[df_caddie_drug_score['DRUG_NAME'].isin(df_overlap['DRUG_NAME'])]['DRUG_NAME']
        
        spearman_cor = stats.spearmanr(drug_list_study, drug_list_caddie, alternative='greater')
        spearman_cor_dict[cell_line] = spearman_cor
        
    return overlap_dict, spearman_cor_dict

def plot(spearman_dict, output_folder):
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    significant_correlations = []
    P = 0.05
    for cell_line, spearman_stats in spearman_dict.items():
        if spearman_stats[1] < 0.05:
            significant_correlations.append((cell_line, spearman_stats))

    corrs = [c[0] for c in spearman_dict.values()]
    corrs_sig = [c[1][0] for c in significant_correlations]

    fig, axes = plt.subplots(1, 2)

    sns.boxplot(ax=axes[0], y=corrs, color='#ff4c4c')
    axes[0].set_title(f'Spearman Correlation n={len(spearman_dict)}')

    sns.boxplot(ax=axes[1], y=corrs_sig, color='#ff4c4c')
    axes[1].set_title(f'Spearman Correlation Significant n={len(significant_correlations)}')

    plt.savefig(f'{output_folder}/spearman_boxplot.png')


def run(algorithm, gene_interaction_dataset, output_folder):
    ### 1. Load Data
    logger.info('1. Load Data')
    df_gdsc2_pancan, df_gdsc2_cell_lines, df_gdsc2_reponse = load_data()
    df_gdsc2_pancan = preprocess_data(df_gdsc2_pancan, df_gdsc2_cell_lines)
    ### 2. Find common drugs
    logger.info('2. Find common drugs between the study and CADDIE')
    found_drugs, _ = find_common_drugs(df_gdsc2_reponse)
    ### 3. Calculate Candidate Cell Lines
    logger.info('3. Calculate Candidate Cell Lines')
    candidate_cell_lines, _ = calculate_cell_line_candidates(df_gdsc2_pancan)
    ### 4. Run task on CADDIE
    logger.info('4. Run task on CADDIE')
    caddie_drug_dict = find_drugs_for_cell_lines(candidate_cell_lines, algorithm, gene_interaction_dataset)
    ### 5. interpret results
    logger.info('5. Interpret Results')
    overlap_dict, spearman_dict = compare_study_and_caddie(df_gdsc2_reponse, candidate_cell_lines, caddie_drug_dict, found_drugs)
    ### 6. plot
    logger.info('6. Plotting')
    plot(spearman_dict, output_folder)
    ### 7. save other stuff
    with open(f'{output_folder}/caddie_drug_dict.json', 'w') as f:
        json.dump(caddie_drug_dict, f)
    with open(f'{output_folder}/overlap_dict.json', 'w') as f:
        json.dump(overlap_dict, f)






