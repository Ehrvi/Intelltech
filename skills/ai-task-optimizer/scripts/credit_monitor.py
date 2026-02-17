#!/usr/bin/env python3
"""
API Credit Monitoring System
Monitors APIs that require credits/payment and notifies user when recharge is needed
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum

class APIStatus(Enum):
    """API credit status"""
    HEALTHY = "healthy"
    LOW_CREDITS = "low_credits"
    NO_CREDITS = "no_credits"
    ERROR = "error"
    UNKNOWN = "unknown"

@dataclass
class APIInfo:
    """Information about an API that requires credits"""
    name: str
    requires_payment: bool
    check_method: str  # 'api_call', 'env_var', 'manual'
    cost_per_request: float
    estimated_monthly_cost: float
    recharge_url: Optional[str] = None
    status: APIStatus = APIStatus.UNKNOWN
    credits_remaining: Optional[float] = None
    last_checked: Optional[str] = None

class CreditMonitor:
    """Monitor APIs that require credits/payment"""
    
    # API Registry
    APIS = {
        'openai': APIInfo(
            name='OpenAI API',
            requires_payment=True,
            check_method='api_call',
            cost_per_request=0.045,
            estimated_monthly_cost=15.0,  # For intensive use
            recharge_url='https://platform.openai.com/settings/organization/billing'
        ),
        'apollo': APIInfo(
            name='Apollo API',
            requires_payment=True,
            check_method='api_call',
            cost_per_request=0.01,
            estimated_monthly_cost=5.0,
            recharge_url='https://app.apollo.io/#/settings/credits'
        ),
        'gmail_mcp': APIInfo(
            name='Gmail MCP',
            requires_payment=False,
            check_method='manual',
            cost_per_request=0.0,
            estimated_monthly_cost=0.0
        ),
        'calendar_mcp': APIInfo(
            name='Google Calendar MCP',
            requires_payment=False,
            check_method='manual',
            cost_per_request=0.0,
            estimated_monthly_cost=0.0
        ),
        'manus': APIInfo(
            name='Manus',
            requires_payment=True,
            check_method='manual',
            cost_per_request=5.0,
            estimated_monthly_cost=150.0,  # With optimization
            recharge_url='https://manus.im/pricing'
        )
    }
    
    def check_openai_status(self) -> APIInfo:
        """Check OpenAI API status"""
        api_info = self.APIS['openai']
        
        try:
            from openai import OpenAI
            client = OpenAI()
            
            # Test with minimal request
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{'role': 'user', 'content': 'test'}],
                max_tokens=1
            )
            
            api_info.status = APIStatus.HEALTHY
            api_info.last_checked = datetime.now().isoformat()
            
        except Exception as e:
            error_str = str(e).lower()
            if 'insufficient_quota' in error_str or 'quota' in error_str:
                api_info.status = APIStatus.NO_CREDITS
            elif 'billing' in error_str:
                api_info.status = APIStatus.LOW_CREDITS
            else:
                api_info.status = APIStatus.ERROR
            
            api_info.last_checked = datetime.now().isoformat()
        
        return api_info
    
    def check_apollo_status(self) -> APIInfo:
        """Check Apollo API status"""
        api_info = self.APIS['apollo']
        
        try:
            import requests
            api_key = os.environ.get('APOLLO_API_KEY')
            
            if not api_key:
                api_info.status = APIStatus.ERROR
                return api_info
            
            # Health check
            response = requests.get(
                'https://api.apollo.io/v1/auth/health',
                headers={'X-Api-Key': api_key},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('healthy') and data.get('is_logged_in'):
                    api_info.status = APIStatus.HEALTHY
                else:
                    api_info.status = APIStatus.ERROR
            else:
                api_info.status = APIStatus.ERROR
            
            api_info.last_checked = datetime.now().isoformat()
            
        except Exception as e:
            api_info.status = APIStatus.ERROR
            api_info.last_checked = datetime.now().isoformat()
        
        return api_info
    
    def check_all_apis(self) -> Dict[str, APIInfo]:
        """Check status of all APIs"""
        results = {}
        
        # Check OpenAI
        results['openai'] = self.check_openai_status()
        
        # Check Apollo
        results['apollo'] = self.check_apollo_status()
        
        # Free services (no check needed)
        results['gmail_mcp'] = self.APIS['gmail_mcp']
        results['calendar_mcp'] = self.APIS['calendar_mcp']
        
        # Manus (manual check)
        results['manus'] = self.APIS['manus']
        
        return results
    
    def get_notifications(self, results: Dict[str, APIInfo]) -> List[str]:
        """Generate notifications for APIs that need attention"""
        notifications = []
        
        for api_name, api_info in results.items():
            if not api_info.requires_payment:
                continue
            
            if api_info.status == APIStatus.NO_CREDITS:
                notifications.append(
                    f"🚨 CRÍTICO: {api_info.name} sem créditos! "
                    f"Recarregue em: {api_info.recharge_url}"
                )
            
            elif api_info.status == APIStatus.LOW_CREDITS:
                notifications.append(
                    f"⚠️ AVISO: {api_info.name} com créditos baixos. "
                    f"Considere recarregar: {api_info.recharge_url}"
                )
            
            elif api_info.status == APIStatus.ERROR:
                notifications.append(
                    f"❌ ERRO: {api_info.name} com problema de conexão. "
                    f"Verifique configuração."
                )
        
        return notifications
    
    def generate_report(self) -> str:
        """Generate comprehensive status report"""
        results = self.check_all_apis()
        notifications = self.get_notifications(results)
        
        report = []
        report.append("="*70)
        report.append("  MONITORAMENTO DE CRÉDITOS - APIs")
        report.append("="*70)
        report.append("")
        
        # Paid APIs
        report.append("APIs QUE REQUEREM PAGAMENTO:")
        report.append("")
        
        for api_name, api_info in results.items():
            if not api_info.requires_payment:
                continue
            
            status_icon = {
                APIStatus.HEALTHY: "✅",
                APIStatus.LOW_CREDITS: "⚠️",
                APIStatus.NO_CREDITS: "🚨",
                APIStatus.ERROR: "❌",
                APIStatus.UNKNOWN: "❓"
            }.get(api_info.status, "❓")
            
            report.append(f"{status_icon} {api_info.name}")
            report.append(f"   Status: {api_info.status.value}")
            report.append(f"   Custo/requisição: ${api_info.cost_per_request:.4f}")
            report.append(f"   Custo mensal estimado: ${api_info.estimated_monthly_cost:.2f}")
            
            if api_info.recharge_url:
                report.append(f"   Recarga: {api_info.recharge_url}")
            
            if api_info.last_checked:
                report.append(f"   Última verificação: {api_info.last_checked}")
            
            report.append("")
        
        # Free services
        report.append("SERVIÇOS GRATUITOS:")
        report.append("")
        
        for api_name, api_info in results.items():
            if api_info.requires_payment:
                continue
            
            report.append(f"✅ {api_info.name} (Grátis)")
        
        report.append("")
        
        # Notifications
        if notifications:
            report.append("="*70)
            report.append("  NOTIFICAÇÕES")
            report.append("="*70)
            report.append("")
            for notification in notifications:
                report.append(notification)
            report.append("")
        
        # Cost summary
        total_monthly = sum([
            api.estimated_monthly_cost 
            for api in results.values() 
            if api.requires_payment
        ])
        
        report.append("="*70)
        report.append("  RESUMO DE CUSTOS")
        report.append("="*70)
        report.append("")
        report.append(f"Custo mensal estimado total: ${total_monthly:.2f}")
        report.append("")
        report.append("Nota: Com o sistema otimizado, 90% das tarefas usam OpenAI")
        report.append("      (muito mais barato que Manus), resultando em economia de 95%")
        report.append("")
        report.append("="*70)
        
        return "\n".join(report)


def main():
    """Main function"""
    monitor = CreditMonitor()
    report = monitor.generate_report()
    print(report)
    
    # Check for critical issues
    results = monitor.check_all_apis()
    notifications = monitor.get_notifications(results)
    
    if any('CRÍTICO' in n for n in notifications):
        print("\n⚠️  AÇÃO NECESSÁRIA: Alguns serviços precisam de recarga imediata!")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
