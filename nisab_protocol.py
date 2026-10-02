#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""بروتوكولُ ما قبلَ العدّ — مُلزِمٌ بالبناء، لا وحدةٌ تُستشار اختيارًا.

§٠ العلّة
─────────
الوحدةُ التي **تُستشار** لا تُلزِم. من شاء دعاها، ومن شاء عدَّ ثمّ أعلن، فيبقى
شرطُ الإمكان وعدًا في وثيقةٍ لا حارسًا في الطريق. وهذا البروتوكولُ يُنقَل من
«يُستحسَن أن يُستشار» إلى «لا يُعَدُّ إلا من خلاله» بأربعةِ أوجهٍ بنيويّة:

① **الموقعُ محفوظٌ بختمه.** `THE_FOUNDING_SITE` مادّةٌ مُعلَنةٌ بمسارها وطولها
   وبصمة sha256، **تُشتَقُّ من القرص عند كلِّ قراءةٍ ولا تُفترَض**. فتحريرُ
   دالّة التأسيس يُبلَّغ، ولا يمرُّ صامتًا.

② **حارسٌ عند الاستيراد.** الموقعُ الغائبُ أو المُحرَّف يَصرُخ لحظةَ
   `import` — لا عند أوّل استعمالٍ قد لا يقع.

③ **الأسبقيّةُ بنيويّةٌ لا موعودة.** `measure_under_the_protocol` يأخذ العادَّ
   **دالّةً لا رقمًا**. وأخذُ رقمٍ مكانَ الدالّة **مردودٌ** — لأنّ الرقمَ متى
   سُلِّم فقد **حُسِب قبل البروتوكول**، فلا يُعلَم أسبقَه أم تأخّر عنه. وبأخذِ
   الدالّةِ يُثبَّت الموقعُ ويُشتَقُّ الشرطُ **ثمّ** يُستدعى العادّ: فالترتيبُ
   مضمونٌ بالبناء لا بحُسن الظنّ.

④ **منعُ الترقية.** `DeclaredFigure` يَرُدُّ عددًا بلا إعلانِ حال، ويَرُدُّ
   عددًا يُكتَب «مرخَّصًا» ونصفٌ من شرطه موقوف. فلا يترقّى المعلَّقُ إلى
   المُرخَّصِ بالسكوت.

§١ الإلزامُ على الإجراء لا على المادّة
──────────────────────────────────────
وهذا موضعُ الدقّة. شرطُ الإمكان ههنا **غيرُ مستوفًى بالبناء**: الأرقامُ
الأعجميّةُ ليست في شجرتنا ولا تُقاس عليها، ولن تُستوفى بحال. فلو أُلزِم
البروتوكولُ بـ**استيفاء** الشرط لامتنع العدُّ رأسًا ولم يُقَل شيء.

فالإلزامُ على **الإجراء**: لا يُعَدُّ إلا من خلاله. والعددُ يخرج **معلَّقًا
بأسماء أنصافه الموقوفة** لا ممنوعًا ولا مُرخَّصًا. وهذا مُسمًّى صراحةً في
`A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION` حتى لا يُقرأ الإلزامُ إجازةً.

    >>> measure_under_the_protocol("جذورُ معجم Xerox", lambda: 4930).standing
    'معلَّقٌ بموقوفٍ مسمّى'

§٢ ما لا يفعله
───────────────
لا يُصحِّح رقمًا، ولا يَحكم بصدقِ ورقةٍ، ولا يُسعِّر شيئًا. إنّما يَضمن أنّ
كلَّ رقمٍ يَعبُر قد عَبَر **من بابٍ واحدٍ معلومٍ قبل أن يُكتَب**.

المخارج: 0 قائم · 2 سوءُ استعمال · 3 الموقعُ غائب · 4 الموقعُ خالف ختمَه.
"""

from __future__ import annotations

import hashlib
import os

E_USAGE, E_SITE_MISSING, E_SITE_ALTERED = 2, 3, 4

ROOT = os.path.dirname(os.path.abspath(__file__))

# ── الحالُ الثلاثة — ولا رابعَ، ولا ترقّيَ بينها بالسكوت ──────────────────────
LICENSED = "مرخَّصٌ بشرطٍ مستوفًى"
CONDITIONAL = "معلَّقٌ بموقوفٍ مسمّى"
REFUSED = "مردودٌ بلا إجراء"

#: الإلزامُ على الإجراء لا على المادّة — يُقرَأ قبل أن يُظَنَّ الإلزامُ إجازةً.
A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION = (
    "إلزامُ البروتوكولِ يَضمن أنّ العدَّ جرى من خلاله، **ولا يَضمن أنّ شرطَ "
    "الإمكان استُوفي**. والأرقامُ الأعجميّةُ شرطُها غيرُ مستوفًى بالبناء: "
    "ليست في شجرتنا ولا تُقاس عليها. فمن قرأ «مرَّ بالبروتوكول» فظنّها "
    "«مختومةً عندنا» فقد قلبَ الإلزامَ إجازةً — وهو عينُ ما يمنعه هذا النصّ."
)


class ProtocolError(Exception):
    """صريخُ البروتوكول — بمخرجٍ معلنٍ لا برسالةٍ وحدَها."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code, self.message = code, message


# ── ① الموقعُ المحفوظ — يُشتَقُّ من القرص عند كلِّ قراءةٍ ولا يُفترَض ──────────
def _digest(path):
    """بصمةُ المادّة وطولُها **من القرص** — فلا قيمةَ محفوظةٌ في الذاكرة تُصدَّق."""
    with open(path, "rb") as fh:
        raw = fh.read()
    return len(raw), hashlib.sha256(raw).hexdigest()


#: دالّةُ التأسيس ههنا نصُّ التسجيل المسبق في وثيقة الباب: ما أُعلن **قبل**
#: أن يُقاس. وهي مادّةٌ على القرص لها طولٌ وبصمة — لا فقرةٌ في ذاكرةٍ تُدَّعى.
FOUNDING_SITE_PATH = os.path.join(ROOT, "NISAB-AJAMI-PRE.md")


def founding_site():
    """الموقعُ مقروءًا الآن: مسارُه وطولُه وبصمتُه — ثلاثتُها من القرص.

    ولِمَ تُشتَقُّ كلَّ مرّة؟ لأنّ قيمةً تُقرأ مرّةً ثمّ تُحفَظ تُصبح **دعوى**
    عن الماضي؛ والمطلوبُ شهادةٌ عن الحاضر.
    """
    if not os.path.exists(FOUNDING_SITE_PATH):
        raise ProtocolError(E_SITE_MISSING,
                            f"موقعُ التأسيس غائب: {FOUNDING_SITE_PATH}")
    length, sha = _digest(FOUNDING_SITE_PATH)
    return dict(مسار=os.path.relpath(FOUNDING_SITE_PATH, ROOT),
                طول=length, بصمة=sha)


#: ختمُ الموقع، مكتوبٌ ههنا ليُصادَم. وهو مكتوبٌ في `induction/seals.py` أيضًا
#: — فتحريرُ دالّة التأسيس يُبلَّغ في موضعين، وهذا عبءُ صيانةٍ **مقصود**:
#: ختمٌ في موضعٍ واحدٍ يُحرَّر مع مادّته في إيداعٍ واحدٍ فلا يَشهد بشيء.
FOUNDING_SITE_SHA256 = "23d774e266851730435ca705e3be2f8214cd73f108f8e17d6af3f9d91ca25c2c"
FOUNDING_SITE_BYTES = 3535


def require_the_protocol():
    """② الحارس — يُستدعى عند الاستيراد، فلا يُؤجَّل إلى استعمالٍ قد لا يقع."""
    site = founding_site()
    if site["بصمة"] != FOUNDING_SITE_SHA256 or site["طول"] != FOUNDING_SITE_BYTES:
        raise ProtocolError(
            E_SITE_ALTERED,
            f"موقعُ التأسيس خالف ختمَه: {site['بصمة'][:16]}… ⟷ "
            f"{FOUNDING_SITE_SHA256[:16]}… (طولٌ {site['طول']} ⟷ "
            f"{FOUNDING_SITE_BYTES}) — أعِد الختمَ في موضعيه أو رُدَّ التحرير")
    return site


# ── ④ منعُ الترقية — العددُ لا يُكتَب إلا بحالِه وأنصافِه الموقوفة ────────────
class DeclaredFigure:
    """عددٌ **لا يُفارِق حالَه**: قيمةٌ وحالٌ وأنصافٌ موقوفةٌ مسمّاة.

    ولِمَ صنفٌ لا مجرّدُ رقم؟ لأنّ الرقمَ المجرّدَ يُنسَخ إلى جدولٍ فيَسقط عنه
    حالُه في الطريق، فيُقرأ مُرخَّصًا وهو معلَّق. فالحالُ ههنا **ملازمٌ للقيمة
    في الصنف نفسِه**، ولا يُنتزَع منه إلا بقصدٍ ظاهر.
    """

    __slots__ = ("value", "standing", "unmet_halves", "note")

    def __init__(self, value, standing, unmet_halves=(), note=""):
        if standing not in (LICENSED, CONDITIONAL, REFUSED):
            raise ProtocolError(E_USAGE, f"حالٌ غيرُ معلن: {standing!r}")
        unmet = tuple(unmet_halves)
        # منعُ الترقية: «مرخَّصٌ» ونصفٌ موقوفٌ قائمٌ — تناقضٌ يُرَدّ لا يُسكَت عنه.
        if standing == LICENSED and unmet:
            raise ProtocolError(
                E_USAGE, "عددٌ يُكتَب «مرخَّصًا» وله نصفٌ موقوفٌ مسمًّى — "
                         f"منعُ الترقية: {unmet}")
        if standing == CONDITIONAL and not unmet:
            raise ProtocolError(
                E_USAGE, "عددٌ «معلَّقٌ» بلا نصفٍ موقوفٍ مسمًّى — "
                         "التعليقُ بلا اسمٍ كتمانٌ لا إعلان")
        self.value, self.standing = value, standing
        self.unmet_halves, self.note = unmet, note

    @property
    def is_licensed(self):
        return self.standing == LICENSED and not self.unmet_halves

    def as_row(self):
        return dict(قيمة=self.value, حال=self.standing,
                    أنصافٌ_موقوفة=list(self.unmet_halves),
                    مرخَّص=self.is_licensed, بيان=self.note)

    def __repr__(self):
        return (f"DeclaredFigure(value={self.value!r}, standing={self.standing!r}, "
                f"unmet_halves={self.unmet_halves!r}, is_licensed={self.is_licensed})")


# ── ③ الأسبقيّةُ بنيويّة — العادُّ **دالّةٌ**، والرقمُ المُسلَّم مردود ────────
#: ما لا يُقبَل عادًّا: رقمٌ سُلِّم، أو نصٌّ، أو قائمةٌ — كلُّها محسوبةٌ سلفًا.
PRECOMPUTED = (int, float, complex, str, bytes, bool, list, tuple, dict, set)


def measure_under_the_protocol(name, measurer, unmet_halves=None, note=""):
    """العدُّ **من خلال** البروتوكول — والترتيبُ مضمونٌ بالبناء.

    `measurer` **دالّةٌ** بلا وسائط. ولو قُبِل مكانَها رقمٌ لكان قد حُسِب قبل أن
    يُثبَّت الموقعُ ويُشتَقَّ الشرط، فلا يُعلَم أسبقَ البروتوكولَ أم تأخّر عنه —
    وهذا عينُ ما يُراد منعُه. فالرقمُ المُسلَّم **مردودٌ بمخرج 2**.

    والترتيبُ ههنا مقروءٌ في الأسطر: يُثبَّت الموقعُ ⟵ تُشتَقُّ الأنصافُ
    الموقوفة ⟵ **ثمّ** يُستدعى العادّ. فمن قلبَ السطرَين سقطَ الاختبارُ ⑥.
    """
    if isinstance(measurer, PRECOMPUTED):
        raise ProtocolError(
            E_USAGE,
            f"«{name}»: سُلِّم رقمٌ مكانَ الدالّة — والرقمُ المُسلَّمُ محسوبٌ "
            "قبل البروتوكول، فلا تُعلَم أسبقيّتُه. مرِّر دالّةً بلا وسائط")
    if not callable(measurer):
        raise ProtocolError(E_USAGE, f"«{name}»: العادُّ ليس دالّةً")

    require_the_protocol()                      # ① الموقعُ أوّلًا — قبلَ كلِّ عدّ
    unmet = tuple(unmet_halves or ())           # ② ثمّ الشرطُ يُشتَقُّ ويُسمّى
    value = measurer()                          # ③ ثمّ — وثمّ فقط — يُستدعى العادّ

    standing = CONDITIONAL if unmet else LICENSED
    return DeclaredFigure(value, standing, unmet, note)


# ── بنودُ البروتوكول — خمسةٌ مُلزِمةٌ وسادسٌ شاهدٌ يُقرأ ولا يُجمَّد ───────────
def clauses():
    """بنودُ البروتوكول مقروءةً الآن — الخامسُ منها شاهدٌ لا يُجمَّد عددُه."""
    site = founding_site()
    return [
        dict(بند="الموقع", مُلزِم=True,
             نصّ="موقعُ التأسيس مادّةٌ على القرص بطولٍ وبصمةٍ تُشتَقّ كلَّ مرّة",
             شاهد=f"{site['مسار']} · {site['طول']} بايتًا · {site['بصمة'][:16]}…"),
        dict(بند="الأسبقيّة", مُلزِم=True,
             نصّ="العادُّ دالّةٌ لا رقم — فالترتيبُ بنيويٌّ لا موعود",
             شاهد="measure_under_the_protocol يَرُدُّ كلَّ صنفٍ محسوبٍ سلفًا"),
        dict(بند="الإعلان", مُلزِم=True,
             نصّ="لا عددَ بلا حالٍ مُعلَن من ثلاثةٍ لا رابعَ لها",
             شاهد=f"{LICENSED} · {CONDITIONAL} · {REFUSED}"),
        dict(بند="التسمية", مُلزِم=True,
             نصّ="المعلَّقُ يُسمّي أنصافَه الموقوفة — والتعليقُ بلا اسمٍ كتمان",
             شاهد="DeclaredFigure يَرُدُّ معلَّقًا بلا نصفٍ مسمًّى"),
        dict(بند="منعُ الترقية", مُلزِم=True,
             نصّ="لا يُكتَب «مرخَّصًا» وله نصفٌ موقوفٌ قائم",
             شاهد="DeclaredFigure يَرُدُّ الجمعَ بين الترخيصِ والوقف"),
        dict(بند="المستوردون", مُلزِم=False,
             نصّ="**شاهدٌ لا يُجمَّد**: من يستورد البروتوكولَ يُقرَأ من الشجرة "
                 "ولا يُكتَب عددُه ختمًا — فالعددُ ينمو بنموِّ الشجرة",
             شاهد=f"{len(importers())} ملفًّا يستورده"),
    ]


def importers():
    """من يستورد البروتوكول — يُقرأ من الشجرة الآن، ولا يُجمَّد عددُه ختمًا."""
    found = []
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".py") or name == os.path.basename(__file__):
            continue
        try:
            with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
                if "nisab_protocol" in fh.read():
                    found.append(name)
        except (OSError, UnicodeDecodeError):
            continue
    return found


# ② الحارسُ يَنفُذ عند الاستيراد — لا عند أوّل استعمالٍ قد لا يقع البتّة.
require_the_protocol()


if __name__ == "__main__":
    import json
    import sys

    site = require_the_protocol()
    print("بروتوكولُ ما قبلَ العدّ — قائمٌ ومُلزِم\n")
    print(f"  الموقع: {site['مسار']} · {site['طول']} بايتًا · {site['بصمة'][:16]}…\n")
    for c in clauses():
        print(f"  [{'مُلزِم' if c['مُلزِم'] else 'شاهد '}] {c['بند']}: {c['نصّ']}")
        print(f"            ⟵ {c['شاهد']}")
    print(f"\n{A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION}")
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(dict(موقعُ_التأسيس=site, بنود=clauses()), fh,
                      ensure_ascii=False, indent=2, sort_keys=True)
        print(f"\nJSON ⟵ {out}")
    sys.exit(0)
