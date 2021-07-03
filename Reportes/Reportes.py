import webbrowser

def createHTML(listTokens, nombreHtml):
    titulo = f"<title>"+nombreHtml+"</title>"
    guardarRegistro = ''
    i = 0
    while i < len(listTokens):
        guardarRegistro += f"<tr><td>{listTokens[i]}</td><td>{listTokens[i+1]}</td><td>{listTokens[i+2]}</td><td>{listTokens[i+3]}</td></tr>"
        i = i + 4

    myFile = open("Reportes/"+nombreHtml+".html", "w")
    docHTML = f"""
    <DOCTYPE html>
        <html>
        <head>
	        {titulo}
	        <link rel="stylesheet" type="text/css" href="plantilla.css">
        </head>
        <body>
            <div class="container">
		        <table>
			        <thead>
				        <tr>
					        <td>TIPO</td>
                            <td>DESCRIPCION</td>
                            <td>FILA</td>
                            <td>COL</td>
				        </tr>
			        </thead> 
                </table>
                <table>
                <br/> <br/>
                </table>
                <table>
                    <thead>	 
                    </tbody>
                        <tr>{guardarRegistro}</tr>
			        </tbody>
		        </table>
        </div>
        </body>
        </html>
        """

    myFile.write(docHTML)
    myFile.close()
    webbrowser.open_new_tab("Reportes\\"+nombreHtml+".html")
    print('-----------------------> Archivo HTML Creado con Exito :) <------------------------------\n')

def createHTML_TS(infTS, nombreHtml):
    titulo = f"<title>"+nombreHtml+"</title>"
    guardarRegistro = ''
    aux = {}
    for key in infTS:
        aux[str(infTS[key][1])+str(infTS[key][5])] = infTS[key]
    for key in aux:
        if str(aux[key][3]) == "TIPO.ENTERO":
            aux[key][3] = "INT"
        elif str(aux[key][3]) == "TIPO.DECIMAL":
            aux[key][3] = "DOUBLE"
        elif str(aux[key][3]) == "TIPO.BOOLEANO":
            aux[key][3] = "BOOLEAN"
        elif str(aux[key][3]) == "TIPO.CHARACTER":
            aux[key][3] = "CHAR"
        elif str(aux[key][3]) == "TIPO.CADENA":
            aux[key][3] = "STRING"
        elif str(aux[key][3]) == "TIPO.NULO":
            aux[key][3] = "NULL"
        elif str(aux[key][3]) == "TIPO.ARREGLO":
            aux[key][3] = "ARRAY"
        guardarRegistro += f"<tr><td>{aux[key][0]}</td><td>{aux[key][1]}</td><td>{aux[key][2]}</td><td>{aux[key][3]}</td><td>{aux[key][4]}</td><td>{aux[key][5]}</td><td>{aux[key][6]}</td></tr>"

    myFile = open("Reportes/"+nombreHtml+".html", "w")
    docHTML = f"""
    <DOCTYPE html>
        <html>
        <head>
	        {titulo}
	        <link rel="stylesheet" type="text/css" href="plantilla.css">
        </head>
        <body>
            <div class="container">
                <table>
                    <thead bgcolor="#FC8965">
				        <tr>
				            <td>AMBITO</td>
				            <td>ID</td>
				            <td>VALOR</td>
					        <td>TIPO</td>
                            <td>ARREGLO</td>
                            <td>FILA</td>
                            <td>COL</td>
				        </tr>
			        </thead> 
                    <thead>	 
                    </tbody>
                        <tr>{guardarRegistro}</tr>
			        </tbody>
		        </table>
        </div>
        </body>
        </html>
        """

    myFile.write(docHTML)
    myFile.close()
    webbrowser.open_new_tab("Reportes\\"+nombreHtml+".html")
    print('-----------------------> Archivo '+nombreHtml+' HTML Creado con Exito :) <------------------------------\n')