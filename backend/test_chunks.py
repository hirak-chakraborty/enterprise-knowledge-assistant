import fitz

file_path = "backend/uploads/Resume Review Feedback.pdf"

document = fitz.open(file_path)

total_chars = 0
pages_with_text = 0

for page in document:
    text = page.get_text().strip()

    if text:
        pages_with_text += 1
        total_chars += len(text)

print("Total pages:", len(document))
print("Pages with text:", pages_with_text)
print("Total extracted characters:", total_chars)