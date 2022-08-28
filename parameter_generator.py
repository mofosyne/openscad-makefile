import json
import sys
import argparse

VARIANTSDIR="variants"

################################################################################
## Parametric File Write

def openscad_parametric_json_change_check(parameterSetsNew:dict, parameterSetsOld:dict):
    # This checks if the new openscad parametric settings is different from the old
    # This does not check if parameters are missing in the new parameter list (e.g. custom parameter added)
    for key in parameterSetsNew:
        if key in parameterSetsOld:
            for entryKey in parameterSetsNew[key]:
                if entryKey in parameterSetsOld[key]:
                    if parameterSetsNew[key][entryKey] != parameterSetsOld[key][entryKey]:
                        return True # Mismatched Settings Value
                else:
                    return True # Mismatched Entry Name
        else:
            return True # Mismatched Set Name
    return False # All New Settings Matched

def get_current_parametric_json(filename:str):
    ## Write Parameter File
    try:
        with open(filename, "r") as f:
            json_object = json.load(f)
            return json_object
    except IOError:
        # Does not exist, create dummy framework
        json_object = {}
        json_object["fileFormatVersion"] = "1"
        json_object["parameterSets"] = {}
        return json_object

def write_parametric_json(parameterSets:dict, filename:str):
    json_object = {}
    json_object["fileFormatVersion"] = "1"
    json_object["parameterSets"] = parameterSets
    serializedOutput = json.dumps(json_object, sort_keys=True, indent=4)
    ## Write Parameter File
    with open(filename, "w") as f:
        f.write(serializedOutput)

def write_single_parametric_json(parameterSets:dict, parameterSetName:str):
    if parameterSetName in parameterSets:
        parametricSettingFilename = f"./{VARIANTSDIR}/{parameterSetName}.json"
        parameterSet = {parameterSetName: parameterSets[parameterSetName]}
        previousParametricSettings = get_current_parametric_json(parametricSettingFilename)
        if openscad_parametric_json_change_check(parameterSet, previousParametricSettings["parameterSets"]):
            # Change detected, write new settings
            write_parametric_json(parameterSet, parametricSettingFilename)
            print(f"{parameterSetName} updated")
        else:
            print(f"{parameterSetName} no change")
    else:
        print(f"{parameterSetName} does not exist")

def remove_scad_filename_extension(model_name:str):
    model_name_no_extension = model_name
    model_name_no_extension_splitted = model_name_no_extension.rsplit( ".", 1 ) # [<filename>,<fileext>]
    if model_name_no_extension_splitted[1] == "scad":
        model_name_no_extension = model_name_no_extension_splitted[0]
    return model_name_no_extension

################################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program helps generate openscad compatible parametric variations')
    parser.add_argument('--JsonPath, -J', dest='parameter_set_path', help='name of openscad parametric settings json file', default="main.json")
    parser.add_argument('--PrintTargets', '-T',  dest='print_targets', action="store_true", help='print targets')
    parser.add_argument('--WriteParameter', '-W',  dest='write_parameters', action="store_true", help='print targets')
    parser.add_argument('--ForceWrite', '-F',  dest='force_write', action="store_true", help='force write')
    args = parser.parse_args()

    ############################################################################
    ## Generate Parameters List

    ## Read Current Parametric Settings
    previousParametricSettings = get_current_parametric_json(args.parameter_set_path)
    parameterSets = {}

    if not args.force_write:
        parameterSets = previousParametricSettings["parameterSets"]

    if len(parameterSets) == 0 or args.force_write:
        ## Generate Parametric Settings
        for i in range(1,10,1):
            rowcount = i
            parameterSets[f"variation_{i}"] = {
                        "$fn": "40",
                        "RODCOUNT": f"{rowcount}"
                    }

    if args.force_write:
        # Always write
        write_parametric_json(parameterSets, args.parameter_set_path)
    elif args.write_parameters:
        # Write only if changed
        currParametricSettings = get_current_parametric_json(args.parameter_set_path)
        if openscad_parametric_json_change_check(parameterSets, currParametricSettings["parameterSets"]):
            write_parametric_json(parameterSets, args.parameter_set_path)

    if args.print_targets:
        parametricSetList = [key for key in parameterSets if key]
        targetsStr = " ".join(parametricSetList)
        print(targetsStr)

else:
    print("Can Ony Be Run By Itself")
