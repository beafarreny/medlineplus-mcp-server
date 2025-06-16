# MedlinePlus MCP Server

This repository contains a reference MCP (Model Context Protocol) server for providing structured, user-friendly, and high-quality medical explanations powered by MedlinePlus (NIH/NLM).

The server is designed for easy integration with the [NANDA Registry](https://ui.nanda-registry.com/) and is fully compatible with the Python MCP SDK.

---

## ✨ Features

- **Multi-language:** Supports Spanish (`es`) and English (`en`)
- **Automatic structuring:** Bullets for symptoms, causes, risk factors, complications, etc.
- **Smart summarization:** Highlights key medical facts
- **Fallback logic:** If not found in one language, searches in the other
- **Direct source links:** Always provides MedlinePlus references

---

## 🚀 Quickstart

1. **Clone the repository**

```bash
git clone https://github.com/beafarreny/medlineplus-mcp-server.git
cd medlineplus-mcp-server
```
2. *(Recommended)* **Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the server**

```bash
python main.py
```

By default, the server runs on localhost:8061.

---

## 🛠️ Example Usage

The main tool is called explain_medical_topic and can be called programmatically or from any MCP-compatible client.

```bash
from mcp.server.fastmcp 
import FastMCP

result = explain_medical_topic(term="flu symptoms", lang="en")
print(result["summary"])
```

---

## 💡 Example Questions

- What are the symptoms of the flu?
- What are the causes of asthma?
- How is diabetes treated?
- What are the side effects of ibuprofen?
- Difference between food allergy and food intolerance
- What are the complications of chickenpox in adults?
- Can I take paracetamol with alcohol?
- What diseases cause chest pain and shortness of breath?
- What are the side effects of the flu vaccine?
- How is hypertension diagnosed?

---

## 📦 Requirements

- Python 3.9 or newer (tested with 3.13)
- See requirements.txt for all dependencies

---

## 👩‍💻 Author

Beatriz Farreny

MIT NANDA 2024 | La Salle BCN

Contact: [beafarreny@gmail.com](mailto:beafarreny@gmail.com)

---

## 📄 License

[MIT License](LICENSE)

Content powered by [MedlinePlus (NIH/NLM)](https://medlineplus.gov/)

See [MedlinePlus Terms of Use](https://medlineplus.gov/about/terms-of-use/)


---

# Servidor MCP de MedlinePlus

Este repositorio contiene un servidor MCP (Model Context Protocol) de referencia que ofrece explicaciones médicas estructuradas, accesibles y de alta calidad, obtenidas directamente de [MedlinePlus (NIH/NLM)](https://medlineplus.gov/).

El servidor está diseñado para integrarse fácilmente con el [NANDA Registry](https://ui.nanda-registry.com/) y es totalmente compatible con el [Python MCP SDK](https://github.com/modelcontextprotocol/sdk-python).


---

## ✨ Características

- **Multilingüe:** consultas en español (`es`) e inglés (`en`)
- **Formato automático:** resalta síntomas, causas, factores de riesgo y complicaciones
- **Resúmenes claros:** listas y bullets para la información clave
- **Búsqueda inteligente:** si no encuentra en un idioma, prueba en el otro
- **Enlaces a MedlinePlus:** siempre con fuente oficial

---

## 🚀 Ejecución rápida

1. **Clona el repositorio**

```bash
git clone https://github.com/beafarreny/medlineplus-mcp-server.git
cd medlineplus-mcp-server
```


2. *(Recomendado)* **Crea un entorno virtual**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instala dependencias**

```bash
pip install -r requirements.txt
```

4. **Ejecuta el servidor**

```bash
python main.py
```
El servidor estará en localhost:8061.

---

## 🛠️ Ejemplo de uso

Puedes llamar la herramienta explain_medical_topic desde cualquier cliente compatible con MCP.

```bash
from mcp.server.fastmcp 
import FastMCP

result = explain_medical_topic(term="flu symptoms", lang="en")
print(result["summary"])
```

---

## 💡 Preguntas de ejemplo

- ¿Cuáles son los síntomas de la gripe?
- ¿Cuáles son las causas del asma?
- ¿Cómo se trata la diabetes?
- ¿Qué efectos secundarios tiene el ibuprofeno?
- Diferencia entre alergia alimentaria e intolerancia alimentaria
- ¿Cuáles son las complicaciones de la varicela en adultos?
- ¿Puedo tomar paracetamol con alcohol?
- ¿Qué enfermedades pueden causar dolor en el pecho y dificultad para respirar?
- ¿Qué efectos secundarios tiene la vacuna de la gripe?
- ¿Cómo se diagnostica la hipertensión?

---

## 👩‍💻 Autoría

Beatriz Farreny

MIT NANDA 2024 | La Salle BCN

Contact: [beafarreny@gmail.com](mailto:beafarreny@gmail.com)

---

## 📄 Licencia

[Licencia MIT](LICENSE)

Content powered by [Contenido vía MedlinePlus (NIH/NLM)](https://medlineplus.gov/)

Ver [Términos de uso de MedlinePlus](https://medlineplus.gov/about/terms-of-use/)

