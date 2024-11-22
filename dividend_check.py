import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define a function to fetch upcoming  dividend dates
def fetch_upcoming_dividends(stock_list):
    url = 'https://www.moneycontrol.com/stocks/marketinfo/dividends_declared/index.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch data from Moneycontrol.")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    dividend_table = soup.find('table', class_='b_12 dvdtbl')
    if not dividend_table:
        print("Dividend table not found on the page.")
        return None

    # Extract data
    data = []
    for row in dividend_table.find_all('tr')[2:]:
        columns = row.find_all('td')
        if len(columns) >= 6:
            stock_name = columns[0].text.strip()
            ex_date_str = columns[5].text.strip()
            try:
                ex_date = datetime.strptime(ex_date_str, '%d-%m-%Y').date()
            except ValueError:
                continue
            if stock_name.upper() in stock_list and ex_date >= datetime.now().date():
                data.append({"Stock": stock_name, "Upcoming Dividend Date": ex_date})

    dividend_df = pd.DataFrame(data)
    return dividend_df

# Function to send an email
def send_email(dividend_df):
    sender_email = "samar03042000@gmail.com"       # Replace with your email
    receiver_email = "ksamarasimhareddy88@gmail.com" # Replace with recipient's email
    password = "oehk scmc vxwe skkh"                    # Replace with your email password
    
    # Create email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Upcoming Dividend Dates for Selected Stocks"
    
    if dividend_df.empty:
        html = "No upcoming dividends found for the specified stocks."
    else:
        html = dividend_df.to_html(index=False)  # Convert DataFrame to HTML
    
    # Attach HTML content
    message.attach(MIMEText(html, "html"))

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

# Define the list of stocks
stock_list = [
    'BHEL', 'BPCL', 'COAL INDIA', 'DWARKESH', 'FCONSUMER', 'GAIL', 'HINDZINC', 
    'HUDCO', 'IEX', 'IOC', 'IRBINVIT', 'JUBZ FOOD', 'MAWANA SUG', 'NBCC', 
    'NHPC', 'NMDC', 'NTPC', 'ONGC', 'PAINVIT', 'PURVA', 'RAJNISH', 'ROOM', 
    'SAIL', 'TATA POWER', 'TATASTEEL', 'TRIDENT', 'VEDL'
]

# Fetch and send data
dividend_df = fetch_upcoming_dividends(stock_list)
if dividend_df is not None:
    send_email(dividend_df)
