import os
from gemsembler import (
    GatheredModels,
    read_supermodel_from_json,
    get_model_of_interest
)

# ── Rutas base ────────────────────────────────────────────────────────────────
base_dir = os.path.expanduser(
    "~/Documents/proyecto_tesis/02_resultados/agosto/"
    "2408_gemsembler_4c/Bacillus_infantis_161_d"
)
output_dir = os.path.join(base_dir, "gemsembler_output")
os.makedirs(output_dir, exist_ok=True)

id_bacteria = "Bacillus_infantis_161"
genome_faa  = os.path.join(base_dir, "genome.faa")

# ── Definición de condiciones ─────────────────────────────────────────────────
condiciones = {
    "na": [
        {
            "model_id": "carveme_na",
            "path_to_model": os.path.join(base_dir, "cc_na_lb_mm_carveme.xml"),
            "model_type": "carveme",
            "path_to_genome": genome_faa
        },
        {
            "model_id": "gapseq_na",
            "path_to_model": os.path.join(base_dir, "cc_na_mm_gapseq.xml"),
            "model_type": "gapseq",
            "path_to_genome": genome_faa
        },
        {
            "model_id": "modelseed_na",
            "path_to_model": os.path.join(base_dir, "cc_na_mm_modelseed.xml"),
            "model_type": "modelseed",
            "path_to_genome": genome_faa
        },
    ],
    "pk": [
        {
            "model_id": "carveme_pk",
            "path_to_model": os.path.join(base_dir, "cc_pk_lb_mm_carveme.xml"),
            "model_type": "carveme",
            "path_to_genome": genome_faa
        },
        {
            "model_id": "gapseq_pk",
            "path_to_model": os.path.join(base_dir, "cc_pk_mm_gapseq.xml"),
            "model_type": "gapseq",
            "path_to_genome": genome_faa
        },
        {
            "model_id": "modelseed_pk",
            "path_to_model": os.path.join(base_dir, "cc_pk_mm_modelseed.xml"),
            "model_type": "modelseed",
            "path_to_genome": genome_faa
        },
    ],
}

# ── Función para procesar cada condición ──────────────────────────────────────
def procesar_condicion(nombre, models):
    print(f"\n{'='*60}")
    print(f"  CONDICIÓN: {nombre.upper()}")
    print(f"{'='*60}")

    # Carpeta de salida por condición
    out_cond = os.path.join(output_dir, nombre)
    os.makedirs(out_cond, exist_ok=True)

    # Paso 1: Cargar modelos
    print(f"\n--- Paso 1: Cargando modelos ({nombre}) ---")
    gathered = GatheredModels()
    for model in models:
        gathered.add_model(**model)
        print(f"  -> Añadido: {model['model_id']}")
    gathered.run()
    print("¡Estandarización completada!")

    # Paso 2: Ensamblar Supermodel
    print(f"\n--- Paso 2: Ensamblando Supermodel ({nombre}) ---")
    supermodel = gathered.assemble_supermodel(
        output_folder=out_cond,
        assembly_id=None   # Reemplaza con tu GCF_XXXXXXX.X si lo tienes
    )
    print("Sources:", supermodel.sources)

    # Paso 3: Exportar modelos consenso
    print(f"\n--- Paso 3: Exportando modelos SBML ({nombre}) ---")

    # Unión total
    xml_union = os.path.join(out_cond, f"{id_bacteria}_{nombre}_union.xml")
    get_model_of_interest(supermodel, "assembly", xml_union)
    print(f"  -> Unión exportada:       {xml_union}")

    # Core en ≥2 de 3 modelos
    supermodel.at_least_in(2)
    xml_core2 = os.path.join(out_cond, f"{id_bacteria}_{nombre}_core2.xml")
    get_model_of_interest(supermodel, "core2", xml_core2)
    print(f"  -> Core ≥2 exportado:     {xml_core2}")

    # Core en los 3 modelos (consenso estricto)
    supermodel.at_least_in(3)
    xml_core3 = os.path.join(out_cond, f"{id_bacteria}_{nombre}_core3.xml")
    get_model_of_interest(supermodel, "core3", xml_core3)
    print(f"  -> Core ≥3 exportado:     {xml_core3}")

    # Paso 4: Guardar JSON
    print(f"\n--- Paso 4: Guardando Supermodel en JSON ({nombre}) ---")
    json_path = os.path.join(out_cond, f"{id_bacteria}_{nombre}_supermodel.json")
    supermodel.write_supermodel_to_json(json_path)
    print(f"  -> JSON guardado:         {json_path}")

    return supermodel


# ── Ejecutar ambas condiciones ────────────────────────────────────────────────
supermodels = {}
for nombre, models in condiciones.items():
    supermodels[nombre] = procesar_condicion(nombre, models)

print("\n\n¡Proceso finalizado para ambas condiciones!")
print(f"Resultados en: {output_dir}")