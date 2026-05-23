# from gemsembler import (
#     GatheredModels,  # Object to collect input models and build a supermodel
#     read_supermodel_from_json,  # Function to read a save supermodel
#     get_models_with_all_confidence_levels,  # creates cobrapy models at all confidence levels
#     get_model_of_interest  # creates one cobrapy model
# )

# from gemsembler.downstream import (
#     glycolysis,  # returns table and/or interactive maps of glycolysis
#     pentose_phosphate,  # returns table and/or interactive maps of pentose phosphate
#     tca,  # # returns table and/or interactive maps of TCA
#     # table_reactions_confidence,  # returns a pandas dataframe with reaction IDs, confidence and additional info
#     # calc_dist_for_synt_path,
#     biomass,
#     get_met_neighborhood,
#     # run_metquest_results_analysis,
#     run_growth_full_flux_analysis,
#     # write_metabolites_production_output,
#     pathway_of_interest,
#     # get_met_neighborhood,
#     GLYCOLYSIS_GLOBAL,
#     PENTOSE_PHOSPHATE_PATHWAY_GLOBAL,
#     TCA_GLOBAL,
#     COFACTORS_GLOBAL
# )
# import os
# import cobra
# from gemsembler.drawing import draw_one_synt_path, MET_NOT_INT_GLOBAL
# from cobra.io import read_sbml_model, write_sbml_model
# genome_path = "./02_data/rizo/anotacion/prokka/ST00060_prokka.faa"

# st60_example = [
#     {
#         "model_id": "st60_carveme",
#         "path_to_model": os.path.join("./02_data/rizo/carveme/ST00042_prokka_carveme_lb.xml"),
#         "model_type": "carveme",
#         "path_to_genome": genome_path
#     },
#     {
#         "model_id": "st60_gapseq",
#         "path_to_model": os.path.join("./02_data/rizo/gapseq/ST00042_prokka_gapseq_lb.xml"),
#         "model_type": "gapseq", 
#         "path_to_genome": genome_path
#     }, 
#      {
#         "model_id": "st60_kabase",
#         "path_to_model": os.path.join("./02_data/rizo/kbase/ST00042_kbase.xml"),
#         "model_type": "modelseed", 
#         "path_to_genome": genome_path
#     }
# ]


# gathered = GatheredModels()
# for model in st60_example:
#     gathered.add_model(**model)
# gathered.run()

# supermodel_42 = gathered.assemble_supermodel("./04_resultados/gemsembler_output/",
#                                                 assembly_id = "GCF_012647205.1")

# supermodel_42_mix = gathered.assemble_supermodel("./04_resultados/gemsembler_output/",
#                                                  assembly_id = "GCF_012647205.1", do_mix_conv_notconv=True)

# supermodel_42.write_supermodel_to_json("./04_resultados/gemsembler_output/42_supermodel.json")

# supermodel_42 = read_supermodel_from_json("./04_resultados/gemsembler_output/42_supermodel.json")
# supermodel_42.at_least_in(2)
# core2 = get_model_of_interest(supermodel_42, "core2")
# core2 = get_model_of_interest(supermodel_42, "core2", "./04_resultados/gemsembler_output/42_core2.xml")



import cobra
model = cobra.io.read_sbml_model("/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rz/Agrobacteriumr_kb_rz_rt.xml")
#ejecucion FBA
solution = model.optimize()

#optimal se refiere a si el software encontró una solución que maximiza la función objetivo (en este caso, la tasa de crecimiento) dentro de las restricciones del modelo. Si el estado es 'optimal', significa que se encontró una solución óptima para el problema de optimización planteado por el modelo metabólico.
#objective_value valor numerico de tasa de crecimiento
#.4f decimales que quiero qeu muetre
#h^-1 unidades tasa crecimiento
if solution.status == 'optimal':
   print(f"Tasa de crecimiento: {solution.objective_value:.4f} h^-1")
else:
   print(f"El modelo NO es funcional. Estado: {solution.status}")
        


