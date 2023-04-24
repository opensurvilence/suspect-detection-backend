#include<bits/stdc++.h>
using namespace std;

#define ll int64_t
#define endl "\n"
const ll mod=998244353;
const ll INF = 1e16;
#define all(x) x.begin(),x.end()


void solve()
{ 
    ll n,t;
    cin>>n>>t;

    vector<ll>a(n),b(n);
    for(int i=0;i<n;i++)cin>>a[i];
    
    for(int i=0;i<n;i++)cin>>b[i];

    ll ans=0,ind=-1;
    for(int i=0;i<n;i++){
        if(a[i]+i<=t){
            if(b[i]>ans){
                ans=b[i];
                ind=i+1;
            }
        }
    }
    cout<<ind<<endl;
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