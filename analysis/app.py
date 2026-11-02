from flask import Flask, render_template, send_file
from analysis.db_setup import init_database
from analysis.data_loader import load_data, get_graph_stats
from analysis.community import detect_louvain, detect_label_propagation, detect_girvan_newman
from analysis.influence import tinh_tat_ca_chi_so
from analysis.prediction import du_doan_ket_noi_truyen_thong
from analysis.evaluation import danh_gia_do_on_dinh
from analysis.export import xuat_bao_cao_excel, xuat_bao_cao_pdf
from analysis.ml_classifier import phan_loai_2_nhom
from analysis.ml_link_prediction import so_sanh_2_mo_hinh, du_doan_cac_cap_tiem_nang, lay_dac_trung_canh
from analysis.ontology_manager import tao_ontology_tu_du_lieu, lay_danh_sach_tu_ontology, lay_theo_khoa

app = Flask(__name__)

# === KHỞI TẠO DỮ LIỆU ===
init_database()
G, df_nodes, df_edges = load_data()
thong_so_tong_quang = get_graph_stats(G)

# === MỨC 1 ===
kq_louvain = detect_louvain(G)
kq_label = detect_label_propagation(G)
kq_girvan = detect_girvan_newman(G)
ds_anh_huong = tinh_tat_ca_chi_so(G)
ds_du_doan_cb = du_doan_ket_noi_truyen_thong(G)
danh_gia_on_dinh = danh_gia_do_on_dinh(G)

# === MỨC 2 ===
ds_phan_loai = phan_loai_2_nhom(G)
bang_do_chinh_xac, mo_hinh_rf = so_sanh_2_mo_hinh(G)
ds_du_doan_ml = du_doan_cac_cap_tiem_nang(G, mo_hinh_rf)
tao_ontology_tu_du_lieu(G, df_nodes)
ds_ont = lay_danh_sach_tu_ontology()
ds_cn_ont = lay_theo_khoa('CNTT')

# === ROUTE ===
@app.route('/')
def trang_chu():
    return render_template('index.html', ts=thong_so_tong_quang,
        danh_sach_nut=df_nodes.to_dict('records'),
        danh_sach_canh=df_edges.to_dict('records'))

@app.route('/communities')
def trang_cong_dong():
    return render_template('communities.html',
        lv=kq_louvain, lp=kq_label, gn=kq_girvan, dg=danh_gia_on_dinh)

@app.route('/influence')
def trang_anh_huong():
    return render_template('influence.html', top10=ds_anh_huong[:10], tat_ca=ds_anh_huong)

@app.route('/prediction')
def trang_du_doan():
    return render_template('prediction.html', cb=ds_du_doan_cb,
        ml=ds_du_doan_ml, acc=bang_do_chinh_xac)

@app.route('/machine_learning')
def trang_ml():
    return render_template('machine_learning.html',
        phanloai=ds_phan_loai, acc=bang_do_chinh_xac)

@app.route('/ontology')
def trang_ontology():
    return render_template('ontology.html', ds=ds_ont, cntt=ds_cn_ont)

@app.route('/visualization')
def trang_truc_quan():
    return render_template('visualization.html',
        nut=df_nodes.to_dict('records'), canh=df_edges.to_dict('records'), phanbo=kq_louvain['phan_bo'])

@app.route('/report')
def trang_bao_cao():
    return render_template('report.html', ts=thong_so_tong_quang,
        top5=ds_anh_huong[:5], lv=kq_louvain, acc=bang_do_chinh_xac)

@app.route('/export/excel')
def tai_excel():
    return send_file(xuat_bao_cao_excel(thong_so_tong_quang, ds_anh_huong,
        kq_louvain, ds_du_doan_cb), as_attachment=True)

@app.route('/export/pdf')
def tai_pdf():
    return send_file(xuat_bao_cao_pdf(thong_so_tong_quang, ds_anh_huong), as_attachment=True)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 KHỞI ĐỘNG HỆ THỐNG PHÂN TÍCH MẠNG XÃ HỘI")
    print(f"  Dữ liệu: {thong_so_tong_quang['so_nut']} nút, {thong_so_tong_quang['so_canh']} cạnh")
    print(f"  Cộng đồng Louvain: {kq_louvain['so_nhom']} nhóm")
    print(f"  Độ chính xác RF: {bang_do_chinh_xac['Random Forest']} | XGB: {bang_do_chinh_xac['XGBoost']}")
    print("=" * 60)
    app.run(debug=True, port=5000)