from psycopg2 import connect


HOST ='ec2-44-207-133-100.compute-1.amazonaws.com'
PUERTO= 5432
BD ='dadc97kv0j3tbo'
USUARIO='wyfqnsybstptuy'
PASSWORD='193627e58982b998405dec36a001fe6d7aa9485ab75114220de6e9feaabafcb3'

def EstablecerConexion():
    try:
        conexion=connect(host=HOST, port=PUERTO, database=BD, user=USUARIO, password=PASSWORD)
        return conexion
    except Exception as e:
        print(e)
        return None