from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

# kế thừa class base để tạo bảng orm 
Base = declarative_base()
class QuoteAnalysisModel(Base):
    __tablename__ = 'quote_analyses'
    
    quote_id = Column(String, primary_key=True)
    analysis_data = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
