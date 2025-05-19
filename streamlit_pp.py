import streamlit as st
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

def get_price(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        price_whole = soup.select_one('span.a-price-whole')
        price_fraction = soup.select_one('span.a-price-fraction')

        if price_whole:
            whole = price_whole.get_text().strip().replace(',', '').replace('.', '')
            fraction = price_fraction.get_text().strip() if price_fraction else "00"
            price_text = f"{whole}.{fraction}"
            return float(price_text)
        return None
    except Exception as e:
        st.error(f"Error fetching price: {e}")
        return None

def send_email(subject, body, recipient_email):
    gmail_user = 'annamanenisai3015@gmail.com'
    gmail_password = 'rnwx mdjg woju uzpp'  # 🔐 Consider moving to Streamlit Secrets for security

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = recipient_email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient_email, msg.as_string())
        server.quit()
        st.success("✅ Email sent successfully!")
    except Exception as e:
        st.error(f"Email failed: {e}")

# Streamlit UI
st.title("📉 Amazon Price Tracker")

url = st.text_input("Enter Amazon Product URL:")
target_price = st.number_input("Set Target Price (INR):", min_value=1)
user_email = st.text_input("Enter your Email for Notification:")
email_alert = st.checkbox("Send Email Notification")

if st.button("Check Price Now"):
    if url and target_price:
        current_price = get_price(url)
        if current_price:
            st.write(f"💰 Current Price: ₹{current_price}")
            if current_price < target_price:
                st.success("✅ Price is below target!")
                if email_alert:
                    if user_email:
                        subject = "📉 Amazon Price Drop Alert!"
                        body = f"The price dropped to ₹{current_price}!\nBelow your target of ₹{target_price}.\nCheck it out:\n{url}"
                        send_email(subject, body, user_email)
                    else:
                        st.warning("⚠️ Please enter your email address to receive alerts.")
            else:
                st.warning("❌ Price is still above target.")
        else:
            st.error("❌ Failed to fetch the current price. Make sure the product URL is correct.")
    else:
        st.warning("⚠️ Please provide both a valid URL and a target price.")
