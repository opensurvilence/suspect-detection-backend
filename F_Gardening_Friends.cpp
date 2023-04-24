#include<bits/stdc++.h>
using namespace std;

#define ll int64_t
#define endl "\n"
const ll mod=998244353;
const ll INF = 1e16;
#define all(x) x.begin(),x.end()

vector<vector<ll>>adj;
vector<bool>vis;
vector<ll>dis,max_dis,ans;

void dfs(ll v){
    vis[v]=1;
    for(auto u:adj[v]){
        if(!vis[u]){
            dis[u]=dis[v]+1;
            dfs(u);
        }
    }
    for(auto u:adj[v]){
        max_dis[v]=max(max_dis[v],max_dis[u]+1);
    }
}

void dfs1(ll v,ll k,ll c){
    vis[v]=1;
    vector<ll>pf,sf;
    for(auto u:adj[v]){
       ans[v]=max(ans[v], (max_dis[u]+1)*k - dis[v]*c);
       pf.push_back(max_dis[u]);
    }
    sf=pf;
    int n=pf.size();
    for(int i=1;i<n;i++){
        pf[i]=max(pf[i-1],pf[i]);
    }
     for(int i=n-2;i>=0;i--){
        sf[i]=max(sf[i+1],sf[i]);
    }
    ll cnt=0;
    for(auto u:adj[v]){
       if(!vis[u]){
          ll temp=-1;
          if(cnt-1>=0)temp=max(temp,pf[cnt-1]);
          if(cnt+1<n)temp=max(temp,sf[cnt+1]);
          max_dis[v]=temp+1;
          dfs1(u,k,c);
       }
       cnt++;
    }
}
void solve()
{ 
    ll n,k,c;
    cin>>n>>k>>c;

    adj=vector<vector<ll>>(n+1);
    vis=vector<bool>(n+1);
    dis=vector<ll>(n+1);
    max_dis=vector<ll>(n+1);
    ans=vector<ll>(n+1);


    for(int i=0;i<n-1;i++){
        ll u,v;
        cin>>u>>v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    dfs(1);

    for(int i=1;i<=n;i++)vis[i]=0,max_dis[i]--;
    
//  for(auto c:max_dis)cout<<c<<" ";cout<<endl;
    dfs1(1,k,c);
    //  for(auto c:max_dis)cout<<c<<" ";cout<<endl;
    // for(auto c:ans)cout<<c<<" ";cout<<endl;
    cout<<*max_element(all(ans))<<endl;


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