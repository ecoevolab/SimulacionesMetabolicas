from comets_functions import media, load_strains, set_sim_params
import cometspy as c
import os
# import argparse



if __name__ == "__main__":
    args = {"gem_path": '/home/sur/lab/exp/2026/today/gems',
            "strains": ['ST00042', 'ST00046'],
            "gem_suffix": '.xml',
            "media": 'lb',
            "media_dil": 0.1,
            "threads": 4,
            "cycles": 20,
            "initial_mass": 1e-8,
            "add_trace_metabolites": True,
            "outdir": 'output'}
    
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
        
    # Set simulation parameters
    sim_params = set_sim_params(args)


    # Create output directory, error if already exists
    if os.path.exists(args["outdir"]):
        raise FileExistsError(f"Output directory {args['outdir']} already exists. Please choose a different name or remove it.") 
    os.makedirs(args["outdir"])

    # Run simulation
    sim = c.comets(layout, sim_params)
    print("Starting simulation...")
    sim.run()






 