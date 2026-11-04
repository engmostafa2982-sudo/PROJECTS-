# خطوات تنفيذ المشروع والأدوات المستخدمة
### منصة التصميم الهندسي بالذكاء الاصطناعي — دليل التنفيذ خطوة بخطوة

> هذا الملف مكمّل لـ [PLAN.md](PLAN.md). الخطة تشرح **ماذا** نبني، وهذا الملف يشرح **كيف** نبنيه، بأي أداة، وبأي ترتيب.
>
> **قاعدة الترتيب:** نبدأ من **المخرج** (ملف Revit و DWG حقيقي) ونرجع للخلف ناحية الذكاء الاصطناعي. لو قدرنا نولّد Revit صحيح من ملف JSON، يبقى كل اللي بعد كده هو "إزاي نطلع الـ JSON ده من صورة أو كلام المستخدم".

---

## نظرة عامة على المراحل

| # | المرحلة | المدة | الناتج |
|---|---|---|---|
| 0 | تجهيز بيئة العمل والحسابات | أسبوع 1 | كل الأدوات والحسابات جاهزة |
| 1 | قالب Revit ومكتبة العائلات | أسبوع 2–4 | ملف `.rte` + Families عربية |
| 2 | تعريف صيغة المبنى الموحدة (Building Schema) | أسبوع 2–3 | ملف JSON Schema |
| 3 | Revit Add-in محلي يبني النموذج من JSON | أسبوع 3–6 | RVT يتولد على جهاز المطور |
| 4 | نقل الـ Add-in إلى Design Automation (السحابة) | أسبوع 6–8 | RVT يتولد سحابياً بدون Revit مفتوح |
| 5 | تصدير AutoCAD DWG + PDF + IFC | أسبوع 7–9 | لوحات DWG بطبقات قياسية |
| 6 | Backend + قاعدة البيانات + الطوابير | أسبوع 6–10 | API شغال |
| 7 | إدخال الأرض (مقاسات + خريطة) | أسبوع 9–11 | المستخدم يرسم/يدخل أرضه |
| 8 | محرك الاشتراطات | أسبوع 10–13 | تقرير مطابقة لكل تصميم |
| 9 | مولّد المساقط (قوالب بارامترية) | أسبوع 11–16 | 3–5 بدائل لكل أرض |
| 10 | الذكاء الاصطناعي: قراءة الكروكي + محادثة الاحتياجات | أسبوع 13–18 | إدخال بالصور والكلام |
| 11 | الواجهة الأمامية + عارض 3D | أسبوع 10–20 | تطبيق ويب كامل |
| 12 | الكميات والتكلفة | أسبوع 18–20 | BOQ Excel |
| 13 | لوحة المهندس المراجع | أسبوع 19–22 | دورة مراجعة واعتماد |
| 14 | الدفع والحسابات والباقات | أسبوع 20–22 | بيع فعلي |
| 15 | الاختبار والجودة | مستمر + أسبوع 22–24 | اختبارات آلية |
| 16 | النشر والمراقبة والإطلاق التجريبي | أسبوع 23–26 | MVP مع 50 مستخدم |
| 17 | ما بعد الـ MVP: محرك تحسين، موبايل LiDAR، إنشائي | شهر 7+ | الإصدار 1.0 وما بعده |

---

## المرحلة 0 — تجهيز بيئة العمل والحسابات (أسبوع 1)

**الخطوات:**
1. إنشاء مستودع GitHub للكود (منفصل عن مستودع متابعة المشاريع) بهيكل المجلدات المقترح في PLAN.md.
2. إنشاء حساب **Autodesk Platform Services (APS)** على `aps.autodesk.com` → إنشاء App → الحصول على `Client ID` و `Client Secret` → تفعيل APIs: Design Automation، Model Derivative، OSS (التخزين).
3. شراء/توفير تراخيص **Revit** و **AutoCAD** لأجهزة التطوير (للاختبار المحلي وبناء القوالب).
4. إنشاء حساب سحابي (AWS أو Azure) — منطقة الشرق الأوسط (مثلاً AWS `me-central-1` الإمارات أو `me-south-1` البحرين، أو Azure Saudi/UAE).
5. إنشاء حساب **Claude API** (Anthropic Console) للحصول على API key.
6. إعداد أداة إدارة المهام وتقسيم المراحل لـ Sprints أسبوعين.

**الأدوات:**

| الأداة | الغرض | التكلفة |
|---|---|---|
| Git + GitHub | إدارة الكود، Pull Requests، CI | مجاني / Team ‎$4 للمستخدم |
| VS Code | تطوير Python و TypeScript | مجاني |
| Visual Studio 2022 Community/Pro | تطوير C# لـ Revit API | مجاني / مدفوع |
| Docker Desktop | تشغيل الخدمات محلياً | مجاني للشركات الصغيرة |
| Autodesk Revit 2025/2026 | بناء القوالب والاختبار | اشتراك سنوي |
| Autodesk AutoCAD 2025/2026 | مراجعة ملفات DWG وتجهيز Title blocks | اشتراك سنوي |
| Revit SDK + RevitLookup | توثيق API وأداة فحص عناصر النموذج | مجاني |
| Autodesk APS | تشغيل Revit/AutoCAD سحابياً + عارض الويب | بالاستهلاك (Cloud Credits) |
| AWS / Azure | الاستضافة | بالاستهلاك |
| Anthropic Claude API | Vision + LLM | بالاستهلاك (لكل توكن) |
| Jira / Linear / ClickUp | إدارة المهام | مجاني للفرق الصغيرة |
| Figma | تصميم الواجهات | مجاني / Pro |
| Postman / Bruno | اختبار الـ APIs | مجاني |

> **ملاحظة مهمة:** Revit 2025 وما بعده يعمل على **‎.NET 8**، أما Revit 2024 وما قبله فيعمل على **‎.NET Framework 4.8**. اختار نسخة واحدة وثبّتها، وتأكد من النسخ المدعومة حالياً في Design Automation من توثيق APS قبل البدء.

---

## المرحلة 1 — قالب Revit ومكتبة العائلات (أسبوع 2–4)

> **أهم مرحلة في جودة المخرج.** الكود بيرصّ العناصر، لكن القالب هو اللي بيحدد شكل اللوحة النهائية.

**الخطوات:**
1. إنشاء **Revit Template (`.rte`)** يحتوي على:
   - وحدات القياس (متر/سم)، المستويات الافتراضية (أرضي، أول، ملحق، سطح).
   - **أنواع الحوائط:** بلوك خارجي 20 سم + عزل + لياسة، بلوك داخلي 10/15 سم، سور.
   - أنواع البلاطات والأسقف والأرضيات.
   - **View Templates** للمساقط والواجهات والقطاعات (سماكات الخطوط، التهشير، الألوان).
   - **أنماط الأبعاد والنصوص** (خط عربي يدعم RTL مثل Arial أو خط المكتب).
   - **Title Block** (إطار اللوحة) A1 و A3 باسم المكتب وحقول: اسم المالك، رقم القطعة، رقم اللوحة، المقياس، التاريخ، اعتماد المهندس.
   - **Schedules** جاهزة: جدول الغرف والمساحات، جدول الأبواب، جدول الشبابيك، جدول الكميات.
2. بناء **مكتبة العائلات (Families `.rfa`)** البارامترية:
   - أبواب (خشب، حديد، منزلق، مزدوج) بمقاسات بارامترية.
   - شبابيك (ألمنيوم منزلق، ثابت، مشربية).
   - أثاث وأدوات صحية مناسبة للسوق المحلي (مجلس عربي، مغاسل، مراحيض عربي/إفرنجي، مطبخ).
   - عائلة **Room Tag** بالعربي والإنجليزي.
3. إعداد **جدول تحويل الطبقات (DWG Export Layer Mapping)** — ملف `.txt` يربط فئات Revit بأسماء طبقات AutoCAD (A-WALL, A-DOOR, A-GLAZ, A-FURN, A-DIMS, A-ANNO, A-AREA…).
4. اختبار يدوي: رسم فيلا كاملة يدوياً بالقالب وطباعة اللوحات للتأكد من الشكل النهائي.

**الأدوات:** Revit (Family Editor)، AutoCAD (لـ Title Block)، Dynamo (اختياري لأتمتة إنشاء الأنواع).
**الناتج:** `templates/revit/Platform_Template.rte` + مجلد `families/` + `dwg_layers.txt`.
**المسؤول:** مهندس BIM.

---

## المرحلة 2 — صيغة المبنى الموحدة Building Schema (أسبوع 2–3)

**الخطوات:**
1. تعريف ملف **JSON Schema** يمثل المبنى بالكامل بشكل مستقل عن أي برنامج:
```json
{
  "units": "m",
  "site": { "boundary": [[0,0],[20,0],[20,25],[0,25]], "north_angle": 15 },
  "levels": [ {"id": "L0", "name": "الدور الأرضي", "elevation": 0.0, "height": 3.6} ],
  "walls": [
    {"id": "W1", "level": "L0", "type": "EXT_200", "start": [3,3], "end": [17,3], "height": 3.6}
  ],
  "openings": [
    {"id": "D1", "host": "W1", "family": "Door_Single", "type": "90x220", "offset": 2.5}
  ],
  "rooms": [
    {"id": "R1", "level": "L0", "name": "مجلس رجال", "boundary": [[3,3],[9,3],[9,8],[3,8]]}
  ],
  "stairs": [], "columns": [], "slabs": [], "sheets": []
}
```
2. كتابة **Pydantic models** في Python تطابق الـ Schema (للتحقق من صحة البيانات قبل الإرسال).
3. كتابة **فاحص هندسي (Validator):** الحوائط تتقابل في نقاط، الأبواب داخل حدود الحائط، الغرف مغلقة، لا تداخل بين الغرف.
4. تجهيز 3 ملفات JSON يدوية كأمثلة اختبار (غرفة واحدة، شقة، فيلا دورين).

**الأدوات:**
| الأداة | الغرض |
|---|---|
| JSON Schema | توصيف الصيغة |
| Pydantic v2 | نماذج Python والتحقق |
| Shapely 2 | العمليات الهندسية (تقاطع، مساحة، إغلاق المضلعات) |
| pytest | اختبارات الفاحص |

**الناتج:** `schema/building.schema.json` + مكتبة `building_schema` في Python.

---

## المرحلة 3 — Revit Add-in محلي (أسبوع 3–6)

**الخطوات:**
1. إنشاء مشروع **C# Class Library** في Visual Studio يرجع لـ `RevitAPI.dll` و `RevitAPIUI.dll`.
2. كتابة **External Command** يقرأ ملف JSON ويبني بالترتيب:
   1. `Level` و `Grid`.
   2. `Wall.Create()` لكل حائط بالنوع المحدد.
   3. `Floor.Create()` و الأسقف.
   4. الأبواب والشبابيك عبر `NewFamilyInstance()` مستضافة على الحوائط.
   5. `Room` بأسمائها (`doc.Create.NewRoom()`).
   6. السلالم (`StairsEditScope`) والأعمدة والكمرات.
3. توليد **Views** آلياً: Floor Plan لكل مستوى، 4 واجهات، قطاعان، Ceiling Plan، 3D View — وتطبيق View Templates عليها.
4. إضافة **الأبعاد والتسميات آلياً** (`NewDimension`، `IndependentTag`) — أصعب جزء، ابدأ بالأبعاد الخارجية للحوائط فقط.
5. إنشاء **Sheets** ووضع الـ Views عليها (`ViewSheet.Create`، `Viewport.Create`) وتعبئة بيانات Title Block.
6. حفظ الملف كـ RVT.
7. اختبار على ملفات المرحلة 2 ومقارنة النتيجة بالرسم اليدوي.

**الأدوات:**
| الأداة | الغرض |
|---|---|
| Visual Studio 2022 + C# | الكود |
| Revit API (RevitAPI.dll) | إنشاء العناصر |
| Newtonsoft.Json / System.Text.Json | قراءة JSON |
| RevitLookup | فحص العناصر وخصائصها أثناء التطوير |
| Revit Add-In Manager | إعادة تحميل الـ Add-in بدون إغلاق Revit |
| The Building Coder (blog) + Revit API Docs (revitapidocs.com) | المراجع |

**الناتج:** `bim-builder/revit-addin/` — Add-in يحول JSON إلى RVT كامل باللوحات.

---

## المرحلة 4 — النقل إلى Design Automation for Revit (أسبوع 6–8)

> Design Automation يشغّل Revit على سيرفرات Autodesk **بدون واجهة**، فتقدر تولّد ملفات لآلاف المستخدمين بدون أجهزة عليها Revit.

**الخطوات:**
1. تعديل الـ Add-in ليكون **`IExternalDBApplication`** بدل External Command (لا يوجد UI في السحابة) واستخدام حزمة `DesignAutomationBridge`.
2. تغليف الـ Add-in كـ **AppBundle** (ملف ZIP يحتوي الـ DLL + ملف `.addin` + `PackageContents.xml`) ورفعه عبر API.
3. إنشاء **Activity:** تعريف المدخلات (`building.json` + `template.rte`) والمخرجات (`result.rvt`, `sheets.pdf`, `drawings.zip`).
4. رفع القالب والعائلات على **OSS bucket** (تخزين Autodesk) أو S3 مع روابط موقعة.
5. تشغيل **WorkItem** لكل طلب، واستقبال النتيجة عبر **Callback URL** (Webhook) على الـ Backend.
6. قياس الزمن والـ Cloud Credits المستهلكة لكل فيلا لتسعير الباقات.

**الأدوات:**
| الأداة | الغرض |
|---|---|
| APS Design Automation API v3 | تشغيل Revit سحابياً |
| `Autodesk.Forge.DesignAutomation.Revit` (DesignAutomationBridge NuGet) | ربط الـ Add-in بالسحابة |
| APS OSS API | تخزين الملفات |
| APS Authentication (OAuth 2-legged) | المصادقة |
| Python `requests` أو APS SDK | استدعاء الـ API من الـ Backend |
| ngrok | استقبال الـ Callback أثناء التطوير المحلي |

**الناتج:** خدمة `bim-builder` تستقبل JSON وترجع رابط RVT + PDF.

---

## المرحلة 5 — تصدير AutoCAD DWG و PDF و IFC (أسبوع 7–9)

**الخطوات:**
1. **DWG من Revit:** داخل نفس الـ WorkItem، استدعاء `doc.Export()` مع `DWGExportOptions` وملف الطبقات من المرحلة 1 → ملف DWG لكل Sheet.
2. **تنظيف وتنسيق DWG (اختياري):** Activity في **Design Automation for AutoCAD** يشغّل سكربت AutoLISP / .NET لـ: دمج الـ Xrefs (Bind)، Purge، Audit، ضبط الـ Plot styles (CTB)، إضافة Layouts للطباعة.
3. **PDF:** `doc.Export()` مع `PDFExportOptions` (متاح من Revit 2022+) لكل اللوحات في ملف واحد.
4. **IFC:** `doc.Export()` مع `IFCExportOptions` (IFC4 أو IFC2x3).
5. **مسار مفتوح المصدر للمعاينة السريعة (بدون تكلفة Autodesk):** من نفس الـ JSON مباشرة:
   - **ezdxf** لتوليد DXF ثنائي الأبعاد للمساقط.
   - **IfcOpenShell** لتوليد IFC ثلاثي الأبعاد يُعرض في المتصفح.
   - يستخدم في المعاينة المجانية، ويتولد Revit فقط بعد الدفع.

**الأدوات:** Revit Export API، APS Design Automation for AutoCAD، AutoLISP / AutoCAD .NET API، ezdxf، IfcOpenShell، LibreDWG/ODA File Converter (للتحويل بين DXF و DWG).
**الناتج:** حزمة ZIP: `project.rvt` + `drawings/*.dwg` + `sheets.pdf` + `model.ifc`.

---

## المرحلة 6 — Backend وقاعدة البيانات والطوابير (أسبوع 6–10)

**الخطوات:**
1. إنشاء خدمة **FastAPI** بالهيكل: `routers/`، `models/`، `services/`، `workers/`.
2. قاعدة بيانات **PostgreSQL + PostGIS** وجداول نموذج البيانات في PLAN.md، مع **Alembic** للـ migrations.
3. **Celery + Redis** للمهام الطويلة (قراءة الصور، توليد البدائل، طلبات Design Automation)، وحالة كل مهمة في جدول `generation_jobs`.
4. تخزين الملفات على **S3** (أو **MinIO** محلياً) بروابط موقعة مؤقتة (Presigned URLs).
5. **WebSocket / Server-Sent Events** لإرسال تقدم التوليد للمستخدم لحظياً.
6. توثيق الـ API آلياً (OpenAPI/Swagger مدمج في FastAPI).
7. ملف `docker-compose.yml` يشغّل: api, worker, postgres, redis, minio.

**الأدوات:**
| الأداة | الغرض |
|---|---|
| Python 3.12 + FastAPI + Uvicorn | الـ API |
| SQLAlchemy 2 + Alembic + GeoAlchemy2 | قاعدة البيانات والجغرافيا |
| PostgreSQL 16 + PostGIS | التخزين |
| Celery + Redis (أو Temporal) | الطوابير |
| boto3 + S3 / MinIO | الملفات |
| Pydantic Settings | الإعدادات والأسرار |
| Docker Compose | التشغيل المحلي |

---

## المرحلة 7 — إدخال الأرض: مقاسات وخريطة (أسبوع 9–11)

**الخطوات:**
1. **نموذج إدخال المقاسات:** أطوال الأضلاع بالترتيب + الزوايا (أو "مستطيل" بنقرة واحدة) → حساب المضلع وإغلاقه رياضياً وعرض الفرق.
2. **محرر مضلعات تفاعلي** على Canvas: سحب الرؤوس، كتابة الطول على كل ضلع، تحديد الضلع المطل على الشارع وعرض الشارع.
3. **الخريطة:** رسم حدود القطعة على صورة القمر الصناعي، تحويل الإحداثيات الجغرافية لإحداثيات محلية بالمتر، حساب زاوية الشمال تلقائياً.
4. حفظ الحدود في `sites.boundary` (PostGIS).

**الأدوات:** Leaflet أو MapLibre GL / Mapbox GL، Google Maps API (صور قمر صناعي)، Turf.js، Konva.js أو Fabric.js (المحرر)، Shapely + pyproj (التحويل في الـ Backend).

---

## المرحلة 8 — محرك الاشتراطات (أسبوع 10–13)

**الخطوات:**
1. جمع اشتراطات المدينة الأولى (البلدية + كود البناء السعودي SBC 201 للمعماري) في جدول مع المهندس المعماري.
2. تحويلها لملفات قواعد **YAML/JSON** مُرقّمة الإصدار:
```yaml
city: riyadh
zone: residential_villa
setbacks: { front: "max(2, street_width*0.2)", side: 2, rear: 2 }
max_coverage: 0.60
max_floors: 2
roof_annex_max_ratio: 0.50
min_room: { bedroom: {area: 9, width: 2.7}, kitchen: {area: 6, width: 2.1} }
stairs: { riser_max: 0.18, tread_min: 0.28, width_min: 1.0 }
ceiling_height_min: 2.7
```
3. كتابة **محرك تقييم** في Python: يحسب المغلف المسموح للبناء من الأرض والارتدادات، ثم يفحص أي Building JSON ويطلع تقرير: ✅ مطابق / ❌ مخالف + السبب + القيمة الفعلية مقابل المسموح.
4. **اختبارات لكل قاعدة** (حالة مطابقة + حالة مخالفة).
5. لوحة إدارة لتعديل القواعد بدون مبرمج (المرحلة 13).

**الأدوات:** Python، PyYAML، Shapely (حساب الارتدادات بـ `buffer` السالب)، `simpleeval` أو `asteval` (حساب المعادلات من الملف بأمان)، pytest.

---

## المرحلة 9 — مولّد المساقط بالقوالب البارامترية (أسبوع 11–16)

**الخطوات:**
1. اختيار **15–20 مخطط فيلا حقيقي** معتمد (من أرشيف مكتب) يغطي أشهر مقاسات الأراضي.
2. تحويل كل مخطط إلى **قالب بارامتري:** الحوائط معرّفة بنسب ومحاور قابلة للتمدد (Grid-based)، مثلاً: "المجلس = 30% من العرض الأمامي"، مع حدود دنيا وقصوى.
3. خوارزمية **الملاءمة (Fitting):** لكل أرض → حساب المغلف → تجربة كل القوالب → تمديد/تصغير → استبعاد ما يخالف الاشتراطات أو الحد الأدنى للغرف.
4. **التقييم والترتيب:** كفاءة المساحة، مطابقة برنامج الفراغات المطلوب، عدد المخالفات، التكلفة التقديرية → أفضل 3–5 بدائل.
5. **انعكاس وتدوير القوالب** حسب اتجاه الشارع والشمال.
6. تخزين كل بديل في `design_options.building_schema`.

**الأدوات:** Python، Shapely، NumPy، (لاحقاً **Google OR-Tools CP-SAT** للتوزيع الحر بدون قوالب)، matplotlib لرسم معاينة سريعة PNG للاختبار.

---

## المرحلة 10 — الذكاء الاصطناعي: قراءة الكروكي ومحادثة الاحتياجات (أسبوع 13–18)

### 10.1 قراءة الكروكي والصك
1. المستخدم يرفع صورة → **معالجة مسبقة:** تصحيح الميلان والمنظور، تحسين التباين.
2. إرسال الصورة لنموذج **Claude (Vision)** مع **Tool Use / Structured Output** لإجبار الرد على صيغة JSON محددة: الأضلاع، الأطوال، المساحة، الشوارع وعروضها، رقم القطعة والمخطط.
3. **تحقق رياضي:** إغلاق المضلع + مطابقة المساحة → عرض النتيجة على المحرر التفاعلي (المرحلة 7) **ليؤكدها المستخدم أو يعدّلها**. لا نعتمد أي قراءة آلية بدون تأكيد.
4. بناء **مجموعة اختبار** من 100 كروكي حقيقي لقياس الدقة (% أضلاع صحيحة) قبل الإطلاق.

### 10.2 محادثة الاحتياجات
1. **System prompt** بالعربي يعرّف دور المساعد وقائمة الفراغات المتاحة وحدودها.
2. أداة (Tool) اسمها `update_space_program` يستدعيها النموذج لتحديث برنامج الفراغات JSON أثناء المحادثة.
3. التحقق من الناتج بـ Pydantic، ثم عرض ملخص للمستخدم للتأكيد.

### 10.3 التعديل بالكلام
- أدوات مثل `resize_room`، `move_room`، `swap_rooms`، `add_window` يستدعيها النموذج → تنفذ على النموذج البارامتري → إعادة فحص الاشتراطات تلقائياً.

### 10.4 صور الوحدات القائمة (المرحلة الثانية)
- **SAM 2** (Segment Anything) لتحديد الحوائط والفتحات، **Depth Anything** لتقدير العمق، + مقاس مرجعي من المستخدم للمعايرة.

**الأدوات:**
| الأداة | الغرض |
|---|---|
| Anthropic Claude API (Vision + Tool use) | قراءة الصور، المحادثة، التعديل بالكلام |
| Anthropic Python SDK | الربط من الـ Backend |
| OpenCV + Pillow | المعالجة المسبقة للصور |
| Pydantic | التحقق من مخرجات النموذج |
| SAM 2 / Depth Anything (PyTorch) | تحليل صور الوحدات القائمة |
| Langfuse أو Promptfoo | متابعة وتقييم جودة الـ Prompts |

---

## المرحلة 11 — الواجهة الأمامية والعارض ثلاثي الأبعاد (أسبوع 10–20)

**الخطوات:**
1. تصميم الشاشات على **Figma:** الرئيسية، مشروع جديد، إدخال الأرض، المحادثة، البدائل، التعديل، الدفع، التحميل، لوحة المهندس.
2. بناء التطبيق بـ **Next.js** مع دعم **RTL** والعربية/الإنجليزية.
3. **عارض 2D** للمساقط (SVG مولّد من الـ JSON — سريع وخفيف).
4. **عارض 3D:** عرض ملف IFC المولّد (المرحلة 5) بـ **That Open Engine / web-ifc + Three.js**، أو ملف RVT بـ **APS Viewer** بعد تحويله بـ **Model Derivative API**.
5. شاشة مقارنة البدائل جنباً إلى جنب مع درجات التقييم وتقرير الاشتراطات.

**الأدوات:** Next.js + React + TypeScript، Tailwind CSS + shadcn/ui، next-intl (الترجمة)، TanStack Query، Zustand، Three.js + React Three Fiber، That Open Engine (IFC)، Autodesk APS Viewer، Figma.

---

## المرحلة 12 — الكميات والتكلفة (أسبوع 18–20)

**الخطوات:**
1. حساب الكميات من الـ JSON مباشرة (سريع) أو من **Revit Schedules** المصدّرة (أدق): خرسانة، بلوك، لياسة، بلاط، دهان، أبواب، شبابيك.
2. قاعدة **أسعار وحدات** لكل مدينة قابلة للتحديث من لوحة الإدارة.
3. إخراج **Excel** بنفس هيكلة جداول BOQ المستخدمة في مشاريعك، + ملخص التكلفة في الواجهة.

**الأدوات:** Python، openpyxl أو XlsxWriter، Pandas، Revit `ViewSchedule.Export`.

---

## المرحلة 13 — لوحة المهندس المراجع والإدارة (أسبوع 19–22)

**الخطوات:**
1. صلاحيات (Roles): عميل، مهندس مراجع، مدير.
2. قائمة المشاريع المنتظرة للمراجعة + عرض اللوحات PDF بأدوات تعليق.
3. تحميل RVT للمهندس → تعديله في Revit → رفعه مرة أخرى → يصبح النسخة المعتمدة.
4. زر **اعتماد** يضيف اسم المهندس ورقم ترخيصه للـ Title Block (بإعادة تشغيل التصدير).
5. لوحة الإدارة: تعديل القواعد، الأسعار، القوالب، متابعة الاستهلاك والتكاليف.

**الأدوات:** نفس الـ Frontend، PDF.js أو react-pdf (عرض وتعليق)، Refine أو React Admin (لوحة الإدارة).

---

## المرحلة 14 — الحسابات والدفع (أسبوع 20–22)

**الخطوات:**
1. تسجيل دخول بالجوال (OTP) والبريد، وحسابات المكاتب الهندسية.
2. ربط بوابة دفع محلية تدعم **مدى و Apple Pay و STC Pay** (أو Fawry/Paymob لمصر).
3. Webhook الدفع → تفعيل الباقة → بدء توليد Revit/DWG.
4. إصدار فاتورة إلكترونية متوافقة مع **الفوترة الإلكترونية (ZATCA / فاتورة)**.

**الأدوات:** Keycloak أو Auth0 أو Supabase Auth، Unifonic / Twilio (رسائل OTP)، Moyasar / Tap / HyperPay (السعودية)، Paymob / Fawry (مصر).

---

## المرحلة 15 — الاختبار والجودة (مستمر)

**الخطوات:**
1. **Unit tests** لكل وحدة (الـ Schema، الاشتراطات، المولّد).
2. **Golden-file tests:** 20 حالة أرض ثابتة → التأكد إن الـ JSON و الـ DXF الناتجين لم يتغيرا بدون قصد.
3. **اختبار Revit:** تشغيل Design Automation ليلياً على الحالات الـ 20 والتأكد من نجاحها وفتح الملفات.
4. **اختبارات الواجهة End-to-End:** رحلة المستخدم من التسجيل للتحميل.
5. **تقييم الـ AI:** مجموعة الكروكيات الـ 100 + محادثات نموذجية، وقياس الدقة بعد أي تعديل في الـ Prompts أو تغيير النموذج.
6. **مراجعة بشرية:** مهندس يراجع عينة أسبوعية من التصميمات المولّدة ويسجل الملاحظات.

**الأدوات:** pytest، xUnit/NUnit (C#)، Playwright (الواجهة)، Promptfoo (تقييم الـ AI)، GitHub Actions (تشغيل كل ده مع كل تعديل).

---

## المرحلة 16 — النشر والمراقبة والإطلاق التجريبي (أسبوع 23–26)

**الخطوات:**
1. **البنية التحتية ككود** (Terraform): VPC، قاعدة البيانات المُدارة، Redis، S3، الحاويات.
2. نشر الخدمات كحاويات Docker على **AWS ECS Fargate** أو **Azure Container Apps** (أبسط من Kubernetes في البداية).
3. **CI/CD:** GitHub Actions يبني ويختبر وينشر تلقائياً على بيئة Staging ثم Production.
4. **المراقبة:** الأخطاء، الأداء، تكلفة Design Automation و Claude API لكل مشروع.
5. **الأمان:** HTTPS، تشفير الملفات، نسخ احتياطي يومي، إدارة الأسرار، الالتزام بنظام حماية البيانات الشخصية (PDPL).
6. **إطلاق تجريبي مغلق** مع 50 مستخدم + مكتب هندسي شريك، وجمع الملاحظات أسبوعياً.

**الأدوات:** Terraform، Docker، AWS ECS / Azure Container Apps، RDS PostgreSQL، ElastiCache Redis، CloudFront / Cloudflare، Sentry (الأخطاء)، Grafana + Prometheus أو Datadog (المراقبة)، AWS Secrets Manager، PostHog (تحليلات سلوك المستخدم).

---

## المرحلة 17 — ما بعد الـ MVP (شهر 7 فما بعد)

| الميزة | الخطوات الرئيسية | الأدوات |
|---|---|---|
| توليد حر بدون قوالب | صياغة التوزيع كمسألة قيود (Constraint satisfaction) + تحسين متعدد الأهداف | Google OR-Tools CP-SAT، pymoo (NSGA-II) |
| عمارات سكنية | دور متكرر + نواة (درج/مصعد) + مواقف قبو | نفس المحرك + قوالب جديدة |
| تطبيق موبايل + LiDAR | مسح الوحدة بـ RoomPlan → JSON → Building Schema | Swift + Apple RoomPlan (iOS 16+)، React Native / Flutter |
| تصميم إنشائي مبدئي | شبكة أعمدة من المسقط + تقدير مقاسات الأعمدة والقواعد + تصدير لبرامج التحليل | Revit Structure، تصدير لـ ETABS / Robot عبر IFC |
| كهروميكانيك مبدئي | توزيع نقاط كهرباء وإنارة وصحي آلياً حسب قواعد | Revit MEP Families + قواعد |
| صور واقعية (Renders) | إخراج مشاهد من النموذج + تحسين بالـ AI | Blender (عبر IFC)، Enscape/Twinmotion، نماذج Image-to-Image |
| نموذج توليد خاص | تدريب على المساقط المعتمدة من المهندسين | PyTorch، Graph Neural Networks (مثل أبحاث Graph2Plan / HouseGAN++) |
| API للمكاتب | واجهة White-label واشتراكات | API Gateway + مفاتيح API |

---

## ملخص الأدوات حسب الطبقة

| الطبقة | الأدوات |
|---|---|
| **BIM و CAD** | Autodesk Revit، Revit API (C#)، AutoCAD، AutoLISP، Dynamo، RevitLookup |
| **أتمتة سحابية** | Autodesk Platform Services: Design Automation (Revit + AutoCAD)، Model Derivative، Viewer، OSS |
| **مفتوح المصدر هندسي** | IfcOpenShell، ezdxf، Shapely، pyproj، That Open Engine (web-ifc)، ODA File Converter |
| **الذكاء الاصطناعي** | Claude API (Vision + Tool use)، OpenCV، SAM 2، Depth Anything، OR-Tools، Promptfoo، Langfuse |
| **Backend** | Python، FastAPI، Pydantic، SQLAlchemy، Alembic، Celery، Redis |
| **قاعدة البيانات والتخزين** | PostgreSQL + PostGIS، S3 / MinIO |
| **Frontend** | Next.js، React، TypeScript، Tailwind، shadcn/ui، Three.js، Leaflet/MapLibre، Konva.js |
| **الموبايل** | React Native أو Flutter، Swift + RoomPlan |
| **الدفع والحسابات** | Moyasar / Tap / HyperPay، Keycloak / Auth0، Unifonic |
| **DevOps** | Docker، GitHub Actions، Terraform، AWS ECS / Azure Container Apps، Sentry، Grafana |
| **التصميم والإدارة** | Figma، Jira / Linear، GitHub |

---

## أول 10 أيام عمل — قائمة تنفيذ فورية

| اليوم | المهمة | الأداة | الناتج |
|---|---|---|---|
| 1 | فتح حسابات APS و Anthropic والسحابة، إنشاء المستودع | المتصفح، GitHub | Keys + Repo |
| 2 | تثبيت Revit + Visual Studio + Revit SDK + RevitLookup | — | بيئة C# جاهزة |
| 3 | Add-in "Hello Wall": حائط واحد من الكود | Revit API | أول عنصر برمجياً |
| 4 | كتابة أول نسخة من Building Schema + مثال غرفة واحدة | JSON Schema، Pydantic | `building.schema.json` |
| 5 | Add-in يقرأ JSON ويبني حوائط + أرضية + باب | Revit API | غرفة من JSON |
| 6 | تشغيل نفس الكود على Design Automation (Activity + WorkItem) | APS | أول RVT من السحابة |
| 7 | إضافة تصدير DWG و PDF للـ WorkItem | Revit Export API | DWG + PDF |
| 8 | سكربت Python يولّد JSON لأرض مستطيلة بارتدادات (مغلف بسيط) | Shapely | مغلف البناء |
| 9 | ربط السكربت بالـ Design Automation من Python | requests / APS | سلسلة كاملة: مقاسات → RVT + DWG |
| 10 | عرض داخلي للنتيجة + تحديد الأولويات للـ Sprint الأول | — | قرار الاستمرار |

> **لو السلسلة دي اشتغلت في 10 أيام، المشروع ممكن تقنياً، والباقي توسيع وتحسين.**
