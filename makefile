# This Makefile generates files for printing SCAD documents
# and is targeted towards single scad projects with multiple variations
# Copyright (C) 2022  Brian Khuu | https://briankhuu.com/
# License: GNU GPL v3 (or later)
## make all    Generate STL and all of it's variations
## make clean  delete all STL and all of it's variations
################################################################################

# OS DETECT https://stackoverflow.com/questions/714100/os-detecting-makefile
ifeq ($(OS),Windows_NT)
    RM_WILDCARD = del /Q /F /S
    MKDIR = mkdir
    RMDIR = rmdir /s /q
    PYTHON = python3
else
    RM_WILDCARD = rm -f
    MKDIR = mkdir
    RMDIR = rmdir
    PYTHON = python3
endif

# SCAD Compiler
SCADC?=openscad

# Parametric Generator
PARAGEN?=parameter_generator.py

# Variation Generator
VARGEN?=parameter_variants.py

# Model Details
PROJNAME = test
SCAD_PATH = models/$(PROJNAME).scad
JSON_PATH = models/$(PROJNAME).json

# Get list of variants
ifneq ("$(wildcard $(JSON_PATH))","")
# parametric configuration json file found. return a list of variants used in this project
	VARIANTS = $(shell $(PYTHON) $(VARGEN) --JsonPath $(JSON_PATH) --PrintTarget)
else
# parametric configuration json file missing. Generate the missing file and return a list of variants that was just generated
	VARIANTS = $(shell $(PYTHON) $(PARAGEN) --JsonPath $(JSON_PATH) --PrintTarget --WriteParameter)
endif

# Get list of targets
VARIANTS_TARGETS = $(patsubst %,variants/%.json,$(VARIANTS))
PNG_TARGETS      = $(patsubst %,png/$(PROJNAME).%.png,$(VARIANTS))
STL_TARGETS      = $(patsubst %,stl/$(PROJNAME).%.stl,$(VARIANTS))

# explicit wildcard expansion suppresses errors when no files are found
include $(wildcard deps/*.deps)

################################################################################
.PHONY: all variants png models clean dev
all: $(JSON_PATH) variants png models

variants: $(VARIANTS_TARGETS)
png: $(PNG_TARGETS)
models: $(STL_TARGETS)

# Generate Variation
variants/%.json: $(JSON_PATH)
	-@ $(MKDIR) variants ||:
	$(PYTHON) $(VARGEN) --JsonPath $(JSON_PATH) --WriteSingle $(patsubst variants/%.json,%,$@) --ForceWrite

# Generate PNG
png/$(PROJNAME).%.png: variants/%.json $(SCAD_PATH)
	-@ $(MKDIR) png ||:
	-@ $(MKDIR) deps ||:
	$(SCADC) -o $@ -d $(patsubst variants/%.json,deps/%.deps,$<) -p $< -P $(patsubst variants/%.json,%,$<) $(SCAD_PATH)

# Generate STL
stl/$(PROJNAME).%.stl: variants/%.json $(SCAD_PATH)
	-@ $(MKDIR) stl ||:
	-@ $(MKDIR) deps ||:
	$(SCADC) -o $@ -d $(patsubst variants/%.json,deps/%.deps,$<) -p $< -P $(patsubst variants/%.json,%,$<) $(SCAD_PATH)

# Clean Up
clean:
	- $(RMDIR) variants
	- $(RMDIR) png
	- $(RMDIR) stl
	- $(RMDIR) deps

# Used during development of this makefile
dev:
	$(info SCAD_PATH : $(SCAD_PATH))
	$(info JSON_PATH : $(JSON_PATH))
	$(info VARIANTS : $(VARIANTS))
	$(info VARIANTS_TARGETS : $(VARIANTS_TARGETS))
	$(info PNG_TARGETS : $(PNG_TARGETS))
	$(info STL_TARGETS : $(STL_TARGETS))


