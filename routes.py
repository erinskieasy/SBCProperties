from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Property, PriceOption, DiscountMethod

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/property_selection')
def property_selection():
    properties = Property.query.all()
    return render_template('property_selection.html', properties=properties)

@app.route('/price_selection/<int:property_id>')
def price_selection(property_id):
    property = Property.query.get_or_404(property_id)
    price_options = PriceOption.query.filter_by(property_id=property_id).all()
    return render_template('price_selection.html', property=property, price_options=price_options)

@app.route('/discount_selection/<int:property_id>/<int:price_option_id>')
def discount_selection(property_id, price_option_id):
    property = Property.query.get_or_404(property_id)
    price_option = PriceOption.query.get_or_404(price_option_id)
    discount_methods = DiscountMethod.query.all()
    return render_template('discount_selection.html', property=property, price_option=price_option, discount_methods=discount_methods)

@app.route('/final_price', methods=['POST'])
def final_price():
    property_id = request.form.get('property_id')
    price_option_id = request.form.get('price_option_id')
    discount_method_id = request.form.get('discount_method_id')

    property = Property.query.get_or_404(property_id)
    price_option = PriceOption.query.get_or_404(price_option_id)
    discount_method = DiscountMethod.query.get_or_404(discount_method_id)

    base_price = property.base_price
    final_price = base_price * price_option.price_multiplier
    discounted_price = final_price * (1 - discount_method.discount_percentage / 100)

    return render_template('final_price.html', property=property, price_option=price_option, discount_method=discount_method, final_price=discounted_price)

@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        new_property = Property(
            name=request.form['name'],
            description=request.form['description'],
            image_url=request.form['image_url'],
            base_price=float(request.form['base_price'])
        )
        db.session.add(new_property)
        db.session.commit()
        flash('New property added successfully!', 'success')
        return redirect(url_for('manage_properties'))
    return render_template('add_property.html')

@app.route('/manage_properties')
def manage_properties():
    properties = Property.query.all()
    return render_template('manage_properties.html', properties=properties)

@app.route('/remove_property/<int:property_id>', methods=['POST'])
def remove_property(property_id):
    property = Property.query.get_or_404(property_id)
    db.session.delete(property)
    db.session.commit()
    flash('Property removed successfully!', 'success')
    return redirect(url_for('manage_properties'))
