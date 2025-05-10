import streamlit as st
from utils import rnd_id
from my_tools import TOOL_CLASSES
from streamlit import session_state as ss
import db_utils

class PageTools:
    def __init__(self):
        self.name = "Ferramentas"
        self.available_tools = TOOL_CLASSES

    def create_tool(self, tool_name):
        tool_class = self.available_tools[tool_name]
        tool_instance = tool_class(rnd_id())
        if 'tools' not in ss:
            ss.tools = []
        ss.tools.append(tool_instance)
        db_utils.save_tool(tool_instance)  # Save tool to database

    def remove_tool(self, tool_id):
        ss.tools = [tool for tool in ss.tools if tool.tool_id != tool_id]
        db_utils.delete_tool(tool_id)
        st.rerun()

    def set_tool_parameter(self, tool_id, param_name, value):
        if value == "":
            value = None
        for tool in ss.tools:
            if tool.tool_id == tool_id:
                tool.set_parameters(**{param_name: value})
                db_utils.save_tool(tool)
                break

    def get_tool_display_name(self, tool):
        first_param_name = tool.get_parameter_names()[0] if tool.get_parameter_names() else None
        first_param_value = tool.parameters.get(first_param_name, '') if first_param_name else ''
        return f"{tool.name} ({first_param_value if first_param_value else tool.tool_id})"

    def draw_tools(self):
        c1,c2 = st.columns([1, 3])
        with c1:
            st.write("##### Ferramentas Disponíveis")
            for tool_name in self.available_tools.keys():
                tool_class = self.available_tools[tool_name]
                tool_instance = tool_class()
                tool_description = tool_instance.description
                if st.button(f"{tool_name}", key=f"enable_{tool_name}", help=tool_description):
                    self.create_tool(tool_name)
        with c2:
            if 'tools' in ss:
                st.write("##### Ferramentas Habilitadas")
                for tool in ss.tools:
                    display_name = self.get_tool_display_name(tool)
                    is_complete = tool.is_valid()
                    expander_title = display_name if is_complete else f"❗ {display_name}"
                    with st.expander(expander_title):
                        st.write(tool.description)
                        for param_name in tool.get_parameter_names():
                            param_value = tool.parameters.get(param_name, "")
                            placeholder = "Obrigatório" if tool.is_parameter_mandatory(param_name) else "Opcional"
                            new_value = st.text_input(f"{param_name}", value=param_value, key=f"{tool.tool_id}_{param_name}", placeholder=placeholder)
                            if new_value != param_value:
                                self.set_tool_parameter(tool.tool_id, param_name, new_value)
                        if st.button(f"Remover ferramenta", key=f"remove_{tool.tool_id}"):
                            self.remove_tool(tool.tool_id)

    def draw(self):
        st.subheader(self.name)
        
        st.markdown("""
        ### Como usar as ferramentas

        As ferramentas fornecem capacidades específicas aos agentes da sua equipe.
        
        Para configurar:
        1. Selecione uma ferramenta da lista à esquerda
        2. Configure os parâmetros necessários à direita
        3. Atribua as ferramentas aos agentes na página de Agentes
        """)
        
        st.divider()
        
        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown("#### Ferramentas Disponíveis")
            st.markdown("Clique para adicionar à sua coleção:")
            for tool_name in self.available_tools.keys():
                tool_class = self.available_tools[tool_name]
                tool_instance = tool_class()
                tool_description = tool_instance.description
                if st.button(f"{tool_name}", key=f"enable_{tool_name}", help=tool_description):
                    self.create_tool(tool_name)
                    st.success(f"Ferramenta {tool_name} adicionada com sucesso!")
        
        with c2:
            if 'tools' in ss:
                st.markdown("#### Ferramentas Configuradas")
                if len(ss.tools) == 0:
                    st.info("Nenhuma ferramenta configurada ainda. Selecione uma ferramenta da lista à esquerda para começar.")
                
                for tool in ss.tools:
                    display_name = self.get_tool_display_name(tool)
                    is_complete = tool.is_valid()
                    expander_title = display_name if is_complete else f"❗ {display_name} (configuração incompleta)"
                    
                    with st.expander(expander_title):
                        st.markdown("##### Descrição")
                        st.write(tool.description)
                        
                        st.markdown("##### Configurações")
                        for param_name in tool.get_parameter_names():
                            param_value = tool.parameters.get(param_name, "")
                            placeholder = "Parâmetro obrigatório" if tool.is_parameter_mandatory(param_name) else "Parâmetro opcional"
                            new_value = st.text_input(
                                f"{param_name}", 
                                value=param_value, 
                                key=f"{tool.tool_id}_{param_name}", 
                                placeholder=placeholder,
                                help="Digite o valor do parâmetro"
                            )
                            if new_value != param_value:
                                self.set_tool_parameter(tool.tool_id, param_name, new_value)
                                st.success("Configuração atualizada!")
                        
                        if st.button("Remover esta ferramenta", key=f"remove_{tool.tool_id}"):
                            self.remove_tool(tool.tool_id)
                            st.success("Ferramenta removida com sucesso!")
