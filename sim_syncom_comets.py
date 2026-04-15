from comets_functions import media, load_strains, set_sim_params
import cometspy as c
import os
# import argparse

if __name__ == "__main__":
    args = {"gem_path": '/home/sur/lab/exp/2026/2026-04-14.sim_syncom_comets/gems/',
            "strains": ['ST00042', 'ST00046'],
            "gem_suffix": '.xml',
            "media": 'lb',
            "media_dil": 0.1,
            "threads": 4,
            "cycles": 20,
            "initial_mass": 1e-8,
            "add_trace_metabolites": True,
            "outdir": 'output'

    }
    # In the future we can do something more fancy with layout
    layout = c.layout()

    # Dictionary of strains and their corresponding GEM paths
    models = dict()
    for strain in args["strains"]:
        gem_file = os.path.join(args["gem_path"], f"{strain}{args['gem_suffix']}")
        if not os.path.isfile(gem_file):
            raise FileNotFoundError(f"GEM file for strain {strain} not found at {gem_file}")            
        models[strain] = gem_file

    # Load models into the layout
    layout = load_strains(layout, models, initial_mass=args["initial_mass"])    

    # Set media
    for metabolite, amount in media(args["media"], dil = args["media_dil"]).items():
        layout.set_specific_metabolite(metabolite, amount)
    
    if(args["add_trace_metabolites"]):
        layout.add_typical_trace_metabolites(amount=1000)
        
    # Set simulation parameters.
    sim_params = set_sim_params(args)
    # print(sim_params.show_params().to_string())

    # Create output directory, error if already exists
    if os.path.exists(args["outdir"]):
        raise FileExistsError(f"Output directory {args['outdir']} already exists. Please choose a different name or remove it.") 
    os.makedirs(args["outdir"])
    os.makedirs("temp")



    # Prepare simulation
    # print(sim_params.get_param("TotalBiomassLogName"))
    # print(sim_params.get_param("MediaLogName"))
    sim = c.comets(layout = layout, parameters = sim_params, relative_dir="temp")
    # Very ugly, but I need to redefine the output filenames
    # https://github.com/segrelab/cometspy/issues/64
    sim.parameters.set_param("BiomassLogName", os.path.join(args["outdir"], "biomass.txt"))
    sim.parameters.set_param("FluxLogName", os.path.join(args["outdir"], "flux.txt"))
    sim.parameters.set_param("MediaLogName", os.path.join(args["outdir"], "media.txt"))
    sim.parameters.set_param("TotalBiomassLogName", os.path.join(args["outdir"], "total_biomass.txt"))
    # sim.parameters.set_param("velocityMultiConvLogName", os.path.join(args["outdir"], "velocity.txt"))

    # print(sim.parameters.get_param("TotalBiomassLogName"))
    # print(sim_params.get_param("TotalBiomassLogName"))
    # print(sim.parameters.get_param("MediaLogName"))
    # print(sim_params.get_param("MediaLogName"))

    print("Starting simulation...")
    sim.run(delete_files=False)
    print(sim.run_output)

    # sim.get_species_exchange_fluxes()


 