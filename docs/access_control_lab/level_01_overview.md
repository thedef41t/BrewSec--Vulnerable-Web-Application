## Access Control Vulnerability ( Basic IDOR ) - Level_01

❗️**Note**: The application contains additional security issues (e.g., plaintext password storage, a weak `secret_key`, missing security headers). However, this assessment focuses exclusively on the vulnerabilities explicitly defined in scope; other findings are out of scope and not evaluated here.

### **Overview**

The application allows an authonticareted user to view other users data manipulating `id` parameter in URL. Attacker can change `&id=3` to `&id=1`, because the code fails to verify wether the logged in user matches or has permission to view the requested `target_id`

### **Vulnerable code**

```python
@access_control_bp.route('/')
@access_control_bp.route('/home')
def home():
    if not session.get('user_id'):
        flash("Please log in first.", "error")
        return redirect(url_for('access_control.login'))

    if 'id' not in request.args:
        return redirect(url_for('access_control.home', id=session.get('user_id')))

    # VULNERABLE line:
    target_id = request.args.get('id', type=int)
    target_user = User.query.get(target_id)

    return render_template("content.html", target_user=target_user, target_id=target_id)
```

- the vulnerability relies on the fact that the application accepts an `id` parameter from the URL (`request.args.get('id')`) and queries the database directly without validating if the currently logged-in user (`session.get('user_id')`) has permission to view that record.

### Impact

Attacker can:

- **Privilege Escalation**: attacker's can directly target `id=1` to gain admin privilege. (In many applications, `id=1` is automatically assigned to the very first user created during setup—which is almost always the **administrator account**.)
- **Privacy Violations**: Depending on what `content.html` displays, private information like email addresses, account details, purchase histories, or private messages could be leaked to unauthorized parties.

### Remedation

1. **Enforce Authentication Checks First**: Always verify that a user has an active, valid session before allowing them to access any protected route or resource. If no session exists, redirect them to login immediately.

   ```python
   current_user_id = session.get('user_id')
   if not current_user_id:
       flash("Please log in first.", "error")
       return redirect(url_for('access_control.login'))
   ```
2. **Implement Server-Side Authorization (Never Trust Client Input)**: Do not rely on the `id` parameter provided by the user in the URL (`request.args`) to determine whose data to fetch. Instead, compare the requested ID against the authenticated session data, or explicitly verify if the current user has administrative permissions to view other accounts.

### Secure code:

```python
@access_control_bp.route('/home')
def home():
    # 1. Authentication check
    current_user_id = session.get('user_id')
    if not current_user_id:
        flash("Please log in first.", "error")
        return redirect(url_for('access_control.login'))

    # 2. Prevent IDOR: Force or validate that the requested ID belongs to the logged-in user
    target_id = request.args.get('id', current_user_id, type=int)
  
    if target_id != current_user_id:
        flash("Unauthorized access attempt detected.", "error")
        return redirect(url_for('access_control.home', id=current_user_id))

    target_user = User.query.get_or_404(target_id)
    return render_template("content.html", target_user=target_user, target_id=target_id)
```
