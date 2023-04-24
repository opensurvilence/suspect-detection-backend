#include<bits/stdc++.h>
using namespace std;

#define ll int64_t
#define endl "\n"
const ll mod=998244353;
const ll INF = 1e16;
#define all(x) x.begin(),x.end()


void solve()
{ 
    ll n;
    cin>>n;

    vector<ll>val(n);
    for(int i=0;i<n;i++)cin>>val[i];

    ll ans=-1e18;
    ans-=1e6;
    sort(all(val));
    for(int i=1;i<n;i++)ans=max(ans, val[i]*val[i-1]);

    cout<<ans<<endl;

}

int main(){
    ios_base::sync_with_stdio(false); cin.tie(NULL);cout.tie(NULL);
    int t=1;
    cin>>t;
    while(t--) {
         solve();
    }
    return 0; 
}