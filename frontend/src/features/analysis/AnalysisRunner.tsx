import { useState } from 'react'

import { apiClient } from '../../shared/api/client'
import type { AnalysisExecutionOut } from '../../shared/types/contracts'

interface AnalysisRunnerProps {
  repositoryId: number | null
  selectedPolicyIds: number[]
  onAnalysisFinished: (execution: AnalysisExecutionOut) => void
}

export function AnalysisRunner({ repositoryId, selectedPolicyIds, onAnalysisFinished }: AnalysisRunnerProps) {
  const [error, setError] = useState<string | null>(null)
  const [running, setRunning] = useState(false)

  const disabled = !repositoryId || selectedPolicyIds.length === 0 || running

  const run = async () => {
    if (!repositoryId) {
      return
    }
    setError(null)
    setRunning(true)
    try {
      const execution = await apiClient.createAnalysis(repositoryId, selectedPolicyIds)
      const finalExecution = await apiClient.runAnalysis(execution.id)
      onAnalysisFinished(finalExecution)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible ejecutar analisis')
    } finally {
      setRunning(false)
    }
  }

  return (
    <section className="rounded-lg border border-slate-300 bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">Motor de analisis</h2>
      <p className="mt-2 text-sm text-slate-700">
        Repositorio: {repositoryId ?? '-'} | Politicas: {selectedPolicyIds.length}
      </p>
      <button
        type="button"
        className="mt-3 rounded bg-emerald-700 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
        disabled={disabled}
        onClick={run}
      >
        {running ? 'Ejecutando...' : 'Ejecutar analisis'}
      </button>
      {error && <p className="mt-3 text-sm text-red-700">{error}</p>}
    </section>
  )
}
