## ==== P1.4: CGAL Voronoi decomposition ====
##
## The container holds only the compiled CGAL program. Your data is mounted into
## it read-only and the program's output is captured out here on the host, so
## nothing inside the container can write into your working folder.
##
## Usual workflow:  make run-cgal
##
## Both the image and the output are tracked by file timestamps, so re-running
## `make run-cgal` when nothing has changed does no work at all -- it will not
## even talk to Docker.

MAJOR ?= 1
MINOR ?= 0
VERSION  = $(MAJOR).$(MINOR)
APP_NAME ?= aii601-p1-cgal
IMAGE     = $(APP_NAME):$(VERSION)

DATA_DIR   = $(CURDIR)/src/data
DATA_FILES = $(wildcard src/data/*.cin)
RESULT     = results/voronoi_lines.txt

# The segment file to decompose. $(DATA_DIR) is mounted at /work/data inside the
# container, so the program is handed the same file as data/$(DATA_NAME).
DATA_NAME ?= data_aii601.cin

# Marks that $(IMAGE) has been built from the current sources. Rebuilt whenever
# the Dockerfile or the C++ program changes.
IMAGE_STAMP = .docker-image.stamp

.DEFAULT_GOAL := help
.PHONY: help
help:  ## Show this help message
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

$(IMAGE_STAMP): Dockerfile src/CMakeLists.txt src/vd_2_point_location.cpp
	@echo "Building the Docker container..."
	DOCKER_CLI_HINTS=false docker build -t $(IMAGE) -f Dockerfile .
	touch $@

.PHONY: build
build: $(IMAGE_STAMP)  ## Build the container if the Dockerfile or C++ source changed

.PHONY: rebuild
rebuild:  ## Rebuild from scratch, ignoring the layer cache
	DOCKER_CLI_HINTS=false docker build --no-cache -t $(IMAGE) -f Dockerfile .
	touch $(IMAGE_STAMP)

$(RESULT): $(IMAGE_STAMP) $(DATA_FILES)
	mkdir -p results
	@echo "Running CGAL..."
	docker run --init --rm \
		--volume="$(DATA_DIR):/work/data:ro" \
		$(IMAGE) data/$(DATA_NAME) > results/.voronoi_lines.tmp \
		|| { rm -f results/.voronoi_lines.tmp; \
		     echo "CGAL run failed -- see the output above."; exit 1; }
	mv results/.voronoi_lines.tmp $@
	@echo "Done: $@ ($$(wc -l < $@ | tr -d ' ') lines)"

.PHONY: run-cgal
run-cgal: $(RESULT)  ## Generate results/voronoi_lines.txt from src/data/

.PHONY: shell
shell: $(IMAGE_STAMP)  ## Open a shell inside the container, for poking around
	docker run --init -it --rm \
		--volume="$(DATA_DIR):/work/data:ro" \
		--entrypoint bash \
		$(IMAGE)

.PHONY: clean
clean:  ## Remove the generated Voronoi output and the image stamp
	rm -f $(RESULT) results/.voronoi_lines.tmp $(IMAGE_STAMP)
