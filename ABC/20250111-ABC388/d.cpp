#include <iostream>
#include <vector>
using namespace std;

int main() {
    int N;
    cin >> N;
    vector<int> A(N);

    for (int i = 0; i < N; ++i) {
        cin >> A[i];
    }

    // Aを事前に累積減算するために、最初の要素から減算数を一度に計算
    for (int n = 1; n < N; ++n) {
        // A[0:n] の値が正の数である部分をカウント
        int count = 0;
        for (int i = 0; i < n; ++i) {
            if (A[i] > 0) {
                ++count;
            }
        }

        // A[n] に count を加える
        A[n] += count;

        // A[0:n] の値を一気に減らす
        for (int i = 0; i < n; ++i) {
            if (A[i] > 0) {
                --A[i];
            }
        }
    }

    for (int i = 0; i < N; ++i) {
        cout << A[i] << " ";
    }
    cout << endl;

    return 0;
}
