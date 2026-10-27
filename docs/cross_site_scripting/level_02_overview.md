## Cross-Site Scripting ( Incomplete Tag Blocklisting ) - Level_02

### **Overview**

The app stores user-submitted reviews after passing them through a single-pass regex **denylist** of HTML tags and then renders them with `|safe`, so any unlisted tag (e.g. `<details ontoggle=…>`), nested-tag trick (`<scr<script>ipt>`), or dangerous attribute (`href="javascript:…"`, `onerror=`) survives and executes as **stored XSS**.

### **Vulnerable code**

```python
# ⚠️ incomplete allow list
BLOCKED_TAGS = [
                    "script", "iframe", "object",
                    "embed", "link", "style",
                    "meta", "img", "svg",
                    "video", "audio", "source",
                    "track", "canvas", "map",
                    "area", "base", "form",
                    "input", "button"
                ]
# ⚠️ it scans once, left to right, and never re-scans its own output
# ⚠️ <scr<script>ipt>alert(1)</scr</script>ipt> is going to become <script>alert(1)</script>
TAG_PATTERN = re.compile(
    r"<\s*/?\s*(" + "|".join(re.escape(t) for t in BLOCKED_TAGS) + r")\b[^>]*>",
    re.IGNORECASE,
)

def sanatizer(value: str) -> str:
    if not value:
        return ""
    cleaned = TAG_PATTERN.sub("", value)
    return cleaned[:1000]

# ---------------------------------------------------------------------
@xss_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        author = sanatizer(request.form.get('author'))[:50]
        comment = sanatizer(request.form.get('comment'))
  
        new_review = Review(author=author, comment=comment)
        db.session.add(new_review)
        db.session.commit()
  
        return redirect(url_for('xss.home'))
  
    reviews = Review.query.order_by(Review.id.desc()).all()
    return render_template('content.html', reviews=reviews)
# ---------------------------------------------------------------------
```

### **POC**

1. **Unlisted-tag bypass** (any tag not in the blocklist works):

```python
<details open ontoggle="alert(document.cookie)">X</details>
```

- `details` isn't blocked, and `ontoggle` fires automatically when opened.

2. **Nested-tag reconstruction** (single-pass `re.sub` bypass):

```python
<scr<script>ipt>alert(document.domain)</scr</script>ipt>
```

- The regex strips the inner `<script>`/`</script>` substrings, leaving `<script>alert(document.domain)</script>` in the stored value — never re-scanned.

**Steps to reproduce:**

1. Open the review form (`POST /`).
2. Submit `comment` = `<details open ontoggle=alert(document.cookie)>X</details>` (or any payload above).
3. The comment is stored after the regex pass (payload survives).
4. Reload `/` — every visitor executes the JavaScript.

### **Impact

* **Stored XSS** — payload persists in the DB and fires for every viewer of the review page.
* **Session hijacking / account takeover** — read cookies or tokens, perform authenticated actions as the victim.
* **Credential theft** — inject fake login forms (form/input tags are only *blocklisted*, not attributes-controlled).
* **CSRF-bypass & forced actions** — fetch() requests with the victim's session.

### **Remedation**

1. **Remove the denylist sanitizer. Escape at output time (primary fix):**

```python
# store raw (length-limited) text; do NOT attempt HTML sanitization here
author  = (request.form.get('author')  or "").strip()[:50]
comment = (request.form.get('comment') or "").strip()[:1000]
```

```html
{# content.html — rely on Jinja autoescaping; NEVER use |safe on user input #}
{{ review.author }}
{{ review.comment }}
```

- Autoescaping (`html.escape` / `markupsafe.escape`) converts `<` to `&lt;` etc., so every tag — known or unknown — becomes inert text. This is the correct, allow-by-default defense.

2. Use allowlisting instead.

```python
import nh3

ALLOWED_TAGS = {"b", "i", "em", "strong", "p", "br", "a", "ul", "ol", "li"}
ALLOWED_ATTRS = {"a": {"href", "title"}}

def render_comment(raw: str) -> str:
    return nh3.clean(
        raw,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        url_schemes={"http", "https", "mailto"},  # excludes javascript:
    )
```

3. Add secure header to every response.
