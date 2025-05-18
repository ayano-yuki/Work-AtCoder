#include <bits/stdc++.h>
using namespace std;

constexpr int TIME_LIMIT_MS = 1950;  // 1.9秒
constexpr int SAMPLE_LENGTH = 900;
constexpr int SAMPLES = 10;
constexpr int BEAM_WIDTH = 30;
constexpr int NEIGHBORS_PER_BEAM = 3;
const vector<char> CHARS = {'a','b','c','d','e','f'};

int N, M, L;
vector<pair<string,int>> patterns;

random_device rd;
mt19937 rng(rd());
uniform_int_distribution<int> dist_char(0, (int)CHARS.size() - 1);
uniform_int_distribution<int> dist_prob(0, 99);
uniform_real_distribution<double> dist_real(0.0, 1.0);
uniform_int_distribution<int> dist_delta(-10, 10);

// Cをランダム生成
vector<char> random_C() {
    vector<char> C(M);
    for (int i = 0; i < M; i++) {
        C[i] = CHARS[dist_char(rng)];
    }
    return C;
}

// Aをランダム生成（各行100点満点に正規化）
vector<vector<int>> random_A() {
    vector<vector<int>> A(M, vector<int>(M));
    for (int i = 0; i < M; i++) {
        vector<int> prob(M);
        int s = 0;
        for (int j = 0; j < M; j++) {
            prob[j] = uniform_int_distribution<int>(0, 100)(rng);
            s += prob[j];
        }
        for (int j = 0; j < M; j++) {
            A[i][j] = prob[j] * 100 / s;
        }
        // 調整
        int sum_row = accumulate(A[i].begin(), A[i].end(), 0);
        A[i][M-1] += 100 - sum_row;
    }
    return A;
}

// C,Aから長さlengthの文字列を生成
string generate_string(const vector<char> &C, const vector<vector<int>> &A, int length) {
    string s;
    s += C[0];
    int cur = 0;
    for (int i = 1; i < length; i++) {
        int r = dist_prob(rng);
        int acc = 0;
        for (int j = 0; j < M; j++) {
            acc += A[cur][j];
            if (r < acc) {
                cur = j;
                break;
            }
        }
        s += C[cur];
    }
    return s;
}

// 生成文字列中にパターンがあるかチェック
bool contains(const string &s, const string &pat) {
    return s.find(pat) != string::npos;
}

// C,Aの評価：SAMPLES回生成してパターン検出率でスコア計算
int evaluate(const vector<char> &C, const vector<vector<int>> &A) {
    vector<int> found(N, 0);
    for (int i = 0; i < SAMPLES; i++) {
        string s = generate_string(C, A, SAMPLE_LENGTH);
        for (int j = 0; j < N; j++) {
            if (contains(s, patterns[j].first)) found[j]++;
        }
    }
    double score = 0;
    for (int i = 0; i < N; i++) {
        score += (double)found[i] / SAMPLES * patterns[i].second;
    }
    return (int)(score + 0.5);
}

// 近傍生成
pair<vector<char>, vector<vector<int>>> neighbor(const vector<char> &C, const vector<vector<int>> &A) {
    vector<char> newC = C;
    vector<vector<int>> newA = A;

    if (dist_real(rng) < 0.5) {
        // Cを1文字ランダムに変更
        int i = uniform_int_distribution<int>(0, M-1)(rng);
        newC[i] = CHARS[dist_char(rng)];
    } else {
        // Aの1要素を±delta変更
        int i = uniform_int_distribution<int>(0, M-1)(rng);
        int j = uniform_int_distribution<int>(0, M-1)(rng);
        int delta = dist_delta(rng);
        int val = newA[i][j] + delta;
        if (0 <= val && val <= 100) {
            newA[i][j] = val;
            // 再正規化
            int total = accumulate(newA[i].begin(), newA[i].end(), 0);
            for (int k = 0; k < M; k++) {
                newA[i][k] = newA[i][k] * 100 / total;
            }
            newA[i][M-1] += 100 - accumulate(newA[i].begin(), newA[i].end(), 0);
        }
    }
    return {newC, newA};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> M >> L;
    patterns.resize(N);
    for (int i = 0; i < N; i++) {
        string s; int p;
        cin >> s >> p;
        patterns[i] = {s, p};
    }

    // 初期化
    auto bestC = random_C();
    auto bestA = random_A();
    int bestScore = evaluate(bestC, bestA);

    using State = tuple<int, vector<char>, vector<vector<int>>>; // score, C, A
    vector<State> beam;
    beam.emplace_back(bestScore, bestC, bestA);

    auto start = chrono::steady_clock::now();

    while (true) {
        auto now = chrono::steady_clock::now();
        auto elapsed_ms = chrono::duration_cast<chrono::milliseconds>(now - start).count();
        if (elapsed_ms > TIME_LIMIT_MS) break;

        vector<State> new_beam;
        for (auto &[score, C, A] : beam) {
            for (int _ = 0; _ < NEIGHBORS_PER_BEAM; _++) {
                auto [C2, A2] = neighbor(C, A);
                int sc = evaluate(C2, A2);
                new_beam.emplace_back(sc, C2, A2);
            }
        }
        sort(new_beam.rbegin(), new_beam.rend());
        if (new_beam.size() > BEAM_WIDTH) new_beam.resize(BEAM_WIDTH);

        beam = move(new_beam);
        if (get<0>(beam[0]) > bestScore) {
            bestScore = get<0>(beam[0]);
            bestC = get<1>(beam[0]);
            bestA = get<2>(beam[0]);
        }
    }

    // 出力
    for (int i = 0; i < M; i++) {
        cout << bestC[i];
        for (int j = 0; j < M; j++) {
            cout << " " << bestA[i][j];
        }
        cout << "\n";
    }

    return 0;
}
