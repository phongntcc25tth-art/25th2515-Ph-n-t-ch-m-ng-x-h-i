import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username_pseudo TEXT NOT NULL UNIQUE,
            node_type TEXT NOT NULL,
            department TEXT NOT NULL,
            description TEXT,
            nam_hoc INTEGER DEFAULT 1
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            weight REAL NOT NULL CHECK(weight > 0 AND weight <= 5),
            edge_type TEXT NOT NULL,
            observed_at TEXT,
            FOREIGN KEY(source_id) REFERENCES nodes(user_id),
            FOREIGN KEY(target_id) REFERENCES nodes(user_id),
            UNIQUE(source_id, target_id)
        )
    ''')

    cur.execute("SELECT COUNT(*) FROM nodes")
    if cur.fetchone()[0] > 0:
        print("✅ Dữ liệu đã có trong CSDL")
        conn.close()
        return

    # 30 NÚT
    nodes = [
        ('nguyen_van_a','student','CNTT','Năm 3, lớp CNTT01',3),
        ('tran_thi_b','student','CNTT','Lớp phó CNTT01',3),
        ('le_van_c','lecturer','CNTT','Giảng viên môn Mạng',0),
        ('pham_thi_d','student','KT','Ban cán sự lớp KT02',2),
        ('hoang_van_e','student','CNTT','Trưởng nhóm đồ án',4),
        ('nguyen_thi_f','student','VT','Đội viên tình nguyện',3),
        ('vo_van_g','student','CNTT','Thư ký lớp',2),
        ('do_thi_h','lecturer','KT','Trưởng bộ môn KT',0),
        ('nguyen_van_i','student','CNTT','Năm cuối, sắp tốt nghiệp',4),
        ('tran_van_k','student','CNTT','Lớp trưởng CNTT01',3),
        ('le_thi_l','student','VT','Ban sự vụ lớp VT03',2),
        ('pham_van_m','student','KT','Nhóm trưởng KT02',3),
        ('nguyen_thi_n','student','CNTT','Nhóm viên dự án',3),
        ('tran_thi_o','student','CNTT','Thành viên tích cực',2),
        ('le_van_p','student','VT','Sinh viên xuất sắc',4),
        ('nguyen_van_q','student','CNTT','Mới chuyển ngành',1),
        ('tran_thi_r','student','CNTT','Bạn cùng phòng KTX',2),
        ('le_van_s','lecturer','VT','Giảng viên hướng dẫn',0),
        ('pham_thi_t','student','KT','Cán sự học vụ',3),
        ('vo_van_u','student','CNTT','Quản lý thư viện lớp',2),
        ('nguyen_thi_v','student','VT','Năm 3, hướng ngoại',3),
        ('tran_van_x','student','CNTT','Nhóm viên nghiên cứu',4),
        ('le_thi_y','student','KT','Thư ký chi đoàn',3),
        ('pham_van_z','student','CNTT','Mới nhập học',1),
        ('nguyen_van_1','student','CNTT','Bạn thân của A',3),
        ('tran_thi_2','student','VT','Thành viên câu lạc bộ',2),
        ('le_van_3','student','KT','Đại diện lớp',4),
        ('pham_thi_4','student','CNTT','Trợ lý giảng viên',3),
        ('vo_van_5','student','CNTT','Bí thư chi đoàn',4),
        ('nguyen_thi_6','student','VT','Tổ trưởng học tập',3),
    ]
    cur.executemany("""
        INSERT INTO nodes (username_pseudo, node_type, department, description, nam_hoc)
        VALUES (?, ?, ?, ?, ?)
    """, nodes)

    # 60 CẠNH
    edges = [
        (1,2,5,'bạn thân','2024-01-10'),(1,3,4,'học cùng','2024-02-15'),(1,5,3,'nhóm','2024-03-01'),
        (1,10,4,'cùng lớp','2024-01-15'),(1,16,2,'giúp đỡ','2024-05-10'),(1,25,5,'bạn thơ ấu','2024-01-05'),
        (2,3,3,'học cùng','2024-02-20'),(2,7,4,'cùng phòng','2024-01-20'),(2,10,5,'công tác lớp','2024-02-01'),
        (2,17,3,'bạn cùng phòng','2024-03-15'),(3,5,2,'hướng dẫn','2024-03-10'),(3,7,3,'học phần','2024-04-01'),
        (3,9,2,'tư vấn','2024-04-15'),(3,14,3,'giảng dạy','2024-02-25'),(4,8,4,'hướng dẫn','2024-02-10'),
        (4,12,5,'nhóm trưởng','2024-03-05'),(4,19,3,'công tác lớp','2024-04-01'),(4,23,4,'chi đoàn','2024-03-20'),
        (4,27,3,'liên ngành','2024-05-05'),(5,6,3,'bạn','2024-03-15'),(5,9,5,'cùng dự án','2024-04-01'),
        (5,10,4,'phối hợp','2024-03-10'),(5,13,4,'nhóm viên','2024-03-12'),(5,22,3,'nghiên cứu','2024-05-01'),
        (5,29,4,'chi đoàn','2024-04-20'),(6,11,3,'cùng lớp','2024-02-20'),(6,15,4,'bạn thân','2024-03-01'),
        (6,26,2,'câu lạc bộ','2024-04-10'),(6,30,3,'học tập','2024-05-01'),(7,10,3,'lớp','2024-02-15'),
        (7,14,4,'bạn','2024-03-20'),(7,20,3,'thư viện','2024-04-05'),(9,10,5,'công tác','2024-03-25'),
        (9,13,4,'nhóm','2024-04-02'),(9,17,3,'học cùng','2024-04-15'),(9,21,2,'quen biết','2024-05-10'),
        (10,13,5,'phân công','2024-03-30'),(10,14,4,'thông tin','2024-04-10'),(10,28,4,'trợ lý','2024-04-25'),
        (10,29,5,'chi đoàn','2024-05-01'),(12,19,4,'phối hợp','2024-03-15'),(12,23,3,'chi đoàn','2024-04-05'),
        (12,27,4,'bạn','2024-04-20'),(13,14,3,'trao đổi','2024-04-15'),(13,22,4,'dự án','2024-05-05'),
        (13,25,3,'quen A','2024-05-12'),(15,18,3,'hướng dẫn','2024-03-25'),(15,21,4,'bạn','2024-04-10'),
        (17,20,3,'cùng phòng','2024-04-01'),(19,23,5,'bạn thân','2024-03-20'),(22,28,3,'trợ lý','2024-05-10'),
        (24,25,2,'mới kết nối','2024-05-15'),(26,30,4,'cùng tổ','2024-04-25'),(29,28,4,'phối hợp','2024-05-08'),
        (8,27,3,'hướng dẫn','2024-04-12'),(18,30,2,'học phần','2024-05-01'),(21,26,3,'câu lạc bộ','2024-04-20'),
    ]
    for s, t, w, loai, ngay in edges:
        a, b = (s, t) if s < t else (t, s)
        cur.execute("""
            INSERT OR IGNORE INTO edges VALUES (NULL, ?, ?, ?, ?, ?)
        """, (a, b, w, loai, ngay))

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM nodes"); n = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM edges"); e = cur.fetchone()[0]
    print(f"✅ Tạo CSDL: {n} nút, {e} cạnh")
    conn.close()

if __name__ == '__main__':
    init_database()