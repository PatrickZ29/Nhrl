from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.templating import Jinja2Templates
import shutil, os, base64
from datetime import datetime

from services.gemini_service import analyze_video
from services.parser_service import parse_result
from database import save_analysis, get_historial

router = APIRouter()
templates = Jinja2Templates(directory="templates")

LAST_VIDEO_TIME = None
LAST_VIDEO_NAME = None
IS_RECORDING = False

if not os.path.exists("videos"):
    os.makedirs("videos")


# ===============================
# ESTADO RASPBERRY
# ===============================
@router.get("/check_status")
def check_status():
    global LAST_VIDEO_TIME, LAST_VIDEO_NAME

    if LAST_VIDEO_TIME is None:
        return {"ready": False}

    return {
        "ready": True,
        "video": LAST_VIDEO_NAME,
        "hora": LAST_VIDEO_TIME.strftime("%H:%M:%S")
    }


@router.get("/start_recording")
def start_recording():
    global IS_RECORDING
    IS_RECORDING = True
    print("🎥 Grabación iniciada")
    return {"recording": True}


@router.get("/stop_recording")
def stop_recording():
    global IS_RECORDING
    IS_RECORDING = False
    print("🛑 Grabación detenida")
    return {"recording": False}


@router.get("/recording_status")
def recording_status():
    return {"recording": IS_RECORDING}


# ===============================
# SUBIR VIDEO DESDE RASPBERRY
# ===============================
@router.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    global LAST_VIDEO_TIME, LAST_VIDEO_NAME

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"fight_{timestamp}.mp4"
    path = f"videos/{filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    print(" Video recibido:", filename)

    LAST_VIDEO_TIME = datetime.now()
    LAST_VIDEO_NAME = filename

    return {"mensaje": "ok"}


# ===============================
# FUNCION BASE64
# ===============================
def file_to_base64(file: UploadFile):
    if file and file.filename != "":
        data = file.file.read()
        return base64.b64encode(data).decode(), file.content_type
    return None, None


# ===============================
# ANALIZAR (AQUÍ VA LO IMPORTANTE)
# ===============================
@router.post("/analyze")
async def analyze(
    request: Request,
    robot_a: str = Form(...),
    robot_b: str = Form(...),
    video: UploadFile = File(None),

    # 🔥 NUEVAS IMÁGENES
    img_a_inicio: UploadFile = File(None),
    img_a_final: UploadFile = File(None),
    img_b_inicio: UploadFile = File(None),
    img_b_final: UploadFile = File(None),
):
    try:
        # ===============================
        # VIDEO
        # ===============================
        if video and video.filename != "":
            filename = f"fight_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            path = f"videos/{filename}"

            with open(path, "wb") as buffer:
                shutil.copyfileobj(video.file, buffer)

            print(" Video subido desde web:", filename)

        else:
            videos = sorted(os.listdir("videos"))
            if not videos:
                raise Exception("No hay videos disponibles")

            filename = videos[-1]
            path = f"videos/{filename}"

            print(" Usando video existente:", filename)

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Error con el video: {str(e)}"
        })

    # ===============================
    # IMÁGENES → BASE64
    # ===============================
    img_ai_b64, img_ai_type = file_to_base64(img_a_inicio)
    img_af_b64, img_af_type = file_to_base64(img_a_final)
    img_bi_b64, img_bi_type = file_to_base64(img_b_inicio)
    img_bf_b64, img_bf_type = file_to_base64(img_b_final)

    # ===============================
    # GEMINI
    # ===============================
    result, tiempo = analyze_video(
        path,
        "video/mp4",
        robot_a,
        robot_b,
        img_ai_b64, img_ai_type,
        img_af_b64, img_af_type,
        img_bi_b64, img_bi_type,
        img_bf_b64, img_bf_type
    )

    if result is None:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Error al procesar el video con Gemini"
        })

    if isinstance(result, dict) and "error" in result:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(result)
        })

    try:
        texto = result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Respuesta inválida de Gemini"
        })

    parsed = parse_result(texto, robot_a, robot_b)

    try:
        save_analysis(path, robot_a, robot_b, texto, tiempo)
    except Exception as e:
        print("⚠️ Error guardando:", e)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "ganador": parsed.get("ganador", "No definido"),
        "response": texto,
        "tiempo": tiempo
    })


# ===============================
# HISTORIAL
# ===============================
@router.get("/historial")
def historial():
    return get_historial()