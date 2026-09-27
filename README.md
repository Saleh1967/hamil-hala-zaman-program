# hamil-hala-zaman-program
برنامجُ حامل/حالة/زمان — سلسلةُ الجدل كاملةً: تسعُ وثائقَ مرتّبةٍ بترتيب الجدل، وسجلُّ أجناس الخطأ العشرة، والمحرّكُ الجبري (algebra_engine.py). كلُّ رقمٍ فيها إمّا معدودٌ معروضٌ أو مقدّمةٌ معلنة.

## التشغيل

```bash
bash fetch_corpus.sh                       # يجلب المجمَّد ويتحقق من بصمته sha256 قبل أيّ عدّ
python algebra_engine.py --json=baselines/results-measured.json --require-corpus
```

- `fetch_corpus.sh` يُنزِّل نصّ Tanzil المشكول (`quran-simple-enhanced.txt`) إلى `mujammad.txt` — وهو ملفٌّ لا يُودَع في المستودع. البصمة تُقرأ من `algebra_engine.py` نفسه، وأيُّ ملفٍّ يخالفها **يُرفَض** ولا يُقاس عليه. لمرآةٍ أخرى: `CORPUS_URL=<رابط> bash fetch_corpus.sh`، ولمسارٍ آخر: `CORPUS_PATH=<مسار>`.
- `--require-corpus`: غيابُ المجمَّد **خروجٌ بخطأ** لا قياسٌ صامتٌ مؤجَّل.
- `--json=PATH`: إيداعُ الأعداد المعروضة ملفًّا (يُنشأ مجلّده إن غاب): الأعدادُ البنيويّة دائمًا، والمقيسةُ (§١٧–§٢٤) حين يحضر المجمَّد بالبصمة.
- المتطلّب الوحيد: `numpy`.
- `fetch_uthmani.sh` يجلب **النسخة العثمانية** (`quran-uthmani.txt`) إلى `uthmani.txt` — المقام الثاني لطبقة حدود الجملة (المرحلة ٢). بايتاتُها مودَعةٌ بختمها (`UTHMANI.md`)، والبصمةُ تُقرأ من `waqf_layer.py` نفسه.
- `python waqf_layer.py --json waqf_v0.json`: المقارنةُ المقيسة لمقترحات حدّ الجملة الثلاثة، وطبقةُ الوقف بمواضعها، والمواءمةُ بين المقامين، والتصادم — `PHASE2-STATUS.md`.
