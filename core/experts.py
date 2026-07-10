class BaseExpert:
    def __init__(self, brain):
        self.brain = brain

class InfraExpert(BaseExpert):
    """Especialista em Redes, Docker e Zabbix (v40.0)."""
    def run(self, context=None):
        self.brain.kernel.log_event("INFRA", "Iniciando Varredura de Observabilidade.")
        
        # 1. Auditoria de Sistema
        audit = self.brain.tools.self_audit()
        
        # 2. Varredura Zabbix
        alerts = self.brain.tools.get_zabbix_alerts()
        critical_alerts = [a for a in alerts if a['severity'] == "Desastre"]
        
        status_msg = "✅ Estável" if "OFFLINE" not in str(audit) else "🚨 Alerta Detectado"
        
        report = []
        report.append(f"**STATUS GERAL:** {status_msg}")
        report.append(f"**SNAPSHOT SISTEMA:** {' | '.join(audit[:3])}")
        
        if critical_alerts:
            report.append("\n🚨 **ALERTAS CRÍTICOS ZABBIX:**")
            for alert in critical_alerts:
                msg = f"Host: {alert['host']} | Incidente: {alert['trigger']}"
                report.append(f"  • {msg}")
                # Auto-Cura: Criar Ticket no GLPI automaticamente
                ticket_created = self.brain.tools.create_glpi_ticket(f"ALERTA ZABBIX: {alert['trigger']}", msg)
                if ticket_created:
                    report.append(f"    └─ ✅ Ticket GLPI criado com sucesso.")
        else:
            report.append("\n🟢 **OBSERVABILIDADE:** Nenhuma anomalia crítica detectada nos hosts monitorados.")
        
        return "\n".join(report)

class DevExpert(BaseExpert):
    """Especialista em Python, PHP e Correção de Código (v40.0)."""
    def run(self, task):
        # 1. Tenta visão se houver menção a "erro na tela" ou "janela"
        vision_report = ""
        if any(x in task.lower() for x in ["tela", "janela", "veja", "olha", "erro visual"]):
            vision_report = self.brain.tools.analyze_screen()
        
        # 2. Usa o researcher para buscar padrões
        examples = self.brain.researcher.scan_for_patterns(task)
        
        res = [f"💻 [DEV-ANALYSIS]: {vision_report}"]
        res.append(f"Analisando lógica para '{task}'.")
        if examples:
            res.append(f"🔍 Encontrei {len(examples)} referências no disco E: para guiar a correção.")
        
        return "\n".join(res)

class VisionExpert(BaseExpert):
    """
    PACOTE 6000: VISION SPECIALIST v40.0
    Interage visualmente com o sistema operacional.
    """
    def run(self, command):
        self.brain.kernel.log_event("VISION", f"Comando visual recebido: {command}")
        report = self.brain.tools.analyze_screen()
        
        if "clique" in command.lower():
            # Exemplo de lógica de clique em coordenadas (Futuro: Detecção por IA)
            return f"{report}\n🖱️ Aguardando coordenadas neurais para execução do clique."
            
        return report

class KnowledgeExpert(BaseExpert):
    """Especialista em RAG e Documentação Corporativa."""
    def run(self, query):
        local = self.brain.knowledge.get_local_intelligence(query)
        return "📚 [KNOWLEDGE-REPORT]: " + ("\n".join(local) or "Nenhuma base local encontrada. Sugiro baixar o site oficial.")

class SQLExpert(BaseExpert):
    """
    PACOTE 1700: SQL SPECIALIST v40.0
    Expert cognitivo em esquemas GLPI (Assets, Tickets, Users).
    """
    def run(self, natural_query):
        cmd = natural_query.lower()
        self.brain.kernel.log_event("SQL", f"Processando query cognitiva: {natural_query}")
        
        # Mapeamento de intenções para tabelas GLPI
        if any(x in cmd for x in ["computador", "ativo", "máquina", "hardware"]):
            return self.execute_and_format("SELECT name, serial, contact FROM glpi_computers LIMIT 5", "Ativos de Hardware")
            
        if any(x in cmd for x in ["chamado", "ticket", "problema", "aberto"]):
            return self.execute_and_format("SELECT id, name, date FROM glpi_tickets WHERE status = 1 LIMIT 5", "Chamados Abertos")

        if any(x in cmd for x in ["usuário", "quem", "pessoa"]):
            return self.execute_and_format("SELECT name, realname FROM glpi_users LIMIT 5", "Lista de Usuários")
        
        # EXECUTIVE CHRONICLER: Documentar ação no KB
        if "documente" in cmd or "registre" in cmd:
            title = f"Documentação Automática: {cmd[:30]}..."
            content = f"Procedimento registrado automaticamente pelo SOLPI-OS v40.0 baseado na interação: {natural_query}"
            if self.brain.tools.create_glpi_kb_article(title, content):
                return f"✅ [CHRONICLER]: Procedimento documentado com sucesso na Base de Conhecimento do GLPI."

        return "🛠️ [SQL]: Não identifiquei uma entidade GLPI clara na sua pergunta. Tente 'listar chamados' ou 'ver ativos'."

    def execute_and_format(self, sql, title):
        try:
            conn = pymysql.connect(host='localhost', port=3306, user='glpi', password='glpi', database='glpi')
            with conn.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
            conn.close()
            
            if not rows: return f"🔍 [SQL]: Nenhum registro encontrado para {title}."
            
            res = [f"📊 [RELATÓRIO GLPI: {title}]:"]
            for row in rows:
                res.append(f" - {' | '.join(map(str, row))}")
            return "\n".join(res)
        except Exception as e:
            return f"❌ [SQL ERROR]: Falha na conexão com o Banco GLPI: {e}"
