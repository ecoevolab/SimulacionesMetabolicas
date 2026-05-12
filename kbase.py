import cobra
import re

# 1. Cargar el modelo
input_path = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data/rizo/kbase/ST00042_kbase.xml"
output_path = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data/rizo/kbase/ST00042_kbase_clean.xml"

model = cobra.io.read_sbml_model(input_path)

# 2. Corregir Compartimentos
# Gemsembler es feliz con 'c' (citoplasma) y 'e' (extracelular)
new_compartments = {}
for cid in list(model.compartments.keys()):
    if cid == 'c0' or cid == 'c':
        new_compartments['c'] = 'cytosol'
    elif cid == 'e0' or cid == 'e':
        new_compartments['e'] = 'extracellular'
    else:
        new_compartments[cid] = model.compartments[cid]

model.compartments = new_compartments

# 3. Corregir Metabolitos y sus IDs
for met in model.metabolites:
    # Cambiar el compartimento asignado
    if met.compartment == 'c0':
        met.compartment = 'c'
    elif met.compartment == 'e0':
        met.compartment = 'e'
    
    # Limpiar el ID: Solo reemplaza si el resultado no es vacío
    old_id = met.id
    new_id = old_id.replace('_c0', '_c').replace('_e0', '_e')
    
    if new_id and new_id != '':
        met.id = new_id
    else:
        # Si por alguna razón queda vacío, mantenemos el ID original 
        # pero forzamos el cambio de compartimento interno
        pass

# 4. Validar Reacciones (KBase a veces deja IDs de reacción extraños)
for rxn in model.reactions:
    if not rxn.id or rxn.id == '':
        rxn.id = f"R_unknown_{rxn.name[:5]}"

# 5. Guardar el modelo
try:
    cobra.io.write_sbml_model(model, output_path)
    print(f"--- Éxito: Modelo guardado en {output_path} ---")
except Exception as e:
    print(f"Error al guardar: {e}")