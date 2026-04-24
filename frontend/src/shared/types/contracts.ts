export type ArtifactType = 'source' | 'config' | 'dependency' | 'other'
export type AnalysisStatus = 'pending' | 'running' | 'completed' | 'failed'
export type PolicyComplianceStatus = 'cumple' | 'no_cumple' | 'requiere_revision'
export type EvidenceResult = 'pass' | 'fail' | 'review' | 'error'

export interface RepositoryOut {
  id: number
  name: string
  root_path: string
  status: 'loaded' | 'invalid'
  loaded_at: string
}

export interface ArtifactOut {
  id: number
  repository_id: number
  relative_path: string
  extension: string
  artifact_type: ArtifactType
  size_bytes: number
}

export interface ArtifactListOut {
  repository_id: number
  total: number
  artifacts: ArtifactOut[]
}

export interface ArtifactSummaryItem {
  artifact_type: ArtifactType
  count: number
}

export interface ArtifactSummaryOut {
  repository_id: number
  summary: ArtifactSummaryItem[]
}

export interface PolicyOut {
  id: number
  code: string
  name: string
  description: string
  category: string
  is_active: boolean
}

export interface RuleOut {
  id: number
  policy_id: number
  code: string
  name: string
  description: string
  rule_type: string
  artifact_scope: string
  severity_default: string
}

export interface AnalysisExecutionOut {
  id: number
  repository_id: number
  status: AnalysisStatus
  started_at: string
  finished_at: string | null
}

export interface PolicyResultOut {
  id: number
  analysis_execution_id: number
  policy_id: number
  status: PolicyComplianceStatus
  score_optional: string | null
  summary: string
}

export interface AnalysisResultsOut {
  analysis_execution_id: number
  results: PolicyResultOut[]
}

export interface EvidenceOut {
  id: number
  analysis_execution_id: number
  policy_id: number
  rule_id: number
  artifact_id: number | null
  result: EvidenceResult
  message: string
  snippet: string | null
}

export interface EvidenceListOut {
  analysis_execution_id: number
  evidence: EvidenceOut[]
}
