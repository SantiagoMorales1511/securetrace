import { useState } from 'react'

import { AnalysisRunner } from '../features/analysis/AnalysisRunner'
import { PolicySelector } from '../features/policies/PolicySelector'
import { ArtifactViews } from '../features/repositories/ArtifactViews'
import { RepositoryPanel } from '../features/repositories/RepositoryPanel'
import { ResultsPanel } from '../features/results/ResultsPanel'
import type {
  AnalysisExecutionOut,
  ArtifactListOut,
  ArtifactSummaryOut,
  PolicyOut,
  RepositoryOut,
} from '../shared/types/contracts'

export function AppShell() {
  const [repository, setRepository] = useState<RepositoryOut | null>(null)
  const [artifacts, setArtifacts] = useState<ArtifactListOut | null>(null)
  const [summary, setSummary] = useState<ArtifactSummaryOut | null>(null)
  const [selectedPolicyIds, setSelectedPolicyIds] = useState<number[]>([])
  const [execution, setExecution] = useState<AnalysisExecutionOut | null>(null)
  const [policies, setPolicies] = useState<PolicyOut[]>([])

  const handleRepositoryLoaded = (
    loadedRepository: RepositoryOut,
    loadedArtifacts: ArtifactListOut,
    loadedSummary: ArtifactSummaryOut,
  ) => {
    setRepository(loadedRepository)
    setArtifacts(loadedArtifacts)
    setSummary(loadedSummary)
    setExecution(null)
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col gap-4 bg-slate-50 p-4">
      <header>
        <p className="text-sm text-slate-700">
          Analisis automatizado preliminar de cumplimiento de politicas de seguridad
        </p>
      </header>

      <RepositoryPanel repository={repository} onRepositoryLoaded={handleRepositoryLoaded} />
      <ArtifactViews artifacts={artifacts} summary={summary} />
      <PolicySelector
        selectedPolicyIds={selectedPolicyIds}
        onChange={setSelectedPolicyIds}
        onPoliciesLoaded={setPolicies}
      />
      <AnalysisRunner
        repositoryId={repository?.id ?? null}
        selectedPolicyIds={selectedPolicyIds}
        onAnalysisFinished={setExecution}
      />
      <ResultsPanel execution={execution} policies={policies} />
    </main>
  )
}
