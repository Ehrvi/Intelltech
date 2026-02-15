# Prompt: Implementar Sistema Moderno de Indexação de Conhecimento (V2.0)

## 1. Contexto e Objetivo

Devido ao crescimento exponencial do conhecimento da AI University e do sistema de gerenciamento de conhecimento global, precisamos de um sistema de indexação de arquivos que torne a informação acessível de forma rápida e confiável a todos os agentes (servos).

**Objetivo:** Criar um sistema de indexação moderno usando as melhores práticas atuais que permita:
1. **Busca rápida** (< 100ms) em toda a base de conhecimento
2. **Indexação incremental** (apenas arquivos modificados)
3. **Busca fuzzy** (tolerante a erros de digitação)
4. **Ranking por relevância** (melhores resultados primeiro)
5. **Filtros por tipo** (lições, projetos, documentação, core)
6. **Extração de metadados** automática de arquivos Markdown
7. **CLI simples** para uso fácil

## 2. Processo de Implementação (OBRIGATÓRIO)

### Fase 1: Pesquisa Científica (OBRIGATÓRIA - 1 hora)

**Antes de escrever QUALQUER código, você DEVE pesquisar:**

1. **Fundamentos de Information Retrieval**
   - Teoria de inverted indices [1]
   - Algoritmos de ranking (BM25, TF-IDF) [2]
   - Otimização de queries

2. **Tecnologias Modernas (2024-2026)**
   - Comparação: Whoosh vs Elasticsearch vs Solr vs SQLite FTS
   - Vector databases para busca semântica
   - Abordagens de busca híbrida

3. **Best Practices de Knowledge Management**
   - Extração de metadados
   - Classificação e tagging
   - Análise de cross-references

**Fontes de Qualidade (OBRIGATÓRIAS):**
- ✅ **OpenAI (gpt-4o)** para overview (0.01 créditos)
- ✅ **Anna's Archive** para papers específicos
- ✅ **Referências Científicas:**
  - Zobel & Moffat (2006) - Inverted files for text search engines [1]
  - Manning, Raghavan & Schütze (2008) - Introduction to Information Retrieval [2]

**Checklist de Pesquisa (OBRIGATÓRIO):**
- [ ] Li profundamente (não apenas superficialmente)
- [ ] Avaliei qualidade da fonte criticamente
- [ ] Cross-referenciei informações
- [ ] Entendi profundamente (posso explicar)
- [ ] Sintetizei conhecimento (não apenas coletei)

### Fase 2: Design (30 min)

**Baseado na pesquisa, você DEVE decidir:**
1. **Tecnologia:** Whoosh (justificativa: sem servidor, Python puro, suficiente)
2. **Schema:** Campos, tipos, pesos
3. **Indexação:** Incremental (hash-based)
4. **Interface:** CLI + API

### Fase 3: Implementação (3.5 horas)

**Ordem de implementação:**
1. Schema definition
2. KnowledgeIndexer class skeleton
3. Index initialization
4. File hashing and cache
5. Metadata extraction
6. Index single file
7. Index all files (incremental)
8. Search functionality
9. Statistics and utilities
10. CLI tool
11. Testing

### Fase 4: Testes (30 min)

**Testes essenciais:**
1. Index all files
2. Search with various queries
3. Incremental indexing
4. Fuzzy search
5. Type filtering
6. Statistics
7. CLI commands

### Fase 5: Documentação (30 min)

**Documentar:**
1. Como usar a classe e o CLI
2. Como fazer rebuild do índice
3. Troubleshooting
4. Referências bibliográficas da pesquisa

## 3. Requisitos Técnicos

### 3.1. Tecnologia
- **Biblioteca:** Whoosh (Python)
- **Ranking:** BM25F

### 3.2. Arquitetura
- `core/knowledge_index.py`
- `tools/search_knowledge.py`
- `search_index/`
- `search_index/file_cache.json`

### 3.3. Schema
```python
Schema(
    path=ID(stored=True, unique=True),
    filename=TEXT(stored=True),
    title=TEXT(stored=True, field_boost=2.0),
    content=TEXT(stored=True),
    tags=KEYWORD(stored=True, commas=True),
    doc_type=ID(stored=True),
    created=DATETIME(stored=True),
    modified=DATETIME(stored=True),
    author=TEXT(stored=True),
    references=KEYWORD(stored=True, commas=True)
)
```

## 4. Enforcement de Normas (OBRIGATÓRIO)

**Este prompt FORÇA o agente a seguir TODAS as normas definidas no sistema:**

### ✅ LESSON_017: Autonomous Decision Making
- **Não pergunte, decida:** O prompt define decisões claras (Whoosh, schema, etc.) sem pedir confirmação.
- **Framework de decisão:** Fase 2 (Design) força decisões baseadas em pesquisa.

### ✅ LESSON_018: Automatic Cost Reporting
- **Custo vs Benefício (Seção 5)** documenta custos e ROI.
- Agente deve usar cost tracking durante implementação.

### ✅ LESSON_019: External Research Integration
- **Fase 1 (Pesquisa)** é OBRIGATÓRIA e inclui fontes externas (OpenAI, Anna's Archive).
- **Fontes de Qualidade** especifica exatamente onde pesquisar.

### ✅ LESSON_020: Integrated Development Process
- **Fase 1 (Pesquisa)** força descoberta interna ANTES de pesquisa externa.
- **Fase 2 (Design)** força decisões baseadas em contexto interno + pesquisa.
- **Fase 3 (Implementação)** segue ordem específica para integração suave.

### ✅ LESSON_021: Scientific Foundation Mandatory
- **Fase 1 (Pesquisa)** exige pesquisa científica de qualidade com fontes autoritativas.
- **Fase 5 (Documentação)** exige referências bibliográficas (Seção 6).
- **Checklist de Pesquisa** força validação de qualidade científica.

### ✅ LESSON_021: Always Study to the Maximum
- **Fase 1 (Pesquisa)** é obrigatória (1 hora) e detalhada, forçando estudo profundo antes de agir.
- **Checklist** com 5 itens obrigatórios antes de continuar.

### ✅ LESSON_021: Quality Research, Not Superficial
- **Checklist de Pesquisa** força:
  - Leitura profunda (não superficial)
  - Avaliação crítica de fontes
  - Cross-referência de informações
  - Compreensão profunda (pode explicar)
  - Síntese de conhecimento

### ✅ LESSON_01: Cost Optimization
- **Fontes de Qualidade** priorizam:
  - OpenAI (0.01 créditos) - PRIMEIRO
  - Anna's Archive (gratuito) - papers específicos
  - Evita `search` (20 créditos) e `browser` (30 créditos)
- **Seção 5 (Custo vs Benefício)** documenta economia.

### ✅ COGNITIVE_ENFORCEMENT_PROTOCOL
- **Fase 1 (Pesquisa)** força checklist mental antes de cada operação.
- **Decisões baseadas em custo** (OpenAI primeiro).

### ✅ SCIENTIFIC_METHODOLOGY_REQUIREMENTS V3.0
- **Fase 1 (Pesquisa)** segue processo científico de 12 passos.
- **Referências obrigatórias** (Seção 6).
- **Anna's Archive** como fonte primária para papers.

---

## 4.1. Validação de Enforcement

**Antes de começar a implementação, o agente DEVE verificar:**

- [ ] Li TODAS as lições relevantes (017, 018, 019, 020, 021, 01)
- [ ] Entendi o COGNITIVE_ENFORCEMENT_PROTOCOL
- [ ] Revisei SCIENTIFIC_METHODOLOGY_REQUIREMENTS V3.0
- [ ] Estou pronto para seguir TODAS as normas

**Se algum item não marcado → Estudar mais antes de continuar.**

## 5. Custo vs Benefício

- **Custo:** 20-50 créditos, 5.5 horas
- **Benefício:** Infinito (uso permanente)
- **ROI:** Extraordinário

## 6. Referências

[1] Zobel, J., & Moffat, A. (2006). Inverted files for text search engines. *ACM Computing Surveys*, 38(2), 6.  
[2] Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
