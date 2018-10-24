import smtplib
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver


class HTTPServerRequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        # Hier voer je een functie uit om een encrypted verbinding te maken met de google smtp mail server. Je krijgt een object terug waar je mee kan werken
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        # Hier log je in
        server.login("Alarmcentrale.CSN@gmail.com", "alarmcentralecsn1")

        # Hier verzend je een de email en geef je de argumenten van wie het komt en naar wie het moet gaan. De from address moet normaal gesproken de url van de server zijn die het verstuurd, anders loop je risico om in de spam te komen. Voor ons maakt het niet uit wat door staat
        server.sendmail(
            "Alarmcentrale.CSN@gmail.com",
            "kenrick_half8@hotmail.com",
            "Het alarm is afgegaan.")

        # Hier sluit je de verbinding met de smtp mail server
        server.quit()

        self.send_response_only(200)
        return


def run():
    with socketserver.TCPServer(("", 8000), HTTPServerRequestHandler) as httpd:
        print("serving at port", 8000)
        httpd.serve_forever()


run()
