import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def trich_dac_trung(G):
    du_lieu = []
    for nut in G.nodes():
        bac_nut = G.degree(nut)
        tong_trong_so = sum(canh[2]['weight'] for canh in G.edges(nut, data=True))
        du_lieu.append({
            'node_id': nut,
            'ten': G.nodes[nut]['name'],
            'khoa': G.nodes[nut]['dept'],
            'bac': bac_nut,
            'so_ket_noi': len(list(G.neighbors(nut))),
            'tong_trong_so': tong_trong_so
        })
    return pd.DataFrame(du_lieu)

def phan_loai_2_nhom(G):
    df = trich_dac_trung(G)
    dac_trung_chon = df[['bac', 'so_ket_noi', 'tong_trong_so']]
    du_lieu_chuan = StandardScaler().fit_transform(dac_trung_chon)
    mo_hinh = KMeans(n_clusters=2, random_state=42, n_init=10)
    df['nhom'] = mo_hinh.fit_predict(du_lieu_chuan)
    trung_binh_bac = df.groupby('nhom')['bac'].mean()
    nhom_anh_huong = trung_binh_bac.idxmax()
    df['phan_loai'] = df['nhom'].map({
        nhom_anh_huong: '⭐ Nhóm Ảnh hưởng cao',
        1 - nhom_anh_huong: '👤 Nhóm Thành viên thông thường'
    })
    return df.to_dict('records')