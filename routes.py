import os
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from app import app, db
from models import Property, PriceOption, DiscountMethod, GalleryImage

# Configure upload settings
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # For static deployment, serve the index.html from root directory
    return send_from_directory('.', 'index.html')

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

            form_data = {k: v for k, v in request.form.items() if k != 'image'}
            app.logger.info(f"Received form data: {form_data}")

            required_fields = ['name', 'description', 'base_price']
            for field in required_fields:
                if not request.form.get(field):
                    raise ValueError(f"Missing required field: {field}")

            name = request.form['name']
            description = request.form['description']
            base_price = float(request.form['base_price'])
            bedrooms = int(request.form['bedrooms']) if request.form.get('bedrooms') else None
            bathrooms = float(request.form['bathrooms']) if request.form.get('bathrooms') else None
            area = float(request.form['area']) if request.form.get('area') else None
            amenities = request.form.get('amenities')

            if 'image' not in request.files:
                raise ValueError("No image file uploaded")
            
            file = request.files['image']
            if file.filename == '':
                raise ValueError("No selected image file")
            
            if not allowed_file(file.filename):
                raise ValueError("Invalid file type for main image")

            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                app.logger.info(f"Saved main image: {file_path}")
            except Exception as e:
                app.logger.error(f"Failed to save file {filename}: {str(e)}")
                raise ValueError(f"Failed to save uploaded file: {str(e)}")

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

            if 'gallery_images' in request.files:
                gallery_files = request.files.getlist('gallery_images')
                for gfile in gallery_files:
                    if gfile and allowed_file(gfile.filename):
                        try:
                            gfilename = secure_filename(gfile.filename)
                            gfile_path = os.path.join(app.config['UPLOAD_FOLDER'], gfilename)
                            gfile.save(gfile_path)
                            app.logger.info(f"Saved gallery image: {gfile_path}")
                            
                            new_gallery_image = GalleryImage(
                                image_url=gfilename,
                                property=new_property
                            )
                            db.session.add(new_gallery_image)
                        except Exception as e:
                            app.logger.error(f"Failed to save gallery image {gfilename}: {str(e)}")
                            raise ValueError(f"Failed to save gallery image: {str(e)}")

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
