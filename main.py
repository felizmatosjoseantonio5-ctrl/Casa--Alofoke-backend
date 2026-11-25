from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess, os, json, glob

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Backend Casa Alofoke Activo"}

@app.get("/cortar")
def cortar(url: str):
    for f in glob.glob("corte*.mp4"):
        os.remove(f)
    if os.path.exists("live.mp4"):
        os.remove("live.mp4")

    subprocess.run(["yt-dlp", "-f", "mp4/best", "-o", "live.mp4", url], check=False)

    if not os.path.exists("live.mp4"):
        return {"error": "No se pudo bajar el live. Usa Grabar Pantalla."}

    cortes = []
    tiempos = [0, 90, 180, 270, 360, 450, 540, 630, 720, 810]
    titulos = [
        "EL INDIRECTO QUE PARÓ LA CASA",
        "SE ARMÓ EL CHISME EN VIVO",
        "ESTA PELEA NADIE LA VIO VENIR",
        "LO DIJO SIN MIEDO EN VIVO",
        "LA CASA SE VOLVIÓ LOCA",
        "INDIRECTO DIRECTO SIN FILTRO",
        "ESTO VA A DAR DE QUE HABLAR",
        "SE PASÓ DE LA RAYA EN VIVO",
        "TODO EL MUNDO QUEDÓ EN SHOCK",
        "EL MOMENTO MÁS VIRAL DE LA NOCHE"
    ]

    for i, t in enumerate(tiempos):
        salida = f"corte{i+1}.mp4"
        subprocess.run(["ffmpeg", "-y", "-ss", str(t), "-i", "live.mp4", "-t", "30", "-c:v", "libx264", "-c:a", "aac", salida], check=False)
        if os.path.exists(salida):
            cortes.append({
                "id": i+1,
                "titulo": titulos[i],
                "score": 95 - i,
                "inicio": t,
                "fin": t+30,
                "video": f"/video/corte{i+1}",
                "descargar": f"/video/corte{i+1}"
            })

    return {"listo": True, "total": len(cortes), "cortes": cortes}

@app.get("/video/{nombre}")
def video(nombre: str):
    path = f"{nombre}.mp4"
    if os.path.exists(path):
        return FileResponse(path, media_type="video/mp4")
    return {"error": "No existe"}
