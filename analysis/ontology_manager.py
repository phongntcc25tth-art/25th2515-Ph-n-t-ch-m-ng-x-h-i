from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import os

def tao_ontology_tu_du_lieu(G, df_nodes):
    g = Graph()
    SNA = Namespace("http://example.org/sna#")
    g.bind('sna', SNA)
    
    # Định nghĩa lớp
    g.add((SNA.NguoiDung, RDF.type, RDFS.Class))
    g.add((SNA.SinhVien, RDFS.subClassOf, SNA.NguoiDung))
    g.add((SNA.GiangVien, RDFS.subClassOf, SNA.NguoiDung))
    
    # Thêm cá thể
    for _, dong in df_nodes.iterrows():
        uri = URIRef(f"http://example.org/sna#{dong['username_pseudo']}")
        lop = SNA.SinhVien if dong['node_type'] == 'student' else SNA.GiangVien
        g.add((uri, RDF.type, lop))
        g.add((uri, SNA.coTen, Literal(dong['username_pseudo'], datatype=XSD.string)))
        g.add((uri, SNA.thuocKhoa, Literal(dong['department'], datatype=XSD.string)))
        g.add((uri, SNA.namHoc, Literal(dong['nam_hoc'], datatype=XSD.integer)))
    
    # Thêm quan hệ
    for u, v, thong_tin in G.edges(data=True):
        uri_u = URIRef(f"http://example.org/sna#{G.nodes[u]['name']}")
        uri_v = URIRef(f"http://example.org/sna#{G.nodes[v]['name']}")
        g.add((uri_u, SNA.coQuanHe, uri_v))
        g.add((uri_u, SNA.trongSo, Literal(thong_tin['weight'], datatype=XSD.float)))
    
    os.makedirs('ontology', exist_ok=True)
    g.serialize(destination='ontology/network_ontology.ttl', format='turtle')
    return g

def lay_danh_sach_tu_ontology():
    g = Graph()
    try:
        g.parse('ontology/network_ontology.ttl')
    except:
        return []
    SNA = Namespace("http://example.org/sna#")
    cau_truy_van = """
        SELECT ?ten ?khoa ?nam
        WHERE {
            ?n a sna:NguoiDung ;
               sna:coTen ?ten ;
               sna:thuocKhoa ?khoa .
            OPTIONAL { ?n sna:namHoc ?nam . }
        }
    """
    ket_qua = []
    for dong in g.query(cau_truy_van, initNs={'sna': SNA}):
        ket_qua.append({
            'ten': str(dong.ten),
            'khoa': str(dong.khoa),
            'nam': int(dong.nam) if dong.nam else None
        })
    return ket_qua

def lay_theo_khoa(ten_khoa):
    ds = lay_danh_sach_tu_ontology()
    return [x for x in ds if x['khoa'] == ten_khoa]