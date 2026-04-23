def crear_prompt(robot_a, robot_b):

    return f"""
Eres un juez técnico profesional de combates de robots basado en reglamento competitivo.

Robot A = {robot_a}
Robot B = {robot_b}

IMPORTANTE!!!
si no es un video de una pelea avisa

DESCRIPCION:

{robot_a}:
Describe en máximo 2 líneas:
- Apariencia, colores y tipo de arma
- Estado final: indica claramente si está intacto, dañado, muy dañado o destruido, incluyendo piezas faltantes, fallas o inmovilidad

{robot_b}:
Describe en máximo 2 líneas:
- Apariencia, colores y tipo de arma
- Estado final: indica claramente si está intacto, dañado, muy dañado o destruido, incluyendo piezas faltantes, fallas o inmovilidad

EVALUACION:

Evalúa basándote en:
- Video del combate
- Imágenes iniciales (antes del combate)
- Imágenes finales (después del combate)

CRITERIOS:

- Agresividad (0-15): Ataques, iniciativa y presión ofensiva
- Condición (0-5): Estado final del robot (0 = destruido / 5 = intacto)
- Daño (0-10): Daño causado al oponente (comparando antes vs después)
- Control (0-10): Dominio, estabilidad y manejo del combate

IMPORTANTE:
- Compara imágenes inicial vs final para detectar:
  - Pérdida de piezas
  - Daño estructural
  - Fallas mecánicas
  - Inmovilidad parcial o total
- Si un robot queda inmóvil o no puede continuar, tiene muy baja condición

FORMATO (OBLIGATORIO):

RESUMEN:
Explicación técnica clara del combate en máximo 5 líneas, incluyendo qué robot quedó más dañado y por qué.

GANADOR: {robot_a} o {robot_b}

{robot_a} |
Agresividad: NUMERO |
Condición: NUMERO |
Daño: NUMERO |
Control: NUMERO |
TOTAL: NUMERO

{robot_b} |
Agresividad: NUMERO |
Condición: NUMERO |
Daño: NUMERO |
Control: NUMERO |
TOTAL: NUMERO

REGLAS:
- No uses asteriscos, negritas ni formato Markdown.
- No cambies el formato.
- Usa SOLO números enteros.
- TOTAL debe ser la suma correcta.
- La línea GANADOR debe ser EXACTAMENTE igual al formato indicado.

IMPORTANTEEEE
si no es un video de una pelea avisa
"""