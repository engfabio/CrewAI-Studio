import streamlit as st
import os
from utils import rnd_id
from crewai_tools import CodeInterpreterTool,ScrapeElementFromWebsiteTool,TXTSearchTool,SeleniumScrapingTool,PGSearchTool,PDFSearchTool,MDXSearchTool,JSONSearchTool,GithubSearchTool,EXASearchTool,DOCXSearchTool,CSVSearchTool,ScrapeWebsiteTool, FileReadTool, DirectorySearchTool, DirectoryReadTool, CodeDocsSearchTool, YoutubeVideoSearchTool,SerperDevTool,YoutubeChannelSearchTool,WebsiteSearchTool
from tools.CSVSearchToolEnhanced import CSVSearchToolEnhanced
from tools.CustomApiTool import CustomApiTool
from tools.CustomCodeInterpreterTool import CustomCodeInterpreterTool
from tools.CustomFileWriteTool import CustomFileWriteTool
from tools.ScrapeWebsiteToolEnhanced import ScrapeWebsiteToolEnhanced

from langchain_community.tools import YahooFinanceNewsTool

class MyTool:
    def __init__(self, tool_id, name, description, parameters, **kwargs):
        self.tool_id = tool_id or rnd_id()
        self.name = name
        self.description = description
        self.parameters = kwargs
        self.parameters_metadata = parameters

    def create_tool(self):
        pass

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, **kwargs):
        self.parameters.update(kwargs)

    def get_parameter_names(self):
        return list(self.parameters_metadata.keys())

    def is_parameter_mandatory(self, param_name):
        return self.parameters_metadata.get(param_name, {}).get('mandatory', False)

    def is_valid(self,show_warning=False):
        for param_name, metadata in self.parameters_metadata.items():
            if metadata['mandatory'] and not self.parameters.get(param_name):
                if show_warning:
                    st.warning(f"O parâmetro '{param_name}' é obrigatório para a ferramenta '{self.name}'")
                return False
        return True

class MyScrapeWebsiteTool(MyTool):
    def __init__(self, tool_id=None, website_url=None):
        parameters = {
            'website_url': {'mandatory': False}
        }
        super().__init__(tool_id, 'ScrapeWebsiteTool', "Uma ferramenta que pode ser usada para ler o conteúdo de um site.", parameters, website_url=website_url)

    def create_tool(self) -> ScrapeWebsiteTool:
        return ScrapeWebsiteTool(self.parameters.get('website_url') if self.parameters.get('website_url') else None)

class MyFileReadTool(MyTool):
    def __init__(self, tool_id=None, file_path=None):
        parameters = {
            'file_path': {'mandatory': False}
        }
        super().__init__(tool_id, 'FileReadTool', "Uma ferramenta que pode ser usada para ler o conteúdo de um arquivo.", parameters, file_path=file_path)

    def create_tool(self) -> FileReadTool:
        return FileReadTool(self.parameters.get('file_path') if self.parameters.get('file_path') else None)

class MyDirectorySearchTool(MyTool):
    def __init__(self, tool_id=None, directory=None):
        parameters = {
            'directory': {'mandatory': False}
        }
        super().__init__(tool_id, 'DirectorySearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de um diretório.", parameters, directory_path=directory)

    def create_tool(self) -> DirectorySearchTool:
        return DirectorySearchTool(self.parameters.get('directory') if self.parameters.get('directory') else None)

class MyDirectoryReadTool(MyTool):
    def __init__(self, tool_id=None, directory_contents=None):
        parameters = {
            'directory_contents': {'mandatory': True}
        }
        super().__init__(tool_id, 'DirectoryReadTool', "Use esta ferramenta para listar o conteúdo do diretório especificado", parameters, directory_contents=directory_contents)

    def create_tool(self) -> DirectoryReadTool:
        return DirectoryReadTool(self.parameters.get('directory_contents'))

class MyCodeDocsSearchTool(MyTool):
    def __init__(self, tool_id=None, code_docs=None):
        parameters = {
            'code_docs': {'mandatory': False}
        }
        super().__init__(tool_id, 'CodeDocsSearchTool', "Uma ferramenta que pode ser usada para pesquisar na documentação do código.", parameters, code_docs=code_docs)

    def create_tool(self) -> CodeDocsSearchTool:
        return CodeDocsSearchTool(self.parameters.get('code_docs') if self.parameters.get('code_docs') else None)

class MyYoutubeVideoSearchTool(MyTool):
    def __init__(self, tool_id=None, youtube_video_url=None):
        parameters = {
            'youtube_video_url': {'mandatory': False}
        }
        super().__init__(tool_id, 'YoutubeVideoSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de um vídeo do Youtube.", parameters, youtube_video_url=youtube_video_url)

    def create_tool(self) -> YoutubeVideoSearchTool:
        return YoutubeVideoSearchTool(self.parameters.get('youtube_video_url') if self.parameters.get('youtube_video_url') else None)

class MySerperDevTool(MyTool):
    def __init__(self, tool_id=None, SERPER_API_KEY=None):
        parameters = {
            'SERPER_API_KEY': {'mandatory': True}
        }

        super().__init__(tool_id, 'SerperDevTool', "Uma ferramenta que pode ser usada para buscar na internet com uma consulta de pesquisa.", parameters)

    def create_tool(self) -> SerperDevTool:
        os.environ['SERPER_API_KEY'] = self.parameters.get('SERPER_API_KEY')
        return SerperDevTool()
    
class MyYoutubeChannelSearchTool(MyTool):
    def __init__(self, tool_id=None, youtube_channel_handle=None):
        parameters = {
            'youtube_channel_handle': {'mandatory': False}
        }
        super().__init__(tool_id, 'YoutubeChannelSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de canais do Youtube. O canal pode ser adicionado como @channel.", parameters, youtube_channel_handle=youtube_channel_handle)

    def create_tool(self) -> YoutubeChannelSearchTool:
        return YoutubeChannelSearchTool(self.parameters.get('youtube_channel_handle') if self.parameters.get('youtube_channel_handle') else None)

class MyWebsiteSearchTool(MyTool):
    def __init__(self, tool_id=None, website=None):
        parameters = {
            'website': {'mandatory': False}
        }
        super().__init__(tool_id, 'WebsiteSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de uma URL específica.", parameters, website=website)

    def create_tool(self) -> WebsiteSearchTool:
        return WebsiteSearchTool(self.parameters.get('website') if self.parameters.get('website') else None)
   
class MyCSVSearchTool(MyTool):
    def __init__(self, tool_id=None, csv=None):
        parameters = {
            'csv': {'mandatory': False}
        }
        super().__init__(tool_id, 'CSVSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de um arquivo CSV.", parameters, csv=csv)

    def create_tool(self) -> CSVSearchTool:
        return CSVSearchTool(csv=self.parameters.get('csv') if self.parameters.get('csv') else None)

class MyDocxSearchTool(MyTool):
    def __init__(self, tool_id=None, docx=None):
        parameters = {
            'docx': {'mandatory': False}
        }
        super().__init__(tool_id, 'DOCXSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de um arquivo DOCX.", parameters, docx=docx)

    def create_tool(self) -> DOCXSearchTool:
        return DOCXSearchTool(docx=self.parameters.get('docx') if self.parameters.get('docx') else None)

class MyEXASearchTool(MyTool):
    def __init__(self, tool_id=None, EXA_API_KEY=None):
        parameters = {
            'EXA_API_KEY': {'mandatory': True}
        }
        super().__init__(tool_id, 'EXASearchTool', "Uma ferramenta que pode ser usada para buscar na internet com uma consulta de pesquisa.", parameters, EXA_API_KEY=EXA_API_KEY)

    def create_tool(self) -> EXASearchTool:
        os.environ['EXA_API_KEY'] = self.parameters.get('EXA_API_KEY')
        return EXASearchTool()

class MyGithubSearchTool(MyTool):
    def __init__(self, tool_id=None, github_repo=None, gh_token=None, content_types=None):
        parameters = {
            'github_repo': {'mandatory': False},
            'gh_token': {'mandatory': True},
            'content_types': {'mandatory': False}
        }
        super().__init__(tool_id, 'GithubSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de um repositório do Github. Tipos de conteúdo válidos: código, repositório, PR, issue (separados por vírgula).", parameters, github_repo=github_repo, gh_token=gh_token, content_types=content_types)

    def create_tool(self) -> GithubSearchTool:
        return GithubSearchTool(
            github_repo=self.parameters.get('github_repo') if self.parameters.get('github_repo') else None,
            gh_token=self.parameters.get('gh_token'),
            content_types=self.parameters.get('search_query').split(",") if self.parameters.get('search_query') else ["code", "repo", "pr", "issue"]
        )

class MyJSONSearchTool(MyTool):
    def __init__(self, tool_id=None, json_path=None):
        parameters = {
            'json_path': {'mandatory': False}
        }
        super().__init__(tool_id, 'JSONSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de um arquivo JSON.", parameters, json_path=json_path)

    def create_tool(self) -> JSONSearchTool:
        return JSONSearchTool(json_path=self.parameters.get('json_path') if self.parameters.get('json_path') else None)

class MyMDXSearchTool(MyTool):
    def __init__(self, tool_id=None, mdx=None):
        parameters = {
            'mdx': {'mandatory': False}
        }
        super().__init__(tool_id, 'MDXSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de um arquivo MDX.", parameters, mdx=mdx)

    def create_tool(self) -> MDXSearchTool:
        return MDXSearchTool(mdx=self.parameters.get('mdx') if self.parameters.get('mdx') else None)
    
class MyPDFSearchTool(MyTool):
    def __init__(self, tool_id=None, pdf=None):
        parameters = {
            'pdf': {'mandatory': False}
        }
        super().__init__(tool_id, 'PDFSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de um arquivo PDF.", parameters, pdf=pdf)

    def create_tool(self) -> PDFSearchTool:
        return PDFSearchTool(self.parameters.get('pdf') if self.parameters.get('pdf') else None)

class MyPGSearchTool(MyTool):
    def __init__(self, tool_id=None, db_uri=None):
        parameters = {
            'db_uri': {'mandatory': True}
        }
        super().__init__(tool_id, 'PGSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de uma tabela de banco de dados.", parameters, db_uri=db_uri)

    def create_tool(self) -> PGSearchTool:
        return PGSearchTool(self.parameters.get('db_uri'))

class MySeleniumScrapingTool(MyTool):
    def __init__(self, tool_id=None, website_url=None, css_element=None, cookie=None, wait_time=None):
        parameters = {
            'website_url': {'mandatory': False},
            'css_element': {'mandatory': False},
            'cookie': {'mandatory': False},
            'wait_time': {'mandatory': False}
        }
        super().__init__(
            tool_id, 
            'SeleniumScrapingTool', 
            r"Uma ferramenta que pode ser usada para ler uma parte específica do conteúdo de um site. Elementos CSS são separados por vírgula, cookies estão no formato {chave1\:valor1},{chave2\:valor2}", 
            parameters, 
            website_url=website_url, 
            css_element=css_element, 
            cookie=cookie, 
            wait_time=wait_time
)
    def create_tool(self) -> SeleniumScrapingTool:
        cookie_arrayofdicts = [{k: v} for k, v in (item.strip('{}').split(':') for item in self.parameters.get('cookie', '').split(','))] if self.parameters.get('cookie') else None

        return SeleniumScrapingTool(
            website_url=self.parameters.get('website_url') if self.parameters.get('website_url') else None,
            css_element=self.parameters.get('css_element').split(',') if self.parameters.get('css_element') else None,
            cookie=cookie_arrayofdicts,
            wait_time=self.parameters.get('wait_time') if self.parameters.get('wait_time') else 10
        )

class MyTXTSearchTool(MyTool):
    def __init__(self, tool_id=None, txt=None):
        parameters = {
            'txt': {'mandatory': False}
        }
        super().__init__(tool_id, 'TXTSearchTool', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de um arquivo TXT.", parameters, txt=txt)

    def create_tool(self) -> TXTSearchTool:
        return TXTSearchTool(self.parameters.get('txt'))

class MyScrapeElementFromWebsiteTool(MyTool):
    def __init__(self, tool_id=None, website_url=None, css_element=None, cookie=None):
        parameters = {
            'website_url': {'mandatory': False},
            'css_element': {'mandatory': False},
            'cookie': {'mandatory': False}
        }
        super().__init__(
            tool_id, 
            'ScrapeElementFromWebsiteTool', 
            r"Uma ferramenta que pode ser usada para ler uma parte específica do conteúdo de um site. Elementos CSS são separados por vírgula, cookies estão no formato {chave1\:valor1},{chave2\:valor2}", 
            parameters, 
            website_url=website_url, 
            css_element=css_element, 
            cookie=cookie
        )

    def create_tool(self) -> ScrapeElementFromWebsiteTool:
        cookie_arrayofdicts = [{k: v} for k, v in (item.strip('{}').split(':') for item in self.parameters.get('cookie', '').split(','))] if self.parameters.get('cookie') else None
        return ScrapeElementFromWebsiteTool(
            website_url=self.parameters.get('website_url') if self.parameters.get('website_url') else None,
            css_element=self.parameters.get('css_element').split(",") if self.parameters.get('css_element') else None,
            cookie=cookie_arrayofdicts
        )
    
class MyYahooFinanceNewsTool(MyTool):
    def __init__(self, tool_id=None):
        parameters = {}
        super().__init__(tool_id, 'YahooFinanceNewsTool', "Uma ferramenta que pode ser usada para buscar notícias do Yahoo Finance.", parameters)

    def create_tool(self) -> YahooFinanceNewsTool:
        return YahooFinanceNewsTool()
    
class MyCustomApiTool(MyTool):
    def __init__(self, tool_id=None, base_url=None, headers=None, query_params=None):
        parameters = {
            'base_url': {'mandatory': False},
            'headers': {'mandatory': False},
            'query_params': {'mandatory': False}
        }
        super().__init__(tool_id, 'CustomApiTool', "Uma ferramenta que pode ser usada para fazer chamadas de API com parâmetros personalizáveis.", parameters, base_url=base_url, headers=headers, query_params=query_params)

    def create_tool(self) -> CustomApiTool:
        return CustomApiTool(
            base_url=self.parameters.get('base_url') if self.parameters.get('base_url') else None,
            headers=eval(self.parameters.get('headers')) if self.parameters.get('headers') else None,
            query_params=self.parameters.get('query_params') if self.parameters.get('query_params') else None
        )

class MyCustomFileWriteTool(MyTool):
    def __init__(self, tool_id=None, base_folder=None, filename=None):
        parameters = {
            'base_folder': {'mandatory': True},
            'filename': {'mandatory': False}
        }
        super().__init__(tool_id, 'CustomFileWriteTool', "Uma ferramenta que pode ser usada para escrever um arquivo em uma pasta específica.", parameters,base_folder=base_folder, filename=filename)

    def create_tool(self) -> CustomFileWriteTool:
        return CustomFileWriteTool(
            base_folder=self.parameters.get('base_folder') if self.parameters.get('base_folder') else "workspace",
            filename=self.parameters.get('filename') if self.parameters.get('filename') else None
        )


class MyCodeInterpreterTool(MyTool):
    def __init__(self, tool_id=None):
        parameters = {}
        super().__init__(tool_id, 'CodeInterpreterTool', "Esta ferramenta é usada para dar ao Agente a capacidade de executar código (Python3) gerado pelo próprio Agente. O código é executado em um ambiente isolado, então é seguro executar qualquer código. Docker necessário.", parameters)

    def create_tool(self) -> CodeInterpreterTool:
        return CodeInterpreterTool()
    

class MyCustomCodeInterpreterTool(MyTool):
    def __init__(self, tool_id=None,workspace_dir=None):
        parameters = {
            'workspace_dir': {'mandatory': False}
        }
        super().__init__(tool_id, 'CustomCodeInterpreterTool', "Esta ferramenta é usada para dar ao Agente a capacidade de executar código (Python3) gerado pelo próprio Agente. O código é executado em um ambiente isolado, então é seguro executar qualquer código. A pasta de trabalho é compartilhada. Docker necessário.", parameters, workspace_dir=workspace_dir)

    def create_tool(self) -> CustomCodeInterpreterTool:
        return CustomCodeInterpreterTool(workspace_dir=self.parameters.get('workspace_dir') if self.parameters.get('workspace_dir') else "workspace")

class MyCSVSearchToolEnhanced(MyTool):
    def __init__(self, tool_id=None, csv=None):
        parameters = {
            'csv': {'mandatory': False}
        }
        super().__init__(tool_id, 'CSVSearchToolEnhanced', "Uma ferramenta que pode ser usada para buscar semanticamente uma consulta no conteúdo de um arquivo CSV.", parameters, csv=csv)

    def create_tool(self) -> CSVSearchToolEnhanced:
        return CSVSearchToolEnhanced(csv=self.parameters.get('csv') if self.parameters.get('csv') else None)
    
class MyScrapeWebsiteToolEnhanced(MyTool):
    def __init__(self, tool_id=None, website_url=None, cookies=None, show_urls=None, css_selector=None):
        parameters = {
            'website_url': {'mandatory': False},
            'cookies': {'mandatory': False},
            'show_urls': {'mandatory': False},
            'css_selector': {'mandatory': False}
        }
        super().__init__(tool_id, 'ScrapeWebsiteToolEnhanced', "Uma ferramenta que pode ser usada para ler o conteúdo de um site.", parameters, website_url=website_url, cookies=cookies, show_urls=show_urls, css_selector=css_selector)

    def create_tool(self) -> ScrapeWebsiteToolEnhanced:
        return ScrapeWebsiteToolEnhanced(
            website_url=self.parameters.get('website_url') if self.parameters.get('website_url') else None,
            cookies=self.parameters.get('cookies') if self.parameters.get('cookies') else None,
            show_urls=self.parameters.get('show_urls') if self.parameters.get('show_urls') else False,
            css_selector=self.parameters.get('css_selector') if self.parameters.get('css_selector') else None
        )

# Register all tools here
TOOL_CLASSES = {
    'SerperDevTool': MySerperDevTool,
    'WebsiteSearchTool': MyWebsiteSearchTool,
    'ScrapeWebsiteTool': MyScrapeWebsiteTool,
    'ScrapeWebsiteToolEnhanced': MyScrapeWebsiteToolEnhanced,
    
    'SeleniumScrapingTool': MySeleniumScrapingTool,
    'ScrapeElementFromWebsiteTool': MyScrapeElementFromWebsiteTool,
    'CustomApiTool': MyCustomApiTool,
    'CodeInterpreterTool': MyCodeInterpreterTool,
    'CustomCodeInterpreterTool': MyCustomCodeInterpreterTool,
    'FileReadTool': MyFileReadTool,
    'CustomFileWriteTool': MyCustomFileWriteTool,
    'DirectorySearchTool': MyDirectorySearchTool,
    'DirectoryReadTool': MyDirectoryReadTool,

    'YoutubeVideoSearchTool': MyYoutubeVideoSearchTool,
    'YoutubeChannelSearchTool' :MyYoutubeChannelSearchTool,
    'GithubSearchTool': MyGithubSearchTool,
    'CodeDocsSearchTool': MyCodeDocsSearchTool,
    'YahooFinanceNewsTool': MyYahooFinanceNewsTool,

    'TXTSearchTool': MyTXTSearchTool,
    'CSVSearchTool': MyCSVSearchTool,
    'CSVSearchToolEnhanced': MyCSVSearchToolEnhanced,
    'DOCXSearchTool': MyDocxSearchTool, 
    'EXASearchTool': MyEXASearchTool,
    'JSONSearchTool': MyJSONSearchTool,
    'MDXSearchTool': MyMDXSearchTool,
    'PDFSearchTool': MyPDFSearchTool,
    'PGSearchTool': MyPGSearchTool    
}