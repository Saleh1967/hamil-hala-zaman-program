# online_peel.py — التقشير الفوري: لا معجمَ كامل يُطالب باستقلال الجذع، بل لواحقَ معلنة
# تُقشَر أولًا بأول (أطولُ لاحقةٍ أولًا) كلما وردت الكلمة — فتُعمَّم على غير المشهود.
# الجدول المعلن (من جدول الأدوار): اللواحق الصريحة + حارسا التاء والمبني.
# الحارسان: ① التاء المربوطة ليست هاءً ضميرًا أبدًا ② المبنيّات المنتهية بصورة الضمير.
import sys, os, json
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from induction_engine import parse_verses

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")
SUF = ("هما", "كما", "هن", "هم", "كن", "كم", "نا", "ها", "ه", "ك", "ي")
GUARD_TA = "ة"                                   # لا تُقشَر هاءً قط
GUARD_WORDS = {"هذه", "هذي", "ذه", "هؤلاء", "فيه", "عليه", "إليه", "لديه", "أنه", "إنه"}
MIN_STEM = 2                                     # جذعٌ أجوف/ناقص لا يقل عن حرفين بعد القلع


def peel(sk):
    """أونلاين: أطولُ لاحقةٍ معلنة تُقشَر أولًا، والحارسان قبل كل قلع."""
    if sk in GUARD_WORDS or sk.endswith(GUARD_TA):
        return sk, None, "حارس"
    for s in SUF:
        if sk.endswith(s) and len(sk) - len(s) >= MIN_STEM:
            return sk[:-len(s)], s, "مقشور"
    return sk, None, "بلا-لاحقة"


def main():
    verses = parse_verses(CORPUS)
    stat = Counter(); by_suf = Counter(); blocked = Counter()
    witness = {}
    for v in verses:
        for w in v:
            sk = "".join(c for c, _ in w)
            stem, suf, how = peel(sk)
            stat[how] += 1
            if suf:
                by_suf[suf] += 1
            if how == "حارس":
                blocked[sk] += 1
            for key in ("أيديهم", "أيديهم", "الآخرة", "ربكم", "بكم", "قبلك", "ملكه", "هداهم"):
                if sk == key and key not in witness:
                    witness[key] = (stem, suf, how)
    R = dict(كلمات=sum(stat.values()), أحوال=dict(stat), لواحق=dict(by_suf.most_common()),
             حارس_التاء=sum(blocked.values()), شواهد=witness)
    print("الأحوال:", dict(stat), "| الكلمات:", sum(stat.values()))
    print("أعلى اللواحق:", by_suf.most_common(8))
    print("حارس التاء حجب:", sum(blocked.values()))
    for k, val in witness.items():
        print(f"  {k} ⟵ جذع: {val[0]} · لاحقة: {val[1]} · {val[2]}")
    return R


if __name__ == "__main__":
    R = main()
    if "--json" in sys.argv:
        p = sys.argv[sys.argv.index("--json") + 1]
        json.dump({"التقشير_الفوري": R}, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {p}")
