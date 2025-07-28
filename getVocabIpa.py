from eng_to_ipa import convert
import pandas as pd
from tqdm import tqdm  # pip install tqdm

# Chuẩn bị thanh tiến trình cho pandas
tqdm.pandas()

# Hàm xử lý cả phrasal verb
def get_ipa(word_or_phrase: str):
    words = word_or_phrase.strip().split()
    ipa_parts = [convert(w) for w in words]
    return " ".join(ipa_parts)

# Đọc file Excel có cột "Vocabulary"
df = pd.read_excel("output.xlsx")

# Thêm cột IPA mới với thanh tiến trình
df["IPA"] = df["Vocabulary"].progress_apply(get_ipa)

# Ghi ra file mới
df.to_excel("output_with_ipa.xlsx", index=False)

print("🎉 Hoàn tất! Đã thêm cột IPA vào file output_with_ipa.xlsx.")
