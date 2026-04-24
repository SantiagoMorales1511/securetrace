import { useEffect, useState } from 'react'

import { apiClient } from '../../shared/api/client'
import type {
  AnalysisExecutionOut,
  AnalysisResultsOut,
  EvidenceListOut,
  PolicyOut,
} from '../../shared/types/contracts'

interface ResultsPanelProps {
  execution: AnalysisExecutionOut | null
  policies: PolicyOut[]
}

const STATUS_COLORS: Record<string, string> = {
  cumple: 'bg-emerald-100 text-emerald-800',
  no_cumple: 'bg-red-100 text-red-800',
  requiere_revision: 'bg-amber-100 text-amber-800',
}

export function ResultsPanel({ execution, policies }: ResultsPanelProps) {
  const [results, setResults] = useState<AnalysisResultsOut | null>(null)
  const [evidence, setEvidence] = useState<EvidenceListOut | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!execution) {
      return
    }

    const load = async () => {
      setError(null)
      try {
        const [resultsResponse, evidenceResponse] = await Promise.all([
          apiClient.getResults(execution.id),
          apiClient.getEvidence(execution.id),
        ])
        setResults(resultsResponse)
        setEvidence(evidenceResponse)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'No se pudieron cargar resultados')
      }
    }

    void load()
  }, [execution])

  if (!execution) {
    return null
  }

  const policyMap = new Map(policies.map((policy) => [policy.id, policy.name]))

  return (
    <section className="rounded-lg border border-slate-300 bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">Resultados preliminares</h2>
      <p className="mt-2 text-sm text-slate-700">
        Ejecucion {execution.id} - estado {execution.status}
      </p>
      {error && <p className="mt-3 text-sm text-red-700">{error}</p>}

      <div className="mt-3 space-y-2">
        {results?.results.map((result) => (
          <div key={result.id} className="rounded border border-slate-200 p-3">
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold text-slate-900">{policyMap.get(result.policy_id) ?? result.policy_id}</p>
              <span className={`rounded px-2 py-1 text-xs font-semibold ${STATUS_COLORS[result.status]}`}>
                {result.status}
              </span>
            </div>
            <p className="mt-1 text-xs text-slate-700">{result.summary}</p>
          </div>
        ))}
      </div>

      <div className="mt-4 max-h-56 overflow-auto rounded border border-slate-200">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-100 text-slate-700">
            <tr>
              <th className="px-2 py-2">Politica</th>
              <th className="px-2 py-2">Regla</th>
              <th className="px-2 py-2">Resultado</th>
              <th className="px-2 py-2">Mensaje</th>
            </tr>
          </thead>
          <tbody>
            {evidence?.evidence.map((item) => (
              <tr key={item.id} className="border-t border-slate-100">
                <td className="px-2 py-1">{policyMap.get(item.policy_id) ?? item.policy_id}</td>
                <td className="px-2 py-1">{item.rule_id}</td>
                <td className="px-2 py-1">{item.result}</td>
                <td className="px-2 py-1">{item.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
