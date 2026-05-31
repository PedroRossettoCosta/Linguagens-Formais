import { API_BASE_URL } from '@/constants/api';

/**
 * Envia o ritual de código místico para o backend para compilação.
 * @param {string} code - Código-fonte místico (.ld).
 * @returns {Promise<object>} Objeto contendo os dados compilados ou erro.
 */
export async function compileRitual(code) {
  const response = await fetch(`${API_BASE_URL}/compile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code })
  });

  const data = await response.json();
  if (!response.ok || data.status !== 'success') {
    throw {
      status: 'error',
      erros: data.erros || [{ mensagem: 'Erro desconhecido no ritual místico.' }]
    };
  }

  return data;
}
