# -*- coding: utf-8 -*-
# @Time    : 5/9/24 13:25
# @Author  : Antoni Joan Morlà
# @Email   : amorvan23a@gmail.com
# @File    : certi_generator.py
# @Copiright: Its use, sale or distribution is prohibited without the authorization of the author.

import sys
import os
from OpenSSL import crypto
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QComboBox, QFileDialog
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta
import zipfile

# Duración de la validez del certificado en días (4 años)
CERT_DURATION_DAYS = 4 * 365


# Función para sanitizar la entrada
def sanitize_input(input_str):
    return ''.join(c for c in input_str if c.isalnum() or c in (' ', '-'))


def generate_certificate(cif, company_name, algorithm):
    # Sanitizamos las entradas
    cif = sanitize_input(cif)
    company_name = sanitize_input(company_name)

    # Crear un par de claves
    key = crypto.PKey()
    if algorithm == "RSA":
        key.generate_key(crypto.TYPE_RSA, 2048)
    elif algorithm == "EC":
        key.generate_key(crypto.TYPE_EC, 256)

    # Crear el certificado autofirmado
    cert = crypto.X509()
    cert.get_subject().C = "ES"  # País
    cert.get_subject().serialNumber = cif  # CIF de la empresa
    cert.get_subject().CN = company_name  # Nombre de la empresa

    # Añadir metainformación personalizada
    cert.get_subject().O = company_name  # Organización
    cert.get_subject().OU = "Departamento de TI"  # Unidad organizativa

    cert.set_serial_number(1000)

    # Fechas de emisión y caducidad
    cert.gmtime_adj_notBefore(0)  # Fecha de emisión (ahora)
    cert.gmtime_adj_notAfter(CERT_DURATION_DAYS * 24 * 60 * 60)  # Validez definida en días

    # Firmar el certificado con la clave privada
    cert.set_issuer(cert.get_subject())  # Emisor y sujeto son la misma entidad (autofirmado)
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')

    # Nombres de los archivos
    private_key_filename = f"private_key_{cif}.pem"
    public_key_filename = f"public_key_{cif}.pem"
    certificate_filename = f"certificate_{cif}.crt"
    txt_filename = f"{cif}-crt.txt"

    # Guardar las claves y el certificado
    with open(private_key_filename, "wb") as private_key_file:
        private_key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

    with open(public_key_filename, "wb") as public_key_file:
        public_key_file.write(crypto.dump_publickey(crypto.FILETYPE_PEM, key))

    with open(certificate_filename, "wb") as certificate_file:
        certificate_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    # Generar el archivo txt que contendrá el certificado completo
    with open(txt_filename, "w") as txt_file:
        txt_file.write(f"Nombre de la empresa: {company_name}\n")
        txt_file.write(f"CIF: {cif}\n")
        txt_file.write(f"Fecha de emisión: {datetime.now().strftime('%Y-%m-%d')}\n")
        txt_file.write(
            f"Fecha de caducidad: {(datetime.now() + timedelta(days=CERT_DURATION_DAYS)).strftime('%Y-%m-%d')}\n")
        txt_file.write("Certificado completo:\n")
        txt_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8'))

    # Crear el archivo ZIP
    zip_filename = f"{company_name}_{cif}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(private_key_filename)
        zipf.write(public_key_filename)
        zipf.write(certificate_filename)
        zipf.write(txt_filename)

    # Eliminar los archivos temporales después de empaquetar
    os.remove(private_key_filename)
    os.remove(public_key_filename)
    os.remove(certificate_filename)
    os.remove(txt_filename)

    return zip_filename, cert, key


def verify_public_key(cert, key):
    public_key_from_cert = cert.get_pubkey()
    return crypto.dump_publickey(crypto.FILETYPE_PEM, public_key_from_cert) == crypto.dump_publickey(
        crypto.FILETYPE_PEM, key)


def verify_private_key_with_signature(cert, key):
    try:
        # Crear un texto arbitrario
        message = b"Test message for signing"

        # Firmar el mensaje con la clave privada
        signature = crypto.sign(key, message, 'sha256')

        # Verificar la firma con la clave pública del certificado
        crypto.verify(cert, signature, message, 'sha256')

        return True
    except crypto.Error:
        return False


class CertApp(QWidget):
    def __init__(self):
        super().__init__()

        self.zip_filename = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.cif_label = QLabel("CIF de la Empresa:")
        self.cif_input = QLineEdit(self)

        self.name_label = QLabel("Nombre de la Empresa:")
        self.name_input = QLineEdit(self)

        self.algorithm_label = QLabel("Algoritmo:")
        self.algorithm_combo = QComboBox(self)
        self.algorithm_combo.addItems(["RSA", "EC"])

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)

        self.generate_button = QPushButton("Generar Certificado", self)
        self.generate_button.clicked.connect(self.generate_certificate)

        self.download_button = QPushButton("Descargar Certificado (ZIP)", self)
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.download_cert)

        layout.addWidget(self.cif_label)
        layout.addWidget(self.cif_input)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.algorithm_label)
        layout.addWidget(self.algorithm_combo)
        layout.addWidget(self.log_output)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.download_button)

        self.setLayout(layout)
        self.setWindowTitle("Generador de Certificados")

        # Ajustar el tamaño de la ventana al 50% de altura y 30% de ancho de la pantalla
        screen_geometry = QApplication.desktop().screenGeometry()
        width = screen_geometry.width() * 0.3
        height = screen_geometry.height() * 0.5
        self.setGeometry(300, 300, int(width), int(height))

    def append_log(self, message, color=None):
        if color:
            self.log_output.setTextColor(color)
        self.log_output.append(message)
        self.log_output.setTextColor(QColor(0, 0, 0))  # Reset color to black

    def generate_certificate(self):
        cif = self.cif_input.text()
        company_name = self.name_input.text()
        algorithm = self.algorithm_combo.currentText()

        if not cif or not company_name:
            QMessageBox.warning(self, "Error", "Por favor, rellene todos los campos.")
            return

        try:
            self.append_log(f"Iniciando la generación del certificado para {company_name} con CIF {cif}...")
            self.zip_filename, cert, key = generate_certificate(cif, company_name, algorithm)

            # Verificar la clave pública
            if verify_public_key(cert, key):
                self.append_log("Verificación de clave pública: Correcto (la clave pública es válida).",
                                QColor(0, 128, 0))  # Verde
            else:
                self.append_log("Verificación de clave pública: Error (la clave pública no es válida).",
                                QColor(255, 0, 0))  # Rojo

            # Verificar la clave privada con una firma
            self.append_log("Verificando firma con clave privada...")
            if verify_private_key_with_signature(cert, key):
                self.append_log("Verificación de clave privada: Correcto (la firma es válida).",
                                QColor(0, 128, 0))  # Verde
            else:
                self.append_log("Verificación de clave privada: Error (la firma no es válida).",
                                QColor(255, 0, 0))  # Rojo

            # Fecha de caducidad
            expiry_date = datetime.now() + timedelta(days=CERT_DURATION_DAYS)
            self.append_log(f"Fecha de caducidad del certificado: {expiry_date.strftime('%Y-%m-%d')}")
            self.append_log(
                f"Advertencia: El certificado dejará de funcionar en esta fecha. Deberás generar uno nuevo para seguir utilizándolo.",
                QColor(255, 0, 0))  # Rojo

            self.download_button.setEnabled(True)
        except Exception as e:
            self.append_log(f"Error al generar el certificado: {str(e)}", QColor(255, 0, 0))

    def download_cert(self):
        if self.zip_filename:
            save_path = QFileDialog.getSaveFileName(self, "Guardar ZIP", self.zip_filename, "ZIP Files (*.zip)")[0]
            if save_path:
                os.rename(self.zip_filename, save_path)
                self.append_log(f"Certificado descargado en: {save_path}")
        else:
            self.append_log("No hay ningún certificado para descargar.", QColor(255, 0, 0))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cert_app = CertApp()
    cert_app.show()
    sys.exit(app.exec_())