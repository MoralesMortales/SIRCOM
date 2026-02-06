from app.windows.py.purchaseWds import Ui_Form
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

from app.database.auth.get import getAllSpecificCompras, getProduct
from app.functions.tools.getIcon import getIcon  # Importar getIcon
from PyQt5 import QtWidgets

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageTemplate, Frame
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tempfile

class PurchaseView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Factura de Operación")
        
        self.adjust_tables()
        self.tableWidget.setStyleSheet("padding-left: 8px; padding-right: 8px;")
        self.btnCancelar.clicked.connect(self.close_window)
        
        # Agregar botón de descargar PDF
        self.setup_pdf_button()

    def setup_pdf_button(self):
        """Configura el botón para descargar PDF"""
        # Crear layout horizontal para los botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(250, 0, 250, 0)
        buttons_layout.setSpacing(60)
        
        # Botón Cancelar ya existe
        self.btnCancelar.setMaximumSize(QtCore.QSize(250, 16777215))
        
        # Botón Descargar PDF
        self.btnDescargarPDF = QPushButton("Descargar PDF")
        self.btnDescargarPDF.setMaximumSize(QtCore.QSize(250, 16777215))
        self.btnDescargarPDF.setObjectName("btnDescargarPDF")
        self.btnDescargarPDF.setStyleSheet("""
            QPushButton#btnDescargarPDF {
                background: #487c7e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 26px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#btnDescargarPDF:hover {
                background: #3a6365;
            }
            QPushButton#btnDescargarPDF:pressed {
                background: #2c4a4c;
            }
        """)
        self.btnDescargarPDF.clicked.connect(self.download_pdf)
        
        # Agregar botones al layout
        buttons_layout.addWidget(self.btnCancelar)
        buttons_layout.addWidget(self.btnDescargarPDF)
        
        # Reemplazar el layout horizontal_5 existente
        self.horizontalLayout_5 = buttons_layout
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

    def adjust_tables(self):
        header_producto = self.tableProducto.horizontalHeader()
        header_producto.setSectionResizeMode(QHeaderView.Stretch)
        self.tableProducto.setEditTriggers(self.tableProducto.NoEditTriggers)
        
        self.tableProducto.verticalHeader().setVisible(False)
        self.tableProducto.setSelectionMode(self.tableProducto.NoSelection) # Evita el azul al hacer click

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setShowGrid(False)
        
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.tableWidget.setSelectionMode(self.tableWidget.NoSelection)

        header_total = self.tableWidget.horizontalHeader()
        header_total.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header_total.setSectionResizeMode(1, QHeaderView.Stretch)

        # INSERTAR EL TEXTO FIJO AQUÍ
        label_item = QTableWidgetItem("TOTAL OPERACIÓN: ")
        label_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        font = label_item.font()
        font.setBold(True)
        label_item.setFont(font)
        self.tableWidget.setItem(0, 0, label_item) 
        
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: #eee;
                gridline-color: transparent;
                border: none;
                font-size: 20px;
                font-weight: bold;
                color: #222;
            }
        """)

    def openWindow(self, purchaseData):
        print("mira", purchaseData)
        if len(purchaseData) >= 6:
            code, username, fecha, hora, total, tasa_bcv = purchaseData
        else:
            code, username, fecha, hora, total = purchaseData
            tasa_bcv = 0.0
        
        self.factura_data = purchaseData  # Guardar datos para el PDF
        self.label_2.setText(f"{fecha} / {hora}")
        self.label.setText(f"Compra realizada por: {username}")
        
        # Si el label ya existe, actualizarlo
        if not hasattr(self, 'label_tasa_bcv'):
            # Crear un contenedor para ambos labels con márgenes
            self.label_container = QtWidgets.QWidget(self)
            self.label_container.setObjectName("label_container")
            
            # Layout vertical para los labels
            container_layout = QtWidgets.QVBoxLayout(self.label_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(2)  # Espacio pequeño entre labels
            
            # Label de usuario (ya existe, lo movemos al contenedor)
            self.label.setParent(self.label_container)
            container_layout.addWidget(self.label)
            
            # Crear label de tasa BCV
            self.label_tasa_bcv = QtWidgets.QLabel(self.label_container)
            self.label_tasa_bcv.setObjectName("label_tasa_bcv")
            self.label_tasa_bcv.setStyleSheet("""
                QLabel {
                    font-size: 17px;
                    font-weight: bold;
                    color: #000;
                    padding-left: 0px;
                    padding-top: 5px;
                }
            """)
            container_layout.addWidget(self.label_tasa_bcv)
            
            # Reemplazar el layout existente en verticalLayout_2
            # Primero quitamos el layout viejo
            old_item = self.verticalLayout_2.takeAt(3)  # Posición del horizontalLayout_6
            if old_item:
                old_item.widget().deleteLater()
            
            # Añadir el nuevo contenedor
            self.verticalLayout_2.insertWidget(3, self.label_container)
        
        # Actualizar el texto
        self.label_tasa_bcv.setText(f"TASA BCV: {float(tasa_bcv):,.2f} Bs/USD")
        
        self.labelTitulo.setText(f"Factura N° {code}")
        total_limpio = total.replace('$', 'Bs').strip()
        item_monto = QTableWidgetItem(total_limpio)
        item_monto.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = item_monto.font()
        font.setBold(True)
        item_monto.setFont(font)
        item_monto.setForeground(QtGui.QColor("#487c7e"))
        self.tableWidget.setItem(0, 1, item_monto)
        
        self.load_products_details(code)
        
        self.showMaximized()
    
    def format_rif(self, rif):
        """Formatea el RIF según su tipo (G-, V-, J-)"""
        if not rif:
            return ""
        
        # Convertir a string y limpiar
        value_str = str(rif).strip()
        
        # Si ya tiene formato (comienza con G-, V-, J-)
        if len(value_str) > 1 and value_str[0] in ['G', 'V', 'J'] and value_str[1] == '-':
            return value_str
        
        # Si comienza con letra pero no tiene guión
        if len(value_str) > 0 and value_str[0] in ['G', 'V', 'J']:
            if '-' not in value_str:
                # Añadir guión después de la letra
                return f"{value_str[0]}-{value_str[1:]}"
            return value_str
        
        # Si es solo número, determinar tipo basado en longitud
        # Eliminar cualquier guión o espacio
        rif_limpio = value_str.replace("-", "").replace(" ", "")
        
        if not rif_limpio.isdigit():
            return value_str  # No es numérico, devolver como está
        
        # Formatear según tipo
        if len(rif_limpio) == 9:  # RIF Jurídico: J-XXXXXXXX-X
            return f"J-{rif_limpio[:8]}-{rif_limpio[8:]}"
        elif len(rif_limpio) == 8:  # RIF Personal/Gubernamental
            # Determinar tipo basado en el primer dígito
            primer_digito = rif_limpio[0]
            if primer_digito in ['1', '2', '3', '4']:  # Personas naturales
                return f"V-{rif_limpio}"
            elif primer_digito in ['8', '9']:  # Personas jurídicas (menos común)
                return f"J-{rif_limpio}"
            elif primer_digito in ['5', '6', '7']:  # Gobierno
                return f"G-{rif_limpio}"
            else:
                return f"J-{rif_limpio}"
        else:
            # Para longitudes diferentes, formatear simple
            return f"J-{rif_limpio}"

    def load_products_details(self, code):
        raw_rows = getAllSpecificCompras(code)
        self.tableProducto.setRowCount(0)
        if raw_rows and len(raw_rows[0]) > 5:
            self.label_tasa_bcv.setText(f"TASA BCV: {raw_rows[0][5]} Bs/USD")
        else:
            self.label_tasa_bcv.setText("TASA BCV: N/A")

        if not raw_rows:
            return

        self.tableProducto.setRowCount(len(raw_rows))
        self.productos_data = []  # Guardar datos para el PDF
        
        for row_idx, row in enumerate(raw_rows):
            # Obtener data extra del producto
            p_data = getProduct(row[1]) 
            
            # --- 1. EXTRACCIÓN DE DATOS ---
            id_producto = str(row[1])
            nombre_producto = str(p_data[1]) if p_data else "N/A"
            nombre_proveedor = str(p_data[2]) if p_data else "N/A"

            rif_sucio = p_data[5]
            rif_formateado = self.format_rif(rif_sucio)
            
            cantidad = str(row[2])
            
            # --- 2. CÁLCULOS Y FORMATEO DE MONTOS ---
            total_con_iva = float(row[4])
            precio_unitario = float(row[3])
            tasa_bcv = float(row[5]) if len(row) > 5 else 0.0
            
            # Fórmulas para desglose
            subtotal_sin_iva = total_con_iva / 1.16
            monto_iva = total_con_iva - subtotal_sin_iva
            
            # Guardar datos para PDF - RIF antes del proveedor
            self.productos_data.append({
                'codigo': id_producto,
                'producto': nombre_producto,
                'rif': rif_formateado,  # RIF antes
                'proveedor': nombre_proveedor,  # Proveedor después
                'cantidad': cantidad,
                'precio_unitario': precio_unitario,
                'iva': monto_iva,
                'subtotal': subtotal_sin_iva,
                'total': total_con_iva
            })
            
            # --- 3. ASIGNACIÓN POR COLUMNA (ORDEN UI) - RIF antes del proveedor ---
            self.tableProducto.setItem(row_idx, 0, QTableWidgetItem(id_producto))
            self.tableProducto.setItem(row_idx, 1, QTableWidgetItem(nombre_producto))
            self.tableProducto.setItem(row_idx, 2, QTableWidgetItem(rif_formateado))  # RIF en columna 2
            self.tableProducto.setItem(row_idx, 3, QTableWidgetItem(nombre_proveedor))  # Proveedor en columna 3
            self.tableProducto.setItem(row_idx, 4, QTableWidgetItem(cantidad))
            self.tableProducto.setItem(row_idx, 5, QTableWidgetItem(f"{precio_unitario:,.2f} Bs"))
            self.tableProducto.setItem(row_idx, 6, QTableWidgetItem(f"{monto_iva:,.2f} Bs"))
            self.tableProducto.setItem(row_idx, 7, QTableWidgetItem(f"{subtotal_sin_iva:,.2f} Bs"))
            self.tableProducto.setItem(row_idx, 8, QTableWidgetItem(f"{total_con_iva:,.2f} Bs"))

            # --- 4. ALINEACIÓN ---
            for col in range(9):
                item = self.tableProducto.item(row_idx, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    
    def download_pdf(self):
        """Genera y descarga un PDF de la factura con logo"""
        try:
            # Obtener datos de la factura
            if not hasattr(self, 'factura_data'):
                QtWidgets.QMessageBox.warning(self, "Error", "No hay datos de factura para exportar.")
                return
            
            # Obtener el logo usando getIcon
            logo_path = getIcon("Logo.png")
            
            if not os.path.exists(logo_path):
                QtWidgets.QMessageBox.warning(self, "Logo no encontrado", 
                                            f"No se encontró el logo en: {logo_path}")
                logo_path = None
            
            code = self.factura_data[0]
            fecha_hora = self.label_2.text()
            usuario = self.label.text().replace("Compra realizada por: ", "")
            total_text = self.tableWidget.item(0, 1).text() if self.tableWidget.item(0, 1) else "0.00 Bs"
            tasa_bcv = self.label_tasa_bcv.text().replace("TASA BCV: ", "")
            
            # Crear nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"factura_{code}_{timestamp}.pdf"
            
            # Preguntar dónde guardar
            filepath, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Guardar Factura como PDF", filename, "PDF Files (*.pdf)"
            )
            
            if not filepath:
                return  # Usuario canceló
            
            # Crear el documento PDF con pie de página
            doc = SimpleDocTemplate(filepath, pagesize=letter, 
                                  leftMargin=0.75*inch, rightMargin=0.75*inch,
                                  topMargin=0.5*inch, bottomMargin=1.0*inch)  # Más margen abajo para pie
            
            # Función para pie de página
            def footer(canvas, doc):
                canvas.saveState()
                canvas.setFont('Helvetica', 8)
                canvas.setFillColor(colors.grey)
                
                # Pie de página centrado
                footer_text = f"Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} • SIRCOM"
                canvas.drawCentredString(doc.width/2 + doc.leftMargin, 0.5*inch, footer_text)
                canvas.restoreState()
            
            # Asignar pie de página
            doc.build = lambda story, **kwargs: SimpleDocTemplate.build(doc, story, onFirstPage=footer, onLaterPages=footer, **kwargs)
            
            elements = []
            
            # Estilos
            styles = getSampleStyleSheet()
            
            # Crear estilos personalizados
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=0,
                alignment=2  # Derecha
            )
            
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#7f8c8d'),
                spaceAfter=0,
                alignment=2  # Derecha
            )
            
            header_style = ParagraphStyle(
                'CustomHeader',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.HexColor('#487c7e'),
                spaceAfter=8,
                alignment=0  # Izquierda
            )
            
            # --- CABECERA CON LOGO Y TÍTULO CENTRADO VERTICALMENTE ---
            if logo_path and os.path.exists(logo_path):
                try:
                    # Crear imagen del logo
                    logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
                    
                    # Celda con logo
                    logo_cell = [[logo]]
                    logo_table = Table(logo_cell, rowHeights=[1.5*inch])
                    logo_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                    ]))
                    
                    # Celda con título - CENTRADO VERTICALMENTE con el logo
                    title_cell = [[
                        Paragraph(f"<b>FACTURA N° {code}</b>", title_style),
                    ]]
                    title_table = Table(title_cell, rowHeights=[1.5*inch])
                    title_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]))
                    
                    # Tabla de cabecera con 2 columnas - CENTRADO VERTICAL
                    header_table = Table([[logo_table, title_table]], 
                                        colWidths=[2.5*inch, 4*inch])
                    header_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # CENTRADO VERTICAL
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    
                    elements.append(header_table)
                    
                except Exception as e:
                    print(f"Error cargando logo: {e}")
                    # Si falla el logo, usar título simple
                    elements.append(Paragraph(f"FACTURA N° {code}", title_style))
                    elements.append(Paragraph(fecha_hora, subtitle_style))
            else:
                # Sin logo, solo título centrado
                elements.append(Paragraph(f"FACTURA N° {code}", title_style))
                elements.append(Paragraph(fecha_hora, subtitle_style))
            
            elements.append(Spacer(1, 10))
            
            # Línea divisoria
            elements.append(Paragraph("<hr/>", styles['Normal']))
            elements.append(Spacer(1, 10))
            
            # --- INFORMACIÓN DE LA FACTURA ---
            info_data = [
                [Paragraph("<b>Cliente:</b>", styles['Normal']), usuario],
                [Paragraph("<b>TASA BCV:</b>", styles['Normal']), tasa_bcv],
                [Paragraph("<b>Fecha y Hora:</b>", styles['Normal']), fecha_hora]
            ]
            
            info_table = Table(info_data, colWidths=[1.5*inch, 5*inch])
            info_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#487c7e')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 15))
            
            # --- TABLA DE PRODUCTOS - RIF ANTES DEL PROVEEDOR ---
            elements.append(Paragraph("<b>DETALLE DE PRODUCTOS</b>", header_style))
            elements.append(Spacer(1, 5))
            
            # Encabezados de la tabla - RIF antes del proveedor
            headers = ['Código', 'Producto', 'RIF', 'Proveedor', 'Cant.', 'P. Unit.', 'IVA', 'Subtotal', 'Total']
            
            # Datos de la tabla
            table_data = [headers]
            total_general = 0
            
            for producto in self.productos_data:
                row = [
                    producto['codigo'],
                    producto['producto'][:20] + '...' if len(producto['producto']) > 20 else producto['producto'],
                    producto['rif'],
                    producto['proveedor'][:15] + '...' if len(producto['proveedor']) > 15 else producto['proveedor'],
                    producto['cantidad'],
                    f"{producto['precio_unitario']:,.2f} Bs",
                    f"{producto['iva']:,.2f} Bs",
                    f"{producto['subtotal']:,.2f} Bs",
                    f"{producto['total']:,.2f} Bs"
                ]
                table_data.append(row)
                total_general += producto['total']
            
            # Ancho de columnas ajustado - MISMO ANCHO QUE LA TABLA DE PRODUCTOS
            col_widths = [0.5*inch, 1.2*inch, 1.0*inch, 1.2*inch, 0.4*inch, 
                         0.7*inch, 0.7*inch, 0.8*inch, 0.8*inch]
            
            product_table = Table(table_data, colWidths=col_widths, repeatRows=1)
            product_table.setStyle(TableStyle([
                # Estilo encabezados
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#487c7e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                
                # Estilo contenido
                ('ALIGN', (4, 1), (4, -1), 'CENTER'),  # Cantidad centrada
                ('ALIGN', (5, 1), (-1, -1), 'RIGHT'),  # Montos a la derecha
                ('ALIGN', (0, 1), (3, -1), 'LEFT'),    # Texto a la izquierda
                
                # Bordes
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                
                # Fondo y texto
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            
            elements.append(product_table)
            elements.append(Spacer(1, 15))
            
            # --- TOTAL GENERAL - MISMO ANCHO QUE LA TABLA DE PRODUCTOS ---
            # --- TOTAL GENERAL - 80% DEL ANCHO, CENTRADO (VERSIÓN SIMPLE) ---
            total_style = ParagraphStyle(
                'TotalStyle',
                parent=styles['Normal'],
                fontSize=16,
                textColor=colors.HexColor('#487c7e'),
                alignment=1,  # CENTRADO
                fontName='Helvetica-Bold'
            )

            # Calcular 80% del ancho
            page_width = letter[0] - doc.leftMargin - doc.rightMargin
            total_table_width = page_width * 0.80

            # Crear tabla de 1 columna con todo en una línea
            total_text_combined = f"TOTAL OPERACIÓN: {total_text}"
            total_data = [[Paragraph(f"<b>{total_text_combined}</b>", total_style)]]

            # Crear la tabla
            total_table = Table(total_data, colWidths=[total_table_width])

            # Estilo - TODO CENTRADO
            total_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#487c7e')),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, 0), 16),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 15),
                ('LINEABOVE', (0, 0), (0, 0), 1, colors.HexColor('#487c7e')),
            ]))

            # Centrar la tabla en la página
            left_padding = (page_width - total_table_width) / 2
            centered_table = Table([[total_table]], colWidths=[page_width])
            centered_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (0, 0), left_padding),
                ('RIGHTPADDING', (0, 0), (0, 0), left_padding),
            ]))

            elements.append(Spacer(1, 15))
            elements.append(centered_table)
            elements.append(Spacer(1, 20))
            
            # --- PIE DE PÁGINA - YA DEFINIDO EN LA FUNCIÓN footer ---
            # El pie de página se generará automáticamente
            
            # --- GENERAR PDF ---
            doc.build(elements)
            
            QtWidgets.QMessageBox.information(self, "PDF Generado", 
                                            f"✅ Factura guardada exitosamente en:\n{filepath}")
            
            # Abrir el PDF automáticamente
            try:
                import subprocess
                import sys
                
                if sys.platform == "win32":
                    os.startfile(filepath)
                elif sys.platform == "darwin":  # macOS
                    subprocess.call(["open", filepath])
                else:  # linux
                    subprocess.call(["xdg-open", filepath])
            except Exception as e:
                print(f"No se pudo abrir el PDF: {e}")
                    
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", 
                                         f"No se pudo generar el PDF:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def close_window(self):
        from app.views.management.history.HistoryView import HistoryView
        self.history = HistoryView()
        self.history.showMaximized()
        self.close()