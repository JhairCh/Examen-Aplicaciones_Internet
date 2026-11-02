
from app import create_app
from app.extensions import db
from app.models import Usuario, Tecnico, Categoria, Prioridad, Ticket, Comentario

app = create_app()

with app.app_context():
    # Categorías
    categorias_data = [
        ("Hardware", "Problemas con componentes físicos."),
        ("Software", "Errores en programas y aplicaciones."),
        ("Redes", "Problemas de conexión y comunicación."),
        ("Rendimiento del sistema", "Lentitud y bajo rendimiento."),
        ("Seguridad", "Incidentes de seguridad informática."),
        ("Otros", "Solicitudes generales.")
    ]

    categorias = {}
    for nombre, descripcion in categorias_data:
        obj = Categoria.query.filter_by(nombre=nombre).first()
        if not obj:
            obj = Categoria(nombre=nombre, descripcion=descripcion)
            db.session.add(obj)
        categorias[nombre] = obj

    # Prioridades
    prioridades_data = [
        ("Baja", 1),
        ("Media", 2),
        ("Alta", 3),
        ("Crítica", 4)
    ]

    prioridades = {}
    for nombre, nivel in prioridades_data:
        obj = Prioridad.query.filter_by(nombre=nombre).first()
        if not obj:
            obj = Prioridad(nombre=nombre, nivel=nivel)
            db.session.add(obj)
        prioridades[nombre] = obj

    # Usuarios
    usuarios_data = [
        ("Carlos Mendoza", "carlos@ejemplo.com", "70010001"),
        ("María López", "maria@ejemplo.com", "70010002"),
        ("Juan Pérez", "juan@ejemplo.com", "70010003"),
        ("Ana Rojas", "ana@ejemplo.com", "70010004"),
        ("Luis Fernández", "luis@ejemplo.com", "70010005")
    ]

    usuarios = {}
    for nombre, correo, telefono in usuarios_data:
        obj = Usuario.query.filter_by(correo=correo).first()
        if not obj:
            obj = Usuario(nombre=nombre, correo=correo, telefono=telefono)
            db.session.add(obj)
        usuarios[correo] = obj

    # Técnicos
    tecnicos_data = [
        ("Pedro Ramírez", "pedro@ejemplo.com", "Hardware"),
        ("Laura Flores", "laura@ejemplo.com", "Software"),
        ("Miguel Torres", "miguel@ejemplo.com", "Redes")
    ]

    tecnicos = {}
    for nombre, correo, especialidad in tecnicos_data:
        obj = Tecnico.query.filter_by(correo=correo).first()
        if not obj:
            obj = Tecnico(
                nombre=nombre,
                correo=correo,
                especialidad=especialidad
            )
            db.session.add(obj)
        tecnicos[correo] = obj

    db.session.flush()

    # Tickets
    tickets_data = [
        ("Computadora lenta", "La computadora tarda demasiado en iniciar Windows.",
         "carlos@ejemplo.com", "pedro@ejemplo.com",
         "Rendimiento del sistema", "Media"),

        ("Error al abrir Excel", "La aplicación se cierra inesperadamente.",
         "maria@ejemplo.com", "laura@ejemplo.com",
         "Software", "Alta"),

        ("Sin conexión a Internet", "El equipo no puede conectarse a la red.",
         "juan@ejemplo.com", "miguel@ejemplo.com",
         "Redes", "Crítica"),

        ("Teclado defectuoso", "Algunas teclas no responden.",
         "ana@ejemplo.com", "pedro@ejemplo.com",
         "Hardware", "Baja"),

        ("Sospecha de virus", "Se muestran ventanas emergentes desconocidas.",
         "luis@ejemplo.com", "laura@ejemplo.com",
         "Seguridad", "Alta")
    ]

    tickets = {}
    for titulo, descripcion, usuario, tecnico, categoria, prioridad in tickets_data:
        obj = Ticket.query.filter_by(titulo=titulo).first()
        if not obj:
            obj = Ticket(
                titulo=titulo,
                descripcion=descripcion,
                estado="Pendiente",
                usuario=usuarios[usuario],
                tecnico=tecnicos[tecnico],
                categoria=categorias[categoria],
                prioridad=prioridades[prioridad]
            )
            db.session.add(obj)
        tickets[titulo] = obj

    db.session.flush()

    # Comentarios
    comentarios_data = [
        ("Se recibió la solicitud y será revisada.",
         "Computadora lenta", "carlos@ejemplo.com"),

        ("Estamos verificando el problema de la aplicación.",
         "Error al abrir Excel", "maria@ejemplo.com"),

        ("Se revisará el router y la conexión.",
         "Sin conexión a Internet", "juan@ejemplo.com"),

        ("Se recomienda revisar la conexión del teclado.",
         "Teclado defectuoso", "ana@ejemplo.com"),

        ("Se realizará un análisis de seguridad.",
         "Sospecha de virus", "luis@ejemplo.com")
    ]

    for contenido, titulo, correo in comentarios_data:
        existe = Comentario.query.filter_by(
            contenido=contenido,
            ticket_id=tickets[titulo].id,
            usuario_id=usuarios[correo].id
        ).first()

        if not existe:
            db.session.add(Comentario(
                contenido=contenido,
                ticket=tickets[titulo],
                usuario=usuarios[correo]
            ))

    db.session.commit()

    print("¡Datos de prueba cargados correctamente!")
