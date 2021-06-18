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