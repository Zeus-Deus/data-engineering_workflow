from dotenv import load_dotenv
load_dotenv(dotenv_path="/usr/src/app/.env")

import os
import requests
import re
from neo4j import GraphDatabase

# Test articles (public domain)
ARTICLES = [
    {
        "id": "article_1",
        "title": "Bush administration drastically cuts penalties sought for in tobacco trial from $130 billion to $10 billion",
        "text": (
            "Bush administration drastically cuts penalties sought for in tobacco trial from $130 billion to $10 billion\n"
            "Washington, D.C. — In a surprise move during the closing days of a federal racketeering trial against major tobacco companies, the Bush administration on Wednesday reduced the penalties it was seeking from $130 billion to $10 billion.\n"
            "The original recommendation sought to require the companies to fund smoking cessation programs over a 25-year period, but the new demand requests only five years of such funding.\n"
            "Critics immediately accused the administration of yielding to industry pressure. 'This is a huge victory for the tobacco companies,' said William Corr, executive director of the Campaign for Tobacco-Free Kids. 'It is a devastating loss for public health.'\n"
            "Department of Justice officials defended the decision, stating that their revised proposal was based on legal advice and a realistic assessment of what would be upheld on appeal.\n"
            "The case, which began in 1999 under the Clinton administration, charged tobacco companies with deceiving the public about the dangers of smoking."
        ),
    },
    {
        "id": "article_2",
        "title": "'Denmark will be attacked' says one expert, 'Denmark safe' says another",
        "text": (
            "'Denmark will be attacked' says one expert, 'Denmark safe' says another\n"
            "Copenhagen, Denmark — Danish media have been abuzz after two security experts gave sharply different assessments of Denmark's risk from terrorist attacks.\n"
            "Jens Hansen, a professor of political science, stated in a Danish newspaper that, 'It is likely that Denmark will suffer an attack in the near future. The political climate and Denmark's role in recent international conflicts make us a target.'\n"
            "In contrast, Lars Nielsen, a senior analyst at the Danish Institute for Security Studies, argued, 'There is no credible evidence to suggest Denmark is at increased risk. Security measures are strong, and the public should not be alarmed by speculation.'\n"
            "Officials declined to comment specifically on the experts' claims but assured citizens that authorities remain vigilant."
        ),
    },
    {
        "id": "article_3",
        "title": "'Afghanistan is a 20-year venture' warns Canadian general",
        "text": (
            "'Afghanistan is a 20-year venture' warns Canadian general\n"
            "Ottawa, Canada — A senior Canadian general has warned that the international mission in Afghanistan could last up to 20 years, emphasizing the complexity and depth of the country's challenges.\n"
            "'We have to be clear with Canadians that this is not a short-term operation,' General Marc Lessard told reporters. 'Stabilizing Afghanistan, building institutions, and establishing security will require a long-term commitment—possibly twenty years or more.'\n"
            "The general's remarks come as Canada considers increasing its military presence. Some politicians have expressed concerns about the duration and goals of the mission.\n"
            "General Lessard stressed that the ultimate aim was stability and self-sufficiency for Afghanistan, but cautioned against expecting quick solutions."
        ),
    },
]

# Get environment variables (no defaults)
NEXT_PUBLIC_FASTAPI_URL = os.getenv("NEXT_PUBLIC_FASTAPI_URL")
if not NEXT_PUBLIC_FASTAPI_URL:
    raise EnvironmentError("NEXT_PUBLIC_FASTAPI_URL environment variable is required.")
NEO4J_URI = os.getenv("NEO4J_URI")
if not NEO4J_URI:
    raise EnvironmentError("NEO4J_URI environment variable is required.")
NEO4J_AUTH = os.getenv("NEO4J_AUTH")
if not NEO4J_AUTH:
    raise EnvironmentError("NEO4J_AUTH environment variable is required.")
NEO4J_USER, NEO4J_PASS = NEO4J_AUTH.split("/")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

PROMPT_TEMPLATE = """
I will provide you with a text. Your task is to analyze the text and identify any cognitive biases that are present or suggested within it. For each bias you identify, provide:
- The name of the bias
- A brief explanation of the bias
- A short justification for why you think this bias is present in the text, citing specific parts of the text as evidence

Here is the text to analyze:
"{article_text}"

Please analyze the text and list any cognitive biases you find, following the structure above.
"""

def parse_llm_response(response_text):
    """
    Parses the LLM response and returns a list of dicts with keys: bias_name, explanation, justification
    """
    # Split by bias blocks (e.g., 'Confirmation Bias:', 'Outcome Bias:')
    bias_blocks = re.split(r"\n(?=[A-Z][a-zA-Z ]+ Bias:)", response_text.strip())
    results = []
    for block in bias_blocks:
        match = re.match(r"([A-Z][a-zA-Z ]+ Bias):\n- (.+?)\n- (.+)", block.strip(), re.DOTALL)
        if match:
            bias_name = match.group(1).replace(":", "")
            explanation = match.group(2).strip()
            justification = match.group(3).strip()
            results.append({
                "bias_name": bias_name,
                "explanation": explanation,
                "justification": justification
            })
    return results

def write_to_neo4j(article, bias_info):
    with driver.session() as session:
        session.run(
            '''
            MERGE (a:Article {id: $article_id, title: $article_title})
            MERGE (b:Bias {name: $bias_name})
            MERGE (a)-[r:HAS_BIAS]->(b)
            SET r.explanation = $explanation, r.justification = $justification
            ''',
            article_id=article["id"],
            article_title=article["title"],
            bias_name=bias_info["bias_name"],
            explanation=bias_info["explanation"],
            justification=bias_info["justification"]
        )

for article in ARTICLES:
    print(f"\nProcessing: {article['title']}")
    prompt = PROMPT_TEMPLATE.format(article_text=article["text"])
    payload = {"question": prompt}
    try:
        response = requests.post(f"{NEXT_PUBLIC_FASTAPI_URL}/query", json=payload)
        response.raise_for_status()
        data = response.json()
        llm_response = data.get("answer", "")
        print("LLM Response:", llm_response)
        bias_infos = parse_llm_response(llm_response)
        for bias_info in bias_infos:
            print(f"  Parsed Bias: {bias_info['bias_name']}")
            write_to_neo4j(article, bias_info)
    except Exception as e:
        print(f"Error processing article {article['id']}: {e}") 