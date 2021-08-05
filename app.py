from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from datetime import datetime

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'signos'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    return render_template('index2.html')

def reporte():
    c = canvas.Canvas('docs/ReporteCompleto.pdf')
    c.setFont("Times-Roman", 24)
    c.drawString(220,800,"Reporte Kmeans")
    c.drawImage('./static/img/logo.png',530,780,60,60)
    c.setFont("Helvetica", 12)
    c.drawString(55,770,"Grafíca de codo")
    c.drawImage('./static/img/codo.jpg', 80, 450, 400, 300)
    c.drawString(55,420,"Grafica de cluster")
    c.drawImage('./static/img/clus1.jpg', 80, 110, 400, 300)
    now = datetime.now()
    c.drawString(55,30,"Fecha: "+now.strftime("%m/%d/%Y")+"")
    c.drawString(350,30,"Equipo: Aurora, Dulce, Jaime")
    c.showPage()
    c.drawImage('./static/img/logo.png',530,780,60,60)
    c.drawString(55,770,"Grafica Dedograma")
    c.drawImage('./static/img/clus2.jpg', 80, 450, 400, 300)
    c.drawString(55,420,"Grafica Cluster final")
    c.drawImage('./static/img/clus3.jpg',80, 110, 400, 300)
    c.drawString(55,30,"Fecha: "+now.strftime("%m/%d/%Y")+"")
    c.drawString(350,30,"Equipo: Aurora, Dulce, Jaime")
    c.showPage()
    c.save()
    return render_template('kmeans.html')
    
@app.route('/exportar_datos',methods=['POST','GET'])
def exportar_datos():
    if request.method == 'POST':
        preg1= request.form.get('preg1') !=None 
        preg2= request.form.get('preg2') !=None
        preg3= request.form.get('preg3') !=None
        preg4= request.form.get('preg4') !=None
        preg5= request.form.get('preg5') !=None
        preg6= request.form.get('preg6') !=None
        preg7= request.form.get('preg7') !=None
        preg8= request.form.get('preg8') !=None
        preg9= request.form.get('preg9') !=None
        preg10= request.form.get('preg10') !=None
        todo= request.form.get('todos') !=None
        cur = mysql.connection.cursor()
        cur.execute('SELECT Pregunta1,Pregunta2,Pregunta3,Pregunta4,Pregunta5,Pregunta6,Pregunta7,Pregunta8,Pregunta9,Pregunta10 FROM preguntas')
        sql='SELECT Pregunta1,Pregunta2,Pregunta3,Pregunta4,Pregunta5,Pregunta6,Pregunta7,Pregunta8,Pregunta9,Pregunta10 FROM preguntas'
        df = pd.read_sql_query(sql,mysql.connection)

        if(todo==True):
            df.to_excel("./static/PDF/datos.xlsx", index=False)
        else:
            if(preg1!=True):
                df=df.drop(['Pregunta1'], axis=1)
            if(preg2!=True):
                df=df.drop(['Pregunta2'], axis=1)
            if(preg3!=True):
                df=df.drop(['Pregunta3'], axis=1)
            if(preg4!=True):
                df=df.drop(['Pregunta4'], axis=1)
            if(preg5!=True):
                df=df.drop(['Pregunta5'], axis=1)
            if(preg6!=True):
                df=df.drop(['Pregunta6'], axis=1)
            if(preg7!=True):
                df=df.drop(['Pregunta7'], axis=1)
            if(preg8!=True):
                df=df.drop(['Pregunta8'], axis=1)
            if(preg9!=True):
                df=df.drop(['Pregunta9'], axis=1)
            if(preg10!=True):
                df=df.drop(['Pregunta10'], axis=1)
            df.to_excel("./static/PDF/datos.xlsx", index=False)
            print(df)
        data = cur.fetchall()
        cur.close()
        return render_template('datos.html', preguntas = data)
@app.route('/ver_datos')
def datos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT Pregunta1,Pregunta2,Pregunta3,Pregunta4,Pregunta5,Pregunta6,Pregunta7,Pregunta8,Pregunta9,Pregunta10 FROM preguntas ORDER BY id DESC')
    sql='SELECT Pregunta1,Pregunta2,Pregunta3,Pregunta4,Pregunta5,Pregunta6,Pregunta7,Pregunta8,Pregunta9,Pregunta10 FROM preguntas'
    df = pd.read_sql_query(sql,mysql.connection)
    print(df)
    df.to_csv("docs/datos.csv", index=False)
    data = cur.fetchall()
    cur.close()
    return render_template('datos.html', preguntas = data)
@app.route('/add_contact', methods=['POST','GET'])
def add_contact():
    select = request.form.get('pregunta1')
    select2 = request.form.get('pregunta2')
    select3 = request.form.get('pregunta3')
    select4 = request.form.get('pregunta4')
    select5 = request.form.get('pregunta5')
    select6 = request.form.get('pregunta6')
    select7 = request.form.get('pregunta7')
    select8 = request.form.get('pregunta8')
    select9 = request.form.get('pregunta9')
    select10 = request.form.get('pregunta10')
    if select !=None and select2!=None and select3!=None and select4!=None and select5!=None and select6!=None and select7!=None and select8!=None and select9!=None and select10!=None :
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO preguntas (Pregunta1, Pregunta2, Pregunta3,Pregunta4,Pregunta5,Pregunta6,Pregunta7,Pregunta8,Pregunta9,Pregunta10) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (select,select2,select3,select4,select5,select6,select7,select8,select9,select10))
        mysql.connection.commit()
        flash('Datos guardados correctamente')
        return redirect(url_for('Index'))


@app.route('/test')
def test():
    return render_template('index.html')
@app.route('/generar_kmeans')
def kmeans():

        sql='SELECT Pregunta1,Pregunta2,Pregunta3,Pregunta4,Pregunta5,Pregunta6,Pregunta7,Pregunta8,Pregunta9,Pregunta10 FROM preguntas'
        df = pd.read_sql_query(sql,mysql.connection)
        df.to_csv("docs/datos.csv", index=False)
        dataset = pd.read_csv('docs/datos.csv')

        
        X = dataset.iloc[:, [1,2,3,4,5,6,7,8,9]].values

        # Metodo del Codo para encontrar el numero optimo de clusters
        from sklearn.cluster import KMeans
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
            
        # Grafica de la suma de las distancias
        plt.plot(range(1, 11), wcss)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.savefig("./static/img/codo.jpg", bbox_inches='tight')
        plt.cla()
            
        # Creando el k-Means para los 4 grupos encontrados
        kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
        y_kmeans = kmeans.fit_predict(X)
            
        colores=['red','green','blue','cyan']
        # Visualizacion grafica de los clusters
        plt.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0, 1], s = 100, c = 'red', label = 'Escorpion')
        plt.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1, 1], s = 100, c = 'green', label = 'Geminis')
        plt.scatter(X[y_kmeans == 2, 0], X[y_kmeans == 2, 1], s = 100, c = 'blue', label = 'Leo')
        plt.scatter(X[y_kmeans == 3, 0], X[y_kmeans == 3, 1], s = 100, c = 'cyan', label = 'Pisis')
            
            
        plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 300, marker='*', c = colores , label = 'Centroids')
            
        plt.title('Clusters of customers')
        plt.xlabel('Annual Income (k$)')
        plt.ylabel('Spending Score (1-100)')
        plt.legend()
        plt.savefig("./static/img/clus1.jpg", bbox_inches='tight')
        plt.cla()
            
            
        # Creamos el dendograma para encontrar el número óptimo de clusters
            
        import scipy.cluster.hierarchy as sch
        dendrogram = sch.dendrogram(sch.linkage(X, method = 'ward'))
            
        plt.title('Dendograma')
        plt.xlabel('Clientes')
        plt.ylabel('Distancias Euclidianas')
        plt.savefig("./static/img/clus2.jpg", bbox_inches='tight')
        plt.cla()
            
            
        from sklearn.cluster import AgglomerativeClustering
        hc = AgglomerativeClustering(n_clusters = 4, 
                                affinity = 'euclidean', 
                                linkage = 'ward')
            
        y_hc = hc.fit_predict(X)
            
            
        plt.scatter(X[y_hc == 0, 0], X[y_hc == 0, 1], s = 100, c = 'red', label = 'Escorpion')
        plt.scatter(X[y_hc == 1, 0], X[y_hc == 1, 1], s = 100, c = 'green', label = 'Geminis')
        plt.scatter(X[y_hc == 2, 0], X[y_hc == 2, 1], s = 100, c = 'blue', label = 'Leo')
        plt.scatter(X[y_hc == 3, 0], X[y_hc == 3, 1], s = 100, c = 'cyan', label = 'Pisis')
            
        plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 300, marker='*', c = colores , label = 'Centroids')
            
        plt.title('Clusters of customers')
        plt.xlabel('Annual Income (k$)')
        plt.ylabel('Spending Score (1-100)')
        plt.legend()
        plt.savefig("./static/img/clus3.jpg", bbox_inches='tight')
        plt.cla()
        plt.switch_backend ('agg')
        reporte()
        return render_template('kmeans.html')

def reporte():
    c = canvas.Canvas('./static/PDF/ReporteCompleto.pdf')
    c.setFont("Times-Roman", 24)
    c.drawString(220,800,"Reporte Kmeans")
    c.drawImage('./static/img/logo.png',530,780,60,60)
    c.setFont("Helvetica", 12)
    c.drawString(55,770,"Grafíca de codo")
    c.drawImage('./static/img/codo.jpg', 80, 450, 400, 300)
    c.drawString(55,420,"Grafica de cluster")
    c.drawImage('./static/img/clus1.jpg', 80, 110, 400, 300)
    now = datetime.now()
    c.drawString(55,30,"Fecha: "+now.strftime("%m/%d/%Y")+"")
    c.drawString(350,30,"Equipo: Aurora, Dulce, Jaime")
    c.showPage()
    c.drawImage('./static/img/logo.png',530,780,60,60)
    c.drawString(55,770,"Grafica Dedograma")
    c.drawImage('./static/img/clus2.jpg', 80, 450, 400, 300)
    c.drawString(55,420,"Grafica Cluster final")
    c.drawImage('./static/img/clus3.jpg',80, 110, 400, 300)
    c.drawString(55,30,"Fecha: "+now.strftime("%m/%d/%Y")+"")
    c.drawString(350,30,"Equipo: Aurora, Dulce, Jaime")
    c.showPage()
    c.save()
    return render_template('kmeans.html')
    
# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
