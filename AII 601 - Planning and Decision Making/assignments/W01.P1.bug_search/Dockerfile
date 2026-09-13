# Minimal container for the P1.4 CGAL Voronoi program.
#
# Two stages: compile against the CGAL headers with a full toolchain, then ship
# only the resulting binary plus the two libraries it actually links against.
# The final image is tens of megabytes rather than ~1 GB, and none of the build
# tooling reaches it.
#
# There is no Python and no Jupyter in here on purpose -- those live in the
# course's uv environment on your own machine. This container does exactly one
# job: turn a file of line segments into a Voronoi decomposition.
#
# The input data is NOT baked into the image; it is mounted at run time (see the
# Makefile), so editing src/data/*.cin does not force a rebuild.

# ---- build stage ----
FROM debian:bookworm-slim AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
        g++ \
        cmake \
        make \
        libcgal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY src/CMakeLists.txt src/vd_2_point_location.cpp /src/
RUN cmake -S /src -B /build -DCMAKE_BUILD_TYPE=Release && cmake --build /build

# ---- runtime stage ----
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgmp10 \
        libmpfr6 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /build/vd_2_point_location /usr/local/bin/vd_2_point_location

# The program reads "data/data_*.cin" relative to its working directory and
# writes the Voronoi lines to stdout.
WORKDIR /work
ENTRYPOINT ["vd_2_point_location"]
