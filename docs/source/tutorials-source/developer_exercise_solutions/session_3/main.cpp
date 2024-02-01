#include <Kokkos_Core.hpp>
#include <Kokkos_ScatterView.hpp>
#include <Kokkos_Random.hpp>
#include <mpi.h>

int main() {
    MPI_Init(NULL, NULL);
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

    // Distribute particles/nodes among tasks.
    int comm_size;
    MPI_Comm_size(MPI_COMM_WORLD, &comm_size);
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    int local_num_particles = num_particles / comm_size;
    if (rank < num_particles % comm_size) {
        local_num_particles++;
    }
    int local_num_nodes = num_nodes / comm_size;
    if (rank < num_nodes % comm_size) {
        local_num_nodes++;
    }
    // Number of nodes each task will receive in the Reduce_scatter.
    std::vector<int> scatter_counts(comm_size, num_nodes / comm_size);
    for (int i=0; i<num_nodes % comm_size; i++) {
        scatter_counts[i]++;
    }

    Kokkos::View<double*> positions("positions", local_num_particles);
    Kokkos::View<double*> velocities("velocities", local_num_particles);

    Kokkos::View<double*> charge("charge", num_nodes);
    Kokkos::Experimental::ScatterView<double*> scatter_charge(charge);
    std::vector<double> local_charge(local_num_nodes);

    // Uniformly distribute particle positions
    // and draw velocities from Gaussian.
    Kokkos::Random_XorShift64_Pool<> rand_pool(0);
    Kokkos::parallel_for(
        "initializeParticles",
        local_num_particles,
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
            local_num_particles,
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

#if MPIX_CUDA_AWARE_SUPPORT && defined(KOKKOS_ENABLE_CUDA)
        Kokkos::View<double*> mpi_charge = charge;
#else
        Kokkos::View<double*>::HostMirror mpi_charge = Kokkos::create_mirror_view(charge);
        Kokkos::deep_copy(mpi_charge, charge);
#endif // MPIX_CUDA_AWARE_SUPPORT && defined(KOKKOS_ENABLE_CUDA)
        MPI_Reduce_scatter(
            mpi_charge.data(),
            local_charge.data(),
            scatter_counts.data(),
            MPI_DOUBLE,
            MPI_SUM,
            MPI_COMM_WORLD
        );
    }

    MPI_Finalize();
    return 0;
}
