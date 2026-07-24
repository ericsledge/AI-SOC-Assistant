from dataclasses import dataclass

@dataclass
class DocumentChunk:
    chunk_id: str
    text: str
    source_name: str
    source_path: str
    category: str
    file_type: str
    page_number: int | None
    chunk_number: int