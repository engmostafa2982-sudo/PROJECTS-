# الخطوة 1: صيغة المبنى الموحدة (Building Schema)

دي أول خطوة في [خطة التنفيذ](../EXECUTION_STEPS.md) (المرحلة 2). الصيغة دي هي "اللغة" اللي كل أجزاء المنصة هتتكلم بيها:

```
صورة / كروكي / مقاسات / كلام المستخدم  ──►  Building JSON  ──►  Revit (RVT) / AutoCAD (DWG, DXF) / IFC / BOQ
```

أي حاجة بتولّد تصميم (قوالب، ذكاء اصطناعي، إدخال يدوي) لازم تطلّع ملف JSON بالصيغة دي، وأي حاجة بتصدّر رسومات بتقرأ من نفس الملف.

## محتوى المجلد

| الملف | وظيفته |
|---|---|
| `building_schema/models.py` | تعريف الصيغة: مشروع، أرض، أدوار، حوائط، فتحات (أبواب/شبابيك)، غرف |
| `building_schema/validate.py` | فاحص هندسي: يرفض أي تصميم هيكسر Revit قبل ما يتبعت له |
| `building_schema/export_dxf.py` | تصدير مسقط لكل دور كملف DXF يفتح في AutoCAD، بطبقات قياسية |
| `building_schema/preview.py` | صورة PNG سريعة للمسقط |
| `schema/building.schema.json` | الصيغة كـ JSON Schema (للمطورين وللـ Revit add-in) |
| `examples/single_room.json` | مثال: غرفة واحدة |
| `examples/villa_ground_floor.json` | مثال: دور أرضي فيلا على أرض 20×25 |
| `examples/output/` | الناتج الجاهز للمثال: DXF و PNG |
| `tests/` | 10 اختبارات آلية |

## التشغيل

محتاج Python 3.11 أو أحدث.

```bash
pip install -r requirements.txt
```

افحص تصميم:

```bash
python -m building_schema validate examples/villa_ground_floor.json
```

صدّر ملف AutoCAD (DXF) لكل دور:

```bash
python -m building_schema dxf examples/villa_ground_floor.json -o out
```

صورة معاينة:

```bash
python -m building_schema preview examples/villa_ground_floor.json -o out
```

شغّل الاختبارات:

```bash
python -m pytest
```

لفتح الـ DXF كـ DWG: افتحه في AutoCAD واعمل Save As ← DWG.

## قواعد الصيغة (نسخة 0.1)

- **الوحدات:** متر. الإحداثيات على المسقط: x ناحية اليمين و y لفوق.
- **الحائط** = خط محور (`start` → `end`) + سماكة + نوع (`EXT_200`, `INT_150`, `INT_100`). اسم النوع هو اللي هيتربط بنوع الحائط في قالب Revit.
- **الفتحة** مربوطة بحائط (`host`)، و`position` = المسافة من بداية الحائط لمنتصف الفتحة. للأبواب: `hinge` (جهة المفصلة) و `swing` (يفتح يمين أو شمال اتجاه الحائط).
- **الغرفة** = مضلع على محاور الحوائط + اسم عربي + `usage` (نوع الفراغ بالإنجليزي للبرمجة).
- كل `id` لازم يكون فريد في الملف كله.

## الفاحص بيرفض إيه؟

| الكود | النوع | المعنى |
|---|---|---|
| `duplicate-id` | خطأ | نفس الـ id متكرر |
| `unknown-level` / `unknown-host` | خطأ | إشارة لدور أو حائط مش موجود |
| `wall-too-short` | خطأ | حائط أقصر من 10 سم |
| `opening-outside-wall` | خطأ | الفتحة طالعة برا طول الحائط |
| `opening-too-tall` | خطأ | الفتحة أعلى من الحائط |
| `opening-on-junction` | خطأ | باب أو شباك في مكان حائط تاني بيقابل الحائط |
| `openings-overlap` | خطأ | فتحتين فوق بعض |
| `room-invalid` / `rooms-overlap` | خطأ | غرفة شكلها غلط أو غرفتين متداخلتين |
| `free-wall-end` | تحذير | طرف حائط مش واصل بحائط تاني (فتحة في المحيط) |
| `wall-outside-site` | تحذير | حائط خارج حدود الأرض |
| `window-no-sill` | تحذير | شباك من غير جلسة |

## الخطوة الجاية

**المرحلة 3: Revit Add-in** يقرأ نفس ملف الـ JSON ويبني الحوائط والأبواب والشبابيك والغرف في Revit. محتاج قبلها على جهازك: Revit + Visual Studio 2022 + حساب Autodesk Platform Services.
