/* 
 * Code execution lib for C++
 */

#ifndef string
    #include <iostream>
#endif
using namespace std;

string getCwd(string path)
{
    int i;
    for (i = path.length(); i > 0; i--) if (path[i] == '/') break;
    return path.substr(0, i);
}

// Replace all single quotes with double quotes
string parse_quotes(string str)
{
    while (str.find('\'') != -1)
    {
        str.replace(str.find('\''), 1, "\"");
    }
    return str;
}

// Make sure to set base_command to python3
int execScript(string base_command, string script)
{
    string command = (string) base_command + " " + "\'" + parse_quotes(script) + "\'";
    return system(command.c_str());
}

int execScriptFromPath(string base_command, string path)
{
    string command = (string) "cd " + getCwd(path) + " && " + base_command + " " + "\"" + path + "\"";
    return system(command.c_str());
}
