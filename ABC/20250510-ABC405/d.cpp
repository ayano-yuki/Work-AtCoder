#include <iostream>
#include <vector>
#include <deque>
#include <tuple>
#include <string>

using namespace std;

int main() {
    int H, W;
    cin >> H >> W;

    vector<string> grid(H);
    for (int i = 0; i < H; ++i) {
        cin >> grid[i];
    }

    vector<pair<int, int>> dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    vector<vector<int>> dist(H, vector<int>(W, -1));
    vector<vector<pair<int, int>>> prev(H, vector<pair<int, int>>(W, {-1, -1}));

    deque<pair<int, int>> q;
    for (int i = 0; i < H; ++i) {
        for (int j = 0; j < W; ++j) {
            if (grid[i][j] == 'E') {
                dist[i][j] = 0;
                q.push_back({i, j});
            }
        }
    }

    while (!q.empty()) {
        int y, x;
        tie(y, x) = q.front();
        q.pop_front();
        for (const auto& dir : dirs) {
            int dy = dir.first, dx = dir.second;
            int ny = y + dy, nx = x + dx;
            if (ny >= 0 && ny < H && nx >= 0 && nx < W) {
                if (grid[ny][nx] == '.' && dist[ny][nx] == -1) {
                    dist[ny][nx] = dist[y][x] + 1;
                    prev[ny][nx] = {-dy, -dx};
                    q.push_back({ny, nx});
                }
            }
        }
    }

    vector<string> res(H, string(W, ' '));
    for (int i = 0; i < H; ++i) {
        for (int j = 0; j < W; ++j) {
            if (grid[i][j] == '#') {
                res[i][j] = '#';
            } else if (grid[i][j] == 'E') {
                res[i][j] = 'E';
            } else {
                int dy = prev[i][j].first, dx = prev[i][j].second;
                for (const auto& dir : dirs) {
                    int ddy = dir.first, ddx = dir.second;
                    if (dy == ddy && dx == ddx) {
                        if (ddy == -1 && ddx == 0) res[i][j] = '^';
                        else if (ddy == 1 && ddx == 0) res[i][j] = 'v';
                        else if (ddy == 0 && ddx == -1) res[i][j] = '<';
                        else if (ddy == 0 && ddx == 1) res[i][j] = '>';
                        break;
                    }
                }
            }
        }
    }

    for (const auto& row : res) {
        cout << row << endl;
    }

    return 0;
}
