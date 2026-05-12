from gemsembler import (
    GatheredModels,  # Object to collect input models and build a supermodel
    read_supermodel_from_json,  # Function to read a save supermodel
    get_models_with_all_confidence_levels,  # creates cobrapy models at all confidence levels
    get_model_of_interest  # creates one cobrapy model
)

from gemsembler.downstream import (
    glycolysis,  # returns table and/or interactive maps of glycolysis
    pentose_phosphate,  # returns table and/or interactive maps of pentose phosphate
    tca,  # # returns table and/or interactive maps of TCA
    # table_reactions_confidence,  # returns a pandas dataframe with reaction IDs, confidence and additional info
    # calc_dist_for_synt_path,
    biomass,
    get_met_neighborhood,
    # run_metquest_results_analysis,
    run_growth_full_flux_analysis,
    # write_metabolites_production_output,
    pathway_of_interest,
    # get_met_neighborhood,
    GLYCOLYSIS_GLOBAL,
    PENTOSE_PHOSPHATE_PATHWAY_GLOBAL,
    TCA_GLOBAL,
    COFACTORS_GLOBAL
)
import os
from gemsembler.drawing import draw_one_synt_path, MET_NOT_INT_GLOBAL
from cobra.io import read_sbml_model, write_sbml_model
genome_path = "./01_raw_data/rizo/ST00060_fixed.faa"

st60_example = [
    {
        "model_id": "st60_carveme",
        "path_to_model": os.path.join("./02_data/rizo/carveme/ST00060_dimont_carveme_lb.xml"),
        "model_type": "carveme",
        "path_to_genome": genome_path
    },
    {
        "model_id": "st60_gapseq",
        "path_to_model": os.path.join("./02_data/rizo/gapseq/ST00060_default_gapseq_lb.xml"),
        "model_type": "gapseq", 
        "path_to_genome": genome_path
    } 
    #  {
    #     "model_id": "st60_kabase",
    #     "path_to_model": os.path.join("./02_data/rizo/kbase/ST00060_kbase.xml"),
    #     "model_type": "modelseed", 
    #     "path_to_genome": genome_path
    # }
]


gathered = GatheredModels()
for model in st60_example:
    gathered.add_model(**model)
gathered.run()

supermodel_60_carvegap = gathered.assemble_supermodel("./04_resultados/gemsembler_output/",
                                                path_final_genome_aa = "./01_raw_data/rizo/ST00060_fixed.faa")


supermodel_60_mix_carvegap = gathered.assemble_supermodel("./04_resultados/gemsembler_output/",
                                                 path_final_genome_aa = ("./01_raw_data/rizo/ST00060_fixed.faa"), do_mix_conv_notconv=True)

supermodel_60_carvegap.write_supermodel_to_json("./04_resultados/gemsembler_output/60_supermodel.json")

supermodel_60_carvegap = read_supermodel_from_json("./04_resultados/gemsembler_output/60_supermodel.json")
supermodel_60_carvegap.at_least_in(2)
core2_carvegap = get_model_of_interest(supermodel_60_carvegap, "core2_carvegap")
core2_carvegap = get_model_of_interest(supermodel_60_carvegap, "core2_carvegap", "./04_resultados/gemsembler_output/60_core_carvegapseq.xml")
