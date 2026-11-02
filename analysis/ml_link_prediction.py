import networkx as nx
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def lay_dac_trung_canh(G, u, v):
    try:
        hang_xom_chung = len(list(nx.common_neighbors(G, u, v)))
    except:
        hang_xom_chung = 0
    jaccard = list(nx.jaccard_coefficient(G, [(u, v)]))[0][2] if u != v else 0
    uu_tien = list(nx.preferential_attachment(G, [(u, v)]))[0][2] if u != v else 0
    adamic_adar = list(nx.adamic_adar_index(G, [(u, v)]))[0][2] if u != v else 0
    return [hang_xom_chung, jaccard, uu_tien, adamic_adar]

def chuan_bo_du_lieu_huan_luyen(G):
    X, y = [], []
    for u, v in G.edges():
        X.append(lay_dac_trung_canh(G, u, v))
        y.append(1)
    so_luong_am = 0
    for u in G.nodes():
        for v in G.nodes():
            if u >= v or G.has_edge(u, v):
                continue
            if so_luong_am >= len(G.edges()):
                break
            X.append(lay_dac_trung_canh(G, u, v))
            y.append(0)
            so_luong_am += 1
    return np.array(X), np.array(y)

def so_sanh_2_mo_hinh(G):
    X, y = chuan_bo_du_lieu_huan_luyen(G)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    do_chinh_xac_rf = round(accuracy_score(y_test, rf.predict(X_test)), 4)
    
    xgb = XGBClassifier(n_estimators=100, learning_rate=0.1, eval_metric='logloss')
    xgb.fit(X_train, y_train)
    do_chinh_xac_xgb = round(accuracy_score(y_test, xgb.predict(X_test)), 4)
    
    return {
        'Random Forest': do_chinh_xac_rf,
        'XGBoost': do_chinh_xac_xgb
    }, rf

def du_doan_cac_cap_tiem_nang(G, mo_hinh, top_n=5):
    ket_qua = []
    for u in G.nodes():
        for v in G.nodes():
            if u >= v or G.has_edge(u, v):
                continue
            dac_trung = np.array([lay_dac_trung_canh(G, u, v)])
            xac_suat = round(mo_hinh.predict_proba(dac_trung)[0][1], 4)
            if xac_suat > 0.3:
                ket_qua.append({
                    'tu': u,
                    'den': v,
                    'ten_tu': G.nodes[u]['name'],
                    'ten_den': G.nodes[v]['name'],
                    'xac_suat': xac_suat
                })
    return sorted(ket_qua, key=lambda x: x['xac_suat'], reverse=True)[:top_n]