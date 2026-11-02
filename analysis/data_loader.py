import sqlite3
import networkx as nx
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')

def load_data(bo_khoa=None, bo_loai=None):
    conn = sqlite3.connect(DB_PATH)
    df_nodes = pd.read_sql_query("SELECT * FROM nodes", conn)
    df_edges = pd.read_sql_query("SELECT * FROM edges", conn)
    
    # Lọc theo khoa/loại nếu có yêu cầu
    if bo_khoa:
        df_nodes = df_nodes[df_nodes['department'] == bo_khoa].reset_index(drop=True)
    if bo_loai:
        df_nodes = df_nodes[df_nodes['node_type'] == bo_loai].reset_index(drop=True)
    
    G = nx.Graph()
    for _, row in df_nodes.iterrows():
        G.add_node(row['user_id'],
            name=row['username_pseudo'],
            type_node=row['node_type'],
            dept=row['department'],
            desc=row['description'],
            nam_hoc=row['nam_hoc'])
    
    for _, row in df_edges.iterrows():
        if int(row['source_id']) in G.nodes() and int(row['target_id']) in G.nodes():
            G.add_edge(int(row['source_id']), int(row['target_id']),
                weight=float(row['weight']), type_edge=row['edge_type'])
    
    conn.close()
    return G, df_nodes, df_edges

def get_graph_stats(G):
    so_nut = G.number_of_nodes()
    so_canh = G.number_of_edges()
    mat_do = round(nx.density(G), 6)
    trung_binh_bac = round(2 * so_canh / so_nut, 3) if so_nut > 0 else 0
    return {
        'so_nut': so_nut,
        'so_canh': so_canh,
        'mat_do': mat_do,
        'trung_binh_bac': trung_binh_bac
    }