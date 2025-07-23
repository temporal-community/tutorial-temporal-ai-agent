import os

from dotenv import load_dotenv


def ensure_customer_exists(
    customer_id: str = "", email: str = "default@example.com"
) -> str:
    """Ensure a Stripe customer exists; create one if not."""
    import stripe

    if customer_id != "":
        try:
            stripe.Customer.retrieve(customer_id)
            return customer_id
        except stripe.InvalidRequestError:
            # Customer ID is invalid or doesn't exist
            pass

    # Create a new customer if no valid customer_id
    customer = stripe.Customer.create(email=email)
    return customer.id


def create_invoice(args: dict) -> dict:
    """Create and finalize a Stripe invoice."""
    import stripe

    load_dotenv(override=True)  # Load environment variables from a .env file

    stripe.api_key = os.getenv("STRIPE_API_KEY")
    # If an API key exists in the env file, find or create customer
    if stripe.api_key is not None and stripe.api_key != "":
        customer_id = ensure_customer_exists(
            args.get("customer_id", ""), args.get("email", "default@example.com")
        )

        # Get amount and convert to cents
        amount = args.get("amount", 200.00)  # Default to $200.00
        try:
            amount_cents = int(float(amount) * 100)
        except (TypeError, ValueError):
            return {"error": "Invalid amount provided. Please confirm the amount."}

        # Create an invoice item
        stripe.InvoiceItem.create(
            customer=customer_id,
            amount=amount_cents,
            currency="usd",
            description=args.get("tripDetails", "Service Invoice"),
        )

        # Create and finalize the invoice
        invoice = stripe.Invoice.create(
            customer=customer_id,
            collection_method="send_invoice",  # Invoice is sent to the customer
            days_until_due=args.get("days_until_due", 7),  # Default due date: 7 days
            pending_invoice_items_behavior="include",  # No pending invoice items
        )

        finalized_invoice = stripe.Invoice.finalize_invoice(invoice.id)

        return {
            "invoiceStatus": finalized_invoice.status,
            "invoiceURL": finalized_invoice.hosted_invoice_url,
            "reference": finalized_invoice.number,
        }
    # if no API key is in the env file, return dummy info
    else:
        print("[CreateInvoice] Creating invoice with:", args)
        return {
            "invoiceStatus": "generated",
            "invoiceURL": "https://pay.example.com/invoice/12345",
            "reference": "INV-12345",
        }
