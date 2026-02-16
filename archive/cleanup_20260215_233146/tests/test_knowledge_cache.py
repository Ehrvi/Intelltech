#!/usr/bin/env python3

import unittest
import sys
import os
import shutil
import numpy as np
from pathlib import Path
from unittest.mock import patch

# Adicionar o diretório raiz do projeto ao Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.knowledge_cache import KnowledgeCache

class TestKnowledgeCache(unittest.TestCase):

    def setUp(self):
        self.base_path = Path(__file__).parent.parent / "test_cache_dir"
        self.base_path.mkdir(exist_ok=True)
        cache_file = self.base_path / "cache" / "knowledge_cache.jsonl"
        if cache_file.exists():
            os.remove(cache_file)

    def tearDown(self):
        if self.base_path.exists():
            shutil.rmtree(self.base_path)

    @patch('core.knowledge_cache.KnowledgeCache._get_embedding_with_retry')
    def test_save_and_search_with_similar_query(self, mock_get_embedding):
        """Testa se uma consulta semanticamente similar resulta em um cache hit."""
        cache = KnowledgeCache(base_path=self.base_path, similarity_threshold=0.9)

        query1 = "Qual é a capital da França?"
        similar_query = "Qual é a cidade capital da França?"
        dissimilar_query = "Qual é a melhor cobertura de pizza?"

        # Criar embeddings mockados
        embedding1 = np.random.rand(1536).astype(np.float32)
        # Criar um vetor muito similar para a consulta parecida
        embedding_similar = embedding1 + (np.random.rand(1536).astype(np.float32) * 0.01)
        # Criar um vetor completamente diferente para a consulta dissimilar
        embedding_dissimilar = np.random.rand(1536).astype(np.float32)

        def get_embedding_side_effect(text):
            if text == query1:
                return embedding1.tolist()
            if text == similar_query:
                return embedding_similar.tolist()
            if text == dissimilar_query:
                return embedding_dissimilar.tolist()
            return np.random.rand(1536).tolist() # Fallback

        mock_get_embedding.side_effect = get_embedding_side_effect

        # Salvar a consulta original
        cache.save(query1, "Paris")

        # Buscar com a consulta similar
        search_result = cache.search(similar_query)

        self.assertIsNotNone(search_result, "A busca por consulta similar não deveria retornar None")
        self.assertTrue(search_result["cache_hit"])
        self.assertEqual(search_result["result"], "Paris")
        self.assertGreater(search_result["similarity"], 0.9, "A similaridade deveria ser alta para consultas parecidas")

        # Buscar com a consulta dissimilar
        search_result_dissimilar = cache.search(dissimilar_query)
        self.assertIsNone(search_result_dissimilar, "A busca por consulta dissimilar deveria retornar None")

if __name__ == '__main__':
    unittest.main()
