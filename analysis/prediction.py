import networkx as nx

def du_doan_ket_noi_truyen_thong(G, top_n=5):
    ket_qua = []
    for u in G.nodes():
        for v in G.nodes():
            if u >= v or G.has_edge(u, v):
                continue
            try:
                hang_xom_chung = len(list(nx.common_neighbors(G, u, v)))
            except:
                hang_xom_chung = 0
            jaccard = list(nx.jaccard_coefficient(G, [(u, v)]))[0][2]
            uu_tien = list(nx.preferential_attachment(G, [(u, v)]))[0][2]
            adamic_adar = list(nx.adamic_adar_index(G, [(u, v)]))[0][2]
            diem = hang_xom_chung * 10 + jaccard * 5 + uu_tien / 100 + adamic_adar * 3
            ket_qua.append({
                'tu': u,
                'den': v,
                'ten_tu': G.nodes[u]['name'],
                'ten_den': G.nodes[v]['name'],
                'hang_xom_chung': hang_xom_chung,
                'jaccard': round(jaccard, 4),
                'uu_tien_ket_noi': round(uu_tien, 2),
                'adamic_adar': round(adamic_adar, 4),
                'diem_du_doan': round(diem, 4)
            })
    return sorted(ket_qua, key=lambda x: x['diem_du_doan'], reverse=True)[:top_n]