import re
import fitz  # pip install pymupdf
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm  # pip install tqdm

# === Chuẩn bị ===
nltk.download('wordnet', quiet=True)
lemmatizer = WordNetLemmatizer()

def normalize_phrasal(phrase: str) -> str:
    words = phrase.split()
    if not words:
        return phrase
    base = lemmatizer.lemmatize(words[0], 'v')
    return " ".join([base] + words[1:])

# === Đường dẫn file ===
pdf_path = "LR.pdf"
phrasal_verbs_path = "phrasalverbFullType.txt"
output_path = "output.xlsx"

print("🚀 Bắt đầu quá trình xử lý...")

# === Đọc danh sách phrasal verbs đã mở rộng ===
print("📥 Đang đọc danh sách phrasal verbs...")
with open(phrasal_verbs_path, "r", encoding="utf-8") as f:
    phrasal_lines = [line.strip().lower().replace("'", "") for line in f if line.strip()]
phrasal_set = set(phrasal_lines)
print(f"✅ Đã tải {len(phrasal_set)} cụm từ từ {phrasal_verbs_path}")

# Sắp xếp theo độ dài giảm dần để ưu tiên cụm dài trước
phrasal_sorted = sorted(phrasal_set, key=lambda x: -len(x.split()))

# === Trích xuất văn bản từ PDF ===
print(f"📄 Đang trích xuất văn bản từ {pdf_path}...")
doc = fitz.open(pdf_path)
text = " ".join([page.get_text() for page in doc])
text = text.lower().replace("’", "'")
print("✅ Hoàn tất trích xuất và chuẩn hóa văn bản.")

# === Thay thế phrasal verbs bằng token đặc biệt ===
print("🔍 Đang thay thế phrasal verbs bằng token (có tiến trình)...")
placeholder_map = {}
token_id = 0

for phrasal in tqdm(phrasal_sorted, desc="Đang xử lý phrasal verbs"):
    pattern = r'(?<!\w)' + re.escape(phrasal) + r'(?!\w)'
    if re.search(pattern, text):
        token = f"__PHV{token_id}__"
        text = re.sub(pattern, token, text)
        placeholder_map[token] = phrasal
        token_id += 1

print(f"✅ Đã thay thế {len(placeholder_map)} phrasal verbs bằng token.")
# === Phân bài học + tách từ vựng ===
print("📚 Đang phân tích bài học và tách từ vựng...")

lines = text.splitlines()
output_rows = []
current_title = ""
seen = set()

for line in lines:
    line = line.strip()
    if not line:
        continue

    # Nhận diện tiêu đề bài học: bắt đầu bằng 1–3 chữ số + dấu chấm
    match = re.match(r'^(\d{1,3})\.\s*(.+)', line)
    if match:
        lesson_number = match.group(1)
        title = match.group(2).strip()
        current_title = f"{lesson_number}. {title}"
        output_rows.append(current_title.lower())  # dòng tiêu đề
    else:
        # Tìm các từ hoặc token trong dòng này
        words = re.findall(r"\b[a-zA-Z']+\b|__PHV\d+__", line)
        for word in words:
            if word.startswith("__PHV"):
                actual_phrase = placeholder_map.get(word, word)
                norm = normalize_phrasal(actual_phrase)
                if norm not in seen:
                    seen.add(norm)
                    output_rows.append(actual_phrase.lower())
            else:
                cleaned = word.strip("'")
                norm = normalize_phrasal(cleaned)
                if cleaned and norm not in seen:
                    seen.add(norm)
                    output_rows.append(cleaned.lower())


# === Xuất ra Excel ===
print(f"✅ Trích xuất được {len(output_rows)} dòng từ vựng và tiêu đề.")
df = pd.DataFrame(output_rows, columns=["Vocabulary"])

df.to_excel(output_path, index=False)
print(f"🎉 Hoàn tất! File đã lưu tại: {output_path}")
