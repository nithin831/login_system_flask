from db import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.String(100), nullable=True)
    mrp = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(100),  nullable=False)

    def json(self):
        return {
            "id": self.id,
            "name": self.name, 
            "category": self.category, 
            "tags": self.tags, 
            "mrp": self.mrp, 
            "sale_price": self.sale_price, 
            "image": self.image, 
            "description": self.description, 
            "slug": self.slug
        }