import networkx as nx
from community import community_louvain

def detect_louvain(G):
    phan_bo = community_louvain.best_partition(G)
    so_nhom = len(set(phan_bo.values()))
    danh_sach_nhom = {}
    for nut, nhom in phan_bo.items():
        ten_nut = G.nodes[nut]['name']
        danh_sach_nhom.setdefault(nhom, []).append(ten_nut)
    do_modun = round(community_louvain.modularity(phan_bo, G), 6)
    return {
        'phuong_phap': 'Louvain',
        'so_nhom': so_nhom,
        'danh_sach': danh_sach_nhom,
        'modularity': do_modun,
        'phan_bo': phan_bo
    }

def detect_label_propagation(G):
    cac_nhom = list(nx.algorithms.community.label_propagation.label_propagation_communities(G))
    phan_bo = {}
    for nhom, thanh_vien in enumerate(cac_nhom):
        for nut in thanh_vien:
            phan_bo[nut] = nhom
    danh_sach_nhom = {}
    for nut, nhom in phan_bo.items():
        ten_nut = G.nodes[nut]['name']
        danh_sach_nhom.setdefault(nhom, []).append(ten_nut)
    return {
        'phuong_phap': 'Label Propagation',
        'so_nhom': len(danh_sach_nhom),
        'danh_sach': danh_sach_nhom,
        'phan_bo': phan_bo
    }

def detect_girvan_newman(G, muc_do=3):
    G_copy = G.copy()
    while len(list(nx.connected_components(G_copy))) < muc_do and G_copy.number_of_edges() > 0:
        canh_trung_gian = max(nx.edge_betweenness_centrality(G_copy).items(), key=lambda x: x[1])[0]
        G_copy.remove_edge(*canh_trung_gian)
    phan_bo = {}
    for nhom, thanh_vien in enumerate(nx.connected_components(G_copy)):
        for nut in thanh_vien:
            phan_bo[nut] = nhom
    danh_sach_nhom = {}
    for nut, nhom in phan_bo.items():
        ten_nut = G.nodes[nut]['name']
        danh_sach_nhom.setdefault(nhom, []).append(ten_nut)
    return {
        'phuong_phap': 'Girvan-Newman',
        'so_nhom': len(danh_sach_nhom),
        'danh_sach': danh_sach_nhom,
        'phan_bo': phan_bo
    }