from analysis.community import detect_louvain

def danh_gia_do_on_dinh(G, so_lan_chay=5):
    danh_sach_kq = []
    for _ in range(so_lan_chay):
        kq = detect_louvain(G)
        danh_sach_kq.append({
            'so_cong_dong': kq['so_nhom'],
            'modularity': kq['modularity']
        })
    trung_binh_mod = sum(x['modularity'] for x in danh_sach_kq) / len(danh_sach_kq)
    do_lech = max(x['modularity'] for x in danh_sach_kq) - min(x['modularity'] for x in danh_sach_kq)
    muc_do_on_dinh = '✅ Rất ổn định' if do_lech < 0.01 else '⚠️ Ít ổn định'
    return {
        'trung_binh_modularity': round(trung_binh_mod, 6),
        'do_lech_max_min': round(do_lech, 6),
        'muc_do_on_dinh': muc_do_on_dinh
    }