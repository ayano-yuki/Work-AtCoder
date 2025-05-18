#include <bits/stdc++.h>
using namespace std;

struct AC {
    static constexpr int ALPHABET_SIZE = 6; // a-f
    static constexpr char FIRST_CHAR = 'a';

    struct Node {
        int next[ALPHABET_SIZE];
        int fail;
        vector<int> output; // matched pattern indices
        Node() : fail(0) {
            fill(begin(next), end(next), -1);
        }
    };

    vector<Node> trie;
    AC() { trie.emplace_back(); }

    int char_to_index(char c) const { return c - FIRST_CHAR; }

    void build(const vector<string> &patterns) {
        trie.clear();
        trie.emplace_back();

        for (int i = 0; i < (int)patterns.size(); i++) {
            const string &p = patterns[i];
            int cur = 0;
            for (char c : p) {
                int idx = char_to_index(c);
                if (trie[cur].next[idx] == -1) {
                    trie[cur].next[idx] = (int)trie.size();
                    trie.emplace_back();
                }
                cur = trie[cur].next[idx];
            }
            trie[cur].output.push_back(i);
        }

        queue<int> q;
        for (int c = 0; c < ALPHABET_SIZE; c++) {
            int nxt = trie[0].next[c];
            if (nxt != -1) {
                trie[nxt].fail = 0;
                q.push(nxt);
            } else {
                trie[0].next[c] = 0;
            }
        }

        while (!q.empty()) {
            int r = q.front(); q.pop();
            for (int c = 0; c < ALPHABET_SIZE; c++) {
                int nxt = trie[r].next[c];
                if (nxt != -1) {
                    trie[nxt].fail = trie[trie[r].fail].next[c];
                    for (int o : trie[trie[nxt].fail].output) {
                        trie[nxt].output.push_back(o);
                    }
                    q.push(nxt);
                } else {
                    trie[r].next[c] = trie[trie[r].fail].next[c];
                }
            }
        }
    }

    vector<bool> search(const string &text, int pattern_count) const {
        vector<bool> matched(pattern_count, false);
        int cur = 0;
        for (char c : text) {
            int idx = char_to_index(c);
            cur = trie[cur].next[idx];
            for (int pidx : trie[cur].output) matched[pidx] = true;
        }
        return matched;
    }
};

constexpr int TIME_LIMIT_MS = 1700;
constexpr int SAMPLE_LENGTH = 2000;
constexpr int SAMPLES = 10;
constexpr int BEAM_WIDTH = 100;
constexpr int NEIGHBORS_PER_BEAM = 8;

const vector<char> CHARS = {'a','b','c','d','e','f'};

int N, M, L;
vector<pair<string,int>> patterns;
AC ac;

random_device rd;
mt19937 rng(rd());
uniform_int_distribution<int> dist_char(0, (int)CHARS.size() - 1);
uniform_int_distribution<int> dist_prob(0, 99);
uniform_real_distribution<double> dist_real(0.0, 1.0);
uniform_int_distribution<int> dist_delta(-10, 10);

using Aflat = vector<int>;

string initial_C() {
    vector<int> freq(6,0);
    for (auto &[p, w] : patterns) {
        for (char c : p) freq[c - 'a'] += w;
    }
    int s = accumulate(freq.begin(), freq.end(), 0);
    string C(M, 'a');
    if (s == 0) {
        for (int i = 0; i < M; i++) C[i] = CHARS[dist_char(rng)];
        return C;
    }
    vector<double> prob(6);
    for (int i = 0; i < 6; i++) prob[i] = freq[i] / (double)s;
    for (int i = 0; i < M; i++) {
        double r = dist_real(rng);
        double acc = 0;
        for (int j = 0; j < 6; j++) {
            acc += prob[j];
            if (r < acc) {
                C[i] = CHARS[j];
                break;
            }
        }
    }
    return C;
}

Aflat initial_A() {
    Aflat A(M * M);
    for (int i = 0; i < M; i++) {
        vector<int> prob(M);
        int s = 0;
        for (int j = 0; j < M; j++) {
            prob[j] = uniform_int_distribution<int>(0, 100)(rng);
            s += prob[j];
        }
        for (int j = 0; j < M; j++) {
            A[i*M + j] = prob[j] * 100 / s;
        }
        int sum_row = 0;
        for (int j = 0; j < M; j++) sum_row += A[i*M + j];
        A[i*M + M-1] += 100 - sum_row;
    }
    return A;
}

vector<int> build_cumulative_row(const Aflat &A, int row) {
    vector<int> cum(M);
    cum[0] = A[row*M + 0];
    for (int i = 1; i < M; i++) cum[i] = cum[i-1] + A[row*M + i];
    return cum;
}

string generate_string(const string &C, const Aflat &A, const vector<vector<int>> &A_cum, int length) {
    string s;
    s += C[0];
    int cur = 0;
    for (int i = 1; i < length; i++) {
        int r = dist_prob(rng);
        auto &cum = A_cum[cur];
        int nxt = (int)(std::lower_bound(cum.begin(), cum.end(), r+1) - cum.begin());
        cur = nxt;
        s += C[cur];
    }
    return s;
}

int evaluate(const string &C, const Aflat &A) {
    vector<vector<int>> A_cum(M);
    for (int i = 0; i < M; i++) {
        A_cum[i] = build_cumulative_row(A, i);
    }

    int score = 0;
    mt19937 local_rng(rd());
    uniform_int_distribution<int> local_dist_prob(0, 99);

    for (int sample = 0; sample < SAMPLES; sample++) {
        string s;
        s += C[0];
        int cur = 0;
        for (int i = 1; i < SAMPLE_LENGTH; i++) {
            int r = local_dist_prob(local_rng);
            auto &cum = A_cum[cur];
            int nxt = (int)(std::lower_bound(cum.begin(), cum.end(), r+1) - cum.begin());
            cur = nxt;
            s += C[cur];
        }
        auto matched = ac.search(s, N);
        for (int i = 0; i < N; i++) {
            if (matched[i]) score += patterns[i].second;
        }
    }
    return (score + SAMPLES/2) / SAMPLES;
}

pair<string, Aflat> neighbor(const string &C, const Aflat &A) {
    string newC = C;
    Aflat newA = A;

    double choice = dist_real(rng);
    if (choice < 0.4) {
        int i = uniform_int_distribution<int>(0, M-1)(rng);
        newC[i] = CHARS[dist_char(rng)];
    } else if (choice < 0.7) {
        int i = uniform_int_distribution<int>(0, M-1)(rng);
        int j = uniform_int_distribution<int>(0, M-1)(rng);
        int delta = dist_delta(rng);
        int idx = i*M + j;
        int val = newA[idx] + delta;
        if (0 <= val && val <= 100) {
            newA[idx] = val;
            int total = 0;
            for (int k = 0; k < M; k++) total += newA[i*M + k];
            for (int k = 0; k < M; k++) newA[i*M + k] = newA[i*M + k] * 100 / total;
            int sum_row = 0;
            for (int k = 0; k < M; k++) sum_row += newA[i*M + k];
            newA[i*M + M-1] += 100 - sum_row;
        }
    } else {
        for (int cnt = 0; cnt < 2; cnt++) {
            int i = uniform_int_distribution<int>(0, M-1)(rng);
            newC[i] = CHARS[dist_char(rng)];
        }
    }
    return {newC, newA};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> M >> L;
    patterns.resize(N);
    for (int i = 0; i < N; i++) cin >> patterns[i].first >> patterns[i].second;

    vector<string> ps(N);
    for (int i = 0; i < N; i++) ps[i] = patterns[i].first;
    ac.build(ps);

    string bestC = initial_C();
    Aflat bestA = initial_A();
    int best_score = evaluate(bestC, bestA);

    auto start = chrono::steady_clock::now();

    using State = tuple<int, string, Aflat>;
    vector<State> beam;
    beam.emplace_back(best_score, bestC, bestA);

    while (true) {
        auto now = chrono::steady_clock::now();
        int elapsed = (int)chrono::duration_cast<chrono::milliseconds>(now - start).count();
        if (elapsed > TIME_LIMIT_MS) break;

        vector<State> candidates;

        for (int i = 0; i < (int)beam.size(); i++) {
            auto [score, C, A] = beam[i];
            for (int _ = 0; _ < NEIGHBORS_PER_BEAM; _++) {
                auto [nC, nA] = neighbor(C, A);
                int nscore = evaluate(nC, nA);
                candidates.emplace_back(nscore, nC, nA);
            }
        }

        sort(candidates.begin(), candidates.end(), [](const State &a, const State &b) {
            return get<0>(a) > get<0>(b);
        });
        if (!candidates.empty() && get<0>(candidates[0]) > best_score) {
          best_score = get<0>(candidates[0]);
          bestC = get<1>(candidates[0]);
          bestA = get<2>(candidates[0]);
        }
            beam.clear();
    for (int i = 0; i < min(BEAM_WIDTH, (int)candidates.size()); i++) {
        beam.push_back(candidates[i]);
    }
}

for (int i = 0; i < M; i++) {
    cout << bestC[i];
    for (int j = 0; j < M; j++) {
        cout << " " << bestA[i*M + j];
    }
    cout << '\n';
}

return 0;
}
