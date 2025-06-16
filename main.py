from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="MedlinePlus MCP",
    host="0.0.0.0",
    port=8061
)

def medlineplus_query(term: str, lang: str = "es"):
    import requests
    import xml.etree.ElementTree as ET

    db = "healthTopicsSpanish" if lang == "es" else "healthTopics"
    url = "https://wsearch.nlm.nih.gov/ws/query"
    params = {
        "db": db,
        "term": term,
        "retmax": 1,
        "rettype": "brief"
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    root = ET.fromstring(r.text)

    summary, title, url_result = None, None, None

    doc = root.find('.//document')
    if doc is not None:
        url_result = doc.attrib.get('url')
        for content in doc.findall('.//content'):
            if content.attrib.get('name') == 'FullSummary':
                summary = content.text
            if content.attrib.get('name') == 'title':
                title = content.text

    return title, summary, url_result

def limpiar_termino(term):
    palabras_excluir = [
        "síntomas", "tratamiento", "complicaciones", "diagnóstico", "causas", "factores de riesgo", "desencadenantes", "prevención",
        "symptoms", "treatment", "complications", "diagnosis", "causes", "risk factors", "triggers", "prevention",
        "Editar", "Edit", "¿", "?", "de", "del", "de la", "los", "las", "the", "of"
    ]
    for palabra in palabras_excluir:
        term = term.replace(palabra, "")
    return term.strip()

def clean_html(text):
    import re
    if not text:
        return ""
    # Quita etiquetas HTML y spans de MedlinePlus
    text = re.sub(r'<span.*?>|</span>', '', text)
    text = re.sub(r'<p>|</p>', '\n', text)
    text = re.sub(r'<ul>|</ul>|<ol>|</ol>', '\n', text)
    text = re.sub(r'<li>', '- ', text)
    text = re.sub(r'</li>', '\n', text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    # Limpia múltiples saltos de línea
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def format_tablas(line, lang):
    """
    Convierte tablas tipo: "Signos y síntomasResfriadoGripeComienzo de síntomasGradualRepentino..." en bullets claros.
    """
    if lang == "es" and "GradualRepentino" in line:
        return (
            "**Diferencias gripe vs resfriado:**\n"
            "- Comienzo: gradual (resfriado) / repentino (gripe)\n"
            "- Fiebre: rara en resfriado / habitual en gripe\n"
            "- Dolores: leves o ausentes en resfriado / habituales en gripe\n"
            "- Fatiga: leve en resfriado / común en gripe\n"
            "- Dolor de cabeza: raro en resfriado / común en gripe\n"
            "- Congestión, estornudos, dolor de garganta: común en resfriado / a veces en gripe\n"
        )
    elif lang == "en" and "SlowlySuddenly" in line:
        return (
            "**Differences: Flu vs Cold**\n"
            "- Onset: gradual (cold) / sudden (flu)\n"
            "- Fever: rare in cold / usual in flu\n"
            "- Aches: slight or absent in cold / usual in flu\n"
            "- Fatigue: mild in cold / common in flu\n"
            "- Headache: rare in cold / common in flu\n"
            "- Stuffy nose, sneezing, sore throat: common in cold / sometimes in flu\n"
        )
    return ""

def smart_bullet_format(text, lang):
    import re
    if not text:
        return ""
    text = clean_html(text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    # Elimina duplicados
    seen = set()
    clean_lines = []
    for l in lines:
        if l not in seen:
            clean_lines.append(l)
            seen.add(l)
    lines = clean_lines

    # Secciones inteligentes
    resumen, sintomas, causas, factores, complicaciones, otros, tablas = [], [], [], [], [], [], []
    sintomas_headers = ["síntomas", "symptoms"]
    causas_headers = ["causas", "causes"]
    factores_headers = ["factores de riesgo", "risk factors", "desencadenantes", "triggers"]
    complicaciones_headers = ["complicaciones", "complications"]

    sintomas_idx = causas_idx = factores_idx = complicaciones_idx = None
    for idx, line in enumerate(lines):
        tablas_txt = format_tablas(line, lang)
        if tablas_txt:
            tablas.append(tablas_txt)
            continue
        for h in sintomas_headers:
            if h in line.lower():
                sintomas_idx = idx
        for h in causas_headers:
            if h in line.lower():
                causas_idx = idx
        for h in factores_headers:
            if h in line.lower():
                factores_idx = idx
        for h in complicaciones_headers:
            if h in line.lower():
                complicaciones_idx = idx

    for idx, line in enumerate(lines):
        if sintomas_idx is not None and idx > sintomas_idx and (causas_idx is None or idx < causas_idx) and (factores_idx is None or idx < factores_idx) and (complicaciones_idx is None or idx < complicaciones_idx):
            if line.startswith("-") or ":" in line or "fiebre" in line.lower() or "cough" in line.lower():
                sintomas.append(line)
        elif causas_idx is not None and idx > causas_idx and (factores_idx is None or idx < factores_idx) and (complicaciones_idx is None or idx < complicaciones_idx):
            if line.startswith("-") or ":" in line or "alergia" in line.lower() or "gen" in line.lower() or "trigger" in line.lower():
                causas.append(line)
        elif factores_idx is not None and idx > factores_idx and (complicaciones_idx is None or idx < complicaciones_idx):
            if line.startswith("-") or ":" in line or "expos" in line.lower() or "risk" in line.lower():
                factores.append(line)
        elif complicaciones_idx is not None and idx > complicaciones_idx:
            if line.startswith("-") or "neumonía" in line.lower() or "pneumonia" in line.lower():
                complicaciones.append(line)
        elif (sintomas_idx is None or idx < sintomas_idx) and (causas_idx is None or idx < causas_idx):
            resumen.append(line)
        else:
            otros.append(line)

    output = ""
    if resumen:
        output += "\n".join(resumen[:2]) + "\n\n"
    if sintomas:
        output += ("**Síntomas principales:**" if lang == "es" else "**Main symptoms:**") + "\n"
        output += "\n".join(f"- {re.sub(r'^[-•* ]+', '', s)}" for s in sintomas) + "\n\n"
    if causas:
        output += ("**Causas y origen:**" if lang == "es" else "**Causes and origin:**") + "\n"
        output += "\n".join(f"- {re.sub(r'^[-•* ]+', '', c)}" for c in causas) + "\n\n"
    if factores:
        output += ("**Factores de riesgo y desencadenantes:**" if lang == "es" else "**Risk factors and triggers:**") + "\n"
        output += "\n".join(f"- {re.sub(r'^[-•* ]+', '', f)}" for f in factores) + "\n\n"
    if complicaciones:
        output += ("**Complicaciones posibles:**" if lang == "es" else "**Possible complications:**") + "\n"
        output += "\n".join(f"- {re.sub(r'^[-•* ]+', '', c)}" for c in complicaciones) + "\n\n"
    if tablas:
        output += "\n".join(tablas) + "\n"
    # Extra: resalta frases clave de advertencia
    for l in otros:
        if "profesional de la salud" in l or "health care provider" in l or "consultar" in l.lower() or "call" in l.lower():
            output += (f"\n> {l}\n")
    return output.strip()

def format_answer(title, summary, url_result, lang):
    encabezados = {
        "es": "### Información sobre: ",
        "en": "### Information about: "
    }
    formatted = smart_bullet_format(summary, lang) if summary else ""
    medical_note = {
        "es": "\n\n**Recuerda:** Esta información es solo orientativa. Consulta siempre a un profesional de la salud para diagnóstico y tratamiento.",
        "en": "\n\n**Note:** This information is for guidance only. Always consult a healthcare professional for diagnosis and treatment."
    }
    output = ""
    if title:
        output += f"{encabezados[lang]}{title.replace('<span class=\"qt0\">','').replace('</span>','').strip()}\n\n"
    output += f"{formatted}\n"
    output += medical_note[lang] + "\n"
    if url_result:
        link_text = "Más información en MedlinePlus" if lang == "es" else "More information at MedlinePlus"
        output += f"\n[{link_text}]({url_result})"
    else:
        # Si no hay link, ofrece buscar manualmente
        query = limpiar_termino(title) if title else ""
        busqueda = f"https://medlineplus.gov/search/?query={query.replace(' ', '+')}"
        link_text = "Buscar manualmente en MedlinePlus" if lang == "es" else "Try searching manually on MedlinePlus"
        output += f"\n[{link_text}]({busqueda})"
    output += "\n\n_Source: MedlinePlus_"
    return output.strip()

@mcp.tool()
def explain_medical_topic(term: str, lang: str = "es") -> dict:
    """
    Explicación médica ultra-pro y adaptable. Extrae y resalta síntomas, causas, factores de riesgo y complicaciones si existen.
    """
    term_clean = limpiar_termino(term)
    title, summary, url_result = medlineplus_query(term_clean, lang=lang)

    palabra_principal = term_clean.split()[0] if " " in term_clean else term_clean
    if (not summary or not title or palabra_principal.lower() not in (title or "").lower()) and palabra_principal:
        title2, summary2, url2 = medlineplus_query(palabra_principal, lang=lang)
        if summary2 and palabra_principal.lower() in (title2 or "").lower():
            title, summary, url_result = title2, summary2, url2

    if not summary:
        title_en, summary_en, url_en = medlineplus_query(term_clean, lang="en")
        if not summary_en and palabra_principal:
            title_en, summary_en, url_en = medlineplus_query(palabra_principal, lang="en")
        if summary_en:
            formatted = format_answer(title_en, summary_en, url_en, "en")
            title = title_en
            summary = summary_en
            url_result = url_en
        else:
            formatted = {
                "es": "No se encontró información relevante en MedlinePlus para ese término en español ni en inglés.",
                "en": "No relevant information was found in MedlinePlus for this term in Spanish or English."
            }[lang]
            return {
                "title": title,
                "summary": formatted,
                "link": url_result,
                "source": "MedlinePlus"
            }
    else:
        formatted = format_answer(title, summary, url_result, lang)

    return {
        "title": title,
        "summary": formatted,
        "link": url_result,
        "source": "MedlinePlus"
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
