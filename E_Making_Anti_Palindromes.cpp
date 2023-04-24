#include <bits/stdc++.h>
using namespace std;

#define ll int64_t
#define endl "\n"
const ll mod = 998244353;
const ll INF = 1e16;
#define all(x) x.begin(), x.end()

void solve()
{
    ll n;
    cin >> n;

    string s;
    cin >> s;

    if (n % 2)
    {
        cout << -1 << endl;
        return;
    }
    map<char, ll> m1, m2;
    for (auto c : s)
    {
        m2[c]++;
    }
    for (int i = 0; i < n / 2; i++)
    {

        if (s[i] == s[n - 1 - i])
        {
            m1[s[i]]++;
        }
    }

    ll sum = 0;
    ll max_m1 = 0;
    ll max_m2 = 0;
    for (auto c : m1)
    {
        sum += c.second;
        max_m1 = max(max_m1, c.second);
    }
    for (auto c : m2)
    {
        max_m2 = max(max_m2, c.second);
    }

    if (max_m2 > n / 2)
    {
        cout << -1 << endl;
    }
    else
    {
        if (sum < 2 * max_m1)
        {
            cout << max_m1 << endl;
        }
        else
        {

            cout << (sum + 1) / 2 << endl;
        }
    }
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
    int t = 1;
    cin >> t;
    while (t--)
    {
        solve();
    }
    return 0;
}