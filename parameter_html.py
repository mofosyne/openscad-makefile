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

    # Detect Parameter Constants
    firstSetValues = {}
    setValuesIsVariable = {}
    for parameterSetName in parameterSets:
        for key, value in parameterSets[parameterSetName].items():
            prevValue = firstSetValues.get(key, None)
            if prevValue == None:
                firstSetValues[key] = value
                continue
            if prevValue != value:
                setValuesIsVariable[key] = True

    # HTML Render
    html_output = f"""
<!doctype html>
<html lang="en">
<html>
<head>
    <meta charset="utf-8">
    <title>{variableNameToTitle(project_name)} OpenSCAD Models Download Page</title>
    <link rel="stylesheet" href="normalize.css">
    <link rel="stylesheet" href="style.css">
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
    html_output += f"""\
    <h2 id="constants">Common Parameters</h2>
    <p>These are common values that are same in all variants below and is placed here to reduce clutter in the download list:</p>
    <ul>
"""
    for key, value in firstSetValues.items():
        if setValuesIsVariable.get(key, None) != True:
            html_output += f"""\
        <li><b>{key}</b> : {value} </li>
"""
    html_output += f"""\
    </ul>
"""

    # Content
    html_output += f"""\
    <h2 id="download">Download</h2>
    <table>
        <tr>
            <th>Contact</th>
            <th>Name</th>
            <th>Parameters</th>
            <th>Download STL</th>
            <th>Table Of Content</th>
        </tr>
"""
    for parameterSetName in parameterSets:
        html_output += f"""
        <tr>
            <th><a href="png/{project_name}.{parameterSetName}.png"><img src="png/{project_name}.{parameterSetName}.png" alt="OpenSCAD generated preview of {parameterSetName}" height="100"></a></th>
            <th id="{parameterSetName}">{variableNameToTitle(parameterSetName)}</th>
"""
        html_output += f"""\
            <th>
                <ul class="parameters">
"""
        for key, value in parameterSets[parameterSetName].items():
            if setValuesIsVariable.get(key, None) == True:
                html_output += f"""\
                    <li><b>{key}</b> : {value} </li>
"""
        html_output += f"""\
                </ul>
            </th>
            <th><a href="stl/{project_name}.{parameterSetName}.stl" download>{project_name}.{parameterSetName}.stl</a></th>
            <th><a href="#toc">TOC</a></th>
        </tr>
"""
    html_output += f"""\
    </table>
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
