import os
from datetime import datetime as dt
import json

dir = os.path.dirname(__file__)

primera_linea  = True
dias_laborales = [0,1,2,3,4]
t              = None
cnt            = 0
es_laboral     = '0'
est            = ''
clas           = '0'
en_pandemia    = '0'

frds =  [    '2025/01/01','2025/03/03','2025/03/04','2025/03/24','2025/04/02','2025/04/18'
            ,'2025/05/01','2025/05/02','2025/05/25','2025/06/16','2025/06/20','2025/07/09'
            ,'2025/08/15','2025/08/17','2025/10/10','2025/11/21','2025/11/24','2025/12/08','2025/12/25'

            ,'2021/01/01','2021/02/15','2021/02/16','2021/03/24','2021/04/02'
            ,'2021/05/01','2021/05/24','2021/05/25','2021/06/20','2021/06/21','2021/07/09','2021/08/16'
            ,'2021/10/08','2021/10/11','2021/11/20','2021/11/22','2021/12/08','2021/12/25'

            ,'2022/01/01','2022/02/28','2022/03/01','2022/03/24','2022/04/02','2022/04/15'
            ,'2022/05/01','2022/05/25','2022/06/17','2022/06/20','2022/07/09','2022/08/15'
            ,'2022/10/07','2022/10/10','2022/11/20','2022/11/21','2022/12/08','2022/12/09','2022/12/25'

            ,'2023/01/01','2023/02/20','2023/02/21','2023/03/24','2023/04/02','2023/04/06','2023/04/07'
            ,'2023/05/01','2023/05/25','2023/06/17','2023/06/20','2023/07/09','2023/08/17'
            ,'2023/10/12','2023/11/20','2023/12/08','2023/12/25'

            ,'2024/01/01','2024/02/12','2024/02/13','2024/03/24','2024/04/24','2024/04/28','2024/04/29'
            ,'2024/05/01','2024/05/25','2024/06/17','2024/06/20','2024/06/21','2024/07/09','2024/08/17'
            ,'2024/10/11','2024/10/12','2024/11/18','2024/12/08','2024/12/25',
        ]

pandemia = [ (dt.strptime('2020-03-20', "%Y-%m-%d").date()), (dt.strptime('2022-03-31', "%Y-%m-%d").date()) ]

def estacion(fecha):
    anio = fecha[0:4]
    f = int(fecha.replace('/',''))
    estaciones = [('VERANO', int(anio+'0101'), int(anio+'0320')),
                  ('OTOÑO', int(anio+'0321'), int(anio+'0620')),
                  ('INVIERNO', int(anio+'0621'), int(anio+'0920')),
                  ('PRIMAVERA', int(anio+'0921'), int(anio+'1220')),
                  ('VERANO', int(anio+'1221'),  int(anio+'1231'))]

    for e, ini, fin in estaciones:
      if ini <= f <= fin:
        return e
      
def clases(fecha):
    anio = fecha[0:4]
    lectivo = {}
    lectivo['2020']=[20200309,20200720,20200731,20201211]
    lectivo['2021']=[20210301,20210719,20210730,20211217]
    lectivo['2022']=[20220302,20220718,20220729,20221222]
    lectivo['2023']=[20230227,20230717,20230723,20231222]
    lectivo['2024']=[20240301,20240715,20240726,20241220]
    lectivo['2025']=[20240305,20240721,20240802,20241222]
    f = int(fecha.replace('/',''))
    
    if (lectivo[anio][0] <= f <= lectivo[anio][1]) or (lectivo[anio][2] <= f <= lectivo[anio][3]):
        return '1'
    return '0'

contenido = os.scandir(dir+'/csv')
cant  = 0
total = 0
"""
for e in contenido:
    f = open(e.path, 'r', encoding='utf-8', errors='ignore')
    lins = f.readlines()
    cant += len(lins) - 1
print(cant)
exit()
"""

for e in contenido:
    origen = open(e.path, 'r', encoding='utf-8', errors='ignore') #open(e.path, 'r')
    destino = open(dir+'/dtaset-'+e.name, 'w')
    lins = origen.readlines()
    destino.write('FECHA;EMPRESA;LINEA;AMBA;TIPO;JURISDICCION;PROVINCIA;MUNICIPIO;CANTIDAD;LABORAL;ESTACION;CLASES;PANDEMIA\n')
    primera_linea  = True
    t              = None
    cant           = 0
    print( "Procesando: ", e.name, end=" " )
    for lin in lins:
        if primera_linea:
            primera_linea = False
            continue

        cols = lin.split(',')

        fch   = dt.strptime(cols[0], "%Y-%m-%d").date()
        fecha = fch.strftime('%Y/%m/%d')
       
        if fch.weekday() in dias_laborales:
            es_laboral = '1'
        else:
            es_laboral = '0'

        en_pandemia = '1' if fch >= pandemia[0] and fch <= pandemia[1] else '0'

        if fch in frds:
            es_laboral = '0'

        est = estacion(fecha)   

        clas = clases(fecha)    

        destino.write( fecha+';'+cols[1]+';'+cols[2]+';'+cols[3]+';'+cols[4]+';'+cols[5]+
                       ';'+cols[6]+';'+cols[7]+';'+cols[8]+';'+es_laboral+';'+est+';'+clas+
                       ';'+en_pandemia+'\n')
        cant += 1
    total += cant
    print(cant)


    origen.close()
    destino.close()
print ("total registros:",total)
