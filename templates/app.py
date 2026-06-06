from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ======================================================
# 🟦 MEMBER 2 - RFQ / VENDOR MODULE (DUMMY ROUTES)
# ======================================================

rfqs = []

@app.route("/member2")
def member2_home():
    return "<h2>Member 2 Dashboard - RFQ System</h2>"

@app.route("/create-rfq")
def create_rfq():
    return """
    <h2>Create RFQ</h2>
    <form action="/submit-rfq" method="POST">
        Title: <input name="title"><br><br>
        Description: <input name="desc"><br><br>
        Budget: <input name="budget"><br><br>
        <button type="submit">Submit RFQ</button>
    </form>
    """

@app.route("/submit-rfq", methods=["POST"])
def submit_rfq():
    rfqs.append({
        "title": request.form["title"],
        "desc": request.form["desc"],
        "budget": request.form["budget"]
    })
    return redirect("/view-rfq")

@app.route("/view-rfq")
def view_rfq():
    return {"rfqs": rfqs}


# ======================================================
# 🟩 MEMBER 3 - PROCUREMENT FLOW (YOUR WORK)
# ======================================================

quotations = []

@app.route("/")
def home():
    return render_template("quotation.html")


@app.route("/submit", methods=["POST"])
def submit():
    quotations.append({
        "vendor": request.form["vendor"],
        "price": float(request.form["price"]),
        "delivery": int(request.form["delivery"]),
        "notes": request.form["notes"],
        "status": "Submitted"
    })
    return redirect("/compare")


@app.route("/compare")
def compare():
    sorted_q = sorted(quotations, key=lambda x: x["price"])
    return render_template("compare.html", quotations=sorted_q)


@app.route("/approve/<int:index>")
def approve(index):
    quotations[index]["status"] = "Approved"
    return redirect("/compare")


@app.route("/reject/<int:index>")
def reject(index):
    quotations[index]["status"] = "Rejected"
    return redirect("/compare")


@app.route("/invoice/<int:index>")
def invoice(index):
    q = quotations[index]
    tax = q["price"] * 0.18
    total = q["price"] + tax
    return render_template("invoice.html", q=q, tax=tax, total=total)


# ======================================================
# 🚀 RUN APP
# ======================================================

if __name__ == "__main__":
    app.run(debug=True)