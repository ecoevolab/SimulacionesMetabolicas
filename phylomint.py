import os
import sys

# agregar ruta
sys.path.append('/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data/PhyloMint')

from lib import BuildGraphNetX, CalculateIndexes

input_dir = '/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data/rizo/carveme/prokka'
output_file = '/home/abigaylmontantearenas/Documents/proyecto_tesis/phylomint/prueba.tsv'

maxcc = 5

# obtener archivos xml
files = [f for f in os.listdir(input_dir) if f.endswith('.xml')]

# guardar datos
ConfidenceDic = {}
nonSeedSetDic = {}

# calcular seed sets
for f in files:
    path = os.path.join(input_dir, f)
    name = f.replace('.xml', '')

    print(f'Procesando: {name}')

    DG = BuildGraphNetX.buildDG(path)
    conf, seed, nonseed = BuildGraphNetX.getSeedSet(DG, maxComponentSize=maxcc)

    ConfidenceDic[name] = conf
    nonSeedSetDic[name] = nonseed

# calcular índices
with open(output_file, 'w') as out:
    out.write('A\tB\tCompetition\tComplementarity\n')

    for A in files:
        for B in files:
            A_name = A.replace('.xml', '')
            B_name = B.replace('.xml', '')

            comp = CalculateIndexes.MetabolicCompetitionIdx(
                ConfidenceDic[A_name], ConfidenceDic[B_name]
            )

            coop = CalculateIndexes.MetabolicCooperationIdx(
                ConfidenceDic[A_name],
                ConfidenceDic[B_name],
                nonSeedSetDic[B_name]
            )

            out.write(f'{A_name}\t{B_name}\t{comp}\t{coop}\n')

print("Listo 🚀")