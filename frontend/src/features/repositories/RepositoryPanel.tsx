import { useState } from 'react'

import { apiClient } from '../../shared/api/client'
import type { ArtifactListOut, ArtifactSummaryOut, RepositoryOut } from '../../shared/types/contracts'

interface RepositoryPanelProps {
  repository: RepositoryOut | null
  onRepositoryLoaded: (repository: RepositoryOut, artifacts: ArtifactListOut, summary: ArtifactSummaryOut) => void
}

export function RepositoryPanel({ repository, onRepositoryLoaded }: RepositoryPanelProps) {
  const [rootPath, setRootPath] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleLoad = async () => {
    setError(null)
    setLoading(true)
    try {
      const repo = await apiClient.loadRepository(rootPath)
      const artifacts = await apiClient.listArtifacts(repo.id)
      const summary = await apiClient.artifactsSummary(repo.id)
      onRepositoryLoaded(repo, artifacts, summary)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No se pudo cargar el repositorio')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="rounded-lg border border-slate-300 bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">Carga de repositorio</h2>
      <div className="mt-3 flex gap-2">
        <input
          className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
          placeholder="/ruta/al/repositorio"
          value={rootPath}
          onChange={(e) => setRootPath(e.target.value)}
        />
        <button
          type="button"
          className="rounded bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
          onClick={handleLoad}
          disabled={loading || rootPath.trim().length === 0}
        >
          {loading ? 'Cargando...' : 'Cargar'}
        </button>
      </div>
      {repository && (
        <p className="mt-3 text-sm text-slate-700">
          Repositorio activo: <span className="font-medium">{repository.name}</span>
        </p>
      )}
      {error && <p className="mt-3 text-sm text-red-700">{error}</p>}
    </section>
  )
}
