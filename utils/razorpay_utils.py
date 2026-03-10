import razorpay
from flask import current_app
import hmac
import hashlib

def get_razorpay_client():
    """Initialize and return Razorpay client"""
    client = razorpay.Client(
        auth=(
            current_app.config['RAZORPAY_KEY_ID'],
            current_app.config['RAZORPAY_KEY_SECRET']
        )
    )
    return client

def create_razorpay_order(amount, order_id, user_email, user_phone):
    """
    Create a Razorpay order
    
    Args:
        amount: Amount in rupees (will be converted to paise)
        order_id: Your order ID
        user_email: Customer email
        user_phone: Customer phone
    
    Returns:
        dict: Razorpay order details
    """
    try:
        client = get_razorpay_client()
        
        # Amount should be in paise (multiply by 100)
        amount_in_paise = int(amount * 100)
        
        order_data = {
            'amount': amount_in_paise,
            'currency': 'INR',
            'receipt': f'receipt#{order_id}',
            'notes': {
                'order_id': str(order_id),
                'email': user_email,
                'phone': user_phone
            }
        }
        
        razorpay_order = client.order.create(data=order_data)
        print(f"Razorpay order created: {razorpay_order['id']}")
        return razorpay_order
    
    except Exception as e:
        print(f"Error creating Razorpay order: {str(e)}")
        raise

def verify_razorpay_payment(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """
    Verify Razorpay payment signature using HMAC SHA256
    
    Args:
        razorpay_order_id: Order ID from Razorpay
        razorpay_payment_id: Payment ID from Razorpay
        razorpay_signature: Signature from Razorpay
    
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        # Create the message to verify
        message = f"{razorpay_order_id}|{razorpay_payment_id}"
        
        # Get the secret key
        secret_key = current_app.config['RAZORPAY_KEY_SECRET']
        
        # Create HMAC SHA256 signature
        generated_signature = hmac.new(
            secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        print(f"Generated signature: {generated_signature}")
        print(f"Received signature: {razorpay_signature}")
        
        # Compare signatures
        if generated_signature == razorpay_signature:
            print("✅ Signature verification successful!")
            return True
        else:
            print("❌ Signature mismatch!")
            return False
    
    except Exception as e:
        print(f"Error verifying payment: {str(e)}")
        return False

def get_payment_details(payment_id):
    """Get payment details from Razorpay"""
    try:
        client = get_razorpay_client()
        payment = client.payment.fetch(payment_id)
        return payment
    except Exception as e:
        print(f"Error fetching payment details: {str(e)}")
        raise