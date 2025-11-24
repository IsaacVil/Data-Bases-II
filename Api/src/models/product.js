const mongoose = require('mongoose');
const productSchema = new mongoose.Schema({
    sku: {type: String, required: true, unique:true},
    name: {type: String, required: true},
    brand: {type: String, required: false},
    category: {type: String, required: true},
    unit: {type: String, required: true},
    price: {type: Number, required: true},
    cost: {type: Number, required: false},
    stock: {type: Number, required: true},
    minStock: {type: Number, required: false},
    location: {type: String, required: false},
    supplierId: {type: String, required: false},
    tags: {type: [String], required:false},
    imageURL: {type: String, required:false},
    active: {type: Boolean, default:true, required:true},
    attributes: [
        {
            key: {type: String, required: true},
            value: {type: String, required: true}
        }
    ]
}, 
    {timestamps: true}
);

module.exports = mongoose.model('Product', productSchema);