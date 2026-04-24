import { useEffect, useMemo, useState } from 'react'

import { apiClient } from '../../shared/api/client'
import type { PolicyOut, RuleOut } from '../../shared/types/contracts'

interface PolicySelectorProps {
  selectedPolicyIds: number[]
  onChange: (policyIds: number[]) => void
  onPoliciesLoaded: (policies: PolicyOut[]) => void
}

export function PolicySelector({ selectedPolicyIds, onChange, onPoliciesLoaded }: PolicySelectorProps) {
  const [policies, setPolicies] = useState<PolicyOut[]>([])
  const [rulesByPolicy, setRulesByPolicy] = useState<Record<number, RuleOut[]>>({})
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const load = async () => {
      setError(null)
      try {
        const response = await apiClient.listPolicies()
        setPolicies(response)
        onPoliciesLoaded(response)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'No se pudieron cargar politicas')
      }
    }
    void load()
  }, [onPoliciesLoaded])

  const selectedPolicies = useMemo(
    () => policies.filter((policy) => selectedPolicyIds.includes(policy.id)),
    [policies, selectedPolicyIds],
  )

  const togglePolicy = (policyId: number) => {
    if (selectedPolicyIds.includes(policyId)) {
      onChange(selectedPolicyIds.filter((id) => id !== policyId))
      return
    }
    onChange([...selectedPolicyIds, policyId])
  }

  const loadRules = async (policyId: number) => {
    if (rulesByPolicy[policyId]) {
      return
    }
    const rules = await apiClient.listPolicyRules(policyId)
    setRulesByPolicy((prev) => ({ ...prev, [policyId]: rules }))
  }

  return (
    <section className="rounded-lg border border-slate-300 bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">Banco de politicas</h2>
      {error && <p className="mt-2 text-sm text-red-700">{error}</p>}

      <div className="mt-3 space-y-2">
        {policies.map((policy) => (
          <div key={policy.id} className="rounded border border-slate-200 p-3">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-sm font-semibold text-slate-900">{policy.name}</p>
                <p className="text-xs text-slate-600">{policy.category}</p>
                <p className="mt-1 text-xs text-slate-700">{policy.description}</p>
              </div>
              <input
                type="checkbox"
                checked={selectedPolicyIds.includes(policy.id)}
                onChange={() => togglePolicy(policy.id)}
              />
            </div>
            <button
              type="button"
              className="mt-2 text-xs font-medium text-slate-700 underline"
              onClick={() => void loadRules(policy.id)}
            >
              Ver reglas
            </button>
            {rulesByPolicy[policy.id] && (
              <ul className="mt-2 list-disc space-y-1 pl-4 text-xs text-slate-700">
                {rulesByPolicy[policy.id].map((rule) => (
                  <li key={rule.id}>
                    {rule.name} ({rule.rule_type})
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>

      <p className="mt-3 text-sm text-slate-700">
        Politicas seleccionadas: <span className="font-semibold">{selectedPolicies.length}</span>
      </p>
    </section>
  )
}
