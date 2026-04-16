import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.analysis import Base, QuoteAnalysisModel

class AnalysisRepository:
    # quản lý đọc ghi vào postgres
    
    def __init__(self):
        # kết nối db và tự tạo bảng nếu chưa có
        self.engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def upsert_analysis(self, quote_id: str, analysis: dict):
        # thêm mới hoặc cập nhật kết quả vào db
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

    def find_by_id(self, quote_id: str):
        # tìm phân tích theo id
        with self.Session() as session:
            item = session.query(QuoteAnalysisModel).filter_by(quote_id=quote_id).first()
            return json.loads(item.analysis_data) if item else None
