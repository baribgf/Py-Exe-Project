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

string readFile(string path)
{
    ifstream f(path);
    string data;
    while (!f.eof())
    {
        string line;
        getline(f, line);
        data += line;
        if (!f.eof()) data += "\n";
    }
    f.close();
    return data;
}

string writeFile(string path, string data)
{
    ofstream f(path);
    f << data;
    f.close();
    return path;
}

string appendToFile(string path, string data)
{
    writeFile(path, readFile(path) + data);
    return path;
}

int getFileSize(string path)
{
    FILE* f = fopen(path.c_str(), "rb");
    fseek(f, 0, SEEK_END);
    int size = ftell(f);
    fclose(f);
    return size;
}

std::vector<unsigned char> readBin(string path)
{
    std::vector<unsigned char> data;
    ifstream bf(path, ifstream::binary);
    char c;
    while (!bf.eof())
    {
        bf.get(c);
        data.emplace_back(c);
    }

    bf.close();
    return data;
}

string writeBin(string path, std::vector<unsigned char> data)
{
    ofstream bf(path, ofstream::binary);

    for (auto &&c : data)
    {
        bf << c;
    }

    bf.close();
    return path;
}
