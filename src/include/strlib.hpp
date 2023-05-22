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
std::vector<int> parse_rep(std::string rep, char sep=',');
