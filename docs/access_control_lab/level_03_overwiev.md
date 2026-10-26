## Access Control Vulnerability ( Referer Based Access Control ) - Level_03

### **Overview**

The `update_role` endpoint enforces its security check **solely by inspecting the `Referer` HTTP header**. Because the `Referer` header is fully attacker-controlled, this check can be trivially bypassed, allowing an attacker to change any user's role — including promoting themselves to admin.

### **Vulnerable Code**

```python
@SessionManager._admin_required
def update_role(user_id):
    # ⚠️ It trusts client-controlled header.
    referer = request.headers.get("Referer", "")
    if referer.startswith(request.host_url + "admin"):
        new_role = request.form.get("new_role")
        user = db.session.get(User, user_id)
        admin_user = 1

        if user is None:
            flash("User not found", "error")
            return redirect(url_for("access_control.admin"))

        if user.id == admin_user:
            flash("Admin user's role cannot be changed!", "error")
            return redirect(url_for("access_control.admin"))
        # ⚠️ no check on who the target is relative to the caller
        user.role = new_role
        db.session.commit()
        flash(f"Updated role for {user.username} to {new_role}.", "success")

    else:
        flash(f"Invalid request source.", "error")

    return redirect(url_for("access_control.admin"))
```

### **POC**

- change a user role and using Burp Repeater, change the `user_id` in HTTP request and `new_role` to `admin` in request body.

### **Impact**

1. **Takeover of other accounts' authority**: grant admin to attacker-controlled sleeper accounts, or to colluding accounts.
2. **Targeted sabotage**: strip roles from specific users (e.g., the security team, finance approvers) to block their work or force them into a weaker state.
3. **Chained escalation**: once admin, the attacker can typically reach user management, audit logs, API keys, integrations, and data exports — the bypass becomes the entry point to a full application compromise.

### **Remediation**

1. Remove the `Referer` check and authorize from the authenticated session.

```python
@SessionManager._admin_required
def update_role(user_id):
    # authorization already established by the decorator from the session
    ...
```

1. Replace the magic-number guard with an allowlist and explicit protected accounts

```python
ASSIGNABLE_ROLES = {"user", "moderator", "admin"}
PROTECTED_USER_IDS = {1}

if new_role not in ASSIGNABLE_ROLES:
    flash("Invalid role requested.", "error")
    return redirect(url_for("access_control.admin"))

if user_id in PROTECTED_USER_IDS:
    flash("This account's role cannot be changed.", "error")
    return redirect(url_for("access_control.admin"))
```

3. Add an object-level check to block self-escalation (and audit the change)

```python
if user.id == current_user.id:
    abort(403)

old_role = user.role
user.role = new_role
db.session.commit()

log_role_change(actor=current_user.id, target=user.id,
                old=old_role, new=new_role)
```
