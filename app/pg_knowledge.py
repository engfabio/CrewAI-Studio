import streamlit as st
from streamlit import session_state as ss
from my_knowledge_source import MyKnowledgeSource
import db_utils
import os
import shutil
from pathlib import Path

class PageKnowledge:
    def __init__(self):
        self.name = "Conhecimento"

    def create_knowledge_source(self):
        knowledge_source = MyKnowledgeSource()
        if 'knowledge_sources' not in ss:
            ss.knowledge_sources = []
        ss.knowledge_sources.append(knowledge_source)
        knowledge_source.edit = True
        db_utils.save_knowledge_source(knowledge_source)
        return knowledge_source

    def clear_knowledge(self):
        # This will clear knowledge stores in CrewAI
        # Get CrewAI home directory
        home_dir = Path.home()
        crewai_dir = home_dir / ".crewai"
        
        # Remove knowledge folder
        knowledge_dir = crewai_dir / "knowledge"
        if knowledge_dir.exists():
            shutil.rmtree(knowledge_dir)
            st.success("Armazéns de conhecimento limpos com sucesso!")
        else:
            st.info("Nenhum armazém de conhecimento encontrado para limpar.")

    def draw(self):
        st.subheader(self.name)
        
        st.markdown("""
        ### Como usar fontes de conhecimento

        As fontes de conhecimento permitem que você forneça informações externas aos seus agentes e equipes.
        
        Você pode:
        - Criar diferentes tipos de fontes (texto, arquivos PDF, CSV, etc.)
        - Atribuir fontes a agentes específicos
        - Atribuir fontes a equipes inteiras
        - Usar as fontes para melhorar o contexto e precisão dos agentes
        """)
        
        os.makedirs("knowledge", exist_ok=True)
        
        st.button("Limpar Cache de Conhecimento", 
                 on_click=self.clear_knowledge, 
                 help="Limpa todos os embeddings e caches de conhecimento no CrewAI")
        
        editing = False
        if 'knowledge_sources' not in ss:
            ss.knowledge_sources = db_utils.load_knowledge_sources()
            
        for knowledge_source in ss.knowledge_sources:
            knowledge_source.draw()
            if knowledge_source.edit:
                editing = True
                
        if len(ss.knowledge_sources) == 0:
            st.write("Nenhuma fonte de conhecimento definida ainda.")
            if st.button('Nova Fonte de Conhecimento', on_click=self.create_knowledge_source, disabled=editing):
                st.success("Nova fonte de conhecimento criada com sucesso!")
        else:
            if st.button('Nova Fonte de Conhecimento', on_click=self.create_knowledge_source, disabled=editing):
                st.success("Nova fonte de conhecimento criada com sucesso!")
