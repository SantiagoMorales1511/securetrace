import type {
  AnalysisExecutionOut,
  AnalysisResultsOut,
  ArtifactListOut,
  ArtifactSummaryOut,
  EvidenceListOut,
  PolicyOut,
  RuleOut,
  RepositoryOut,
} from '../types/contracts'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: 'Error inesperado' }))
    throw new Error(payload.detail ?? 'Error inesperado')
  }
  return (await response.json()) as T
}

export const apiClient = {
  loadRepository: (rootPath: string) =>
    request<RepositoryOut>('/repositories/load', {
      method: 'POST',
      body: JSON.stringify({ root_path: rootPath }),
    }),

  listArtifacts: (repositoryId: number) =>
    request<ArtifactListOut>(`/repositories/${repositoryId}/artifacts`),

  artifactsSummary: (repositoryId: number) =>
    request<ArtifactSummaryOut>(`/repositories/${repositoryId}/artifacts/summary`),

  listPolicies: () => request<PolicyOut[]>('/policies'),

  listPolicyRules: (policyId: number) => request<RuleOut[]>(`/policies/${policyId}/rules`),

  createAnalysis: (repositoryId: number, policyIds: number[]) =>
    request<AnalysisExecutionOut>('/analysis', {
      method: 'POST',
      body: JSON.stringify({ repository_id: repositoryId, policy_ids: policyIds }),
    }),

  runAnalysis: (executionId: number) =>
    request<AnalysisExecutionOut>(`/analysis/${executionId}/run`, {
      method: 'POST',
    }),

  getResults: (executionId: number) => request<AnalysisResultsOut>(`/analysis/${executionId}/results`),

  getEvidence: (executionId: number) => request<EvidenceListOut>(`/analysis/${executionId}/evidence`),
}
