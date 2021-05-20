# FILES AND FOLDERS
PROJECT_NAME := warnings-dropoff-analysis
PACKAGE_NAME := warnings_dropoff_analysis
MAIN := -m $(PACKAGE_NAME)
PROGRAM_FLAGS := Wikipedia-breaks-uw cawiki_users --output-compression gzip
FUNCTION_TO_RUN := extract-user-warnings-metrics
FUNCTION_SUB_COMMANDS := 6
DOCS_FOLDER := docs

# COMMANDS
ECHO := echo -e
MKDIR := mkdir -p

# COLORS
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
NONE := \033[0m

# PLOTTER
PLOTTER := plotter/retired_stats.py 
PLOTTER_ARGV := es

# RULES

.PHONY: run coverage build test update check show lint fix doc openDoc install all installBasePkg buildDocsFolder help envinfo env deleteenv plot

.SILENT:

# Run with poetry
run:
	$(ECHO) '$(BLUE)Running the application...$(NONE)'
	@poetry run python $(MAIN) $(PROGRAM_FLAGS) $(FUNCTION_TO_RUN) $(FUNCTION_SUB_COMMANDS)
	$(ECHO) '$(BLUE)Done$(NONE)'

# Build
build:
	$(ECHO) '$(GREEN)Building the source..$(NONE)'
	@poetry build
	$(ECHO) '$(GREEN)Done$(NONE)'

# Tests
test:
	$(ECHO) '$(YELLOW)Running tests...$(NONE)'
	@poetry run pytest
	$(ECHO) '$(YELLOW)Done$(NONE)'

# Test coverage
coverage:
	$(ECHO) '$(YELLOW)Running coverage report...$(NONE)'
	@poetry run coverage run --source=$(PACKAGE_NAME) -m unittest discover
	@poetry run coverage report
	$(ECHO) '$(YELLOW)Done$(NONE)'

# Update dependencies
update:
	$(ECHO) '$(GREEN)Updating dependencies...$(NONE)'
	@poetry update
	$(ECHO) '$(GREEN)Done$(NONE)'

# Check if the structure of the pyproject.toml is correct and reports errors if any
check:
	$(ECHO) '$(GREEN)Checking toml integrity...$(NONE)'
	@poetry check
	$(ECHO) '$(GREEN)Done$(NONE)'

# Show packages
show:
	$(ECHO) '$(GREEN)Packages:$(NONE)'
	@poetry show
	$(ECHO) '$(GREEN)Done$(NONE)'

# lint
lint:
	@poetry run pylint --disable=W0311 $(PACKAGE_NAME)

fix:
	@poetry run autopep8 --in-place --aggressive --recursive $(PACKAGE_NAME)

# Documentation
doc: buildDocsFolder
	@poetry run pdoc --html $(PACKAGE_NAME) --output-dir $(DOCS_FOLDER) --force
	$(ECHO) 'Documentation generated'

# Open the documentation
openDoc: doc
	$(ECHO) '$(GREEN)Opening documentation...$(NONE)'
	@xdg-open $(DOCS_FOLDER)/$(PACKAGE_NAME)/index.html
	$(ECHO) '$(GREEN)Done$(NONE)'

# Install all the dependencies and resolve them in the pyproject.toml
install:
	$(ECHO) '$(GREEN)Install the dependencies...$(NONE)'
	@poetry install
	$(ECHO) '$(GREEN)Done$(NONE)'

# build the plots using the plotter
plot:
	$(ECHO) '$(BLUE)Plotting graphs..$(NONE)'
	@poetry run python $(PLOTTER) $(PLOTTER_ARGV)
	$(ECHO) '$(BLUE)Done$(NONE)'

# Generate the documentation and runs it
all:
	doc
	run

# install the basics packages, just to get started
installBasePkg:
	$(ECHO) '$(GREEN)Adding useful development dependencies...$(NONE)'
	@poetry add pytest@latest --dev
	@poetry add pdoc@latest --dev
	@poetry add pylint@latest --dev
	@poetry add autopep8@latest --dev
	@poetry add faker@latest --dev
	@poetry add coverage@latest --dev
	$(ECHO) '$(GREEN)Done$(NONE)'

# Create the docs folder if it does not exists
buildDocsFolder: 
	$(MKDIR) $(DOCS_FOLDER)

# To define the help command
help:
	$(ECHO) "Makefile help\n \
	* run			: runs the main file within the poetry virtual environment\n \
	* plot			: plot grahs\n \
	* build		: builds the source \n \
	* coverage		: runs the coverage command and outputs the tests coverage\n \
	* test 		: runs the test\n \
	* update 		: updates the poetry dependencies\n \
	* check 		: checks the structure of the pyproject.toml is correct and reports errors if any\n \
	* show 		: shows poetry packages\n \
	* lint 		: runs the linter\n \
	* fix 			: fixes, if possibile, some linter warnings automatically\n \
	* doc 			: generates the documentation\n \
	* openDoc 		: generates and opens the documentation\n \
	* install 		: install the packages within the poetry virtual environment\n \
	* all 			: generates the documentation and runs the application\n \
	* installBasePkg	: installs the basic packages\n \
	* envinfo 		: shows the poetry virtual environment information\n \
	* env 			: generates the poetry virtual environment\n \
	* deleteenv		: deletes the poetry virtual environment"

# environment info
envinfo:
	$(ECHO) '$(GREEN)Env info:$(NONE)'
	@poetry env info

# Create the environment for the project
env:
	$(ECHO) '$(GREEN)Creating virtual environment...$(NONE)'
	which python | xargs poetry env use

# delete env
deleteenv:
	$(ECHO) '$(RED)Deleting virtual environment...$(NONE)'
	poetry env info --path | sed "s/.*\///" | xargs poetry env remove
