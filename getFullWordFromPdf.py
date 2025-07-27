import fitz  # pip install pymupdf
import re
import pandas as pd

# === Đường dẫn file ===
pdf_path = "ESL_Fast.pdf"
phrasal_verbs_path = "phrasalverbFullType.txt"
output_path = "output.xlsx"

print("🚀 Bắt đầu quá trình xử lý...")

# === Đọc danh sách phrasal verbs đã mở rộng ===
print("📥 Đang đọc danh sách phrasal verbs...")
with open(phrasal_verbs_path, "r", encoding="utf-8") as f:
    phrasal_lines = [line.strip().lower().replace("'", "") for line in f if line.strip()]
phrasal_set = set(phrasal_lines)
print(f"✅ Đã tải {len(phrasal_set)} cụm từ từ {phrasal_verbs_path}")

# Sắp xếp theo độ dài từ nhiều từ đến ít từ
phrasal_sorted = sorted(phrasal_set, key=lambda x: -len(x.split()))

# === Trích xuất văn bản từ PDF ===
print(f"📄 Đang trích xuất văn bản từ {pdf_path}...")
doc = fitz.open(pdf_path)
text = " ".join([page.get_text() for page in doc])
text = text.lower().replace("’", "'")
print("✅ Hoàn tất trích xuất và chuẩn hóa văn bản.")

# === Thay thế phrasal verbs bằng token đặc biệt ===
print("🔍 Đang thay thế phrasal verbs bằng token...")
placeholder_map = {}
token_id = 0

for phrasal in phrasal_sorted:
    # process each phrasal verb
    pattern = r'(?<!\w)' + re.escape(phrasal) + r'(?!\w)'
    if re.search(pattern, text):
        token = f"__PHV{token_id}__"
        text = re.sub(pattern, token, text)
        placeholder_map[token] = phrasal
        token_id += 1

print(f"✅ Đã thay thế {len(placeholder_map)} phrasal verbs bằng token.")

# === Tách từ và loại trùng lặp ===
print("🧹 Đang lọc từ vựng và loại trùng lặp...")
seen = set()
vocab_ordered = []

for word in re.findall(r"\b[a-zA-Z']+\b|__PHV\d+__", text):
    if word.startswith("__PHV"):
        actual_phrase = placeholder_map[word]
        if actual_phrase not in seen:
            seen.add(actual_phrase)
            vocab_ordered.append(actual_phrase)
    else:
        cleaned = word.strip("'")
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            vocab_ordered.append(cleaned)

print(f"✅ Trích xuất được {len(vocab_ordered)} từ vựng duy nhất.")

# === Xuất ra Excel ===
print(f"💾 Đang lưu danh sách từ vựng vào {output_path}...")
df = pd.DataFrame(vocab_ordered, columns=["Vocabulary"])
df.to_excel(output_path, index=False)
print(f"🎉 Hoàn tất! File đã lưu tại: {output_path}")
