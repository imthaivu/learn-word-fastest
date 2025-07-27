import re

# === Đọc file phrasal verb (dạng nguyên mẫu) ===
with open("PhVerb.txt", "r", encoding="utf-8") as f:
    phrasal_verbs = [line.strip() for line in f if line.strip()]

# === Đọc file động từ bất quy tắc ===
irregular_dict = {}
with open("irregular_verbs.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 3:
            base, past, past_participle = parts
            for b in base.split("/"):
                irregular_dict[b] = {
                    "past": past.split("/")[0],
                    "past_participle": past_participle.split("/")[0]
                }

# === Hàm chia động từ thường ===
def regular_forms(verb):
    if verb.endswith('e'):
        ing = verb + 'ing'
        ed = verb + 'd'
    elif re.match(r'.*[^aeiou][aeiou][^aeiou]$', verb):  # run -> running, rob -> robbed
        ing = verb + verb[-1] + 'ing'
        ed = verb + verb[-1] + 'ed'
    else:
        ing = verb + 'ing'
        ed = verb + 'ed'

    if verb.endswith('y') and not verb.endswith(('ay', 'ey', 'oy', 'uy')):
        s = verb[:-1] + 'ies'
    elif verb.endswith(('s', 'sh', 'ch', 'x', 'z', 'o')):
        s = verb + 'es'
    else:
        s = verb + 's'
    return ing, ed, s

# === Tạo biến thể ===
all_forms = set()

for phrase in phrasal_verbs:
    parts = phrase.split(" ")
    verb = parts[0]
    tail = " ".join(parts[1:]) if len(parts) > 1 else ""

    if verb in irregular_dict:
        past = irregular_dict[verb]["past"]
        past_part = irregular_dict[verb]["past_participle"]
    else:
        _, past, past_part = regular_forms(verb)

    ing, _, _ = regular_forms(verb)
    _, _, sform = regular_forms(verb)

    forms = {
        f"{verb} {tail}".strip(),
        f"{ing} {tail}".strip(),
        f"{past} {tail}".strip(),
        f"{past_part} {tail}".strip(),
        f"{sform} {tail}".strip()
    }

    all_forms.update(forms)

# === Ghi kết quả ra file ===
with open("phrasalverbFullType.txt", "w", encoding="utf-8") as f:
    for item in sorted(all_forms):
        f.write(item + "\n")
