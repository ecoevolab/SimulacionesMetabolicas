import cobra.io
import pandas as pd
import os


def variables_totales(paths, csv_output_path):

    os.makedirs(csv_output_path, exist_ok=True)

    for anotacion, model_list in paths.items():

        model_reactions = {}
        model_metabolites = {}
        model_genes = {}

        for model_path in model_list:

            file_name = os.path.basename(model_path)
            model_id = file_name.replace('.xml', '')

            if '-draft' in file_name:
                continue

            try:
                cobra_model = cobra.io.read_sbml_model(model_path)

                model_reactions[model_id] = len(cobra_model.reactions)
                model_metabolites[model_id] = len(cobra_model.metabolites)
                model_genes[model_id] = len(cobra_model.genes)

                print(f"{model_id}: "
                      f"R={len(cobra_model.reactions)} "
                      f"M={len(cobra_model.metabolites)} "
                      f"G={len(cobra_model.genes)}")

            except Exception as e:
                print(f"ERROR cargando {model_id}: {e}")

        df = pd.DataFrame({
            "Model ID": list(model_reactions.keys()),
            "Total Reactions": list(model_reactions.values()),
            "Total Metabolites": list(model_metabolites.values()),
            "Total Genes": list(model_genes.values())
        })

        output_file = os.path.join(csv_output_path, f"rizo_variables_{anotacion}.csv")
        df.to_csv(output_file, index=False)

        print(f"✅ CSV guardado: {output_file}")
        print(df)