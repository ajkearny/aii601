## ==== P2.3: Fast Downward and PDDL ====
##
## The container holds Fast Downward and the Downward benchmark problems. The
## `pddl/` folder beside this Makefile is mounted into it read-write, so the
## domain and problem files you edit out here are the ones the planner reads.
##
## Usual workflow:  make downward
##
## That builds the image if it is not already built, then drops you at a shell
## inside the container with /downward as the working directory.

## ==== Core Arguments and Parameters ====
MAJOR ?= 0
MINOR ?= 1
VERSION = $(MAJOR).$(MINOR)
APP_NAME ?= aii601-p2-pddl

# Build parallelism. `getconf` answers on both macOS and Linux; /proc/cpuinfo,
# the usual incantation, does not exist on a Mac and just prints an error.
NUM_BUILD_CORES ?= $(shell getconf _NPROCESSORS_ONLN 2>/dev/null)
NUM_BUILD_CORES := $(if $(NUM_BUILD_CORES),$(NUM_BUILD_CORES),4)

# Benchmark domains baked into the image. P2.3 only uses `blocks`; widen it to
# explore, e.g. `make build BENCHMARK_DOMAINS="blocks gripper"`, or "." for all.
BENCHMARK_DOMAINS ?= blocks

# Docker args
DOCKER_FILE_DIR = "."
DOCKERFILE = ./Dockerfile
IMAGE_NAME = ${APP_NAME}
PDDL_DIR = $(shell pwd)/pddl

.DEFAULT_GOAL := help
.PHONY: help
help:  ## Show this help message
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: build
build:  ## Build the Fast Downward container
	@echo "Building the Docker container ($(NUM_BUILD_CORES) threads)"
	@docker build -t ${IMAGE_NAME}:${VERSION} \
		--build-arg NUM_BUILD_CORES=$(NUM_BUILD_CORES) \
		--build-arg BENCHMARK_DOMAINS="$(BENCHMARK_DOMAINS)" \
		-f ./${DOCKERFILE} .

.PHONY: rebuild
rebuild:  ## Rebuild from scratch, ignoring the layer cache
	@docker build -t ${IMAGE_NAME}:${VERSION} --no-cache \
		--build-arg NUM_BUILD_CORES=$(NUM_BUILD_CORES) \
		--build-arg BENCHMARK_DOMAINS="$(BENCHMARK_DOMAINS)" \
		-f ./${DOCKERFILE} .

.PHONY: downward
downward: build  ## Build if needed, then open a shell with pddl/ mounted
	@docker run --init -it --rm \
		--volume="$(PDDL_DIR):/downward/pddl:rw" \
		${IMAGE_NAME}:${VERSION} \
		bash

.PHONY: shell
shell:  ## Open a shell in the container without mounting pddl/
	@docker run --init -it --rm \
		${IMAGE_NAME}:${VERSION} \
		bash
