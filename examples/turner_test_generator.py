# Before running these problems, the following steps must be performed:
# 1. Download the supplementary material from Turner's paper:
#    https://doi.org/10.1063/1.4775084
# 2. Copy the cross section data into space-separated .dat files for each
#    collision type, with the units converted to SI.
#    I.e., convert electron-volts to joules and 10^-20 m^2 to m^2.
#    The filenames should be
#    he_ion_elastic.dat for the ion-neutral isotropic elastic collisions,
#    he_ion_back.dat for the ion-neutral backscattering collisions,
#    he_electron_elastic.dat for the electron-neutral elastic collisions,
#    he_electron_excitation_1.dat for the first set of excitation collisions,
#    he_electron_excitation_2.dat for the second set of excitation collisions,
#    he_electron_ionization.dat for the electron-neutral ionization collisions.

import numpy as np
import sys
import matplotlib.pyplot as plt
import h5py

def main(params):
    tag = params["tag"]
    length = 6.7e-2
    neutral_n = params["neutral_n"]
    neutral_temp = 300.0
    frequency = 13.56e6
    voltage = params["voltage"]
    simulation_periods = params["simulation_periods"]
    simulation_time = simulation_periods / frequency

    electron_mass = 9.109e-31
    ion_mass = 6.67e-27

    plasma_density = params["plasma_density"]
    electron_temperature = 30_000.0
    ion_temperature = 300.0
    ppc = params["ppc"]

    num_cells = params["num_cells"]
    num_time_steps = params["num_time_steps"]

    input_deck = f"""
[input_mode]
hpic_mode = "pic"
simulation_tag = "{tag}"
units = "si"

[mesh]
type = "uniform"
    [mesh.type_specification]
    x1_points = [0.0, {length}]
    x1_num_elems = {num_cells}

[time]
termination_time = {simulation_time}
num_time_steps = {num_time_steps}

[species."e"]
mass = {electron_mass}
type = "boris_buneman"
    [species."e".type_params]
    atomic_number = -1
    initial_condition = "uniform_beam"
        [species."e".type_params.initial_condition_params]
        num_particles = {ppc*num_cells}
        charge_states = [ {{ charge_number = -1, density = {plasma_density} }} ]
        flow_velocity_1 = 0.0
        flow_velocity_2 = 0.0
        flow_velocity_3 = 0.0
        temperature = {electron_temperature}
        [[species."e".type_params.boundary_conditions]]
        boundary = "west"
        type = "absorbing"
        [[species."e".type_params.boundary_conditions]]
        boundary = "east"
        type = "absorbing"

[species."He+"]
mass = {ion_mass}
type = "boris_buneman"
    [species."He+".type_params]
    atomic_number = 2
    initial_condition = "uniform_beam"
        [species."He+".type_params.initial_condition_params]
        num_particles = {ppc*num_cells}
        charge_states = [ {{ charge_number = 1, density = {plasma_density} }} ]
        flow_velocity_1 = 0.0
        flow_velocity_2 = 0.0
        flow_velocity_3 = 0.0
        temperature = {ion_temperature}
        [[species."He+".type_params.boundary_conditions]]
        boundary = "west"
        type = "absorbing"
        [[species."He+".type_params.boundary_conditions]]
        boundary = "east"
        type = "absorbing"

[species."He"]
mass = {ion_mass + electron_mass}
type = "uniform_background"
[species."He".type_params]
    charge_number = 0
    density = {neutral_n}
    temperature = {neutral_temp}

[magnetic_field]
type = "uniform"
    [magnetic_field.type_params]
    b1 = 0.0
    b2 = 0.0
    b3 = 0.0

[[interactions.MCC]]
source_species = "He+"
target_species = "He"
cross_section = "from_file"
effect = "isotropic_scattering"
    [interactions.MCC.cross_section_params]
    filename = "he_ion_elastic.dat"
    [interactions.MCC.effect_params]
    heat_of_reaction = 0.0 # elastic

[[interactions.MCC]]
source_species = "He+"
target_species = "He"
cross_section = "from_file"
effect = "backward_scattering"
    [interactions.MCC.cross_section_params]
    filename = "he_ion_back.dat"
    [interactions.MCC.effect_params]
    heat_of_reaction = 0.0 # elastic

[[interactions.MCC]]
source_species = "e"
target_species = "He"
cross_section = "from_file"
effect = "isotropic_scattering"
    [interactions.MCC.cross_section_params]
    filename = "he_electron_elastic.dat"
    [interactions.MCC.effect_params]
    heat_of_reaction = 0.0 # elastic

[[interactions.MCC]]
source_species = "e"
target_species = "He"
cross_section = "from_file"
effect = "isotropic_scattering"
    [interactions.MCC.cross_section_params]
    filename = "he_electron_excitation_1.dat"
    [interactions.MCC.effect_params]
    heat_of_reaction = 3.175514088587999860e-18

[[interactions.MCC]]
source_species = "e"
target_species = "He"
cross_section = "from_file"
effect = "isotropic_scattering"
    [interactions.MCC.cross_section_params]
    filename = "he_electron_excitation_2.dat"
    [interactions.MCC.effect_params]
    heat_of_reaction = 3.302086042673999814e-18

[[interactions.MCC]]
source_species = "e"
target_species = "He"
cross_section = "from_file"
effect = "kinetic_ionization"
    [interactions.MCC.cross_section_params]
    filename = "he_electron_ionization.dat"
    [interactions.MCC.effect_params]
    heat_of_reaction = 3.939752343005999908e-18
    ion_species = "He+"

[electric_potential]
poisson_solver = "hypre"
    [[electric_potential.boundary_conditions]]
    boundary = "west"
    type = "dirichlet"
    function = "constant"
        [electric_potential.boundary_conditions.function_params]
        value = 0.0
    [[electric_potential.boundary_conditions]]
    boundary = "east"
    type = "dirichlet"
    function = "sine"
        [electric_potential.boundary_conditions.function_params]
        amplitude = {voltage}
        angular_frequency = {2.0 * np.pi * frequency}

[output_diagnostics]
output_dir = "{tag}_out"
    [output_diagnostics.logging]
    log_level = "debug"
    timing_log_enabled = false

    [output_diagnostics.moment_output]
    stride = 1
    species = ["He+"]
    lab_frame_moment_exponents = [[0,0,0]]

    """

    with open(f"{tag}.toml", 'w') as f:
        f.write(input_deck)

def plot(tag):
    helium_mass = 6.67e-27
    output_filename = f"{tag}_out/{tag}_moments.hdf"
    file = h5py.File(output_filename, 'r')
    num_cells = file["VTKHDF/NumberOfCells"][0]
    num_points = num_cells+1
    normalized_points = np.linspace(0.0, 1.0, num=num_points)
    normalized_cell_centers = (normalized_points[:-1] + normalized_points[1:])/2.0
    nsteps = file["VTKHDF/Steps"].attrs["NSteps"]
    ion_density = file["VTKHDF/CellData/He+_lab_frame_moment_000"]
    ion_density = np.reshape(ion_density, (nsteps, -1))
    # Set the upper plot limit to match Turner's plots
    # and also only consider the last few time steps,
    # depending on the test case.
    ylim = 0.0
    if tag == "test_1":
        ylim = 0.16
        ion_density = ion_density[-12800:,:]
    elif tag == "test_2":
        ylim = 1.0
        ion_density = ion_density[-25600:,:]
    elif tag == "test_3":
        ylim = 2.0
        ion_density = ion_density[-51200:,:]
    elif tag == "test_4":
        ylim = 2.8
        ion_density = ion_density[-102400:,:]
    avg_ion_density = np.mean(ion_density, axis=0)/helium_mass
    plt.plot(normalized_cell_centers, avg_ion_density/1.e15)
    plt.ylim((0, ylim))
    plt.xlim((0.0, 1.0))
    plt.xlabel("x/L")
    plt.ylabel("ion number density (10^15 m^-3)")
    plt.savefig(f"{tag}.png")
    plt.close()

if __name__ == "__main__":
    test_cases = [{
        "tag" : "test_1",
        "neutral_n" : 9.64e20,
        "voltage" : 450.0,
        "simulation_periods" : 1280,
        "plasma_density" : 2.56e14,
        "ppc" : 512,
        "num_cells" : 128,
        "num_time_steps" : 512_000
    }, {
        "tag" : "test_2",
        "neutral_n" : 32.1e20,
        "voltage" : 200.0,
        "simulation_periods" : 5120,
        "plasma_density" : 5.12e14,
        "ppc" : 256,
        "num_cells" : 256,
        "num_time_steps" : 4_096_000
    }, {
        "tag" : "test_3",
        "neutral_n" : 96.4e20,
        "voltage" : 150.0,
        "simulation_periods" : 5120,
        "plasma_density" : 5.12e14,
        "ppc" : 128,
        "num_cells" : 512,
        "num_time_steps" : 8_192_000
    }, {
        "tag" : "test_4",
        "neutral_n" : 321.0e20,
        "voltage" : 120.0,
        "simulation_periods" : 15_360,
        "plasma_density" : 3.84e14,
        "ppc" : 64,
        "num_cells" : 512,
        "num_time_steps" : 49_152_000
    }]

    if len(sys.argv) > 1:
        plot(sys.argv[1])
    else:
        for test_case in test_cases:
            main(test_case)
