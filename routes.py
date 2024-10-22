import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from models import Property, PriceOption, DiscountMethod, GalleryImage

# Configure upload settings
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/property_selection')
def property_selection():
    properties = Property.query.all()
    return render_template('property_selection.html', properties=properties)

@app.route('/price_selection/<int:property_id>', methods=['GET', 'POST'])
def price_selection(property_id):
    property = Property.query.get_or_404(property_id)
    price_options = PriceOption.query.filter_by(property_id=property_id).all()

    if request.method == 'POST':
        name = request.form.get('name')
        price_multiplier = request.form.get('price_multiplier')
        if name and price_multiplier:
            try:
                price_multiplier = float(price_multiplier)
                new_option = PriceOption(name=name, price_multiplier=price_multiplier)
                new_option.property = property
                db.session.add(new_option)
                db.session.commit()
                flash('New price option added successfully!', 'success')
            except ValueError:
                flash('Invalid price multiplier. Please enter a valid number.', 'error')
        else:
            flash('Please fill in all required fields.', 'error')
        return redirect(url_for('price_selection', property_id=property_id))

    return render_template('price_selection.html', property=property, price_options=price_options)

@app.route('/discount_selection/<int:property_id>/<int:price_option_id>')
def discount_selection(property_id, price_option_id):
    property = Property.query.get_or_404(property_id)
    price_option = PriceOption.query.get_or_404(price_option_id)
    discount_methods = DiscountMethod.query.all()
    return render_template('discount_selection.html', property=property, price_option=price_option, discount_methods=discount_methods)

@app.route('/view_discounts/<int:property_id>/<int:price_option_id>', methods=['GET', 'POST'])
def view_discounts(property_id, price_option_id):
    property = Property.query.get_or_404(property_id)
    price_option = PriceOption.query.get_or_404(price_option_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        discount_percentage = request.form.get('discount_percentage')
        if name and discount_percentage:
            try:
                discount_percentage = float(discount_percentage)
                new_discount = DiscountMethod(name=name, discount_percentage=discount_percentage)
                db.session.add(new_discount)
                db.session.commit()
                flash('New discount added successfully!', 'success')
            except ValueError:
                flash('Invalid discount percentage. Please enter a valid number.', 'error')
        else:
            flash('Please fill in all required fields.', 'error')
        return redirect(url_for('view_discounts', property_id=property_id, price_option_id=price_option_id))
    
    discount_methods = DiscountMethod.query.all()
    return render_template('view_discounts.html', property=property, price_option=price_option, discount_methods=discount_methods)

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
        try:
            app.logger.info("Received add_property POST request")
            
            # Check if UPLOAD_FOLDER exists, if not create it
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
                app.logger.info(f"Created UPLOAD_FOLDER: {app.config['UPLOAD_FOLDER']}")

            # Log received form data (exclude file data)
            form_data = {k: v for k, v in request.form.items() if k != 'image'}
            app.logger.info(f"Received form data: {form_data}")

            # Validate required fields
            required_fields = ['name', 'description', 'base_price']
            for field in required_fields:
                if not request.form.get(field):
                    raise ValueError(f"Missing required field: {field}")

            # Validate and process form data
            name = request.form['name']
            description = request.form['description']
            base_price = float(request.form['base_price'])
            bedrooms = int(request.form['bedrooms']) if request.form.get('bedrooms') else None
            bathrooms = float(request.form['bathrooms']) if request.form.get('bathrooms') else None
            area = float(request.form['area']) if request.form.get('area') else None
            amenities = request.form.get('amenities')

            # Validate file upload
            if 'image' not in request.files:
                raise ValueError("No image file uploaded")
            
            file = request.files['image']
            if file.filename == '':
                raise ValueError("No selected image file")
            
            if not allowed_file(file.filename):
                raise ValueError("Invalid file type for main image")

            # Process file upload
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            app.logger.info(f"Saved main image: {file_path}")

            # Create new property
            new_property = Property(
                name=name,
                description=description,
                image_url=filename,
                base_price=base_price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                area=area,
                amenities=amenities
            )
            db.session.add(new_property)

            # Process gallery images
            if 'gallery_images' in request.files:
                gallery_files = request.files.getlist('gallery_images')
                for gfile in gallery_files:
                    if gfile and allowed_file(gfile.filename):
                        gfilename = secure_filename(gfile.filename)
                        gfile_path = os.path.join(app.config['UPLOAD_FOLDER'], gfilename)
                        gfile.save(gfile_path)
                        app.logger.info(f"Saved gallery image: {gfile_path}")
                        new_gallery_image = GalleryImage(image_url=gfilename)
                        new_gallery_image.property = new_property
                        db.session.add(new_gallery_image)

            db.session.commit()
            app.logger.info("Successfully added new property to database")
            flash('New property added successfully!', 'success')
            return redirect(url_for('manage_properties'))

        except ValueError as e:
            db.session.rollback()
            app.logger.error(f"ValueError in add_property: {str(e)}")
            flash(f"Error: {str(e)}", 'error')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Unexpected error in add_property: {str(e)}")
            flash("An unexpected error occurred. Please try again.", 'error')

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
    if Property.query.count() > 0:
        flash('Properties have already been initialized.', 'info')
        return redirect(url_for('property_selection'))

    properties = [
        {"name": "Tropical Resort", "description": "Tropical resort with bicycle rentals", "image_url": "384207928.jpg", "base_price": 250, "bedrooms": 2, "bathrooms": 2.5, "area": 1500, "amenities": "Pool, Bicycle rentals"},
        {"name": "Luxury Villa", "description": "Luxury villa with private pool", "image_url": "387887682.jpg", "base_price": 500, "bedrooms": 4, "bathrooms": 3.5, "area": 3000, "amenities": "Private pool, Garden"},
        {"name": "Beachfront Property", "description": "Modern beachfront property with twin pools", "image_url": "474497619.jpg", "base_price": 450, "bedrooms": 3, "bathrooms": 3, "area": 2000, "amenities": "Twin pools, Beach access"}
    ]

    for prop_data in properties:
        new_property = Property(**prop_data)
        db.session.add(new_property)

        gallery_images = [
            GalleryImage(image_url=f"{prop_data['image_url'][:-4]}_1.jpg"),
            GalleryImage(image_url=f"{prop_data['image_url'][:-4]}_2.jpg"),
            GalleryImage(image_url=f"{prop_data['image_url'][:-4]}_3.jpg")
        ]
        for gallery_image in gallery_images:
            gallery_image.property = new_property
            db.session.add(gallery_image)

    db.session.commit()
    flash('Properties have been initialized successfully!', 'success')
    return redirect(url_for('property_selection'))

@app.route('/initialize_price_options_and_discounts')
def initialize_price_options_and_discounts():
    if PriceOption.query.count() > 0 or DiscountMethod.query.count() > 0:
        flash('Price options and discount methods have already been initialized.', 'info')
        return redirect(url_for('property_selection'))

    properties = Property.query.all()
    price_options = [
        {'name': 'Standard', 'price_multiplier': 1.0},
        {'name': 'Premium', 'price_multiplier': 1.2},
        {'name': 'Deluxe', 'price_multiplier': 1.5}
    ]

    for property in properties:
        for option in price_options:
            new_option = PriceOption(**option)
            new_option.property = property
            db.session.add(new_option)

    discount_methods = [
        {'name': 'No Discount', 'discount_percentage': 0},
        {'name': 'Early Bird', 'discount_percentage': 10},
        {'name': 'Last Minute', 'discount_percentage': 15},
        {'name': 'Loyalty Program', 'discount_percentage': 20}
    ]

    for method in discount_methods:
        new_method = DiscountMethod(**method)
        db.session.add(new_method)

    db.session.commit()
    flash('Price options and discount methods have been initialized successfully!', 'success')
    return redirect(url_for('property_selection'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
