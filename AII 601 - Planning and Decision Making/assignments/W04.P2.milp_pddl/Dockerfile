# Minimal container for P2.3's PDDL planning with Fast Downward.
#
# Two stages, the same shape as P1.4's CGAL container: build Fast Downward with
# a full toolchain, then ship only what running a plan actually needs -- the
# search binary, the Python translator, and the driver that ties them together.
# None of the build tooling (cmake, g++, git) reaches the final image.
#
# There is no course Python environment in here on purpose -- the notebook half
# of P2 runs under uv on your own machine. This container does exactly one job:
# turn a PDDL domain and problem into a plan.
#
# Your pddl/ folder is NOT baked into the image; it is mounted at run time (see
# the Makefile), so editing a domain file does not force a rebuild.

# ---- build stage ----
FROM debian:bookworm-slim AS build

ARG NUM_BUILD_CORES=4

# Which benchmark domains to ship. P2.3 only ever runs `blocks`, and the full
# benchmark repository is a few hundred megabytes of PDDL that the assignment
# never touches. To explore further, pass a longer list:
#
#     make build BENCHMARK_DOMAINS="blocks gripper logistics00"
#
# or "." for all of them.
ARG BENCHMARK_DOMAINS="blocks"

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        g++ \
        git \
        make \
        python3 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/aibasel/downward.git /downward \
    && cd /downward && ./build.py -j${NUM_BUILD_CORES}

# A release build still carries its debug symbols, which are most of the search
# binary's size and of no use to anyone running a plan. Stripping is its own
# layer so editing it does not invalidate the (slow) compile above.
RUN strip /downward/builds/release/bin/downward

RUN git clone --depth 1 \
        https://github.com/aibasel/downward-benchmarks.git /benchmarks-src \
    && mkdir -p /benchmarks \
    && for d in ${BENCHMARK_DOMAINS}; do cp -R "/benchmarks-src/$d" /benchmarks/; done

# ---- runtime stage ----
FROM debian:bookworm-slim

# python3 runs the driver and the translator; libstdc++6 is what the C++ search
# binary links against. Nothing else is needed to plan.
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Everything ./fast-downward.py reaches for, and nothing else: the entry point,
# the driver package, and the built bin/ holding the `downward` search binary
# next to the `fast_downward` translator module.
COPY --from=build /downward/fast-downward.py   /downward/fast-downward.py
COPY --from=build /downward/driver             /downward/driver
COPY --from=build /downward/builds/release/bin /downward/builds/release/bin
COPY --from=build /benchmarks                  /downward/pddl-benchmark-examples

RUN echo 'export PS1="AII601.P2: \w $ "' >> /root/.bashrc

WORKDIR /downward
