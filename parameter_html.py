import json
import sys
import argparse

VARIANTSDIR="variants"

################################################################################
## Parametric File Write

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

def write_parametric_html(parametricSettings:dict, project_name:str, filename:str):
    parameterSets = parametricSettings["parameterSets"]
    html_output = f"""
<!DOCTYPE html>
<html>
<head>
<title>{project_name}</title>
</head>
<body>
<h1>{project_name}</h1>
"""
    for parameterSetName in parameterSets:
        html_output += f"""
<h2>{parameterSetName}</h2>
<img src="png/{project_name}.{parameterSetName}.png" alt="OpenSCAD generated preview of {parameterSetName}" height="100">
<a href="stl/{project_name}.{parameterSetName}.stl">click to download</a>
"""
        for key, value in parameterSets[parameterSetName].items():
            html_output += f"""\
<p>{key}:{value}</p>
"""


    html_output += f"""
</body>
</html>
"""

    ## Write Parameter File
    with open(filename, "w") as f:
        f.write(html_output)


################################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program helps generate openscad compatible parametric variations')
    parser.add_argument('--ProjectName, -N', dest='project_name', help='name', default="test")
    parser.add_argument('--JsonPath, -J', dest='parameter_set_path', help='name of openscad parametric settings json file', default="main.json")
    parser.add_argument('--Output', '-O',  dest='output_path', help='output', default="index.html")
    parser.add_argument('--ForceWrite', '-F',  dest='force_write', action="store_true", help='force write')
    args = parser.parse_args()

    ############################################################################
    ## Generate HTML
    write_parametric_html(get_current_parametric_json(args.parameter_set_path), args.project_name, args.output_path)
else:
    print("Can Ony Be Run By Itself")
