import pandas as pd

data_url = "http://bigg.ucsd.edu/static/namespace/bigg_models_metabolites.txt"
# You can now mix common names and chemical formulas
medio_names = ['glucose', 'ethanol', 'o2', 'h2o', 'phosphate']

def defmedio(url, name_mets):
    df = pd.read_csv(url, sep="\t")
    
    # Use the column names identified in your previous terminal output
    id_col = 'bigg_id' if 'bigg_id' in df.columns else df.columns[0]
    name_col = 'name' if 'name' in df.columns else df.columns[1]
    
    medio = []
    for m in name_mets:
        # This regex looks for the string anywhere in the name (case-insensitive)
        # It handles 'O2' inside 'Oxygen' or 'Glc' inside 'Glucose'
        matches = df[
            (df[name_col].str.contains(m, case=False, na=False)) & 
            (df[id_col].str.endswith('_e', na=False))
        ]
        
        # If we found matches, we try to find the "cleanest" one
        if not matches.empty:
            # Sort by the length of the name so 'Oxygen' comes before 'Oxygenated compound'
            matches = matches.assign(name_len=matches[name_col].str.len())
            matches = matches.sort_values('name_len').drop(columns='name_len')
            
            # Take the top 3 most likely candidates
            medio.append(matches.head(3))
            
    if not medio:
        return pd.DataFrame()
        
    return pd.concat(medio).drop_duplicates()

# Execute
final_df = defmedio(data_url, medio_names)
print(final_df[[final_df.columns[0], 'name']])