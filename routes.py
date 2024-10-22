from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app import app, db
from models import Property, PriceOption, DiscountMethod, GalleryImage
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/property_selection')
def property_selection():
    properties = Property.query.all()
    return render_template('property_selection.html', properties=properties)

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), filename)

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
        new_property = Property()
        new_property.name = request.form['name']
        new_property.description = request.form['description']
        new_property.image_url = request.form['image_url']
        new_property.base_price = float(request.form['base_price'])
        new_property.bedrooms = int(request.form['bedrooms']) if request.form['bedrooms'] else None
        new_property.bathrooms = float(request.form['bathrooms']) if request.form['bathrooms'] else None
        new_property.area = float(request.form['area']) if request.form['area'] else None
        new_property.amenities = request.form['amenities']
        
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

@app.route('/property_gallery/<int:property_id>')
def property_gallery(property_id):
    property = Property.query.get_or_404(property_id)
    gallery_images = GalleryImage.query.filter_by(property_id=property_id).all()
    return render_template('property_gallery.html', property=property, gallery_images=gallery_images)

@app.route('/initialize_properties')
def initialize_properties():
    # Check if properties already exist
    if Property.query.count() > 0:
        flash('Properties have already been initialized.', 'info')
        return redirect(url_for('property_selection'))

    # Add the three properties with correct image_url and additional details
    properties = [
        {"name": "Tropical Resort", "description": "Tropical resort with bicycle rentals", "image_url": "384207928.jpg", "base_price": 250, "bedrooms": 2, "bathrooms": 2.5, "area": 1500, "amenities": "Pool, Bicycle rentals"},
        {"name": "Luxury Villa", "description": "Luxury villa with private pool", "image_url": "387887682.jpg", "base_price": 500, "bedrooms": 4, "bathrooms": 3.5, "area": 3000, "amenities": "Private pool, Garden"},
        {"name": "Beachfront Property", "description": "Modern beachfront property with twin pools", "image_url": "474497619.jpg", "base_price": 450, "bedrooms": 3, "bathrooms": 3, "area": 2000, "amenities": "Twin pools, Beach access"}
    ]

    for prop_data in properties:
        new_property = Property()
        for key, value in prop_data.items():
            setattr(new_property, key, value)
        db.session.add(new_property)

    db.session.commit()
    flash('Properties have been initialized successfully!', 'success')
    return redirect(url_for('property_selection'))
