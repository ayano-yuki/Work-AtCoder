#include <bits/stdc++.h>
using namespace std;

// --- Aho-Corasick class for multi-pattern matching ---
struct AC
{
    static constexpr int ALPHABET_SIZE = 6; // a-f
    static constexpr char FIRST_CHAR = 'a';

    struct Node
    {
        int next[ALPHABET_SIZE];
        int fail;
        vector<int> output; // pattern indices matched at this node
        Node() : fail(0)
        {
            fill(begin(next), end(next), -1);
        }
    };

    vector<Node> trie;
    AC() { trie.emplace_back(); }

    int char_to_index(char c) { return c - FIRST_CHAR; }

    void build(const vector<string> &patterns)
    {
        trie.clear();
        trie.emplace_back();

        // build trie
        for (int i = 0; i < (int)patterns.size(); i++)
        {
            const string &p = patterns[i];
            int cur = 0;
            for (char c : p)
            {
                int idx = char_to_index(c);
                if (trie[cur].next[idx] == -1)
                {
                    trie[cur].next[idx] = (int)trie.size();
                    trie.emplace_back();
                }
                cur = trie[cur].next[idx];
            }
            trie[cur].output.push_back(i);
        }

        // build fail links (BFS)
        queue<int> q;
        for (int c = 0; c < ALPHABET_SIZE; c++)
        {
            int nxt = trie[0].next[c];
            if (nxt != -1)
            {
                trie[nxt].fail = 0;
                q.push(nxt);
            }
            else
            {
                trie[0].next[c] = 0;
            }
        }
        while (!q.empty())
        {
            int r = q.front();
            q.pop();
            for (int c = 0; c < ALPHABET_SIZE; c++)
            {
                int nxt = trie[r].next[c];
                if (nxt != -1)
                {
                    trie[nxt].fail = trie[trie[r].fail].next[c];
                    // merge output links
                    for (int o : trie[trie[nxt].fail].output)
                    {
                        trie[nxt].output.push_back(o);
                    }
                    q.push(nxt);
                }
                else
                {
                    trie[r].next[c] = trie[trie[r].fail].next[c];
                }
            }
        }
    }

    // Search and return a vector<bool> of matched patterns (true=found)
    vector<bool> search(const string &text, int pattern_count)
    {
        vector<bool> matched(pattern_count, false);
        int cur = 0;
        for (char c : text)
        {
            int idx = char_to_index(c);
            cur = trie[cur].next[idx];
            for (int pidx : trie[cur].output)
            {
                matched[pidx] = true;
            }
        }
        return matched;
    }
};

// ------------------------

constexpr int TIME_LIMIT_MS = 1950;
constexpr int SAMPLE_LENGTH = 2000; // 基本同じ（長さ変え過ぎは時間に影響）
constexpr int SAMPLES = 10;         // 評価回数を少し増やす
constexpr int BEAM_WIDTH = 30;
constexpr int NEIGHBORS_PER_BEAM = 4; // 少し増やす
const vector<char> CHARS = {'a', 'b', 'c', 'd', 'e', 'f'};

int N, M, L;
vector<pair<string, int>> patterns;
AC ac; // AC automaton

random_device rd;
mt19937 rng(rd());
uniform_int_distribution<int> dist_char(0, (int)CHARS.size() - 1);
uniform_int_distribution<int> dist_prob(0, 99);
uniform_real_distribution<double> dist_real(0.0, 1.0);
uniform_int_distribution<int> dist_delta(-10, 10);
uniform_int_distribution<int> dist_pos(0, 0); // will update

// --- 初期C生成：パターンの文字を重視して出現頻度から生成 ---
vector<char> initial_C()
{
    vector<int> freq(M, 0);
    for (auto &[p, w] : patterns)
    {
        for (char c : p)
        {
            freq[c - 'a'] += w;
        }
    }
    // freq正規化（0割対策）
    int s = accumulate(freq.begin(), freq.end(), 0);
    if (s == 0)
    {
        // 全くなければランダム
        vector<char> C(M);
        for (int i = 0; i < M; i++)
            C[i] = CHARS[dist_char(rng)];
        return C;
    }
    vector<double> prob(M);
    for (int i = 0; i < M; i++)
        prob[i] = freq[i] / (double)s;

    vector<char> C(M);
    for (int i = 0; i < M; i++)
    {
        double r = dist_real(rng);
        double acc = 0;
        for (int j = 0; j < M; j++)
        {
            acc += prob[j];
            if (r < acc)
            {
                C[i] = CHARS[j];
                break;
            }
        }
    }
    return C;
}

// --- 初期A生成 ---
vector<vector<int>> initial_A()
{
    vector<vector<int>> A(M, vector<int>(M));
    for (int i = 0; i < M; i++)
    {
        vector<int> prob(M);
        int s = 0;
        for (int j = 0; j < M; j++)
        {
            prob[j] = uniform_int_distribution<int>(0, 100)(rng);
            s += prob[j];
        }
        for (int j = 0; j < M; j++)
        {
            A[i][j] = prob[j] * 100 / s;
        }
        int sum_row = accumulate(A[i].begin(), A[i].end(), 0);
        A[i][M - 1] += 100 - sum_row;
    }
    return A;
}

// --- 文字列生成 ---
string generate_string(const vector<char> &C, const vector<vector<int>> &A, int length)
{
    string s;
    s += C[0];
    int cur = 0;
    for (int i = 1; i < length; i++)
    {
        int r = dist_prob(rng);
        int acc = 0;
        for (int j = 0; j < M; j++)
        {
            acc += A[cur][j];
            if (r < acc)
            {
                cur = j;
                break;
            }
        }
        s += C[cur];
    }
    return s;
}

// --- 評価関数：Aho-Corasickで高速かつ正確に判定 ---
int evaluate(const vector<char> &C, const vector<vector<int>> &A)
{
    int score = 0;
    for (int sample = 0; sample < SAMPLES; sample++)
    {
        string s = generate_string(C, A, SAMPLE_LENGTH);
        auto matched = ac.search(s, N);
        for (int i = 0; i < N; i++)
        {
            if (matched[i])
                score += patterns[i].second;
        }
    }
    // 評価は平均的スコアを返す
    return (score + SAMPLES / 2) / SAMPLES; // 四捨五入風
}

// --- 近傍生成：多様化（複数箇所変化含む） ---
pair<vector<char>, vector<vector<int>>> neighbor(const vector<char> &C, const vector<vector<int>> &A)
{
    vector<char> newC = C;
    vector<vector<int>> newA = A;

    double choice = dist_real(rng);
    if (choice < 0.4)
    {
        // Cの1文字ランダム変更
        int i = uniform_int_distribution<int>(0, M - 1)(rng);
        newC[i] = CHARS[dist_char(rng)];
    }
    else if (choice < 0.7)
    {
        // Aの1要素を±delta変更
        int i = uniform_int_distribution<int>(0, M - 1)(rng);
        int j = uniform_int_distribution<int>(0, M - 1)(rng);
        int delta = dist_delta(rng);
        int val = newA[i][j] + delta;
        if (0 <= val && val <= 100)
        {
            newA[i][j] = val;
            // 再正規化
            int total = accumulate(newA[i].begin(), newA[i].end(), 0);
            for (int k = 0; k < M; k++)
            {
                newA[i][k] = newA[i][k] * 100 / total;
            }
            newA[i][M - 1] += 100 - accumulate(newA[i].begin(), newA[i].end(), 0);
        }
    }
    else
    {
        // 複数変更：Cを2箇所変える
        int cnt = 2;
        for (int _ = 0; _ < cnt; _++)
        {
            int i = uniform_int_distribution<int>(0, M - 1)(rng);
            newC[i] = CHARS[dist_char(rng)];
        }
    }
    return {newC, newA};
}

// --- 温度関数（焼きなまし風） ---
double temperature(int step, int max_steps)
{
    // 線形温度降下
    return max(0.01, 1.0 - (double)step / max_steps);
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> M >> L;
    patterns.resize(N);
    vector<string> pstrs(N);
    for (int i = 0; i < N; i++)
    {
        string s;
        int w;
        cin >> s >> w;
        patterns[i] = {s, w};
        pstrs[i] = s;
    }

    // ACビルド
    ac.build(pstrs);

    // 初期化
    auto bestC = initial_C();
    auto bestA = initial_A();
    int bestScore = evaluate(bestC, bestA);

    using State = tuple<int, vector<char>, vector<vector<int>>>;
    vector<State> beam;
    beam.emplace_back(bestScore, bestC, bestA);

    auto start = chrono::steady_clock::now();
    int step = 0;

    while (true)
    {
        auto now = chrono::steady_clock::now();
        int elapsed_ms = chrono::duration_cast<chrono::milliseconds>(now - start).count();
        if (elapsed_ms > TIME_LIMIT_MS)
            break;

        double temp = temperature(step, 5000); // 5000目安で温度下げる

        vector<State> new_beam;
        for (auto &[score, C, A] : beam)
        {
            for (int _ = 0; _ < NEIGHBORS_PER_BEAM; _++)
            {
                auto [C2, A2] = neighbor(C, A);
                int sc = evaluate(C2, A2);
                // 焼きなまし風確率
                if (sc >= score)
                {
                    new_beam.emplace_back(sc, C2, A2);
                }
                else
                {
                    double prob_accept = exp((sc - score) / (10.0 * temp)); // スコア差に依存
                    if (dist_real(rng) < prob_accept)
                    {
                        new_beam.emplace_back(sc, C2, A2);
                    }
                }
            }
        }

        if (new_beam.empty())
            break;

        sort(new_beam.rbegin(), new_beam.rend());
        if ((int)new_beam.size() > BEAM_WIDTH)
            new_beam.resize(BEAM_WIDTH);
        beam = move(new_beam);

        if (get<0>(beam[0]) > bestScore)
        {
            bestScore = get<0>(beam[0]);
            bestC = get<1>(beam[0]);
            bestA = get<2>(beam[0]);
        }
        step++;
    }

    // 出力
    for (int i = 0; i < M; i++)
    {
        cout << bestC[i];
        for (int j = 0; j < M; j++)
        {
            cout << " " << bestA[i][j];
        }
        cout << "\n";
    }

    return 0;
}
