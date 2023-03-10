#--------------------------------------Importamos librerias--------------------------------------------

from tkinter import *
import os
import cv2                          # Para el procesamiento de imagenes
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN       # Detector de rostros
import numpy as np
from PIL import ImageTk, Image
import tkinter as tk

#------------------------ Crearemos una funcion que se encargara de registrar el usuario ---------------------

def registrar_usuario():
    usuario_info = usuario.get() #Obetnemos la informacion alamcenada en usuario
    contra_info = contra.get() #Obtenemos la informacion almacenada en contra

    archivo = open(usuario_info, "w") #Abriremos la informacion en modo escritura
    archivo.write(usuario_info + "\n")   #escribimos la info
    archivo.write(contra_info)
    archivo.close()

    #Limpiaremos los text variable
    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    #Ahora le diremos al usuario que su registro ha sido exitoso
    Label(pantalla1, text = "Registro Convencional Exitoso", fg = "green", font = ("Calibri",11)).pack()
    

#--------------------------- Funcion para almacenar el registro facial --------------------------------------
    
def registro_facial():
    #Vamos a capturar el rostro
    cap = cv2.VideoCapture(0)               #Elegimos la camara con la que vamos a hacer la deteccion
    while(True):
        ret,frame = cap.read()              #Leemos el video
        cv2.imshow('Registro Facial',frame)         #Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:            #Cuando oprimamos "Escape" rompe el video
            break
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img+".jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cerramos
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)   #Limpiamos los text variables
    contra_entrada.delete(0, END)
    Label(pantalla1, text = "Registro Facial Exitoso", fg = "green", font = ("Calibri",11)).pack()

    #----------------- Detectamos el rostro y exportamos los pixeles --------------------------
    
    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen con un tama??o de 150x200
            cv2.imwrite(usuario_img+".jpg",cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img+".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)   
    
#------------------------Crearemos una funcion para asignar al boton registro --------------------------------
def registro():
    global usuario
    global contra  #Globalizamos las variables para usarlas en otras funciones
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla) #Esta pantalla es de un nivel superior a la principal
    pantalla1.title("Registro")
    pantalla1.geometry("800x320")   #Creamos la ventana
    pantalla1.configure(bg='#8E8D8E') # Asignamos el color de fondo de la ventana 
    pantalla1.resizable(False, False) # Quitamos el responsive
    
    # RUTAS PARA LAS IM??GENES
    carpeta_principal = os.path.dirname(__file__) # Direcci??n de la carpeta principal
    carpeta_imagenes = os.path.join(carpeta_principal, "imagenesDetector") # Directorio de im??genes
    dir = file=os.path.join(carpeta_imagenes, "Logo.png") # direcci??n imagen (logo)

    # Ajustando el logo
    image = Image.open(dir)
    icon =  ImageTk.PhotoImage(image)
    pantalla1.iconphoto(False, icon)

    #--------- Empezaremos a crear las entradas ----------------------------------------
    
    usuario = StringVar()
    contra = StringVar()
    
    Label(pantalla1, text = "Registro facial: debe ingresar su correo institucional:", fg="white", bg = "#5C0A1B", width = "300").pack()
    Label(pantalla1, text = "Registro tradicional: debe ingresar un correo y su CUI:", fg="white", bg = "#5C0A1B", width = "300").pack()
    Label(pantalla1, text = "", bg='#8E8D8E').pack()  #Dejamos un poco de espacio
    Label(pantalla1, text = "Correo Institucional").pack()  #Mostramos en la pantalla 1 el usuario
    Label(pantalla1, text = "", bg='#8E8D8E').pack()
    usuario_entrada = Entry(pantalla1, textvariable = usuario, borderwidth=1, relief="solid") #Creamos un text variable para que el usuario ingrese la info
    usuario_entrada.pack()
    Label(pantalla1, text = "", bg='#8E8D8E').pack()
    Label(pantalla1, text = "CUI").pack()  #Mostramos en la pantalla 1 la contrase??a
    Label(pantalla1, text = "", bg='#8E8D8E').pack()
    contra_entrada = Entry(pantalla1, textvariable = contra, borderwidth=1, relief="solid") #Creamos un text variable para que el usuario ingrese la contra
    contra_entrada.pack()
    Label(pantalla1, text = "", bg='#8E8D8E').pack()  #Dejamos un espacio para la creacion del boton
    Button(pantalla1, text = "Registro Tradicional", width = 15, height = 1, command = registrar_usuario).pack()  #Creamos el boton

    #------------ Vamos a crear el boton para hacer el registro facial --------------------
    Label(pantalla1, text = "", bg='#8E8D8E').pack()
    Button(pantalla1, text = "Registro Facial", width = 15, height = 1, command = registro_facial).pack()

#------------------------------------------- Funcion para verificar los datos ingresados al login ------------------------------------
    
def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    lista_archivos = os.listdir()   #Vamos a importar la lista de archivos con la libreria os
    if log_usuario in lista_archivos:   #Comparamos los archivos con el que nos interesa
        archivo2 = open(log_usuario, "r")  #Abrimos el archivo en modo lectura
        verificacion = archivo2.read().splitlines()  #leera las lineas dentro del archivo ignorando el resto
        if log_contra in verificacion:
            print("Inicio de sesion exitoso")
            Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).pack()
        else:
            print("Contrase??a incorrecta, ingrese de nuevo")
            Label(pantalla2, text = "Contrase??a Incorrecta", fg = "red", font = ("Calibri",11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()
    
#--------------------------Funcion para el Login Facial --------------------------------------------------------
def login_facial():
#------------------------------Vamos a capturar el rostro-----------------------------------------------------
    cap = cv2.VideoCapture(0)               #Elegimos la camara con la que vamos a hacer la deteccion
    while(True):
        ret,frame = cap.read()              #Leemos el video
        cv2.imshow('Detector de rostors',frame)         #Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:            #Cuando oprimamos "Escape" rompe el video
            break
    usuario_login = verificacion_usuario.get()    #Con esta variable vamos a guardar la foto pero con otro nombre para no sobreescribir
    cv2.imwrite(usuario_login+"LOG.jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
    cap.release()                               #Cerramos
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)   #Limpiamos los text variables
    contra_entrada2.delete(0, END)

    #----------------- Funcion para guardar el rostro --------------------------
    
    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1,y1,ancho, alto = lista_resultados[i]['box']
            x2,y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i+1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen 150x200
            cv2.imwrite(usuario_login+"LOG.jpg",cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    #-------------------------- Detectamos el rostro-------------------------------------------------------
    
    img = usuario_login+"LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    #-------------------------- Funcion para comparar los rostros --------------------------------------------
    def orb_sim(img1,img2):
        orb = cv2.ORB_create()  #Creamos el objeto de comparacion
 
        kpa, descr_a = orb.detectAndCompute(img1, None)  #Creamos descriptor 1 y extraemos puntos claves
        kpb, descr_b = orb.detectAndCompute(img2, None)  #Creamos descriptor 2 y extraemos puntos claves

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos comparador de fuerza

        matches = comp.match(descr_a, descr_b)  #Aplicamos el comparador a los descriptores

        regiones_similares = [i for i in matches if i.distance < 70] #Extraemos las regiones similares en base a los puntos claves
        if len(matches) == 0:
            return 0
        return len(regiones_similares)/len(matches)  #Exportamos el porcentaje de similitud
        
    #---------------------------- Importamos las imagenes y llamamos la funcion de comparacion ---------------------------------
    
    im_archivos = os.listdir()   #Vamos a importar la lista de archivos con la libreria os
    if usuario_login+".jpg" in im_archivos:   #Comparamos los archivos con el que nos interesa
        rostro_reg = cv2.imread(usuario_login+".jpg",0)     #Importamos el rostro del registro
        rostro_log = cv2.imread(usuario_login+"LOG.jpg",0)  #Importamos el rostro del inicio de sesion
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.98:
            Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).pack()
            print("Bienvenido al sistema usuario: ",usuario_login)
            print("Compatibilidad con la foto del registro: ",similitud)
        else:
            print("Rostro incorrecto, Cerifique su usuario")
            print("Compatibilidad con la foto del registro: ",similitud)
            Label(pantalla2, text = "Incompatibilidad de rostros", fg = "red", font = ("Calibri",11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()
            

#------------------------Funcion que asignaremos al boton login -------------------------------------------------
        
def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2
    
    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("800x320")   #Creamos la ventana
    pantalla2.configure(bg='#8E8D8E') # Asignamos el color de fondo de la ventana 
    pantalla2.resizable(False, False) # Quitamos el responsive


    # RUTAS PARA LAS IM??GENES
    carpeta_principal = os.path.dirname(__file__) # Direcci??n de la carpeta principal
    carpeta_imagenes = os.path.join(carpeta_principal, "imagenesDetector") # Directorio de im??genes
    dir = file=os.path.join(carpeta_imagenes, "Logo.png") # direcci??n imagen (logo)

    # Ajustando el logo
    image = Image.open(dir)
    icon =  ImageTk.PhotoImage(image)
    pantalla2.iconphoto(False, icon)

    Label(pantalla2, text = "Login facial: debe de ingresar su correo institucional:",fg="white", bg = "#5C0A1B", width = "300").pack()
    Label(pantalla2, text = "Login tradicional: debe ingresar su correo y CUI",fg="white", bg = "#5C0A1B", width = "300").pack()
    Label(pantalla2, text = "", bg='#8E8D8E').pack()  #Dejamos un poco de espacio
    
    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()
    
    #---------------------------------- Ingresamos los datos --------------------------
    Label(pantalla2, text = "Correo Institucional").pack()
    Label(pantalla2, text = "", bg='#8E8D8E').pack()
    usuario_entrada2 = Entry(pantalla2, textvariable = verificacion_usuario, borderwidth=1, relief="solid")
    usuario_entrada2.pack()
    Label(pantalla2, text = "", bg='#8E8D8E').pack()
    Label(pantalla2, text = "CUI").pack()
    Label(pantalla2, text = "", bg='#8E8D8E').pack()
    contra_entrada2 = Entry(pantalla2, textvariable = verificacion_contra, borderwidth=1, relief="solid")
    contra_entrada2.pack()
    Label(pantalla2, text = "", bg='#8E8D8E').pack()
    Button(pantalla2, text = "Inicio de Sesi??n Tradicional", width = 20, height = 1, command = verificacion_login).pack()

    #------------ Vamos a crear el boton para hacer el login facial --------------------
    Label(pantalla2, text = "", bg='#8E8D8E').pack()
    Button(pantalla2, text = "Inicio de Sesi??n Facial", width = 20, height = 1, command = login_facial).pack()
        
#------------------------- Funcion de nuestra pantalla principal ------------------------------------------------
    
def pantalla_principal():
    global pantalla          #Globalizamos la variable para usarla en otras funciones
    pantalla = Tk()
    pantalla.geometry("800x250")  #Asignamos el tama??o de la ventana 
    pantalla.configure(bg='#8E8D8E') # Asignamos el color de fondo de la ventana 
    pantalla.resizable(False, False) # Quitamos el responsive
    
    # RUTAS PARA LAS IM??GENES
    carpeta_principal = os.path.dirname(__file__) # Direcci??n de la carpeta principal
    carpeta_imagenes = os.path.join(carpeta_principal, "imagenesDetector") # Directorio de im??genes
    
    dir1 = file=os.path.join(carpeta_imagenes, "Logo.png") # direcci??n imagen1 (logo)

    dir2 = file=os.path.join(carpeta_imagenes, "Unsa.png") # direcci??n imagen2

    # Ajustando el logo
    image1 = Image.open(dir1)
    icon =  ImageTk.PhotoImage(image1)
    pantalla.iconphoto(False, icon)

    # Insertando imagen 2
    image2 = Image.open(dir2)
    image2 = image2.resize((150,50), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image2)
    lbl_img = tk.Label(pantalla, image=img)
    lbl_img.pack()

    pantalla.title("Detector Facial")       #Asignamos el titulo de la pantalla
    Label(text = "SISTEMA DE MATR??CULAS",fg="white", bg = "#5C0A1B", width = "300", height = "2", font = ("Open Sans", 13)).pack() #Asignamos caracteristicas de la ventana

#------------------------- Vamos a Crear los Botones ------------------------------------------------------
    
    Label(text = "", bg='#8E8D8E').pack()  #Creamos el espacio entre el titulo y el primer boton
    Button(text = "Iniciar Sesion", font = ("Open Sans", 9), height = "2", width = "30", command = login).pack()
    Label(text = "", bg='#8E8D8E').pack() #Creamos el espacio entre el primer boton y el segundo boton
    Button(text = "Registro", font = ("Open Sans", 9), height = "2", width = "30", command = registro).pack()

    pantalla.mainloop()

pantalla_principal()