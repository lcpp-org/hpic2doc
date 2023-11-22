#include <Kokkos_Core.hpp>
#include <Kokkos_ScatterView.hpp>
#include <Kokkos_Random.hpp>

int main() {
    Kokkos::ScopeGuard scope_guard;

    // "Physical" and numerical parameters.
    int num_particles = 10000;
    double particle_weight = 1.0;
    double particle_sqrtkT_over_m = 1.0;
    int num_elems = 1000;
    int num_nodes = num_elems + 1;
    double dx = 1.0e-2;
    double length = dx * num_elems;
    int num_timesteps = 1000;
    double dt = 1.0e-12;
    double accel = 9.8;

    Kokkos::View<double*> positions("positions", num_particles);
    Kokkos::View<double*> velocities("velocities", num_particles);

    Kokkos::View<double*> charge("charge", num_nodes);
    Kokkos::Experimental::ScatterView<double*> scatter_charge(charge);

    // Uniformly distribute particle positions
    // and draw velocities from Gaussian.
    Kokkos::Random_XorShift64_Pool<> rand_pool(0);
    Kokkos::parallel_for(
        "initializeParticles",
        num_particles,
        KOKKOS_LAMBDA (const int ipart)
    {
        auto rgen = rand_pool.get_state();
        positions(ipart) = rgen.drand(0.0, length);
        velocities(ipart) = rgen.normal(0.0, particle_sqrtkT_over_m);
        rand_pool.free_state(rgen);
    });

    for (int istep=0; istep<num_timesteps; istep++) {
        scatter_charge.reset();

        Kokkos::parallel_for(
            "particlePush",
            num_particles,
            KOKKOS_LAMBDA (const int jpart)
        {
            // Accelerate + push
            velocities(jpart) += accel * dt;
            double &position = positions(jpart);
            position += velocities(jpart) * dt;
            // Periodic BCs
            while (position > length) {
                position -= length;
            }
            while (position < 0.0) {
                position += length;
            }

            // Determine adjacent nodes
            int left_node = position / dx;
            double left_node_pos = dx * left_node;
            double right_weight = (position - left_node_pos) / dx;
            double left_weight = 1.0 - right_weight;

            // Add into ScatterView
            auto access = scatter_charge.access();
            access(left_node) += particle_weight * left_weight;
            access(left_node+1) += particle_weight * right_weight;
        });

        Kokkos::Experimental::contribute(charge, scatter_charge);

        // I'm gonna print out the charge too.
        Kokkos::View<double*>::HostMirror h_charge =
            Kokkos::create_mirror_view(charge);
        Kokkos::deep_copy(h_charge, charge);
        std::cout << "Charge at timestep " << istep << std::endl;
        for (int jnode=0; jnode<num_nodes; jnode++) {
            std::cout << h_charge(jnode) << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}
