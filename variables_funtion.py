import cobra.io
import pandas as pd
import os


def variables_totales(paths, csv_output_path):

    os.makedirs(csv_output_path, exist_ok=True)

    rows = []  # aquí se guardarán todos los resultados

    for anotacion, model_list in paths.items():

        for model_path in model_list:

            file_name = os.path.basename(model_path)
            model_id = file_name.replace('.xml', '')

            if '-draft' in file_name:
                continue

            try:
                cobra_model = cobra.io.read_sbml_model(model_path)

                R = len(cobra_model.reactions)
                M = len(cobra_model.metabolites)
                G = len(cobra_model.genes)

                print(f"{model_id}: R={R} M={M} G={G}")

                rows.append({
                    "Model_ID": model_id,
                    "Annotation": anotacion,
                    "Total_Reactions": R,
                    "Total_Metabolites": M,
                    "Total_Genes": G
                })

            except Exception as e:
                print(f"ERROR cargando {model_id}: {e}")

    df = pd.DataFrame(rows)

    output_file = os.path.join(csv_output_path, "variables_totales.csv")
    df.to_csv(output_file, index=False)

    print(f"✅ CSV guardado: {output_file}")
    print(df)