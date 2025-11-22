import cometspy as c
import cobra.io


modelo = cobra.io.read_sbml_model('02_data/rizo/carveme/ST00000_dimont_carveme_lb.xml')

print(len(modelo.metabolites))
print(len(modelo.genes))
print(len(modelo.reactions))