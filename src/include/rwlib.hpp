/* 
 * Read and write lib for C++
 */

#ifndef string
    #include <iostream>
    using namespace std;
#endif
#ifndef fstream
    #include <fstream>
#endif
#ifndef vector
    #include <vector>
#endif

typedef string string;

string readFile(string path);

string writeFile(string path, string data);

string appendToFile(string path, string data);

int getFileSize(string path);

std::vector<unsigned char> readBin(string path);

string writeBin(string path, std::vector<unsigned char> data);
