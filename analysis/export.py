import pandas as pd
import os
from fpdf import FPDF

def xuat_bao_cao_excel(thong_so, ds_anh_huong, ds_cong_dong, ds_du_doan, thu_muc='output'):
    os.makedirs(thu_muc, exist_ok=True)
    duong_dan = os.path.join(thu_muc, 'Bao_Cao_Du_Lieu.xlsx')
    with pd.ExcelWriter(duong_dan) as writer:
        pd.DataFrame([thong_so]).to_excel(writer, sheet_name='Tong_Quan', index=False)
        pd.DataFrame(ds_anh_huong).to_excel(writer, sheet_name='Anh_Huong', index=False)
        pd.DataFrame([{'Phuong_phap': k, **v} if isinstance(v, dict) else {} for k, v in ds_cong_dong.items()]).to_excel(writer, sheet_name='Cong_Dong', index=False)
        pd.DataFrame(ds_du_doan).to_excel(writer, sheet_name='Du_Doan', index=False)
    return duong_dan

def xuat_bao_cao_pdf(thong_so, ds_anh_huong, thu_muc='output'):
    os.makedirs(thu_muc, exist_ok=True)
    duong_dan = os.path.join(thu_muc, 'Bao_Cao_Tom_Tat.pdf')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 12, 'BAO CAO PHAN TICH MANG XA HOI', 0, 1, 'C')
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '1. Thong so tong quan', 0, 1)
    pdf.set_font('Arial', '', 11)
    for k, v in thong_so.items():
        pdf.cell(0, 8, f'{k}: {v}', 0, 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '2. Top 5 nguoi co anh huong cao nhat', 0, 1)
    pdf.set_font('Arial', '', 11)
    for i, n in enumerate(ds_anh_huong[:5], 1):
        pdf.cell(0, 8, f'{i}. {n["ten"]} - Tong diem: {n["tong_diem"]}', 0, 1)
    pdf.output(duong_dan)
    return duong_dan