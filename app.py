from flask import Flask, render_template, request, redirect, url_for, session
import random
import string

app = Flask(__name__)
app.secret_key = "supersecretkey"  

def generate_password(length, include_upper, include_digits, include_special):
    chars = string.ascii_lowercase
    if include_upper:
        chars += string.ascii_uppercase
    if include_digits:
        chars += string.digits
    if include_special:
        chars += string.punctuation

    if not chars:
        return ""

    password = "".join(random.choice(chars) for _ in range(length))
    return password

def password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    if len(password) >= 14:
        score += 1

    if score <= 2:
        return "Weak"
    elif score == 3:
        return "Medium"
    elif score == 4:
        return "Strong"
    else:
        return "Very Strong"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        length = int(request.form.get("length", 12))
        count = int(request.form.get("count", 1))
        include_upper = "upper" in request.form
        include_digits = "digits" in request.form
        include_special = "special" in request.form

        passwords = []
        for _ in range(count):
            pwd = generate_password(length, include_upper, include_digits, include_special)
            if pwd:
                passwords.append({
                    "value": pwd,
                    "strength": password_strength(pwd)
                })

        session["passwords"] = passwords
        session["length"] = length
        session["count"] = count
        session["include_upper"] = include_upper
        session["include_digits"] = include_digits
        session["include_special"] = include_special

        return redirect(url_for("index"))

    
    passwords = session.get("passwords", [])
    length = session.get("length", 12)
    count = session.get("count", 1)
    include_upper = session.get("include_upper", False)
    include_digits = session.get("include_digits", False)
    include_special = session.get("include_special", False)

    return render_template(
        "index.html",
        passwords=passwords,
        length=length,
        count=count,
        include_upper=include_upper,
        include_digits=include_digits,
        include_special=include_special,
    )

if __name__ == "__main__":
    app.run(debug=True)
