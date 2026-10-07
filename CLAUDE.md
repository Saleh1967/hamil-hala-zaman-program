# تعليماتٌ لكلّ وكيلٍ قبل الدخول — مستودع hamil (hamil-hala-zaman-program)

اقرأ هذا كلَّه قبل أيّ أمر. ما خالفه يُرفض بالاسم.

## القانون الواحد (يحكم الغانم وSLGE وhamil وAlgebra والدساتير الثلاثة؛ وTaaqol-GPT ليس منها)

**لا يدخل نصٌّ إلى أيّ مستودعٍ من هذه ولا يخرج منه إلّا من مدخلٍ واحد: بوّابةُ الغانم وبرهانُها.**

- المدخل: `gate.enter(bytes) → Certificate | Refusal` في `Saleh1967/Alghanem` (فرع `claude/official-gate`، حزمة `gate/`، البرهان `formal/a116`؛ بروتوكول A116-CANONICAL-TXT-1.1). الرفضُ مسمًّى ولا يُخمَّن شيء.
- المخرج: `gate.exit(cert) → bytes`. والترخيصُ الثلاثيُّ `gate.licence`، والاشتقاقُ والاسترجاعُ `gate.derive`/`gate.recover` مقيسان على مرجعٍ بشريٍّ محجوب.
- المستهلك: `slge.entry.from_atoms(cert.atoms)` في SLGE يحوّل ذرّاتِ الشهادة إلى خانات، ولا شيء غيره.

## حال هذا المستودع (نُفِّذ التعليقُ في 2026-10-07 — ADR ١ في `docs/adr/`)

فيه `algebra_engine.py` (يدخل من الـ116 بالترخيص التدريجي ويُخرج بتّاتٍ مفسَّرة) ومحرّكاتٌ وبوّاباتٌ وطبقاتٌ كثيرة تقرأ النصّ مباشرة؛ `parse_stream` فيه يسقط على 22% من الصور (مقيس)، وجداولُ `peel112/peel256` يدويّة. مدوّنتُه تخالف مدوّنةَ الغانم بالحجم (1,306,770 مقابل 1,319,901 بايت) — قرارُ المطابقة لصاحب المستودع.

كلُّ قارئٍ للنصّ أو كاتبٍ له أو مطبِّعٍ هنا **معلَّقٌ حكمًا** من 2026-10-05 حتى يُنقل فعليًّا إلى `suspended/` بسجلٍّ `SUSPENDED_REGISTRY.json` (سبب، تاريخ، شرطُ عودة) على طريقة الغانم وSLGE — نقلٌ لا حذف، والتاريخُ في git. وحتى يتمّ النقل: **لا يُشغَّل** شيءٌ ممّا يلي، ولا يُستشهد بخضرته، ولا يُبنى عليه:

- `alama_layer.py`
- `algebra_engine.py`
- `aqsam_gate.py`
- `awzan_engine.py`
- `burhan/cert_boundary.py`
- `burhan/cert_corpus.py`
- `burhan/cert_fingerprints.py`
- `burhan/cert_generations.py`
- `burhan/cert_inertness.py`
- `burhan/cert_normalize.py`
- `burhan/cert_partition.py`
- `burhan/cert_sukun.py`
- `burhan/run_all.py`
- `context_ladder.py`
- `contract_line.py`
- `dalalat_gate.py`
- `dall_gate.py`
- `dictionary_engine.py`
- `duyun_gate.py`
- `field112_laws.py`
- `harakat_layer.py`
- `i3lal_layer.py`
- `ihala_gate.py`
- `imla_layer.py`
- `induction/deposit_law.py`
- `induction/export_seals.py`
- `induction/hiyad.py`
- `induction/induction_engine.py`
- `induction/jami3_mani3.py`
- `induction/mirror.py`
- `induction/online_peel.py`
- `induction/seals.py`
- `induction/tensor_law.py`
- `isnad_layer.py`
- `jar_gate.py`
- `jumla_gate.py`
- `jumla_links.py`
- `mabna_gate.py`
- `madlul_gate.py`
- `manhaj_gate.py`
- `maqayis_layer.py`
- `masadir_gate.py`
- `mawsua_gate.py`
- `mihwar_gate.py`
- `mu3jam_gate.py`
- `nisab_gate.py`
- `niyaba_gate.py`
- `normalize.py`
- `pairs_engine.py`
- `qisma_gate.py`
- `rukhsa/cert_hawiyat.py`
- `rukhsa/cert_jabr.py`
- `rukhsa/cert_sijill.py`
- `rukhsa/ikhraj.py`
- `rukhsa/run_all.py`
- `rukhsa_check.py`
- `sarf_gate.py`
- `shakhsiyya_extract.py`
- `sigha_gate.py`
- `sources_census.py`
- `ta3allum_gate.py`
- `tamakkun_gate.py`
- `tarjih_gate.py`
- `tashkil_layer.py`
- `tawhid_gate.py`
- `tawlid_gate.py`
- `wad3_gate.py`
- `waqf_layer.py`
- `wasl_gate.py`
- `wazn_gate.py`

## ما لا تفعله

1. لا تشغّل محرّكًا من المحرّكات أعلاه ولا تستورده في عملٍ جديد؛ وإن احتجت خاناتٍ فمن شهادة الغانم.
2. لا تكتب `open`، `print`، `read_text`، `encode`، `decode`، `normalize`، `argv` في وحدةٍ جديدة؛ الحارسُ (على طريقة `gate.guard` في الغانم) سيُسقط البناء حين يُنصَّب هنا.
3. لا تُعِد وحدةً معلَّقة إلّا بثلاثة معًا: (١) مدخلُها ومخرجُها عبر بوّابة الغانم، (٢) اختباراتٌ توقعاتُها مستقلّةٌ عن شيفرتها مطعَّمةٌ بالطفرة (20/20)، (٣) ADR مسجَّل.
4. لا تحذف؛ انقل إلى `suspended/` وسجِّل. ولا تدمج في `main` بلا إذن صاحب المستودع.
5. لا تكتب «مبرهن» إلّا لما في Lean باسمه مدقَّقَ المسلّمات، ولا «مفحوص» إلّا لما له اختبارٌ باسمه، ولا «مقيس» إلّا لما له رقمٌ على مرجعٍ محجوب؛ وما سوى ذلك «معلن» أو «رأي». ولا تُثبت ادّعاءً قبل وجود ما يثبته.
6. أثبت وجودَ كلّ ملفٍّ تذكره قبل الكلام عنه («لا ثقة بلا طبعة»)، وافصل في جوابك ما فحصته الآلة عمّا استنتجتَه.

## ما نُفِّذ (2026-10-07)

- الوحداتُ أعلاه، ومعها اختباراتُها (`test_*.py`) وسكربتاتُ الجلب والتطبيع (`fetch_*.sh`، `test_fetch_source.sh`) ومسارُ CI القديم (`sources-exit-codes.yml`)، نُقلت إلى `suspended/` — 81 وحدةً في `SUSPENDED_REGISTRY.json` المولَّد بـ`python tools/gen_registry.py` (`--check` في CI).
- الحارسُ `tools/guard.py` (`python tools/guard.py` → «لا خرق») يُسقط البناء على أيّ قراءةٍ أو كتابةٍ أو تطبيعٍ أو استيرادٍ للمعلَّق خارج `tests/`؛ اختباراتُه في `tests/test_guard.py`.
- المدخلُ الوحيد: `src/entry.py` — `from_atoms(cert.atoms) → خانات`، `to_atoms(خانات) → ذرّاتٌ بعينها`، `licensed`. لا نصَّ فيه ولا تخمين. المدوّناتُ (`mujammad.txt`، `uthmani.txt`، `corpora/`) بايتاتٌ مودَعةٌ لا تقرؤها شيفرةٌ هنا.

## قبل أن تقول «تمّ»

```sh
python3 tools/gen_registry.py --check && python3 tools/guard.py && python3 -m pytest tests -q   # 5 اختبارات
```

## الخطوة التالية المأذونة

إعادةُ ما يعود عبر البوّابة وحدةً وحدة (الشرطُ الثلاثيّ)، وأوّلُها `algebra_engine` إن عاد: مدخلُه خاناتُ الشهادة من `src/entry.py` ومخرجُه ذرّاتٌ بعينها، وقياسُه على مودَع شهادات المصحف في SLGE لا على مدوّنته؛ وقرارُ مطابقة المدوّنة لمدوّنة الغانم المختومة لصاحب المستودع.
