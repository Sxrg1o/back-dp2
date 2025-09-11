**PONTIFICIA‌ ‌UNIVERSIDAD‌ ‌CATÓLICA‌ ‌DEL‌ ‌PERÚ**

**FACULTAD DE CIENCIAS E INGENIERÍA**

**![LogotipoDescripción generada automáticamente][image1]**

**TRABAJO GRUPAL**

Curso			:	\[1INF50\] Proyecto de implementación de Software

Título				:	

Número de grupo		:	

Nombres y códigos	:	

Jefe de Práctica		: 	

SEMESTRE 2024-1

Índice

[**1\. Introducción	3**](#introducción)

[**2\. Principios de Arquitectura de Datos	3**](#principios-de-arquitectura-de-datos)

[**2\. Modelo Conceptual (UML)	4**](#2.-modelo-conceptual-\(uml\))

[**3\. Modelo Lógico de Datos	4**](#3.-modelo-lógico-de-datos)

[**4\. Modelo Físico de Datos	12**](#4.-modelo-físico-de-datos)

1. # Introducción {#introducción}

Este documento presenta la arquitectura de datos para el Sistema de Gestión Administrativa y Operativa del restaurante “Domótica”. A lo largo del documento, se detalla cómo se gestionarán y procesarán los datos esenciales para asegurar la correcta implementación del sistema, garantizando que este aporte significativamente al cumplimiento de los objetivos estratégicos del restaurante.

El proceso de diseño de la arquitectura de datos comenzó con la definición precisa de los requerimientos del sistema, los cuales sirven como base para la organización, gestión y validación de los datos. Estos requerimientos permiten asegurar que la infraestructura de datos será adecuada para soportar las operaciones y decisiones del restaurante de manera eficiente y segura. 

2. # Principios de Arquitectura de Datos {#principios-de-arquitectura-de-datos}

A continuación, se detallan los principios clave de arquitectura de datos que guiarán el diseño y desarrollo del sistema de gestión del restaurante “Domótica”.

1. Identificación de Entidades:  
   Se asignará un identificador único o se utilizará el código predefinido por el restaurante para distinguir las entidades dentro del sistema. Esto facilitará el control de acceso a los recursos e información, asegurando la correcta gestión en los distintos ámbitos del sistema.  
   2. Minimización de Datos:  
      Se recopilarán solo los datos esenciales para la operación del restaurante, como pedidos, productos, pagos, y contacto con el cliente, además de una trazabilidad mínima de las transacciones. No se almacenarán datos sensibles como información fiscal o facturación electrónica en esta fase inicial para asegurar eficiencia y privacidad.  
   3. Integridad Referencial:  
      Para garantizar la consistencia de los datos, se implementarán relaciones referenciales a través de claves foráneas (FK), que asegurarán la integridad entre los pedidos, ítems y atenciones. Este mecanismo evitará la posibilidad de que se realicen pedidos con productos inexistentes o no disponibles, asegurando un proceso operativo fluido y sin errores.

   4. Trazabilidad Operativa:  
      Con el objetivo de permitir una auditoría eficiente y asegurar el seguimiento adecuado de las operaciones, se registrará cada cambio de estado de los pedidos (por ejemplo, en cola, preparando, listo, entregado), junto con un timestamp y la identificación del actor (cliente, cocina o sistema).

   5. Cumplimiento Normativo Local:  
      El sistema se adherirá a las normativas locales de protección de datos, especialmente en relación con el almacenamiento de datos personales. Solo se mantendrán los datos personales mínimos necesarios para la operación, en cumplimiento con la Ley de Protección de Datos Personales. La privacidad y seguridad de los clientes serán prioridades en el diseño del sistema.

        
   6. Alcance Limitado y Futuro Crecimiento:  
      El alcance de esta primera versión del sistema se centrará en la gestión avanzada de mesas y la emisión de comprobantes fiscales quedará fuera del alcance inicial. Sin embargo, la arquitectura estará diseñada de manera que permitirá la integración de estas funciones en futuras versiones del sistema, sin requerir un rediseño significativo

   7. Disponibilidad y Baja Latencia:

      La arquitectura estará diseñada para garantizar operaciones en tiempo real, especialmente para sistemas como el KDS (Kitchen Display System), que requieren baja latencia. Para ello, se utilizarán colas de mensajes y tecnologías como WebSockets para asegurar la transmisión de datos en tiempo real. Además, se implementará una tolerancia a fallos con reintentos automáticos en caso de caídas parciales del sistema, asegurando la disponibilidad continua de los servicios.

# 2\. Modelo Conceptual (UML) {#2.-modelo-conceptual-(uml)}

![][image2]

# 3\. Modelo Lógico de Datos {#3.-modelo-lógico-de-datos}

Diccionario:

**Paquete:Gestión de Pedidos**

| Clase / Enum | Atributo / Método | Tipo | Descripción |
| ----- | ----- | ----- | ----- |
| **Pedido** | id | Integer | Identificador único del pedido. |
|  | mesero | Mesero | Mesero que atiende el pedido. |
|  | mesa | Mesa | Mesa asociada al pedido. |
|  | numItems | Integer | Cantidad de ítems en el pedido. |
|  | items | List | Lista de ítems pedidos (productos del menú). |
|  | clientes | List | Clientes que participan en el pedido. |
|  | prioridad | Integer | Nivel de prioridad del pedido (ej. urgencias). |
|  | estado | EstadoPedido | Estado del pedido en su ciclo de vida. |
|  | lineaPedidos | List | Detalle de productos con cantidades. |
|  | fecha | DateTime | Fecha y hora del pedido. |
|  | pago | Pago | Pago asociado al pedido. |
|  | montoTotal | double | Monto total calculado del pedido. |
|  | activo | boolean | Indica si el pedido está activo o cerrado. |
|  | **\+ calcularMontoTotal()** | void | Calcula el monto total a partir de los ítems. |
| **Mesero** | id | Integer | Identificador único del mesero. |
|  | nombre | String | Nombre del mesero. |
|  | mesasAsignadas | List | Mesas a cargo del mesero. |
|  | atenciones | List | Atenciones realizadas a clientes. |
|  | desempenio | float | Evaluación del desempeño. |
|  | activo | Boolean | Estado del mesero en el sistema. |
|  | fechaContrato | DateTime | Fecha de inicio de contrato. |
| **ItemPedido** | id | Integer | Identificador único del ítem pedido. |
|  | item | Item | Producto del menú solicitado. |
|  | pedido | Pedido | Pedido al que pertenece. |
|  | cantPedida | Integer | Cantidad solicitada del ítem. |
|  | subtotal | double | Subtotal (cantidad × precio). |
|  | **\+ calcularSubtotal()** | double | Calcula el subtotal del ítem. |
| **EstadoPedido (Enum)** | NO\_ATENDIDO, ORDEN\_TOMADA, EN\_PREPARACION, ENTREGADO, PAGO\_PENDIENTE, PAGADO | \- | Estados del ciclo de vida del pedido. |

Paquete: Atenciones en cocina

| Clase / Enum | Atributo / Método | Tipo | Descripción |
| ----- | ----- | ----- | ----- |
| **Atención** | id | Integer | Identificador único de la atención. |
|  | pedido | Pedido | Pedido asociado. |
|  | clientes | List | Clientes atendidos. |
|  | puntaje | float | Calificación de la atención. |
|  | comentarios | String | Observaciones de clientes. |
|  | estadoAtencion | EstadoAtencion | Estado de satisfacción. |
|  | fecha | DateTime | Fecha de la atención. |
| **CocinaKDS** | nombreEncargado | String | Nombre del encargado de cocina. |
|  | apellidoEncargado | String | Apellido del encargado. |
|  | numeroEncargado | String | Número de contacto del encargado. |
|  | codEncargado | Integer | Código único del encargado. |
|  | meseros | List | Meseros que interactúan con cocina. |
|  | historicoAtenciones | List | Registro histórico de atenciones. |
|  | numAtenciones | Integer | Total de atenciones registradas. |
|  | numAtenAprob | Integer | Cantidad de atenciones aprobadas. |
|  | numAtenDesap | Integer | Cantidad de atenciones desaprobadas. |
|  | numMeseros | Integer | Número de meseros bajo supervisión. |
| **EstadoAtencion (Enum)** | MUY\_SATISFACTORIO, SATISFACTORIO, DEFICIENTE, MUY\_DEFICIENTE | \- | Nivel de satisfacción reportado. |

**Paquete: Estancia Cliente**

| Clase / Enum | Atributo / Método | Tipo | Descripción |
| ----- | ----- | ----- | ----- |
| **Mesa** | id | Integer | Identificador único de la mesa. |
|  | numAsientos | Integer | Número de asientos disponibles. |
|  | habilitado | Boolean | Indica si la mesa está disponible. |
|  | meseroPrincipal | Mesero | Mesero principal asignado. |
|  | meseroApoyo | Mesero | Mesero de apoyo. |
|  | reservado | Boolean | Estado de reserva de la mesa. |
|  | fechaRenovacion | DateTime | Fecha de próxima habilitación. |
|  | pedidos | List | Pedidos realizados en la mesa. |
|  | **\- calcularTotalGenerado()** | double | Total generado en pedidos de la mesa. |
| **Cliente** | id | Integer | Identificador único del cliente. |
|  | nombre | String | Nombre del cliente. |
|  | primerApellido | String | Primer apellido. |
|  | segundoApellido | String | Segundo apellido. |
|  | telefono | String | Número de contacto. |
|  | correoElectronico | String | Email del cliente. |
|  | nombreUsuario | String | Nombre de usuario en la app. |
|  | contrasena | String | Contraseña cifrada. |
|  | frecuencia | double | Frecuencia de visitas. |
|  | fotoPerfil | byte\[\] | Imagen del cliente. |
|  | activo | Boolean | Estado de la cuenta. |
|  | fechaCreacion | DateTime | Fecha de registro. |
|  | fechaModificacion | DateTime | Última modificación. |
|  | historialAtenciones | List | Registro de atenciones recibidas. |
|  | preferencias | String | Preferencias de consumo. |
| **EstadoMesa (Enum)** | RESERVADA, DISPONIBLE, OCUPADA, EN\_LIMPIEZA | \- | Estados posibles de una mesa. |

**Paquete: Gestión de Pago**

| Clase / Enum | Atributo / Método | Tipo | Descripción |
| ----- | ----- | ----- | ----- |
| **Pago** | id | Integer | Identificador único del pago. |
|  | metodo | Enum | Forma de pago utilizada. |
|  | monto | double | Monto total abonado. |
|  | propina | double | Propina asociada. |
|  | descuento | double | Descuento aplicado. |
|  | pedido | Pedido | Pedido asociado al pago. |
|  | atencion | Atencion | Atención asociada. |
|  | estado | Enum | Estado del pago. |
|  | factura | boolean | Indica si requiere factura. |
|  | **\+ procesar()** | void | Procesa el pago. |
| **MetodoPago (Enum)** | CREDITO, DEBITO, EFECTIVO, TRANSFERENCIA\_INMEDIATA, WALLET | \- | Métodos de pago disponibles. |
| **EstadoPago (Enum)** | EMITIDO, EN\_ESPERA, FALLIDO | \- | Estado del proceso de pago. |

**Paquete: Menú y Carta**

| Clase / Enum | Atributo / Método | Tipo | Descripción |
| ----- | ----- | ----- | ----- |
| **Item** | id | Integer | Identificador único del ítem. |
|  | valorNutricional | String | Información nutricional. |
|  | precio | double | Precio del ítem. |
|  | tiempoPreparacion | double | Tiempo promedio de preparación. |
|  | comentarios | String | Notas adicionales. |
|  | receta | String | Receta asociada. |
|  | disponible | Boolean | Disponibilidad en carta. |
|  | unidadesDisponibles | Integer | Stock disponible. |
|  | numIngredientes | Integer | Número de ingredientes. |
|  | kcal | Integer | Calorías. |
|  | calorias | double | Energía total en calorías. |
|  | proteinas | double | Contenido de proteínas. |
|  | azucares | double | Contenido de azúcares. |
|  | descripcion | String | Descripción del ítem. |
|  | **\+ verificarStock()** | Boolean | Verifica stock disponible. |
| **Ingrediente** | id | Integer | Identificador único. |
|  | nombre | String | Nombre del ingrediente. |
|  | stock | double | Cantidad en stock. |
|  | peso | double | Peso por unidad. |
|  | tipo | Enum | Tipo de ingrediente. |
| **Plato** | peso | double | Peso total. |
|  | receta | String | Receta del plato. |
|  | tipo | Enum | Tipo de plato (entrada, fondo, postre). |
| **Bebida** | litros | double | Cantidad en litros. |
|  | alcoholico | Boolean | Si contiene alcohol. |
| **EtiquetaItem (Enum)** | SIN\_GLUTEN, PICANTE, SALADO, CALIENTE, FRIO, ACIDO, AGRIO, CON\_GLUTEN, VEGANO | \- | Clasificación de ítems. |
| **EtiquetaIngrediente (Enum)** | VERDURA, CARNE, FRUTA | \- | Clasificación de ingredientes. |
| **EtiquetaPlato (Enum)** | ENTRADA, FONDO, POSTRE | \- | Clasificación de platos. |

# 4\. Modelo Físico de Datos {#4.-modelo-físico-de-datos}

**4.1 Motor de Base de Datos**

* **Motor elegido:** MySQL (puede migrar a PostgreSQL sin cambios en la capa de aplicación).  
* **Versión:** MySQL 8.x.  
* **Justificación:** Soporte a transacciones, integridad referencial, replicación y alta disponibilidad.

**4.2 Acceso y Persistencia**

* **Mecanismo:** ORM (Object Relational Mapper).  
* **Herramienta seleccionada:** **SQLAlchemy (Python)**.  
* **Complemento de migraciones:** **Alembic** (para versionado del esquema).

**Justificación del ORM:**

* Permite trabajar con entidades de negocio como objetos en lugar de tablas y SQL plano.  
* Automatiza la creación y modificación del esquema de BD.  
* Asegura la portabilidad entre diferentes motores (ej. pasar de MySQL a PostgreSQL sin cambios drásticos).  
* Centraliza la lógica de integridad en el modelo Python.  
* Facilita la trazabilidad y mantenimiento del esquema.

**4.3 Definición de Entidades en ORM**

El esquema físico se define en clases Python que representan las tablas.  
 Los atributos de clase se mapean a columnas de la tabla, y las relaciones ORM representan las claves foráneas.

 
 