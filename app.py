import streamlit as st
import requests
from datetime import datetime
import pytz

def get_exchange_rate():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        data = response.json()
        base_rate = data['rates']['CAD']
        # Add 2% to the exchange rate
        return base_rate * 1.02
    except:
        return 1.35 * 1.02  # Fallback rate with 2% added

def calculate_costs(units, price_per_unit, freight, exchange_rate, duty_rate, brokerage, markup):
    # Base calculations
    subtotal = units * price_per_unit
    total_with_freight = subtotal + freight
    
    # Exchange calculations
    exchange_amount = total_with_freight * (exchange_rate - 1)
    total_with_exchange = total_with_freight + exchange_amount
    
    # Duty and brokerage
    duty_amount = total_with_exchange * (duty_rate / 100)
    total_with_brokerage = total_with_exchange + duty_amount + brokerage
    
    # Cost per unit and markup
    cost_each = total_with_brokerage / units
    markup_amount = total_with_brokerage * (markup / 100)
    total_selling_price = total_with_brokerage + markup_amount
    
    # Price each calculations
    price_each = total_selling_price / units
    
    return {
        "subtotal": subtotal,
        "total_with_freight": total_with_freight,
        "exchange_amount": exchange_amount,
        "total_with_exchange": total_with_exchange,
        "duty_amount": duty_amount,
        "total_with_brokerage": total_with_brokerage,
        "cost_each": cost_each,
        "markup_amount": markup_amount,
        "total_selling_price": total_selling_price,
        "price_each": price_each
    }

def main():
    st.title("Price Calculator")
    
    # Get current exchange rate
    exchange_rate = get_exchange_rate()
    
    # Current date
    current_date = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d')
    st.write(f"Date: {current_date}")
    st.write(f"Current USD to CAD Rate: {exchange_rate:.2f}")
    
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("Product Name", "")
        units = st.number_input("Units", min_value=1, value=33)
        price_per_unit = st.number_input("Price per Unit ($)", min_value=0.0, value=0.0)
        freight = st.number_input("Freight ($)", min_value=0.0, value=0.0)
    
    with col2:
        duty_rate = st.number_input("Duty Rate (%)", min_value=0.0, value=0.0)
        brokerage = st.number_input("Brokerage ($)", min_value=0.0, value=130.00)
        markup = st.number_input("Markup (%)", min_value=0.0, value=50.0)
        client = st.text_input("Client", "")

    if st.button("Calculate"):
        results = calculate_costs(
            units, price_per_unit, freight, exchange_rate,
            duty_rate, brokerage, markup
        )
        
        # Display results
        st.write("---")
        st.subheader("Calculation Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"Subtotal: ${results['subtotal']:,.2f}")
            st.write(f"Freight: ${freight:,.2f}")
            st.write(f"Total w/Freight: ${results['total_with_freight']:,.2f}")
            st.write(f"Exchange ({((exchange_rate-1)*100):.1f}%): ${results['exchange_amount']:,.2f}")
            st.write(f"Total w/Exchange: ${results['total_with_exchange']:,.2f}")
        
        with col2:
            st.write(f"Duty ({duty_rate}%): ${results['duty_amount']:,.2f}")
            st.write(f"Brokerage: ${brokerage:,.2f}")
            st.write(f"Total Cost w/Brokerage: ${results['total_with_brokerage']:,.2f}")
            st.write(f"Total Cost Each: ${results['cost_each']:,.2f}")
            st.write(f"Markup ({markup}%): ${results['markup_amount']:,.2f}")
        
        st.write("---")
        st.subheader("Final Pricing")
        st.write(f"Total Selling Price: ${results['total_selling_price']:,.2f}")
        st.write(f"Price Each: ${results['price_each']:,.2f}")

if __name__ == "__main__":
    main()
