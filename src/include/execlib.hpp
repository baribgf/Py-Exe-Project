/* 
 * Code execution lib for C++
 */

#ifndef string
    #include <iostream>
#endif
using namespace std;

string getCwd(string path);

// Replace all single quotes with double quotes
string parse_quotes(string str);

// Make sure to set base_command to python3
int execScript(string base_command, string script);

int execScriptFromPath(string base_command, string path);
