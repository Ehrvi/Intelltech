#!/usr/bin/env python3
"""
Automatic Credit Check with Mobile Notifications
Runs at the start of every chat to check API credits and notify user
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from credit_monitor import CreditMonitor, APIStatus

def format_notification(api_name: str, api_info, notification_type: str) -> dict:
    """Format notification for mobile app"""
    
    if notification_type == 'critical':
        return {
            'level': 'critical',
            'title': f'🚨 AÇÃO NECESSÁRIA: {api_name} sem créditos!',
            'message': f"""
Recarregue em: {api_info.recharge_url}

Impacto: Sistema vai usar só Manus (99% mais caro)
Custo extra estimado: ${api_info.estimated_monthly_cost * 4:.0f}/dia sem {api_name}

AÇÃO IMEDIATA NECESSÁRIA para manter economia de 95%
""".strip(),
            'url': api_info.recharge_url,
            'priority': 'high'
        }
    
    elif notification_type == 'warning':
        return {
            'level': 'warning',
            'title': f'⚠️ AVISO: {api_name} com créditos baixos',
            'message': f"""
Recarregue em: {api_info.recharge_url}

Impacto: Pode ficar sem créditos em breve
Custo mensal: ${api_info.estimated_monthly_cost:.2f}

Recomendado recarregar nas próximas 24-48h
""".strip(),
            'url': api_info.recharge_url,
            'priority': 'medium'
        }
    
    elif notification_type == 'error':
        return {
            'level': 'error',
            'title': f'❌ ERRO: {api_name} com problema de conexão',
            'message': f"""
Verifique configuração da API

Impacto: {api_name} não disponível
Sistema vai usar alternativas ou Manus

Verifique: API key, billing, configuração
""".strip(),
            'url': api_info.recharge_url if api_info.recharge_url else None,
            'priority': 'medium'
        }
    
    return None

def check_and_notify():
    """
    Check all API credits and generate notifications
    Returns: (has_critical, has_warnings, notifications)
    """
    monitor = CreditMonitor()
    results = monitor.check_all_apis()
    
    notifications = []
    has_critical = False
    has_warnings = False
    
    for api_name, api_info in results.items():
        # Skip free services
        if not api_info.requires_payment:
            continue
        
        # Check status and generate notifications
        if api_info.status == APIStatus.NO_CREDITS:
            notification = format_notification(api_info.name, api_info, 'critical')
            notifications.append(notification)
            has_critical = True
        
        elif api_info.status == APIStatus.LOW_CREDITS:
            notification = format_notification(api_info.name, api_info, 'warning')
            notifications.append(notification)
            has_warnings = True
        
        elif api_info.status == APIStatus.ERROR:
            # Only notify for critical APIs (OpenAI)
            if api_name == 'openai':
                notification = format_notification(api_info.name, api_info, 'error')
                notifications.append(notification)
                has_warnings = True
    
    return has_critical, has_warnings, notifications, results

def generate_summary_message(results: dict) -> str:
    """Generate summary message for chat start"""
    
    lines = []
    lines.append("=" * 60)
    lines.append("  STATUS DE CRÉDITOS - APIs")
    lines.append("=" * 60)
    
    # Count statuses
    healthy = 0
    issues = 0
    
    for api_name, api_info in results.items():
        if not api_info.requires_payment:
            continue
        
        if api_info.status == APIStatus.HEALTHY:
            healthy += 1
        else:
            issues += 1
    
    if issues == 0:
        lines.append("")
        lines.append("✅ Todos os sistemas operacionais")
        lines.append(f"   {healthy} APIs com créditos suficientes")
        lines.append("")
        lines.append("Sistema otimizado ativo:")
        lines.append("  • 90% das tarefas → OpenAI ($0.045/tarefa)")
        lines.append("  • 10% das tarefas → Manus ($5.00/tarefa)")
        lines.append("  • Economia: 95% vs Manus-only")
        lines.append("")
    else:
        lines.append("")
        lines.append(f"⚠️  {issues} problema(s) detectado(s)")
        lines.append(f"✅ {healthy} API(s) funcionando normalmente")
        lines.append("")
        
        # List issues
        for api_name, api_info in results.items():
            if not api_info.requires_payment:
                continue
            
            if api_info.status != APIStatus.HEALTHY:
                status_icon = {
                    APIStatus.NO_CREDITS: "🚨",
                    APIStatus.LOW_CREDITS: "⚠️",
                    APIStatus.ERROR: "❌"
                }.get(api_info.status, "❓")
                
                lines.append(f"{status_icon} {api_info.name}: {api_info.status.value}")
                if api_info.recharge_url:
                    lines.append(f"   Recarregar: {api_info.recharge_url}")
        lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)

def main():
    """Main function for automatic credit check"""
    
    print("\n🔍 Verificando créditos de APIs...\n")
    
    has_critical, has_warnings, notifications, results = check_and_notify()
    
    # Print summary
    summary = generate_summary_message(results)
    print(summary)
    
    # Print notifications if any
    if notifications:
        print("\n📱 NOTIFICAÇÕES PARA CELULAR:")
        print("=" * 60)
        for notif in notifications:
            print(f"\n{notif['title']}")
            print(notif['message'])
            print()
        print("=" * 60)
    
    # Return exit code
    if has_critical:
        print("\n⚠️  AÇÃO IMEDIATA NECESSÁRIA: Alguns serviços sem créditos!")
        return 2  # Critical
    elif has_warnings:
        print("\n⚠️  Atenção: Alguns serviços precisam de atenção")
        return 1  # Warning
    else:
        print("\n✅ Tudo funcionando perfeitamente!")
        return 0  # OK

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
