# openscad-multivariants-python-makefile

This is a build system that uses python to automatically generates a list of
different variations. In addition it will autogenerate a html download page of
all your model variations for easy web sharing.

[Click here for a live example of an autogenerated html download page](https://mofosyne.github.io/openscad-makefile/)

This is suitable for openscad users who is creating a
singular scad projects with lots of variations or parts.

* `make all` - Make all png previews and stl files
* `make clear` - Clear all build files

Tip:
* `make -j8 all` - Same as `make all` but runs up to 8 jobs at the same time, leading to faster compilation. This is called Parallel Execution as explained in [gnu make manual](https://www.gnu.org/software/make/manual/make.html#Parallel).

This is a community supported build system so feel free to suggest change or
put in a pull request for consideration.

## Minimum support

This is intented to be used by windows users and linux users.

You need at least minimum:
* OpenSCAD installed
* makefile support
* Python 3.6 or higher

## Features

* changes to `models/*.json` does not always kick off all the stl builds if there is no changes to source code or the variation in file.

## How does this build system works

```mermaid
graph TD
    paramGen(["parameter_generator.py"])     -- generates if missing  --> paramSettings
    paramSettings["models/*.json"]           -- used by    --> paramVariants
    paramVariants(["parameter_variants.py"]) -- updates on change  --> variants
    variants["variants/*.json"]              -- settings   --> scadGen
    sourcecode["models/*.scad"]              -- sourcecode --> scadGen
    scadGen(["openScad"])
    scadGen                                  --> png
    scadGen                                  --> stl
    png["png/*.png"]                         -- used for image preview --> paramHTML
    stl["stl/*.stl"]                         -- used for download link --> paramHTML
    paramSettings                            -- used for documentation --> paramHTML
    paramHTML(["parameter_html.py"])         -- generates  --> html
    html["index.html"]
```

## Adapting to your project
* Run `make clean` to clean out any existing generated stls
* Change `parameter_generator.py` to match your needs then delete `models/*.json` file
* Adapt `models/*.scad` to include your code
* Update `makefile` changing these below settings to match your source name

```makefile
# Model Details
PROJNAME = test
SCAD_PATH = models/$(PROJNAME).scad
JSON_PATH = models/$(PROJNAME).json
```

* Run `make all` to autogenerate the missing parameter setting list `models/*.json` and kick off the variations

Let me know if instructions does not make sense and we can update it to make it clearer

## Tips

### Compiling multiple makefile folders

```makefile
SUBDIRS = $(sort $(dir $(wildcard ./*/))) #folders to look for

# OS DETECT https://stackoverflow.com/questions/714100/os-detecting-makefile
isWindows=
ifeq ($(OS),Windows_NT)
ifeq (, $(shell uname))
	isWindows=Yes
endif
endif
ifeq ($(isWindows),Yes)
    SPLITCOMMAND = &
else
    SPLITCOMMAND = ;
endif

# Stackoverflow: How to write a loop in a makefile https://stackoverflow.com/a/1491012/2850957
.PHONY: all clean $(SUBDIRS)
all:
	$(foreach var,$(SUBDIRS),$(MAKE) --directory=$(var) all $(SPLITCOMMAND))
clean:
	$(foreach var,$(SUBDIRS),$(MAKE) --directory=$(var) clean $(SPLITCOMMAND))
```
