from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import qrcode


def create_ticket(date_of_film, date_purchased, name, film, time, screen, seat, price, card, transaction_id, id_required, certificate):

    # name the ticket after the person
    pdf_name = "app/utilities/tickets/ticket.pdf"
    canvas = Canvas(pdf_name, pagesize=A4)

    left_aligned = 60
    right_aligned = 400
    page_height = 800
    default_font = "Helvetica-Bold"
    def_size = 10

    # set the font
    canvas.setFont(default_font, def_size)

    # make the film title bigger
    canvas.setFont(default_font, 20)

    # write film
    canvas.drawString(left_aligned, 0.9*page_height, film)

    # set the font back to default
    canvas.setFont(default_font, def_size)

    # write date
    canvas.drawString(left_aligned+50, 0.87*page_height, date_of_film)

    # write time
    canvas.drawString(left_aligned, 0.87*page_height, time + ",")

    # write screen
    canvas.drawString(left_aligned, 0.85*page_height, "Screen: " + seat)

    # write seat
    canvas.drawString(left_aligned, 0.83*page_height, "Seat(s): " + screen)

    # writes id message
    canvas.drawString(left_aligned, 0.81*page_height, "ID Required: " + id_required)

    # writes certificate
    canvas.drawString(left_aligned, 0.79*page_height, "Certificate: " + certificate)


    # make the transaction title bigger
    canvas.setFont(default_font, 20)

    # transaction title
    canvas.drawString(left_aligned, 0.75*page_height, "Transaction details")

    # set the font back to default
    canvas.setFont(default_font, def_size)

    # write name
    canvas.drawString(left_aligned, 0.72*page_height, "Name: " + name)


    # write price
    canvas.drawString(left_aligned, 0.7*page_height, "Paid: " + price)


    # write purchase date
    canvas.drawString(left_aligned, 0.68*page_height, "Date of purchase: "+ date_purchased)

    # create and draw qr code
    img = qrcode.make(transaction_id)
    img_name = "app/utilities/tickets/qr.png"
    img.save(img_name)
    logo = ImageReader(img_name)
    canvas.drawImage(logo, 10,200, mask='auto')

    #add cinema logo
    image = "app/static/images/app_static_images_dadpad_small.png"
    logo = ImageReader(image)
    canvas.drawImage(logo, left_aligned, 0.95*page_height, mask="auto")

    canvas.save()
