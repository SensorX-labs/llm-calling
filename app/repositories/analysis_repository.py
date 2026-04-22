import json
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.analysis import Base, QuoteAnalysisModel

class AnalysisRepository:
    # quản lý đọc ghi vào postgres
    def __init__(self):
        # 1. Tạo database nếu chưa có
        self._ensure_database_exists()
        
        # 2. kết nối db chính và tự tạo bảng nếu chưa có
        self.engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def _ensure_database_exists(self):
        # Kết nối tới database mặc định 'postgres' để kiểm tra và tạo database mới
        # Tách URL để lấy thông tin kết nối cơ bản
        base_url = settings.DATABASE_URL.rsplit('/', 1)[0] + "/postgres"
        db_name = settings.DATABASE_URL.rsplit('/', 1)[-1]
        
        temp_engine = create_engine(base_url, isolation_level="AUTOCOMMIT")
        with temp_engine.connect() as conn:
            # Kiểm tra database tồn tại
            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
            ).fetchone()
            
            if not result:
                print(f"[*] Database '{db_name}' chưa tồn tại. Đang tiến hành tạo mới...")
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"[ok] Đã tạo thành công database '{db_name}'")
        temp_engine.dispose()

    # thêm mới hoặc cập nhật kết quả vào db
    def upsert_analysis(self, quote_id: str, analysis: dict):
        with self.Session() as session:
            db_item = session.query(QuoteAnalysisModel).filter_by(quote_id=quote_id).first()
            if db_item:
                db_item.analysis_data = json.dumps(analysis)
                db_item.created_at = datetime.utcnow()
            else:
                new_item = QuoteAnalysisModel(
                    quote_id=quote_id,
                    analysis_data=json.dumps(analysis)
                )
                session.add(new_item)
            session.commit()

    # tìm phân tích theo id
    def find_by_id(self, quote_id: str):
        with self.Session() as session:
            item = session.query(QuoteAnalysisModel).filter_by(quote_id=quote_id).first()
            return json.loads(item.analysis_data) if item else None
