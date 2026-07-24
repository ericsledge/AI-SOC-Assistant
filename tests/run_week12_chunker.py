"""
Manual verification script for the Week 12 text chunker.
"""

from pathlib import Path

from backend.document_loader import DocumentLoader
from backend.text_chunker import TextChunker


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIRECTORY = PROJECT_ROOT / "knowledge_base" / "documents"


def main() -> None:
    """Load all knowledge-base documents and create text chunks."""
    loader = DocumentLoader(DOCUMENT_DIRECTORY)
    documents = loader.load_documents()

    if not documents:
        print("No documents were found.")
        print(f"Checked directory: {DOCUMENT_DIRECTORY}")
        return

    chunker = TextChunker(
        chunk_size=500,
        overlap=100,
    )

    total_chunks = 0
    successful_documents = 0
    failed_documents = 0

    print()
    print("WEEK 12 TEXT CHUNKER")
    print("=" * 70)

    for document in documents:
        document_name = document.get(
            "name",
            "Unknown document",
        )

        if not document.get("loaded_successfully", False):
            failed_documents += 1

            print()
            print(f"Document: {document_name}")
            print("Status:   FAILED")
            print(
                f"Error:    {document.get('error', 'Unknown error')}"
            )
            continue

        chunks = chunker.chunk_document(document)
        successful_documents += 1
        total_chunks += len(chunks)

        print()
        print(f"Document:   {document_name}")
        print(f"Pages:      {document.get('page_count', 0)}")
        print(f"Characters: {document.get('character_count', 0):,}")
        print(f"Words:      {document.get('word_count', 0):,}")
        print(f"Chunks:     {len(chunks)}")

        if chunks:
            first_chunk = chunks[0]

            print(f"First ID:   {first_chunk.chunk_id}")
            print(
                "Preview:    "
                f"{first_chunk.text[:120].replace(chr(10), ' ')}..."
            )

    print()
    print("=" * 70)
    print("CHUNKING SUMMARY")
    print("-" * 70)
    print(f"Documents discovered: {len(documents)}")
    print(f"Documents processed:  {successful_documents}")
    print(f"Documents failed:     {failed_documents}")
    print(f"Total chunks:         {total_chunks}")
    print(f"Chunk size:           {chunker.chunk_size}")
    print(f"Chunk overlap:        {chunker.overlap}")

    if total_chunks == 0:
        raise RuntimeError(
            "No text chunks were created. Verify that the PDFs contain "
            "extractable text."
        )


if __name__ == "__main__":
    main()