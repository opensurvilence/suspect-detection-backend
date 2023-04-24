#include<bits/stdc++.h>
using namespace std;

#define ll int64_t
#define endl "\n"
const ll mod=998244353;
const ll INF = 1e16;
#define all(x) x.begin(),x.end()

vector<ll>mp(1e6+10);
void solve()
{ 
    ll n;
    cin>>n;

   
    vector<ll>val(n);
    for(int i=0;i<n;i++)cin>>val[i];
    set<ll>temp;
    for(auto c:val)mp[c]++,temp.insert(c);
    ll ans=0;
    for(auto c:temp){
        ll f=mp[c];
        ll temp=(f)*(f-1)*(f-2);
        ans+=temp;
        for(ll i=2;i*i*c<=ll(1000000);i++){
            ll f1=mp[c],f2=mp[i*c],f3=mp[i*i*c];
            ans+=f1*f2*f3;
        }
    }
    for(auto c:temp)mp[c]=0;
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