from flask import Flask, render_template, request, redirect, url_for
import inventory_app.db as db
from datetime import datetime
from flask import flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.secret_key = "development-key" 


@app.route("/")
def home():
    try:
        products = db.get_all_products()
        print(f"DEBUG: Products to display: {products}")  
        return render_template("index.html", products=products)
    except Exception as e:
        print(f"ERROR: {e}")
        return render_template("index.html", products=[])  

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        product_name = request.form["product_name"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])
        
        
        db.add_product(product_name, quantity,price)
        flash("Product added successfully", "success")
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/delete/<string:product_id>") 
def delete(product_id):
    db.delete_product(product_id) 
    return redirect(url_for("home"))

@app.route("/locations")
def locations():
    locations = db.get_all_locations()
    return render_template("locations.html", locations=locations)

@app.route("/add_location", methods=["GET", "POST"])
def add_location():
    if request.method == "POST":
        location_id = request.form["location_id"]
        location_name = request.form["location_name"]
        address = request.form.get("address", "")
        
        db.add_location(location_id, location_name, address)
        return redirect(url_for("locations"))
    return render_template("add_location.html")

@app.route("/movements")
def movements():
    movements = db.get_all_movements()
    products = db.get_all_products()  
    locations = db.get_all_locations()
    return render_template("movements.html", 
                         movements=movements,
                         products=products,
                         locations=locations)

@app.route("/add_movement", methods=["GET", "POST"])
def add_movement():
    if request.method == "POST":
        movement_id = request.form["movement_id"]
        from_location = request.form["from_location"] or None
        to_location = request.form["to_location"] or None
        product_id = request.form["product_id"]
        qty = int(request.form["qty"])
        
        db.add_movement(movement_id, product_id, qty, from_location, to_location)
        return redirect(url_for("movements"))
    
    products = db.get_all_products() 
    locations = db.get_all_locations()
    return render_template("add_movement.html", 
                         products=products,
                         locations=locations)

@app.route("/report")
def report():
    balances = db.get_product_balances()  
    return render_template("report.html", balances=balances)

@app.route("/move_product", methods=["GET", "POST"])
def move_product():
    if request.method == "POST":
        try:
            movement_id = f"move_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            product_id = request.form["product_id"]
            from_location = request.form["from_location"] or None
            to_location = request.form["to_location"] or None
            qty = int(request.form["qty"])
            
            if not from_location and not to_location:
                flash("Must specify at least one location (from or to)", "error")
                return redirect(url_for("move_product"))
            
            db.add_movement(movement_id, product_id, qty, from_location, to_location)
            flash("Product movement recorded successfully", "success")
            return redirect(url_for("movements"))
        
        except Exception as e:
            flash(str(e), "error")
            return redirect(url_for("move_product"))
    
    products = db.get_all_products()
    locations = db.get_all_locations()
    return render_template("move_product.html", 
                         products=products,
                         locations=locations)


@app.route("/delete_location/<string:location_id>")
def delete_location(location_id):
    try:
        db.delete_location(location_id)
        flash("Location deleted successfully", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("locations"))

@app.route("/delete_movement/<string:movement_id>")
def delete_movement(movement_id):
    try:
        db.delete_movement(movement_id)
        flash("Movement deleted successfully", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("movements"))

@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit(product_id):
    product = db.get_product_by_id(product_id)
    
    if request.method == "POST":
        product_name = request.form["product_name"]
        description = request.form["description"]
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])
        
        db.update_product(product_id, product_name, description, price, quantity)
        flash("Product updated successfully", "success")
        return redirect(url_for("home"))
    
    return render_template("edit.html", product=product)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
