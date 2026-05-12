import cobra

model = cobra.io.read_sbml_model("/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/gemsembler_output/60_core3.xml")

# ejecucion FBA
solution = model.optimize()

# optimal se refiere a si el software encontró una solución que maximiza la función objetivo (en este caso, la tasa de crecimiento) dentro de las restricciones del modelo. Si el estado es 'optimal', significa que se encontró una solución óptima para el problema de optimización planteado por el modelo metabólico.
# objective_value valor numerico de tasa de crecimiento
# .4f decimales que quiero qeu muetre
# h^-1 unidades tasa crecimiento
if solution.status == 'optimal':
    print(f"Tasa de crecimiento: {solution.objective_value:.4f} h^-1")
else:
    print(f"El modelo NO es funcional. Estado: {solution.status}")
        


