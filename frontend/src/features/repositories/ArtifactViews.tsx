import type { ArtifactListOut, ArtifactSummaryOut } from '../../shared/types/contracts'

interface ArtifactViewsProps {
  artifacts: ArtifactListOut | null
  summary: ArtifactSummaryOut | null
}

export function ArtifactViews({ artifacts, summary }: ArtifactViewsProps) {
  if (!artifacts || !summary) {
    return null
  }

  return (
    <section className="rounded-lg border border-slate-300 bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">Artefactos detectados</h2>
      <p className="mt-2 text-sm text-slate-700">Total de archivos: {artifacts.total}</p>

      <div className="mt-3 flex flex-wrap gap-2">
        {summary.summary.map((item) => (
          <span key={item.artifact_type} className="rounded bg-slate-100 px-2 py-1 text-xs text-slate-700">
            {item.artifact_type}: {item.count}
          </span>
        ))}
      </div>

      <div className="mt-4 max-h-64 overflow-auto rounded border border-slate-200">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-100 text-slate-700">
            <tr>
              <th className="px-2 py-2">Archivo</th>
              <th className="px-2 py-2">Tipo</th>
              <th className="px-2 py-2">Tamano</th>
            </tr>
          </thead>
          <tbody>
            {artifacts.artifacts.map((artifact) => (
              <tr key={artifact.id} className="border-t border-slate-100">
                <td className="px-2 py-1 font-mono">{artifact.relative_path}</td>
                <td className="px-2 py-1">{artifact.artifact_type}</td>
                <td className="px-2 py-1">{artifact.size_bytes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
