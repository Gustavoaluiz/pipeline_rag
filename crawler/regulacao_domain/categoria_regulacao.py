from enum import Enum


class EnumWithAttrs(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, name, description):
        self.description = description


class CategoriaRegulacao(EnumWithAttrs):
    NOTA_TECNICA = "NOTA_TECNICA", "Nota Técnica"
    LEI_GERACAO = "LEI_GERACAO", "Lei de Geração"
    LEI_CONCESSAO = "LEI_CONCESSAO", "Lei de Concessão"
    TEMA_INTERESSE = "TEMA_INTERESSE", "Tema de Interesse"
    POLITICAS_PUBLICAS = "POLITICAS_PUBLICAS", "Políticas Públicas"
    GERENCIAMENTO_PROJETOS = "GERENCIAMENTO_PROJETOS", "Gerenciamento de Projetos"

    REGRA_SERVICOS_TRANSMISSAO = "REGRA_SERVICOS_TRANSMISSAO", "Regras dos Serviços de Transmissão"
    NORMATIVA_DISTRIBUICAO = "NORMATIVA_DISTRIBUICAO", "Normativa de Distribuição"
    NORMATIVA_TARIFARIA = "NORMATIVA_TARIFARIA", "Normativa Tarifária"
    NORMATIVA_PROCEDIMENTOS_PARTICIPACAO = "NORMATIVA_PROCEDIMENTOS_PARTICIPACAO", "Normativa de Procedimentos de Participação"
    NORMATIVA_PROCEDIMENTOS_PESQUISA_DESENVOLVIMENTO = "NORMATIVA_PROCEDIMENTOS_PESQUISA_DESENVOLVIMENTO", "Normativa de Procedimentos de Pesquisa e Desenvolvimento"
    NORMAS_GLOBAIS_AUDITORIA_INTERNA = "NORMAS_GLOBAIS_AUDITORIA_INTERNA", "Normas Globais de Auditoria Interna"

    MANUAL_DE_CONTABILIDADE_DO_SETOR_ELETRICO_MCSE = "MANUAL_DE_CONTABILIDADE_DO_SETOR_ELETRICO_MCSE", "Manual de Contabilidade do Setor Elétrico – MCSE"
    MANUAL_DE_CONTROLE_PATRIMONIAL_DO_SETOR_ELETRICO_MCPSE = "MANUAL_DE_CONTROLE_PATRIMONIAL_DO_SETOR_ELETRICO_MCPSE", "Manual de Controle Patrimonial do Setor Elétrico – MCPSE"

    PROCEDIMENTOS_DE_COMERCIALIZACAO_PDC = "PROCEDIMENTOS_DE_COMERCIALIZACAO_PDC", "Procedimentos de Comercialização - PdC"
    PROCEDIMENTO_PROGRAMA_EFICIENCIA_ENERGETICA_PROPEE = "PROCEDIMENTO_PROGRAMA_EFICIENCIA_ENERGETICA_PROPEE", "Procedimentos do Programa de Eficiência Energética - PROPEE"
    PROCEDIMENTO_DE_DISTRIBUICAO_DE_ENERGIA_ELETRICA_PRODIST = "PROCEDIMENTO_DE_DISTRIBUICAO_DE_ENERGIA_ELETRICA_PRODIST", "Procedimentos de Distribuição de Energia Elétrica no Sistema Elétrico Nacional – PRODIST"
    PROCEDIMENTOS_REDE_ONS = "PROCEDIMENTOS_REDE_ONS", "Procedimentos de Rede do Operador Nacional do Sistema Elétrico (ONS)"

    RELATORIO_ADMNISTRACAO = "RELATORIO_ADMNISTRACAO", "Relatório de Administração"
    RELATORIO_IMPACTO_REGULATORIO = "RELATORIO_IMPACTO_REGULATORIO", "Relatório de Impacto Regulatório"

    SUSTENTABILIDADE_AMBIENTAL = "SUSTENTABILIDADE_AMBIENTAL", "Sustentabilidade Ambiental"
    SUSTENTABILIDADE_SOCIAL = "SUSTENTABILIDADE_SOCIAL", "Sustentabilidade Social"
