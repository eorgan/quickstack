from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.agent.postgres import PostgresAgentStorage
# from agno.knowledge.pdf import PDFUrlKnowledgeBase
# from agno.vectordb.pgvector import PgVector2
import os

# Database connection string from environment variables
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/agno")

# Define the Agent Storage (Memory)
storage = PostgresAgentStorage(
    # Table name to store sessions
    table_name="agent_sessions",
    # Database URL
    db_url=DB_URL
)

# Example Knowledge Base (Placeholder - needed for RAG)
# vector_db = PgVector2(
#     collection="agency_knowledge",
#     db_url=DB_URL,
# )

def get_agent_response(message: str, user_id: str, session_id: str = None, is_audio: bool = False) -> str:
    """
    Creates or retrieves an agent and gets a response.
    """
    
    additional_instructions = [
        "Sempre tente extrair o nome do cliente e o que ele procura.",
        "Se não souber a resposta, diga que vai verificar com um especialista.",
        "Não invente informações sobre imóveis.",
    ]

    if is_audio:
        additional_instructions.append("O usuário enviou um áudio. Responda de forma extremamente concisa, curta e natural, ideal para ser falada. Evite listas longas ou markdown complexo.")

    # Define the Agent
    maya = Agent(
        name="Maya",
        role="Secretária Virtual Imobiliária",
        model=Gemini(id="gemini-flash-latest"), # Usando Gemini Flash Latest

        description="""
        Você é Maya, a secretária virtual da imobiliária. 
        Seu objetivo é atender clientes, entender suas necessidades (comprar/alugar, tipo de imóvel, orçamento) 
        e auxiliar os corretores.
        Seja sempre cordial, profissional e breve.
        """,
        instructions=additional_instructions,
        # Storage for persistent memory
        storage=storage,
        # Load existing session if session_id is provided
        session_id=session_id if session_id else None,
        # Add history to context so she remembers
        add_history_to_context=True,
        # Debug helper
        # show_tool_calls=True,
        markdown=True,
    )

    # If it's a new session, you might want to print a greeting manually, 
    # but here we just process the message.
    
    response = maya.run(message)
    return response.content
