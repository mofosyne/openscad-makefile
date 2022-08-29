import json
import argparse

################################################################################
## Parametric File Write
def variableNameToTitle(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return ' '.join(i.capitalize() for i in s[0:])

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
<!doctype html>
<html lang="en">
<html>
<head>
    <meta charset="utf-8">
    <title>{variableNameToTitle(project_name)} OpenSCAD Models Download Page</title>
</head>
<body>
    <h1>{variableNameToTitle(project_name)} OpenSCAD Models Download Page</h1>

    <h2 id="toc">Table Of Content</h2>
    <ul class="toc_list">
"""
    for parameterSetName in parameterSets:
        html_output += f"""\
        <li><a href="#{parameterSetName}">{variableNameToTitle(parameterSetName)}</a></li>
"""
    html_output += f"""\
    </ul>
"""

    # Content
    for parameterSetName in parameterSets:
        html_output += f"""
    <h2 id="{parameterSetName}">{variableNameToTitle(parameterSetName)}</h2>
    <img src="png/{project_name}.{parameterSetName}.png" alt="OpenSCAD generated preview of {parameterSetName}" height="100">
    <p><a href="stl/{project_name}.{parameterSetName}.stl" download>click to download</a></p>
    <p><a href="#toc">click to jump back to TOC</a></p>
"""
        html_output += f"""\
    <details>
        <summary>Click To Show Parameter Settings Used In This Variation</summary>
        <ul class="parameters">
"""
        for key, value in parameterSets[parameterSetName].items():
            html_output += f"""\
            <li><p>{key} : {value}</p></li>
"""
        html_output += f"""\
        </ul>
    </details>
"""

    html_output += f"""
</body>
</html>
"""

    ## Write HTML File
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
