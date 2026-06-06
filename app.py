from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>VendorBridge ERP</h1>
    <ul>
        <li><a href='/vendors'>Vendor Management</a></li>
        <li><a href='/add_vendor'>Add Vendor</a></li>
        <li><a href='/rfq'>RFQ Management</a></li>
        <li><a href='/create_rfq'>Create RFQ</a></li>
    </ul>
    """

@app.route('/vendors')
def vendors():
    return render_template('vendors.html')

@app.route('/add_vendor')
def add_vendor():
    return render_template('add_vendor.html')

@app.route('/rfq')
def rfq():
    return render_template('rfq.html')

@app.route('/create_rfq')
def create_rfq():
    return render_template('create_rfq.html')

if __name__ == '__main__':
    app.run(debug=True)