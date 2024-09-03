import os
import subprocess
import requests

def ping_server(ip):
    """Realiza un ping al servidor y devuelve True si está accesible."""
    try:
        output = subprocess.run(['ping', '-c', '4', ip], capture_output=True, text=True)
        if "0% packet loss" in output.stdout:
            # Parse the average latency
            latency_line = [line for line in output.stdout.splitlines() if "avg" in line]
            avg_latency = latency_line[0].split('/')[4] if latency_line else 'N/A'
            return True, avg_latency
        else:
            return False, 'N/A'
    except Exception as e:
        return False, 'N/A'

def generate_report(servers):
    """Genera un reporte de accesibilidad y latencia de cada servidor."""
    report = []
    for server in servers:
        accessible, latency = ping_server(server)
        status = "Online" if accessible else "Offline"
        report.append(f"Server: {server}, Status: {status}, Avg Latency: {latency} ms")
    return "\n".join(report)

def send_email(report, email_address, api_key, domain):
    """Envía el reporte a la dirección de correo electrónico especificada."""
    url = f"https://api.mailgun.net/v3/{domain}/messages"
    data = {
        "from": f"Server Report <mailgun@{domain}>",
        "to": email_address,
        "subject": "Server Accessibility Report",
        "text": report
    }

    response = requests.post(url, auth=("api", api_key), data=data)
    return response.status_code == 200

def main():
    servers = ['192.168.1.1', '192.168.1.2', '192.168.1.3']  # Reemplaza con tus direcciones IP
    email_address = "destination@example.com"  # Reemplaza con la dirección de correo
    api_key = "your-mailgun-api-key"  # Reemplaza con tu API Key de Mailgun
    domain = "your-mailgun-domain"  # Reemplaza con tu dominio de Mailgun

    report = generate_report(servers)
    print("Generated Report:\n", report)

    success = send_email(report, email_address, api_key, domain)
    if success:
        print("Report sent successfully.")
    else:
        print("Failed to send report.")

if __name__ == "__main__":
    main()


# Con ciertas librerias especiales

import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Lista de direcciones IP de los servidores
servers = ["192.168.1.1", "192.168.1.2", "8.8.8.8"]  # Reemplaza con las direcciones IP de los servidores

def ping_server(ip):
    try:
        output = subprocess.check_output(["ping", "-c", "4", ip], stderr=subprocess.STDOUT)
        output = output.decode()
        if "0% packet loss" in output:
            latency = output.split("rtt min/avg/max/mdev = ")[1].split("/")[1]
            return True, latency
        else:
            return False, None
    except subprocess.CalledProcessError:
        return False, None

def generate_report():
    report = "Server Accessibility Report\n\n"
    for server in servers:
        online, latency = ping_server(server)
        if online:
            report += f"Server {server} is online with average latency {latency} ms\n"
        else:
            report += f"Server {server} is offline\n"
    return report

def send_email(report, recipient_email):
    sender_email = "your_email@example.com"  # Reemplaza con tu dirección de correo electrónico
    password = "your_password"  # Reemplaza con tu contraseña de correo electrónico

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Server Accessibility Report"
    
    msg.attach(MIMEText(report, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Reemplaza con tu servidor SMTP
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Report sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    report = generate_report()
    recipient_email = "recipient@example.com"  # Reemplaza con la dirección de correo del destinatario
    send_email(report, recipient_email)

