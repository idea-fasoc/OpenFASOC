# Makefile for installing and updating dependencies

DEPENDENCIES_SCRIPT = dependencies.sh

# Phony targets
.PHONY: install update #clean clean_install clean_update

# Default target
all: install update

# Target for installing dependencies
install:
	echo "y" | ./$(DEPENDENCIES_SCRIPT)

# Target for updating dependencies
update:
	echo "u" | ./$(DEPENDENCIES_SCRIPT)

# # Target for cleaning up generated files
# clean:
# 	# Command to clean up generated files goes here, but
# 	# currently this makefile does not generate new files in the first place

# # Target for cleaning up and reinstalling dependencies
# clean_install: clean install

# # Target for cleaning up and updating dependencies
# clean_update: clean update
