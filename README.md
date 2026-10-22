# سوق الأدوات والمهارات

لوحة اكتشاف للأدوات والمهارات والوكلاء الأكثر استخداماً، مستضافة مجاناً على GitHub Pages، بلا خادم.

## التشغيل المحلي
    python collector/collect.py --demo   # بيانات تجريبية بلا إنترنت
    python collector/collect.py          # بيانات حقيقية (يفضل ضبط GITHUB_TOKEN)
    cd web && python -m http.server 8000

## النشر
1. Settings ← Pages ← Source: GitHub Actions.
2. Actions ← update ← Run workflow. يتجدد بعدها يومياً تلقائياً.

## إضافة عنصر
أضف سطراً في collector/seeds.json (repo, type, dom, cmd، واختيارياً npm أو pypi).

## الاستخدام
التحميلات اليومية من npm أو PyPI إن وجدت، وإلا عدد النجوم. التغير 24س يقارن بلقطة اليوم السابق في data/history.json.

## الاكتشاف التلقائي
collector/discover.py يبحث يومياً عن مستودعات بوسوم mcp-server وclaude-skills وagent-skills وai-agent (أكثر من 200 نجمة، نشاط خلال 180 يوماً، رخصة، ليست fork) ويدمجها collect.py مع seeds.json.

## تليمتري زر التثبيت (اختياري)
يعد ضغطات "نسخ أمر التثبيت" بلا بيانات شخصية.
1. أنشئ حساب Cloudflare مجاني ثم: `cd worker && npx wrangler kv namespace create KV` وضع المعرف في wrangler.toml.
2. `npx wrangler deploy` وانسخ رابط الـ Worker.
3. في المستودع: Settings ← Variables ← Actions، أضف TELEMETRY_URL بقيمة الرابط.
