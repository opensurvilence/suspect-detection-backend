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

    if(n==1){
        cout<<1<<endl;
        return;
    }else if(n%2){
        cout<<-1<<endl;
    }else{
        vector<int>val(n);
        ll cnt=n-1;
        for(int i=1;i<n;i+=2){
            val[i]=cnt;
            cnt-=2;
        }
        int i=0,j=n-2;
        set<ll>st;
        for(int i=2;i<=n;i+=2)st.insert(i);
         cnt=0;
        while(i<=j){
            if(st.empty() or i>j)break;
            if(cnt%2==0){
                val[i]=*(--st.end());
                i+=2;
                st.erase(--st.end());

                   if(st.empty() or i>j)break;

                   val[j]=*(--st.end());
                   j-=2;
                   st.erase(--st.end());

            }else{
                  val[i]=*(st.begin());
                i+=2;
                st.erase(st.begin());

                   if(st.empty() or i>j)break;

                   val[j]=*(st.begin());
                   j-=2;
                   st.erase(st.begin());
            }
            cnt++;
        }
        ll sum=0;
        for(auto c:val){
            sum+=c;
            sum%=n;
            cout<<sum<<" ";
        }cout<<endl;
        for(auto c:val)cout<<c<<" ";cout<<endl;
    }
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