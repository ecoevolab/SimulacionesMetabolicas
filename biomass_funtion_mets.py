import cometspy as c
import cobra.io
import pandas as pd
import os
import glob 

def biomass_comunidades(ruta_csv_syncoms, patron_xml, 
                        threads, cycles, mass, media, folder_resultados):
    # --- 1. CONFIGURACIÓN DE PARÁMETROS (IGUAL QUE E. COLI) ---
    sim_params = c.params()
    sim_params.set_param('numRunThreads', threads)
    sim_params.set_param('maxCycles', cycles)
    sim_params.set_param('timeStep', 0.1)
    
    sim_params.set_param('writeMediaLog', True)
    sim_params.set_param('MediaLogRate', 1)
    sim_params.set_param('writeTotalBiomassLog', True)
    
    initial_mass = [0, 0, mass]
    os.makedirs(folder_resultados, exist_ok=True)

    # --- 2. SELECCIONAR COMUNIDADES ---
    df = pd.read_csv(ruta_csv_syncoms)
    id_comunidad = df.columns[1:].tolist() # Asumiendo que la 1ra col es ID y el resto bacterias
    
    # --- 3. CARGAR MODELOS A MEMORIA ---
    modelos_base = {}
    lista_archivos = glob.glob(patron_xml)
    
    print(f"Cargando {len(lista_archivos)} modelos SBML...")
    for path_completo in lista_archivos:
        archivo = os.path.basename(path_completo)
        # Extraer ID (ej: ST001 de ST001_prokka...)
        model_id = archivo.split('_')[0] 
        try:
            modelos_base[model_id] = cobra.io.read_sbml_model(path_completo)
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")

    # --- 4. CICLO DE SIMULACIÓN ---
    for index, row in df.iterrows():
        num = row.iloc[0] # ID de la comunidad
        bacterias_en_comunidad = [col for col in df.columns[1:] if row[col] == 1]
        
        print(f"\n>>> Procesando Comunidad {num}: {bacterias_en_comunidad}")
        
        test_tube = c.layout()
        modelos_agregados = []

        try:
            # Agregar cada bacteria al layout
            for b_id in bacterias_en_comunidad:
                if b_id in modelos_base:
                    # Convertir modelo COBRA a COMETS
                    comets_model = c.model(modelos_base[b_id])
                    comets_model.id = b_id
                    comets_model.initial_pop = initial_mass
                    test_tube.add_model(comets_model)
                    modelos_agregados.append(b_id)
                else:
                    print(f"Advertencia: Modelo {b_id} no encontrado en archivos XML.")

            if not modelos_agregados:
                print(f"Saltando Comunidad {num}: No hay modelos válidos.")
                continue

            # --- CONFIGURACIÓN DEL MEDIO ---
            for met, conc in media.items():
                try:
                    test_tube.set_specific_metabolite(met, conc)
                except:
                    pass

            # Trace metabolites (Efecto Static como en el script de E. coli)
            trace_metabolites = ['ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e', 'h_e', 
                                 'k_e', 'h2o_e', 'mg2_e', 'mn2_e', 'mobd_e', 'na1_e', 'ni2_e', 
                                 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e']
            
            for i in trace_metabolites:
                test_tube.set_specific_metabolite(i, 1000)
                test_tube.set_specific_static(i, 1000)

            # --- EJECUCIÓN ---
            experiment = c.comets(test_tube, sim_params)
            experiment.run()

            # --- GUARDADO DE RESULTADOS (Lógica E. coli) ---
            
            # A. Biomasa
            df_biomasa = experiment.total_biomass
            if df_biomasa is not None:
                # Renombrar columnas para claridad
                df_biomasa.columns = ['cycle'] + modelos_agregados
                df_biomasa.to_csv(os.path.join(folder_resultados, f"comunidad_{num}_biomasa.csv"), index=False)

            # B. Metabolitos (Usando el filtro de 500 para ignorar los trace)
            df_metabolites = experiment.get_metabolite_time_series(upper_threshold=500.0)
            if df_metabolites is not None:
                df_metabolites.to_csv(os.path.join(folder_resultados, f"comunidad_{num}_metabolitos.csv"), index=False)
                
                # C. Concentraciones Finales (Opcional, igual que E. coli)
                ultimo_ciclo = df_metabolites['cycle'].max()
                mets_finales = df_metabolites[df_metabolites['cycle'] == ultimo_ciclo]
                mets_finales.to_csv(os.path.join(folder_resultados, f"comunidad_{num}_mets_finales.csv"), index=False)

            print(f"Comunidad {num} completada exitosamente.")

        except Exception as e:
            print(f"Error crítico en Comunidad {num}: {e}")
