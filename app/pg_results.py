import streamlit as st
from streamlit import session_state as ss
from db_utils import delete_result, load_results
from datetime import datetime
from utils import rnd_id, format_result, generate_printable_view

class PageResults:
    def __init__(self):
        self.name = "Resultados"

    def draw(self):
        st.subheader(self.name)

        if 'results' not in ss:
            ss.results = load_results()

        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            crew_filter = st.multiselect(
                "Filtrar por Equipe",
                options=list(set(r.crew_name for r in ss.results)),
                default=[],
                key="crew_filter"
            )
        with col2:
            date_filter = st.date_input(
                "Filtrar por Data",
                value=None,
                key="date_filter"
            )

        # Aplicar filtros
        filtered_results = ss.results
        if crew_filter:
            filtered_results = [r for r in filtered_results if r.crew_name in crew_filter]
        if date_filter:
            filter_date = datetime.combine(date_filter, datetime.min.time())
            filtered_results = [r for r in filtered_results if datetime.fromisoformat(r.created_at).date() == date_filter]

        # Ordenar resultados por data de criação (mais recentes primeiro)
        filtered_results = sorted(
            filtered_results,
            key=lambda x: datetime.fromisoformat(x.created_at),
            reverse=True
        )

        # Exibir resultados
        for result in filtered_results:
            # Formatar entradas para exibição no título do expansor
            input_summary = ""
            input_items = list(result.inputs.items())
            
            if len(input_items) == 0:
                input_summary = ""
            elif len(input_items) == 1:
                key, value = input_items[0]
                input_summary = f" | {key}: {value[:30]}" + ("..." if len(value) > 30 else "")
            else:
                max_chars = max(40 // len(input_items), 10)
                input_parts = []
                
                for key, value in input_items:
                    if len(value) <= max_chars:
                        input_parts.append(f"{key}: {value}")
                    else:
                        input_parts.append(f"{key}: {value[:max_chars]}...")
                
                input_summary = " | " + " | ".join(input_parts)
            
            timestamp = datetime.fromisoformat(result.created_at).strftime('%d/%m/%Y %H:%M:%S')
            expander_title = f"{result.crew_name} - {timestamp}{input_summary}"
            
            with st.expander(expander_title, expanded=False):
                st.markdown("#### Entradas")
                for key, value in result.inputs.items():
                    st.text_input(key, value, disabled=True, key=rnd_id())

                st.markdown("#### Resultado")
                formatted_result = format_result(result.result)

                # Mostrar versões formatada e bruta usando abas
                tab1, tab2 = st.tabs(["Formatado", "Bruto"])
                with tab1:
                    st.markdown(formatted_result)
                with tab2:
                    st.code(formatted_result)

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Excluir", key=f"delete_{result.id}"):
                        delete_result(result.id)
                        ss.results.remove(result)
                        st.rerun()
                with col2:
                    html_content = generate_printable_view(
                        result.crew_name,
                        result.result,
                        result.inputs,
                        formatted_result,
                        result.created_at
                    )
                    if st.button("Abrir Visualização para Impressão", key=f"print_{result.id}"):
                        js = f"""
                        <script>
                            var printWindow = window.open('', '_blank');
                            printWindow.document.write({html_content!r});
                            printWindow.document.close();
                        </script>
                        """
                        st.components.v1.html(js, height=0)