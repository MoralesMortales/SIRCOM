import sqlite3
from app.database.connect import connectDB

def getAllProducts():
    connection = connectDB()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT 
            p.codigo,
            p.nombre AS nombreProducto,
            p.descripcion,
            p.stock,
            pr.rif,
            pr.nombreEmpresa,
            p.precioUnitario,
            p.descuento,
            p.descuentoDesde,
            p.stockMinimo,
            p.compraEstado
        FROM producto p 
        JOIN proveedor pr ON p.rifProveedor = pr.rif 
        WHERE pr.estado = 1 
        AND p.estado = 1
        AND p.stock > 0
        -- EXCLUIR productos que ya están en compras "En Curso"
        AND NOT EXISTS (
            SELECT 1 
            FROM detalleCompra dc
            JOIN compra c ON dc.idCompra = c.idCompra
            WHERE dc.codigoProducto = p.codigo 
            AND c.estado = 'En Curso'
        )
    """)
    
    rows = cursor.fetchall()
    connection.close()
    return rows