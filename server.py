from flask import Flask, send_file, request
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

class PDF(FPDF):

    def background(self, name, x, y, w, h):
        self.image(name, x, y, w, h)

    
    def date(self, text, bold, x, y, sizeFont):
        self.set_xy(x, y)
        self.set_text_color(0, 44, 118)
        self.set_font('Arial', bold, sizeFont)
        self.multi_cell(0, 10, text)

    def text(self, text, bold, x, y, sizeFont):
        self.set_xy(x, y)
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', bold, sizeFont)
        self.multi_cell(0, 5, text)


def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    day = date.day
    month = months[date.month - 1]
    year = date.year
    messsage = "{} de {} del {}".format(day, month, year)

    return messsage
        

@app.route('/pdf', methods=['POST'])
def DownloadPDF():

    diaRegistro = current_date_format(datetime.now())
    distancia_x = 25
    textoNombreEmpresa = 'ANDREYDEVS S.A.S'
    textoConstar = 'HACE CONSTAR'
    nombreEmpleado = request.get_json()['nombreEmpleado']
    cedulaEmpleado = request.get_json()['cedulaEmpleado']
    salarioEmpleado = request.get_json()['salarioEmpleado']
    fechaInicioEmpleado = current_date_format(datetime.strptime(request.get_json()['fechaInicioEmpleado'], '%d/%m/%Y'))
    fechaFinEmpleado = current_date_format(datetime.strptime(request.get_json()['fechaFinEmpleado'], '%d/%m/%Y'))
    textoPrincipal = 'Que el (a) Señor (a), {}, con Cédula de Ciudadanía No. {}, laboró con nosotros desde {} hasta el {}, desempeñándose como Desarrollador Full-Stack con Angular - Python, con un salario ordinario de {} COP con contrato a termino indefinido.\n\nEn caso de requerir validación a esta información, por favor comunicarse con Andrey Herrera al celular 3134508305 o através del correo electrónico empleo@andreydevs.com'.format(nombreEmpleado, cedulaEmpleado, fechaInicioEmpleado, fechaFinEmpleado, salarioEmpleado)
    textoPresente = 'La presente se expide el {} a solicitud del interesado.'.format(diaRegistro)
    textoAtentamente = 'Atentamente,'
    textoFirma = 'Wolfang Andrey Herrera Casallas'
    textoFirmaSecundario = 'CEO de AndreyDevs'

    pdf = PDF(orientation='P',format='A4', unit='mm')
    pdf.add_page()
    pdf.background('static/formato-pdf.jpg', 0, 0, 215, 285)
    pdf.set_margins(top = 40, left = 15, right = 35)

    pdf.date(str(diaRegistro), 'B', distancia_x, 60, 10)
    pdf.text(textoNombreEmpresa, 'B', distancia_x + 54, 80, 12)
    pdf.text(textoConstar, 'B',distancia_x + 58, 100, 12)
    pdf.text(textoPrincipal, '', distancia_x, 120, 12)
    pdf.text(textoPresente, '',distancia_x, 177, 12)
    pdf.text(textoAtentamente, '', distancia_x, 195, 12)
    pdf.text(textoFirma, 'B', distancia_x, 222, 10)
    pdf.text(textoFirmaSecundario, '', distancia_x, 227, 10)

    download_pdf = BytesIO(pdf.output())

    return send_file(download_pdf, download_name="Certificado Laboral - {}.pdf".format(nombreEmpleado), as_attachment=True)
        
    
if __name__ == '__main__':
    app.run(port = 3000, debug = True)