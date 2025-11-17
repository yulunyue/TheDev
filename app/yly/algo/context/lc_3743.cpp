#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    typedef long long ll;
    const ll I = 1e15;
    vector<ll> max_plus_convolution(vector<ll> a, vector<ll> b)
    {
        vector<ll> c(a.size() + b.size() - 1);
        c[0] = a[0] + b[0];
        adjacent_difference(a.begin(), a.end(), a.begin());
        adjacent_difference(b.begin(), b.end(), b.begin());
        merge(a.begin() + 1, a.end(), b.begin() + 1, b.end(), c.begin() + 1, greater<>());
        partial_sum(c.begin(), c.end(), c.begin());
        return c;
    }
    vector<ll> right_shift(vector<ll> a)
    {
        return a.insert(a.begin(), -I), a;
    }
    void dot_chmax(vector<ll> &a, vector<ll> b)
    {
        for (int i = 0; i < min(a.size(), b.size()); i++)
            a[i] = max(a[i], b[i]);
    }
    ll maximumScore(vector<int> &a, int k)
    {
        int n = a.size(), c = 0;
        vector f(n << 1, vector(3, vector(3, vector<ll>())));
        auto dc = [&](auto &&self, int l, int r) -> int
        {
            int w = c++, m = l + r >> 1;
            for (int i = 0; i < 3; i++)
                for (int j = 0; j < 3; j++)
                    f[w][i][j].resize(r - l + 2, -I);
            if (l == r)
            {
                f[w][0][0][0] = f[w][0][0][1] = 0;
                f[w][0][1][0] = f[w][1][0][0] = a[l];
                f[w][0][2][0] = f[w][2][0][0] = -a[l];
                return w;
            }
            int lw = self(self, l, m), rw = self(self, m + 1, r);
            for (int i = 0; i < 3; i++)
                for (int j = 0; j < 3; j++)
                {
                    dot_chmax(f[w][i][j], f[lw][i][j]), dot_chmax(f[w][i][j], f[rw][i][j]);
                    dot_chmax(f[w][i][j], max_plus_convolution(f[lw][i][0], f[rw][0][j]));
                    dot_chmax(f[w][i][j], right_shift(max_plus_convolution(f[lw][i][1], f[rw][2][j])));
                    dot_chmax(f[w][i][j], right_shift(max_plus_convolution(f[lw][i][2], f[rw][1][j])));
                }
            return w;
        };
        dc(dc, 0, n - 1);
        ll w = 0;
        for (int i = 1; i <= k; i++)
            w = max({w, f[0][0][0][i], i < k ? f[0][1][2][i] : 0, i < k ? f[0][2][1][i] : 0});
        return w;
    }
};
