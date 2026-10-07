# rukhsa/run_all.py — مُشغِّلُ بيتِ الترخيص: يجمع الشهاداتِ الثلاثَ ويودعها، ولا يقيس بنفسه
# رقمًا واحدًا.
#
# والاستقلالُ محفوظٌ كما في `burhan/`: الشهاداتُ تُشغَّل **عمليّاتٍ منفصلة** لا تُستورَد،
# ولا تستورد شجرةَ المشروع (تقرأ بايتاتِها بمواضعها: `git ls-files` · `LICENSE` ·
# `sources_manifest.tsv` · كائناتُ التاريخ). وما يفعله المُشغِّلُ زيادةً على الجمع شيئان:
#   ① مصادمةُ الثوابت المكرَّرة بـ`ast` عبر الملفّات — فثمنُ الاستقلال تكرارٌ، وثمنُ
#      التكرار انزياحٌ صامت؛ فيُقتَل بالمصادمة لا بالرجاء.
#   ② ختمُ البيت: `SHA256SUMS.txt` يُولَّد ويُتحقَّق منه بـ`--check`، ويستثني نفسَه.
#
# وهذه الوديعةُ **تسقط من لحظتها** متى دخل الشجرةَ ملفٌّ لا يصنّفه سطرُ الترخيص: ذلك
# شرطُها لا عطبُها — رقمٌ لا يشيخ صادقَ الظاهر كاذبَ المقدار (`CONTRIBUTING.md` §١).
import argparse, ast, hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SUMS = os.path.join(HERE, "SHA256SUMS.txt")
DEPOSIT = os.path.join(HERE, "rukhsa_v0.json")
DOC = os.path.join(HERE, "JABR-RUKHSA.md")

CERTS = [
    ("CERT-JABR", ["cert_jabr.py"]),
    ("CERT-SIJILL", ["cert_sijill.py"]),
    ("CERT-HAWIYAT", ["cert_hawiyat.py"]),
]

SHARED = ("BOT", "SUS", "TOP", "ORDER", "MIT_EXT", "CC_EXT", "CONTAINER_EXT",
          "REGISTRY", "ORIGIN_VERDICT")


def literals(path):
    """قيمُ الثوابت المُعلَنة — بـ`ast` لا بمشطِ البايتات.

    وتُحَلُّ **الأسماءُ** المُعرَّفةُ قبلها في الملفّ نفسِه، وإلّا لأفلتَ
    `ORDER = [BOT, SUS, TOP]` و`ORIGIN_VERDICT = {…: BOT}` من المصادمة لأنّهما
    ليسا حرفيَّين — وهما بعينُهما بابُ الانزياح الصامت الذي بُني المُشغِّلُ ليقتله.
    """
    tree = ast.parse(open(path, encoding="utf-8").read(), os.path.basename(path))
    wrap = {"list": list, "set": set, "tuple": tuple, "frozenset": frozenset}

    def value_of(node, env):
        if isinstance(node, ast.Name):
            if node.id not in env:
                raise ValueError(f"اسمٌ غيرُ معرَّف: {node.id}")
            return env[node.id]
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            items = [value_of(e, env) for e in node.elts]
            return items if isinstance(node, ast.List) else (
                tuple(items) if isinstance(node, ast.Tuple) else set(items))
        if isinstance(node, ast.Dict):
            return {value_of(k, env): value_of(v, env)
                    for k, v in zip(node.keys, node.values)}
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in wrap and len(node.args) == 1:
            return wrap[node.func.id](value_of(node.args[0], env))
        raise ValueError("ليس قيمةً تُحَلّ")

    env, out = {}, {}
    for node in tree.body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            continue
        name = node.targets[0].id
        try:
            value = value_of(node.value, env)
        except ValueError:
            continue
        env[name] = value
        if name in SHARED:
            out[name] = value
    return out


def canonical(value):
    if isinstance(value, dict):
        return ("dict",) + tuple(sorted((str(k), str(v)) for k, v in value.items()))
    if isinstance(value, (set, frozenset)):
        return ("set",) + tuple(sorted(str(v) for v in value))
    if isinstance(value, (list, tuple)):
        return ("seq",) + tuple(canonical(v) for v in value)
    return value


def collide_constants():
    """انزياحُ نسخةٍ عن أختها صريخٌ — بالقيمة في صورتها الواحدة لا بتشابه الاسم."""
    seen, problems = {}, []
    for fname in sorted(os.listdir(HERE)):
        if not fname.startswith("cert_") or not fname.endswith(".py"):
            continue
        for name, value in literals(os.path.join(HERE, fname)).items():
            key = canonical(value)
            if name in seen and seen[name][1] != key:
                problems.append(f"الثابتُ «{name}» انزاح بين {seen[name][0]} و{fname}")
            seen.setdefault(name, (fname, key))
    return problems, sorted(seen)


HEAD = """<!-- وثيقةٌ مولَّدة. لا تُحرَّر بيدٍ: كلُّ رقمٍ فيها مقروءٌ من `rukhsa_v0.json`،
     وتُعاد كتابتُها بـ`python rukhsa/run_all.py`، ويصادمها CI بنسختها المودَعة. -->

# جبرُ الترخيص — ثلاثةُ أحكامٍ لا اثنان

`LICENSE` يقول ما يَمنح، و`RUKHSA.md` يَعُدُّ ما في الشجرة، وهذا البيتُ يجيب عن
السؤال الذي لا يجيب عنه عدٌّ ولا نثر: **ما حكمُ ما لم يُقَس؟**

فالثنائيّةُ («مباحٌ أو ممنوع») تُجبِر المرءَ على أن يقرأ الجهلَ حكمًا: فإمّا قال
«لم أفحص فهو مباح» فادّعى إذنًا لم يُمنَح، وإمّا قال «فهو ممنوع» فحكمَ على غائبٍ
بغير قياس. والحاملُ ههنا **ثلاثيٌّ** (`CONTRIBUTING.md` §١ — المحجورُ T₃):

> `⊥` مُثبَتُ المنع · `⊘` محجورٌ لم يُقَس · `⊤` مُثبَتُ الإذن

وثلاثُ شهاداتٍ مستقلّةٍ تُشغَّل عمليّاتٍ منفصلة: الأولى تُبرهن أحكامَ هذا الجبر
**بالاستقصاء**، والثانيةُ تُعامل الرخصةَ معاملةَ **قاعدة بيانات** (علاقةٌ بمفتاحٍ
وقيودِ سلامة)، والثالثةُ تَزِن قرارَ الحاويات **بقياسٍ مضادٍّ للواقع**."""

METHOD = """## المنهجُ الذي يُحاكَم به

بنودُ `burhan/THE-PROOF.md` السبعةُ بأعيانها: ① الأساسُ يُعلَن قبل العدد ·
② المتوقَّعُ يُسجَّل قبل التشغيل في بايتات الشهادة · ③ القيدُ الساقطُ يُثبَّت بعدده ·
④ ما لم يُعلَن متوقَّعُه يبقى معلَّقًا · ⑤ كلُّ حارسٍ يَعُدُّ غيرَ الصفر في صورةٍ
مكذِّبة · ⑥ القيدُ يُحَلّ ولا يُختار · ⑦ العطبُ يُقاس مداه."""


def h(n):
    return f"{n:,}" if isinstance(n, int) else str(n)


def write_doc(deposit):
    D = deposit["جبر_الرخصة_v0"]
    J = D["شهادات"]["CERT-JABR"]
    S = D["شهادات"]["CERT-SIJILL"]
    W = D["شهادات"]["CERT-HAWIYAT"]
    L = [HEAD, "", METHOD, "", "## ① الشهاداتُ الثلاث", "",
         "| الشهادة | الأساس | الحكم | مآخذ |", "|---|---|---|---|"]
    for name, cert in D["شهادات"].items():
        L.append(f"| `{name}` | {cert['الأساس']} | {cert['حكم']} | {len(cert['مآخذ'])} |")
    L += ["", f"**{D['مقيس']['شهاداتٌ_خضراء']}/{D['مقيس']['شهادات']}** خضراء · "
          f"**{len(D['ثوابتُ_مُصادَمةٌ_عبر_الملفّات'])}** ثابتًا مُصادَمًا عبر الملفّات.", ""]

    jm = J["مقيس"]
    L += ["## ② الجبرُ — مُستقصًى لا مُستنبَطٌ بمثال", "",
          f"الحاملُ `{' < '.join(J['الحامل'])}`، و⊗ أصغرُ الرتبتين و⊕ أكبرُهما — "
          "مشتقَّين من الترتيب المُعلَن لا مكتوبَين جدولًا بيد.", "",
          "| البند | العدد |", "|---|---|",
          f"| أحكامُ الشبكة المُستقصاة بلا مخالفة | {len(J['أحكامٌ_مُستقصاةٌ_بلا_مخالفة'])} |",
          f"| ثلاثيّاتٌ مُشِّطت | {h(jm['ثلاثيّات'])} |",
          f"| شواهدُ قانون الحجر | {h(jm['شواهدُ_قانونِ_الحجر'])} |",
          f"| ثلاثيّاتٌ يُبدِّل طيُّ الحجر **دعواها** | {h(jm['ثلاثيّاتٌ_يُبدِّلها_طيُّ_الحجر'])} |",
          f"| استكمالاتُ المحجور المُشِّطة | {h(jm['استكمالات'])} |",
          f"| منها تُكذِّبُ العملَ المتحفِّظ | {h(jm['استكمالاتٌ_تُكذِّبُ_المتحفِّظ'])} |",
          f"| ومنها تُكذِّبُ السياسةَ المتفائلة | {h(jm['استكمالاتٌ_تُكذِّبُ_المتفائل'])} |", "",
          "فمنه ثلاثةُ أحكامٍ مُبرهَنةٍ بالعدّ: **المحجورُ لا يُفتي** (حزمةٌ فيها ⊘ ولا ⊥ "
          "تُساوي ⊘ لا ⊤) · **ولا يُعَدُّ علينا** (طيُّ ⊘ إلى ⊥ يُبدِّل الدعوى ولا يُبدِّل "
          "العملَ في صورةٍ واحدة) · **والعملُ ثابتٌ تحت كلِّ تأويل** (لا استكمالَ واحدٌ "
          "يُكذِّب المتحفِّظ). وهذا جوابُ «مرايا Zenodo لم تُفحَص» مقيسًا: فحصُها لاحقًا — "
          "في أيِّ الاتجاهين كان — لا يَنقُض عملًا قائمًا ولا يَمنح إذنًا جديدًا لعملٍ لم يُعمَل.", ""]
    dropped = J["قيدٌ_سقط_فثُبِّت_بعدده"]
    L += [f"> **قيدٌ سقط فثُبِّت بعدده** (البند ③): سُجِّل متوقَّعُ "
          f"«{dropped['البند']}» أوّلًا **{dropped['المسجَّلُ_أوّلًا']}** فكذّبه التشغيلُ "
          f"بـ**{dropped['المقيس']}** — {dropped['العلّة']}.", ""]

    sm = S["مقيس"]
    L += ["## ③ السجلُّ — الرخصةُ جدولٌ بقيود", "",
          "| البند | العدد |", "|---|---|",
          f"| ملفّاتُ الشجرة | {h(sm['ملفّاتُ الشجرة'])} |",
          f"| ممنوحٌ بنصِّ الرخصة (`{'` · `'.join(('*.py','*.sh','*.yml','*.md','*.json','*.tsv'))}`) | {h(sm['ممنوحٌ بنصِّ الرخصة'])} |",
          f"| حاوياتٌ في الرأس | {h(sm['حاوياتٌ في الرأس'])} |",
          f"| خارجَ صنفَي المنحة | {h(sm['خارجَ صنفَي المنحة'])} |",
          f"| حاوياتٌ مخرَجةٌ مقيسةٌ من التاريخ | {h(sm['حاوياتٌ مخرَجةٌ مقيسةٌ من التاريخ'])} |",
          f"| صفوفُ العلاقة | {h(sm['صفوفُ العلاقة'])} |",
          f"| دعاوى محجورةٌ خارجَ الصندوق | {h(sm['دعاوى محجورةٌ خارجَ الصندوق'])} |",
          f"| بايتاتُ طرفٍ ثالثٍ في الرأس | {h(sm['بايتاتُ طرفٍ ثالثٍ في الرأس'])} |",
          f"| بايتاتُ حاوياتٍ خرجت إلى التاريخ | {h(sm['بايتاتُ حاوياتٍ خرجت إلى التاريخ'])} |", "",
          f"والقسمةُ تنغلق **جمعًا لا طرحًا**: {h(sm['ممنوحٌ بنصِّ الرخصة'])} + "
          f"{h(sm['حاوياتٌ في الرأس'])} + {h(sm['خارجَ صنفَي المنحة'])} = "
          f"{h(sm['ملفّاتُ الشجرة'])}. فلا ملفَّ يسقط في فرق، ولا سكوتَ يُقرَأ إذنًا.", "",
          f"و**{len(S['قيودُ_السلامة'])}** قيدَ سلامةٍ تُفحَص على الصفوف، صفرُ مخالفاتٍ "
          "في كلٍّ منها: مفتاحٌ أوّليٌّ لا يتكرّر · حكمٌ لا يخرج عن الحامل · صفٌّ لا يخلو "
          "من شاهد · إذنٌ لا يُدَّعى بلا نصٍّ في `LICENSE` · ملفٌّ خارجَ صنفَي المنحة لا "
          "يدخل الشجرةَ بلا سطرِ نسبةٍ · وثيقةُ نسبةٍ لا تُذكَر وهي غائبةٌ عن الشجرة · "
          "ولا وحدةَ شبكةٍ في الشهادة نفسِها.", "",
          "| الحزمة | صفوف | الحكم | بايتات |", "|---|---|---|---|"]
    for name, b in S["حزم"].items():
        size = h(b["بايتات"]) if b["بايتاتٌ مقيسة"] else "غيرُ مقيسة"
        L.append(f"| {name} | {b['صفوف']} | `{b['طيُّ_الشبكة']}` | {size} |")
    L += ["", "وكلُّ حزمةٍ محسوبةٌ بطريقين لا يلتقيان إلا على الصواب: **طيُّ الشبكة** "
          "(⊗ على الأحكام) و**جمعُ العلاقة** (عدُّ صفوفِ كلِّ حكم) — واختلافُهما صريخ.", "",
          "> وحَجرُ الدعاوى الثلاثِ الخارجيّة **بنيويٌّ لا عارض**: الشهادةُ لا تستورد "
          "وحدةَ شبكةٍ البتّة، ويُفحَص ذلك بـ`ast` في بايتاتها نفسِها. فقولُنا «لم "
          "تُفحَص» خاصّةُ الآلة لا عُذرُ المشغِّل — ودعوى «CC BY 4.0» الشائعةُ على نصوص "
          "OpenITI مسجّلةٌ ههنا صفًّا محجورًا: لا تُصدَّق ولا تُكذَّب، ولا يُبنى عليها عمل.", ""]

    wm = W["مقيس"]
    road = W["الطريقُ_إلى_⊤"]
    L += ["## ④ الحاويات — قرارُ مالكٍ **نُفِّذ** على فاتورةٍ معدودة", "",
          f"الحاوياتُ الثلاثُ أُخرِجت من رأس الشجرة بصكٍّ موقَّعٍ على بايتاتها: "
          f"المالكُ **{W['صكُّ_الإخراج']['المالك']}**، "
          f"بتاريخ **{W['صكُّ_الإخراج']['التاريخ']}**، ونصُّ الإذن منقولٌ بحرفه: "
          f"«{W['صكُّ_الإخراج']['نصُّ_الإذن']}». وحدُّه معلنٌ: "
          f"{W['صكُّ_الإخراج']['حدُّ_الإذن']}", "",
          "| البند | العدد |", "|---|---|"]
    for name, value in W["صكُّ_الإخراج"]["خانات"].items():
        L.append(f"| {name} | {h(value)} |")
    L += ["", "والتوقيعُ **على البايتات لا على الأسماء**: كلُّ حاويةٍ مقيَّدةٌ في الصكِّ "
          "بختمها الثلاثيِّ (بصمةُ كائن git · الطول · sha256)، فلو بُدِّلت بايتاتُ ملفٍّ "
          "تحت اسمِه المأذونِ فيه سقط الإذنُ عنه. ولا بايتةَ حُذفت حتى قُرِئت من "
          "التاريخ وصُودِم ختمُها — **فالإخراجُ نقلٌ إلى التاريخ لا إعدام**.", "",
          "| الشجرة | ملفّات | حكمُها |", "|---|---|---|",
          f"| T — اليومَ، بعد الإخراج | {h(wm['ملفّاتُ الشجرة'])} | `{wm['حكمُ الشجرة اليوم']}` |",
          f"| T⁺ — لو عادت الحاوياتُ الثلاث | "
          f"{h(wm['ملفّاتُ الشجرة'] + wm['حاوياتٌ في الصكّ'])} | "
          f"`{wm['حكمُ الشجرة لو عادت الحاويات']}` |",
          f"| T″ — بلا كلِّ ما لا يملكه المشروع | "
          f"{h(wm['ملفّاتُ الشجرة'] - wm['ملفّاتٌ لا يملكها المشروع'])} | "
          f"`{wm['حكمُ الشجرة بعد خروج كلِّ ما لا يُملَك']}` |", "",
          f"وأحكامُ **{h(wm['أحكامٌ صُودِمت بين الشجرتين'])}** ملفًّا صُودِمت بين T وT⁺ صفًّا "
          f"إلى صفّ: تبدّل منها **{wm['أحكامٌ تبدّلت بخروج الحاويات']}**. فخروجُ الحاويات "
          "لم يمسّ حكمَ ملفٍّ واحدٍ من الباقي، ولم يبلغ بالشجرة `⊤` — وهذا هو الفارقُ "
          "الذي كان مظنونًا فصار **مقيسًا بعد وقوعه**: الصكُّ لم يَشترِ حكمًا، وإنّما "
          "أخرج بايتاتٍ لا يملكها المشروعُ من رأسه.", "",
          f"والطريقُ إلى `⊤` مقيسٌ بشِقَّيه: حذفُ ما لا يُملَك "
          f"(**{road['حذفُ ما لا يُملَك']['ملفّات']}** ملفًّا · "
          f"**{h(road['حذفُ ما لا يُملَك']['بايتات'])}** بايتًا) **و**تسميةُ ما سكتت عنه "
          f"المنحةُ (**{road['تسميةُ المسكوتِ عنه في نصّ المنحة']['ملفّات']}** ملفّات: "
          + " · ".join(f"`{p}`" for p in road["تسميةُ المسكوتِ عنه في نصّ المنحة"]["أسماء"])
          + ") — ولا يبلغه أحدُهما وحدَه.", "",
          f"وبصماتُ الحاويات لم تنكسر بخروجها: طريقُ `self` في `fetch_source.sh` يقرأ "
          f"بايتاتِها من إيداعٍ مثبَّتٍ في التاريخ لا من شجرة العمل — "
          f"**{W['استردادُ_طريقِ_self']['كائناتٌ حاضرة']}/"
          f"{W['استردادُ_طريقِ_self']['سطور']}** كائنًا حاضرًا، "
          f"**{W['استردادُ_طريقِ_self']['بصماتٌ طابقت البيان']}** بصمةً طابقت البيان. "
          "والقيدُ المقابلُ معلنٌ لا مطويّ: استنساخٌ ضحلٌ لا يحمل التاريخَ فلا يحمل "
          "الكائن — ولذلك يُستنسَخ في CI بـ`fetch-depth: 0`.", "",
          f"> **فالخلاصةُ مقيسةٌ لا مُفتًى بها**: {W['خلاصةٌ_مقيسة']}.", ""]

    L += ["## ⑤ ما يُسقِط هذا البيت", "",
          "| الحادث | أيُّ حارسٍ يصرخ |", "|---|---|",
          "| ملفٌّ يدخل الشجرةَ لا يصنّفه سطرُ الترخيص ولا يسمّي السجلُّ نسبتَه | "
          "`CERT-SIJILL` — قيدُ «ملفٌّ خارجَ صنفَي المنحة بلا سطرٍ في السجلّ» |",
          "| وثيقةُ نسبةٍ تُذكَر في السجلّ وهي غائبةٌ عن الشجرة | "
          "`CERT-SIJILL` — قيدُ «وثيقةُ نسبةٍ غائبةٌ عن الشجرة» |",
          "| إذنٌ يُدَّعى على صنفٍ لا نصَّ له في `LICENSE` | "
          "`CERT-SIJILL` — قيدُ «إذنٌ بلا نصٍّ في LICENSE» |",
          "| وحدةُ شبكةٍ تدخل الشهادةَ فيصير الحجرُ عارضًا لا بنيويًّا | "
          "`CERT-SIJILL` — قيدُ «وحدةُ شبكةٍ في الشهادة» |",
          "| حاويةٌ تخرج من التاريخ فينكسر استردادُ بصمتها | "
          "`CERT-HAWIYAT` — كائنُ `self` الغائب |",
          "| حاويةٌ تعود إلى رأس الشجرة فيُنقَض الصكُّ صامتًا | "
          "`rukhsa/ikhraj.py --check` وسطرُ الترخيص |",
          "| ثابتٌ ينزاح بين شهادةٍ وأختها | المُشغِّل — مصادمةُ `ast` عبر الملفّات |",
          "| ملفٌّ في البيت بلا ختمٍ أو ختمٌ خُولِف | `SHA256SUMS.txt` بـ`--check` |", "",
          "```bash",
          "python rukhsa/run_all.py            # تشغيلٌ وكتابةُ الوديعة والوثيقة والختم",
          "python rukhsa/run_all.py --check    # تشغيلٌ وتحقُّقٌ من الختم بلا تجديد",
          "```", ""]

    open_debts = D["مفتوحات"]
    L += ["## ⑥ المفتوحاتُ — مسمّاةً لا مطويّة", ""]
    L += [f"- {d}" for d in open_debts] + [""]

    with open(DOC, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))


def write_sums():
    rows = []
    for base, _dirs, files in os.walk(HERE):
        for fn in sorted(files):
            if fn == os.path.basename(SUMS) or "__pycache__" in base:
                continue
            path = os.path.join(base, fn)
            rel = os.path.relpath(path, HERE)
            with open(path, "rb") as fh:
                rows.append(f"{hashlib.sha256(fh.read()).hexdigest()}  {rel}")
    rows.sort(key=lambda r: r.split("  ", 1)[1])
    with open(SUMS, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(rows) + "\n")
    return len(rows)


def check_sums():
    problems = []
    if not os.path.exists(SUMS):
        return ["لا ختمَ للبيت — SHA256SUMS.txt غائب"]
    declared = {}
    for ln in open(SUMS, encoding="utf-8"):
        if ln.strip():
            digest, rel = ln.rstrip("\n").split("  ", 1)
            declared[rel] = digest
    found = set()
    for base, _dirs, files in os.walk(HERE):
        for fn in files:
            if fn == os.path.basename(SUMS) or "__pycache__" in base:
                continue
            rel = os.path.relpath(os.path.join(base, fn), HERE)
            found.add(rel)
            with open(os.path.join(base, fn), "rb") as fh:
                got = hashlib.sha256(fh.read()).hexdigest()
            if rel not in declared:
                problems.append(f"ملفٌّ بلا ختم: {rel}")
            elif declared[rel] != got:
                problems.append(f"ختمٌ خُولِف: {rel}")
    for rel in sorted(set(declared) - found):
        problems.append(f"ختمٌ لملفٍّ غائب: {rel}")
    return problems


def main():
    ap = argparse.ArgumentParser(description="مُشغِّلُ بيتِ جبر الترخيص")
    ap.add_argument("--check", action="store_true", help="يتحقّق من الختم ولا يُجدِّده")
    ap.add_argument("--json", default=DEPOSIT)
    args = ap.parse_args()

    shifts, shared = collide_constants()
    for p in shifts:
        print(f"::error::{p}")

    results, fails = {}, list(shifts)
    for name, argv in CERTS:
        tmp = os.path.join(HERE, f".{name}.tmp.json")
        run = subprocess.run([sys.executable, os.path.join(HERE, argv[0])] + argv[1:]
                             + ["--json", tmp], cwd=HERE, capture_output=True, text=True)
        sys.stdout.write(run.stdout)
        if run.stderr.strip():
            sys.stdout.write(run.stderr)
        if run.returncode != 0:
            fails.append(f"{name}: سقطت")
        with open(tmp, encoding="utf-8") as fh:
            results[name] = json.load(fh)
        os.remove(tmp)

    S, W = results["CERT-SIJILL"], results["CERT-HAWIYAT"]
    silent = W["الطريقُ_إلى_⊤"]["تسميةُ المسكوتِ عنه في نصّ المنحة"]
    deposit = {
        "جبر_الرخصة_v0": {
            "الحامل": results["CERT-JABR"]["الحامل"],
            "شهادات": results,
            "ثوابتُ_مُصادَمةٌ_عبر_الملفّات": shared,
            "مقيس": {
                "شهاداتٌ_خضراء": sum(1 for r in results.values() if r["حكم"] == "خضراء"),
                "شهادات": len(results),
                "قيودُ_سلامةٍ_مفحوصة": len(S["قيودُ_السلامة"]),
                "صفوفُ_العلاقة": S["مقيس"]["صفوفُ العلاقة"],
                "دعاوى_محجورة": S["مقيس"]["دعاوى محجورةٌ خارجَ الصندوق"],
            },
            "مفتوحات": [
                "مرايا Zenodo لإصدارات OpenITI — محجورةٌ بالبناء (لا شبكةَ في هذا البيت). "
                "وفحصُها لاحقًا لا يَنقُض عملًا قائمًا ولا يَمنح إذنًا لعملٍ لم يُعمَل: "
                "ذلك مُبرهَنٌ بالاستقصاء في CERT-JABR لا موعودٌ به",
                "دعوى «CC BY 4.0» على نصوص OpenITI — صفٌّ محجورٌ في السجلّ: لم تُقَس "
                "فلا تُصدَّق ولا تُكذَّب",
                "**مقضيّ**: بقاءُ الحاويات الثلاث في الشجرة — كان قرارَ مالكٍ لا "
                "يقتضيه الجبرُ ولا يمنعه، فقضى المالكُ بإخراجها بصكٍّ موقَّعٍ على "
                "بايتاتها (`rukhsa/ikhraj.py`) ونُفِّذ، وفاتورتُه مقيسةٌ بعد وقوعها "
                "في CERT-HAWIYAT. والباقي منه قيدٌ لا دَين: الاستنساخُ الضحلُ لا "
                "يحمل كائناتِ التاريخ، فـ`fetch-depth: 0` شرطُ قراءتها",
                f"ما سكتت عنه المنحةُ ({silent['ملفّات']} ملفّاتٍ من إنشاء المشروع: "
                + " · ".join(silent["أسماء"]) + ") — محجورٌ حتى يُسمّى صنفُه في "
                "`LICENSE` بقرارِ مالك",
            ],
        }
    }
    with open(args.json, "w", encoding="utf-8") as fh:
        json.dump(deposit, fh, ensure_ascii=False, indent=1)

    write_doc(deposit)

    if args.check:
        fails.extend(check_sums())
        print(f"— ختمُ البيت: تحقُّقٌ من {os.path.basename(SUMS)} —")
    else:
        n = write_sums()
        print(f"— ختمُ البيت: {n} ملفًّا مختومًا في {os.path.basename(SUMS)} —")

    green = sum(1 for r in results.values() if r["حكم"] == "خضراء")
    print(f"— جبرُ الترخيص: {green}/{len(results)} شهادةً خضراء · "
          f"{len(shared)} ثابتًا مُصادَمًا عبر الملفّات —")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ البيتُ مغلق" if not fails else "    ✗ البيتُ مفتوح")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
