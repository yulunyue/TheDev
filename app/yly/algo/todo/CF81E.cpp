#include<bits/stdc++.h>
using namespace std;
#define fo(i,a,b) for(int i = a;i <= b;i++)
#define pb push_back
struct node{int x , y;
    bool operator <(node b) {return x == b.x ? y < b.y : x < b.x;} 
    node operator +(node b) const {node ans; ans.x = x + b.x;ans.y = y + b.y;return ans;}
    node operator -(node b) const {node ans; ans.x = x - b.x;ans.y = y - b.y;return ans;}
};
const int N = 1e5 + 5;
int n, in[N] , g[N] , rt , s[N] , v[N];
node f[N][2] , ans;
vector<int> c[N];
vector<node> p , q;
void calc(int u) {
    f[u][1] = f[u][0] = node{0,0}, g[u] = 0, v[u] = 1;
    for(auto P : c[u]) {
        if(P == rt) continue;
        calc(P);
        f[u][0] = f[u][0] + f[P][1];
        node t = f[P][0] - f[P][1] + node{1 ,s[u] ^ s[P]};
        if(f[u][1] < t) f[u][1] = t , g[u] = P;
    }
    f[u][1] = f[u][1] + f[u][0];
}
void get(int u , int i) {
    for(auto P : c[u])  { 
        if(P == rt) continue;
        if(!i || g[u] != P) get(P , 1); else p.pb(node{u,P}) , get(P , 0);
    }
}
void solve(int u) {
    for(;!v[u];u = in[u]) v[u] = 1; // 找环上的点
    node r = node{0,0};
    fo(i,1,2) {
        rt = u; // 断边
        calc(u);
        if(r < f[u][1]) r = f[u][1] , p.clear() , get(u,1);
        u = in[u]; // 换边
    }
    for(auto P : p) q.pb(P);
    ans = ans + r;
}
int main() {
    scanf("%d" , &n);
    fo(i,1,n) scanf("%d %d",in + i , s + i) , s[i]--,c[in[i]].pb(i);
    fo(i,1,n) if(!v[i]) solve(i);
    printf("%d %d\n" , ans.x , ans.y);
    for(auto P:q) printf("%d %d\n" , P.x , P.y);
    return 0;
}