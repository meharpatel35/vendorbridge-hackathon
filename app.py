from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "vendorbridge_saas"

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("erp.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS quotation(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor TEXT,
        price TEXT,
        delivery TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= AI SCORE =================
def ai_score(price, delivery):
    try:
        p = float(price)
        d = float(delivery)
    except:
        return "UNKNOWN"

    score = (1200 / (p + 1)) + (60 / (d + 1))

    if score > 70:
        return "BEST"
    elif score > 35:
        return "GOOD"
    else:
        return "RISK"

# ================= UI =================
UI = """
<style>

body{
    margin:0;
    font-family:Segoe UI;
    background:#0b1220;
    color:white;
}

/* SIDEBAR */
.sidebar{
    position:fixed;
    width:240px;
    height:100vh;
    background:#050a16;
    padding:20px;
}

.sidebar h2{
    color:#a78bfa;
}

.sidebar a{
    display:block;
    padding:10px;
    margin:6px 0;
    color:#cbd5e1;
    text-decoration:none;
    border-radius:10px;
}

.sidebar a:hover{
    background:#1e293b;
}

/* MAIN */
.main{
    margin-left:260px;
    padding:25px;
}

/* CARD */
.card{
    background:#111827;
    padding:18px;
    border-radius:14px;
    margin:10px 0;
}

/* BUTTON */
button{
    background:#7c3aed;
    color:white;
    border:none;
    padding:10px;
    border-radius:10px;
    cursor:pointer;
}

input{
    width:100%;
    padding:10px;
    margin:8px 0;
    border-radius:10px;
    border:none;
}

</style>
"""

# ================= LOGIN =================
@app.route("/")
def home():
    return """
    <style>
    body{
        margin:0;
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
        font-family:Segoe UI;
        background:url('https://images.unsplash.com/photo-1521737604893-d14cc237f11d');
        background-size:cover;
    }

    .box{
        background:rgba(0,0,0,0.6);
        padding:30px;
        border-radius:16px;
        width:320px;
        color:white;
    }

    input{
        width:100%;
        padding:10px;
        margin:8px 0;
        border-radius:10px;
        border:none;
    }

    button{
        width:100%;
        padding:10px;
        border:none;
        border-radius:10px;
        background:#7c3aed;
        color:white;
    }
    </style>

    <div class='box'>
        <h2>VendorBridge</h2>
        <form method='POST' action='/login'>
            <input name='username' placeholder='Name'>
            <input name='password' type='password' placeholder='Password'>
            <button>Login</button>
        </form>
    </div>
    """

@app.route("/login", methods=["POST"])
def login():
    session["user"] = request.form["username"]
    return redirect("/dashboard")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return UI + f"""
    <div class='sidebar'>
        <h2>VendorBridge</h2>
        <a href='/dashboard'>Dashboard</a>
        <a href='/quotation'>Quotation</a>
        <a href='/compare'>AI Compare</a>
        <a href='/invoice_list'>Invoice</a>
    </div>

    <div class='main'>

        <!-- HERO SECTION (IMPROVED SaaS STORY) -->
        <div class='card'>
            <h1>Welcome back, {session['user']} 👋</h1>
            <p style="color:#cbd5e1; line-height:1.6;">
                VendorBridge is your intelligent procurement control center built for modern businesses.
                Manage vendors, compare quotations, and generate invoices with AI-powered insights in seconds.
            </p>

            <p style="color:#a78bfa;">
                ⚡ Faster decisions • 📊 Smart analytics • 🤖 AI-assisted procurement workflows
            </p>
        </div>

        <!-- FEATURE BANNER IMAGES -->
        <div class='grid'>

            <div class='card'>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135706.png" width="50">
                <h3>Smart Vendor Tracking</h3>
                <p>Monitor all vendor activity in one unified dashboard.</p>
            </div>

            <div class='card'>
                <img src="https://cdn-icons-png.flaticon.com/512/2920/2920244.png" width="50">
                <h3>Automated RFQ Flow</h3>
                <p>Create and manage quotations without manual effort.</p>
            </div>

            <div class='card'>
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712039.png" width="50">
                <h3>AI Decision Engine</h3>
                <p>Compare vendors instantly using intelligent scoring.</p>
            </div>

        </div>

        <!-- EXTRA VISUAL STRIP -->
        <div class='card' style="margin-top:20px;">
            <h2>Why VendorBridge?</h2>

            <p style="color:#cbd5e1;">
                Traditional procurement systems are slow and manual. VendorBridge transforms it into a
                real-time intelligent workflow system with automation, analytics, and AI-driven insights.
            </p>

            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71"
                 style="width:100%;border-radius:12px;margin-top:10px;">
        </div>

    </div>
    """

# ================= QUOTATION =================
@app.route("/quotation")
def quotation():
    return UI + """
    <div class='main'>
        <h2>Create Quotation</h2>

        <div class='card'>
            <form method='POST' action='/submit'>
                <input name='vendor' placeholder='Vendor'>
                <input name='price' placeholder='Price'>
                <input name='delivery' placeholder='Delivery Days'>
                <button>Create</button>
            </form>
        </div>
    </div>
    """

@app.route("/submit", methods=["POST"])
def submit():
    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    c.execute("INSERT INTO quotation VALUES(NULL,?,?,?)",
              (request.form["vendor"],
               request.form["price"],
               request.form["delivery"]))
    conn.commit()
    conn.close()
    return redirect("/invoice_list")

# ================= AI COMPARE =================
@app.route("/compare")
def compare():
    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    c.execute("SELECT * FROM quotation")
    data = c.fetchall()
    conn.close()

    html = UI + "<div class='main'><h2>AI Compare</h2>"

    rank = 1
    for q in data:
        html += f"""
        <div class='card'>
            <h3>{q[1]}</h3>
            <p>₹{q[2]}</p>
            <p>{q[3]} days</p>
            <b>{ai_score(q[2], q[3])} | Rank {rank}</b>
            <br><br>
            <a href='/invoice/{q[0]}'><button>View Invoice</button></a>
        </div>
        """
        rank += 1

    return html + "</div>"

# ================= INVOICE LIST =================
@app.route("/invoice_list")
def invoice_list():
    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    c.execute("SELECT * FROM quotation")
    data = c.fetchall()
    conn.close()

    html = UI + "<div class='main'><h2>Invoices</h2>"

    for q in data:
        html += f"""
        <div class='card'>
            <h3>Invoice - {q[1]}</h3>
            <p>Price ₹{q[2]}</p>
            <a href='/invoice/{q[0]}'><button>Open Invoice</button></a>
        </div>
        """

    return html + "</div>"

# ================= SINGLE INVOICE PRINT (FIXED) =================
@app.route("/invoice/<int:id>")
def invoice(id):
    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    c.execute("SELECT * FROM quotation WHERE id=?", (id,))
    q = c.fetchone()
    conn.close()

    if not q:
        return "Invoice not found"

    total = float(q[2]) * 1.18

    return UI + f"""
    <div class='main'>
        <div class='card' id='invoice'>
            <h2>🧾 VendorBridge Invoice</h2>
            <hr>
            <p><b>Vendor:</b> {q[1]}</p>
            <p><b>Base Price:</b> ₹{q[2]}</p>
            <p><b>Delivery:</b> {q[3]} days</p>
            <p><b>GST (18%):</b> Included</p>
            <h3>Total: ₹{total}</h3>

            <button onclick="window.print()">Print This Invoice</button>
        </div>
    </div>
    """

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)