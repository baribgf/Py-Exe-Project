/* 
 * String handling lib for C++
 */

#ifndef string
    #include <iostream>
#endif
#ifndef vector
    #include <vector>
#endif

// Parse a string of hex items into a vector if integers
std::vector<int> parse_rep(std::string rep, char sep=',')
{
    std::vector<int> rep_arr;
    std::string item = "";
    for (int i = 0; i < rep.length(); i++)
    {
        if (rep[i] != sep) item += rep[i];
        else
        {
            rep_arr.emplace_back(stoi(item, 0, 16));
            item = "";
        }
    }
    
    return rep_arr;
}
