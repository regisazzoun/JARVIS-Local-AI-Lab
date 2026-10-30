# Catalogue raccordé

Catalogue dérivé du registre réellement chargé : 86 définitions enregistrées, dont64 schémas visibles hors contexte de mission et34 exposés à la façade WebUI. Qwen Code utilise six outils de transport MCP pour la découverte et les appels ; le MCP historique de huit outils est conservé.

| Outil canonique | Paramètres | Qwen Code |
|---|---|---|
| `active_memories` |  | oui |
| `capability_status` | resource | oui |
| `compute_status` |  | oui |
| `disk_usage` |  | oui |
| `google_workspace` | profile, action, parameters | oui |
| `hardware_inventory` |  | oui |
| `host_ansible` | host, action, path, content, package, service, service_action | oui |
| `host_delete_file` | path | oui |
| `host_diagnostics` | action | oui |
| `host_edit_file` | path, old, new, count, expected_sha256 | oui |
| `host_exec` | command, timeout, argv | oui |
| `host_github` | repository, action, path, branch, file, body, destination, files, commit, title, message, query | oui |
| `host_logs` | service | oui |
| `host_package` | package, action | oui |
| `host_policy` |  | oui |
| `host_project_service` | project, name, action, argv, history | oui |
| `host_read_file` | path, offset, limit | oui |
| `host_remote` | host, action, path, content, package, service, service_action, project, command, local_path, model, probe | oui |
| `host_resources` |  | oui |
| `host_service` | service, action | oui |
| `host_write_file` | path, content | oui |
| `jarvis_services` |  | oui |
| `mcp_tools` | action, name, arguments | oui |
| `propose_memory` | content | oui |
| `qwen_code_run` | task, project | pas de délégation récursive |
| `qwen_code_status` |  | oui |
| `read_configuration` | name | oui |
| `service_logs` | service | oui |
| `skill_list` | name | oui |
| `skill_run` | name, parameters, run_id | oui |
| `software_versions` |  | oui |
| `system_status` |  | oui |
| `web_fetch` | url, offset | oui |
| `web_search` | query | oui |

Le catalogue se découvre par pages et les schémas exacts par nom. Google exige une authentification locale. Les appels de missions passent par le moteur canonique. Les opérations d’administration restent soumises au broker et à leurs périmètres existants. Un outil découvert n’est pas déclaré reçu avant son utilisation réelle.
