# Agora B2B Database Design
## Supplier
### Supplier
- **supplier_id** (Primary Key, UUID)
- company (Charfield, Unique)
- phone (Charfield, max_length=10)
- city(Charfield)
- tin(Charfield, max_length=9)
   - Description: The Tax Identification Number (TIN) associated with the entity.
- summary(Textfield)

- created_at (DateTimeField)
- updated_at (DateTimeField)


### Shop
- **shop_id** (Primary Key, UUID)
- shop_code (CharField)
- assigned (Bool)

- created_at (DateTimeField)
- updated_at (DateTimeField)


### SupplierShop
- **supplier_shop_id** (Primary Key, UUID)
- supplier (ForeignKey to Supplier)
- shop (ForeignKey to Shop)

- created_at (DateTimeField)
- updated_at (DateTimeField)

## Product

### Category
- **category_id** (Primary Key, UUID)
- category_name (CharField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### Variant
- **variant_id** (Primary Key, UUID)
- variant_name (CharField)
- summary(Textfield)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### Product
- **product_id** (Primary Key, UUID)
- category (ForeignKey to Category)
- variant (ForeignKey to Variant)
- product_name (CharField)
- quality(CharField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

## Order

### Order
- **order_id** (Primary Key, UUID)
- total_costs (DecimalField)
- total_taxes (DecimalField)
- additional_costs (DecimalField)
- total-amount (DecimalField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### OrderItem
- **order_item_id** (Primary Key, UUID)
- product (ForeignKey to Product)
- shop (ForeignKey to Shop)
- order (ForeignKey to Order)
- source (CharField)
- quantity (DecimalField)
- unit_price (DecimalField)
- amount (DecimalField)
- tax_rate (DecimalField)
- taxes (DecimalField)
- total (DecimalField)
## Payment
### PayeeType
- **payee_type_id** (Primary Key, UUID)
- label (CharField)

### Payee
- **payee_id** (Primary Key, UUID)
- name (CharField)
- payee_type (ForeignKey to PayeeType)
- summary(CharField)
- active(Bool)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### Payment
- **payment_id** (Primary Keyy, UUID)
- payee (ForeignKey to Payee)
- amount (DecimalField)
- summary(CharField)
- payment_day (DateTimeField)
- paid(Bool)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### Source
- **source_id** (Primary Key, UUID)
- source (CharField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### Income
- **income_id** (Primary Key, UUID)
- source (ForeignKey to Source)
- amount (DecimalField)
- income_date (DateTimeField)
- summary(CharField)
- created_at (DateTimeField)
- updated_at (DateTimeField)



## Abstract Class

### TimeStampedModel
- **id** (Primary Key, UUID)
- created_at (DateTimeField)
- updated_at (DateTimeField)

All tables use `uuid` as their primary key. Each model inherits from the abstract class `TimeStampedModel` to include the common fields `created_at` and `updated_at` for tracking timestamps.
