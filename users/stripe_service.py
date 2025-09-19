import stripe
from django.conf import settings


def create_stripe_product(name, description):
    """Создание продукта в Stripe"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    product = stripe.Product.create(
        name=name,
        description=description
    )
    return product.id


def create_stripe_price(product_id, amount, currency='rub'):
    """Создание цены в Stripe"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),  # Конвертируем в копейки
        currency=currency
    )
    return price.id


def create_stripe_checkout_session(price_id, success_url, cancel_url):
    """Создание сессии оплаты в Stripe"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url, session.id


def get_stripe_session_status(session_id):
    """Получение статуса сессии оплаты из Stripe"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session['payment_status']  # 'paid', 'unpaid', 'no_payment_required'
    except stripe.error.StripeError as e:
        # Логируем ошибку для дебага
        print(f"Stripe API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None