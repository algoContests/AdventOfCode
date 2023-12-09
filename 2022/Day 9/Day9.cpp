#include "Vec2.h"
#include <vector>
#include <iostream>

 
int main()
{
    cout << "Day 09\n";
    ifstream ifs("input.txt");

    sInfo info;
    vector<sInfo> data;
    while (!ifs.eof()) { ifs >> info.dir >> info.dist; data.push_back(info); /* cerr << info.dir << " " << info.dist << "\n";*/ }
    ifs.close();

    // Part 1
    Vec2<int> headPos, tailPos;
    set<Vec2<int>> tailMarks;
    tailMarks.insert(tailPos);
    for (const sInfo& info : data)
    {
        switch (info.dir)
        {
            case 'R': { for (int i = 0; i < info.dist; ++i) { ++headPos.x; tailPos += TRAILING_MOVE.at(headPos - tailPos); tailMarks.insert(tailPos); } break; }
            case 'L': { for (int i = 0; i < info.dist; ++i) { --headPos.x; tailPos += TRAILING_MOVE.at(headPos - tailPos); tailMarks.insert(tailPos); } break; }
            case 'D': { for (int i = 0; i < info.dist; ++i) { ++headPos.y; tailPos += TRAILING_MOVE.at(headPos - tailPos); tailMarks.insert(tailPos); } break; }
            case 'U': { for (int i = 0; i < info.dist; ++i) { --headPos.y; tailPos += TRAILING_MOVE.at(headPos - tailPos); tailMarks.insert(tailPos); } break; }
            default: { cerr << "WTF dir ?!? -> " << info.dir << "\n"; break; }
        }
    }
    cout << tailMarks.size() << "\n";
    // Draw(tailMarks, cerr);

    // Part 2
    vector<Vec2<int>> snake(10);
    tailMarks.clear();
    tailMarks.insert(snake[9]);
    for (const sInfo& info : data)
        {
        switch (info.dir)
        {
            case 'R': { for (int i = 0; i < info.dist; ++i) { ++snake[0].x; for (int j = 1; j < 10; ++j) snake[j] += TRAILING_MOVE.at(snake[j - 1] - snake[j]); tailMarks.insert(snake[9]); } break; }
            case 'L': { for (int i = 0; i < info.dist; ++i) { --snake[0].x; for (int j = 1; j < 10; ++j) snake[j] += TRAILING_MOVE.at(snake[j - 1] - snake[j]); tailMarks.insert(snake[9]); } break; }
            case 'D': { for (int i = 0; i < info.dist; ++i) { ++snake[0].y; for (int j = 1; j < 10; ++j) snake[j] += TRAILING_MOVE.at(snake[j - 1] - snake[j]); tailMarks.insert(snake[9]); } break; }
            case 'U': { for (int i = 0; i < info.dist; ++i) { --snake[0].y; for (int j = 1; j < 10; ++j) snake[j] += TRAILING_MOVE.at(snake[j - 1] - snake[j]); tailMarks.insert(snake[9]); } break; }
            default: { cerr << "WTF dir ?!? -> " << info.dir << "\n"; break; }
        }
    }
    cout << tailMarks.size() << "\n";
    // Draw(tailMarks, cerr);

    return 0;
}