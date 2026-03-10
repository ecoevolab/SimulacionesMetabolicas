from variables_funtion import variables_totales
import glob


paths = {
    "rast": glob.glob("/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data/rizo/kbase/ST*.fbamodel.xml"),
}

variables_totales(paths, "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/reacciones")

