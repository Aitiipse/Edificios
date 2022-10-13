from werkzeug.security import check_password_hash, generate_password_hash

class Usuario():
    def __init__(self, id, usuario, contraseña, nombres="" ):
        self.id=id
        self.usuario=usuario
        self.contraseña=contraseña
        self.nombres=nombres