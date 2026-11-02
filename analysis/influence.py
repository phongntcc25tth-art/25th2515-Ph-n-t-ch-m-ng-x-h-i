import networkx as nx

def tinh_tat_ca_chi_so(G):
    deg = nx.degree_centrality(G)
    bet = nx.betweenness_centrality(G, weight='weight', normalized=True)
    clo = nx.closeness_centrality(G, distance='weight')
    eig = nx.eigenvector_centrality(G, weight='weight', max_iter=2000)
    pgr = nx.pagerank(G, weight='weight')
    
    danh_sach = []
    for nut in G.nodes():
        danh_sach.append({
            'ten': G.nodes[nut]['name'],
            'degree': round(deg[nut], 4),
            'betweenness': round(bet[nut], 4),
            'closeness': round(clo[nut], 4),
            'eigenvector': round(eig[nut], 4),
            'pagerank': round(pgr[nut], 4),
            'tong_diem': round(deg[nut] + bet[nut] + clo[nut] + eig[nut] + pgr[nut], 4)
        })
    return sorted(danh_sach, key=lambda x: x['tong_diem'], reverse=True)