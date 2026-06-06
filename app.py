from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# =========================
# 🗄️ DATABASE
# =========================
def init_db():
    conn = sqlite3.connect("erp.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS rfq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        budget TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS quotation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor TEXT,
        price REAL,
        delivery TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# 🌌 ULTRA MODERN UI
# =========================
UI = """
<style>
body{
    margin:0;
    font-family:Segoe UI;
    background: linear-gradient(135deg, #0f172a, #020617);
    color:white;
}

/* Sidebar */
.sidebar{
    position:fixed;
    width:250px;
    height:100vh;
    background: rgba(15,23,42,0.95);
    padding:20px;
    border-right:1px solid #1e293b;
}

.sidebar h2{
    color:#38bdf8;
    margin-bottom:20px;
}

.sidebar a{
    display:block;
    color:#e2e8f0;
    padding:10px;
    margin:6px 0;
    text-decoration:none;
    border-radius:8px;
    transition:0.2s;
}

.sidebar a:hover{
    background:#1e293b;
    color:#38bdf8;
}

/* Main */
.main{
    margin-left:270px;
    padding:30px;
}

/* Cards */
.card{
    background: rgba(255,255,255,0.06);
    border:1px solid rgba(255,255,255,0.1);
    padding:20px;
    margin:15px 0;
    border-radius:16px;
    backdrop-filter: blur(10px);
    transition:0.3s;
}

.card:hover{
    transform:scale(1.02);
    background: rgba(255,255,255,0.1);
}

/* Inputs */
input{
    width:100%;
    padding:10px;
    margin:8px 0;
    border-radius:8px;
    border:none;
    background:#0f172a;
    color:white;
}

/* Button */
button{
    padding:10px 15px;
    background:#38bdf8;
    border:none;
    border-radius:8px;
    font-weight:bold;
    cursor:pointer;
}

button:hover{
    background:#0ea5e9;
}

/* Dashboard cards */
.grid{
    display:grid;
    grid-template-columns: repeat(3, 1fr);
    gap:15px;
}

.smallcard{
    background: rgba(255,255,255,0.05);
    padding:15px;
    border-radius:12px;
    border:1px solid #1e293b;
}
</style>
"""

# =========================
# 🏠 DASHBOARD
# =========================
@app.route("/")
def home():

    conn = sqlite3.connect("erp.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM rfq")
    rfq_count = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM quotation")
    q_count = c.fetchone()[0]

    conn.close()

    return UI + f"""
    <div class='sidebar'>
        <h2>🚀 ERP SYSTEM</h2>
        <a href='/'>Dashboard</a>
        <a href='/rfq'>RFQ</a>
        <a href='/quotation'>Quotation</a>
        <a href='/compare'>Comparison</a>
        <a href='/invoice'>Invoice</a>
    </div>

    <div class='main'>
        <h1>📊 Procurement Dashboard</h1>

        <div class='grid'>
            <div class='smallcard'>📩 RFQs<br><h2>{rfq_count}</h2></div>
            <div class='smallcard'>📄 Quotations<br><h2>{q_count}</h2></div>
            <div class='smallcard'>⚡ System<br><h2>Active</h2></div>
        </div>

        <div class='card'>
            <h3>Welcome to Smart ERP System</h3>
            <p>Manage procurement workflow from RFQ to Invoice in one system.</p>
        </div>
    </div>
    """

# =========================
# 📩 RFQ MODULE
# =========================
@app.route("/rfq")
def rfq():

    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    c.execute("SELECT * FROM rfq")
    data = c.fetchall()
    conn.close()

    html = UI + """
    <div class='sidebar'>
        <h2>ERP</h2>
        <a href='/'>Dashboard</a>
    </div>

    <div class='main'>
        <h1>📩 RFQ Management</h1>

        <div class='card'>
            <a href='/create-rfq'><button>Create RFQ</button></a>
        </div>
    """

    for r in data:
        html += f"""
        <div class='card'>
            <b>📌 {r[1]}</b><br>
            💰 Budget: {r[2]}
        </div>
        """

    return html + "</div>"

@app.route("/create-rfq")
def create_rfq():
    return UI + """
    <div class='sidebar'><h2>ERP</h2><a href='/rfq'>Back</a></div>

    <div class='main'>
        <h1>Create RFQ</h1>

        <div class='card'>
            <form method='POST' action='/submit-rfq'>
                <input name='title' placeholder='RFQ Title'>
                <input name='budget' placeholder='Budget'>
                <button>Submit</button>
            </form>
        </div>
    </div>
    """

@app.route("/submit-rfq", methods=["POST"])
def submit_rfq():
    title = request.form.get("title")
    budget = request.form.get("budget")

    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    c.execute("INSERT INTO rfq (title, budget) VALUES (?, ?)", (title, budget))
    conn.commit()
    conn.close()

    return redirect("/rfq")

# =========================
# 📄 QUOTATION MODULE
# =========================
@app.route("/quotation")
def quotation():
    return UI + """
    <div class='sidebar'><h2>ERP</h2><a href='/'>Back</a></div>

    <div class='main'>
        <h1>📄 Vendor Quotation</h1>

        <div class='card'>
            <form method='POST' action='/submit'>
                <input name='vendor' placeholder='Vendor'>
                <input name='price' placeholder='Price'>
                <input name='delivery' placeholder='Delivery Days'>
                <button>Submit</button>
            </form>
        </div>
    </div>
    """

@app.route("/submit", methods=["POST"])
def submit():
    vendor = request.form.get("vendor")
    price = request.form.get("price")
    delivery = request.form.get("delivery")

    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    c.execute("INSERT INTO quotation (vendor, price, delivery) VALUES (?, ?, ?)",
              (vendor, price, delivery))
    conn.commit()
    conn.close()

    return redirect("/compare")

# =========================
# 📊 COMPARISON
# =========================
@app.route("/compare")
def compare():

    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    c.execute("SELECT * FROM quotation")
    data = c.fetchall()
    conn.close()

    html = UI + """
    <div class='sidebar'><h2>ERP</h2><a href='/'>Back</a></div>

    <div class='main'>
        <h1>📊 Comparison</h1>
    """

    for q in data:
        html += f"""
        <div class='card'>
            🏷 <b>{q[1]}</b><br>
            💰 {q[2]}<br>
            🚚 {q[3]}
        </div>
        """

    return html + "</div>"

# =========================
# 🧾 INVOICE
# =========================
@app.route("/invoice")
def invoice():

    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    c.execute("SELECT * FROM quotation")
    data = c.fetchall()
    conn.close()

    if not data:
        return UI + "<div class='main'><div class='card'>No Data</div></div>"

    q = data[0]
    price = float(q[2])
    tax = price * 0.18

    return UI + f"""
    <div class='sidebar'><h2>ERP</h2><a href='/'>Back</a></div>

    <div class='main'>
        <h1>🧾 Invoice</h1>

        <div class='card'>
            <h3>Vendor: {q[1]}</h3>
            <p>Price: {price}</p>
            <p>Tax: {tax}</p>
            <h2>Total: {price + tax}</h2>
        </div>
    </div>
    """

# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)