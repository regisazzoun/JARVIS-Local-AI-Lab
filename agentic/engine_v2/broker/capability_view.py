"""Read-only views of existing policy and receipts; never confer authority."""
import hashlib
import json

VERSION = '23C.1'


def policy_identity(cfg):
    return {
        'policy_sha256': hashlib.sha256(json.dumps(cfg, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
        'policy_path': '/etc/jarvis/host-policy.json',
        'selection': 'single-persistent-owner-policy',
        'reload': 'each-request',
        'broker_version': VERSION,
    }


def public_scope(cfg):
    """Allowlist only: SSH keys, addresses, commands and arbitrary config stay private."""
    result = {k: cfg.get(k, [] if k != 'services' else {}) for k in
              ('write_roots', 'read_roots', 'packages', 'services', 'repositories', 'read_repositories', 'diagnostics')}
    result['projects'] = list(cfg.get('project_services', {}))
    result['machines'] = {
        name: {k: value for k, value in profile.items() if k in
               ('allow_admin', 'ansible_enabled', 'administration_operations', 'project_exec_projects', 'services')}
        for name, profile in cfg.get('remote_hosts', {}).items()
    }
    return result


def error_category(result):
    if result.get('ok'):
        return None
    detail = result.get('result', {})
    if detail.get('timeout'):
        return 'timeout'
    code = result.get('error_code', '')
    if code == 'PermissionError':
        return 'permission_denied'
    if code in ('KeyError', 'ValueError', 'TypeError'):
        return 'invalid_parameter' if result.get('error') != 'Opération inconnue' else 'not_implemented'
    if code == 'FileNotFoundError':
        return 'resource_missing'
    if code in ('ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError'):
        return 'service_unavailable'
    if code in ('TimeoutError', 'TimeoutExpired'):
        return 'timeout'
    if code in ('gaierror', 'NetworkError'):
        return 'network_error'
    if detail.get('returncode') == 127:
        return 'command_missing'
    # Never guess network/permission from arbitrary stderr or a generic exit code.
    return 'application_error'


def diagnostic(op, arguments, result, cfg):
    category = error_category(result)
    # Retain transmitted selectors, not shell/source bodies or arbitrary secret fields.
    selectors = {k: v for k, v in arguments.items() if k in
                 ('service', 'action', 'service_action', 'host', 'project', 'repository', 'branch', 'capability')}
    return {
        **policy_identity(cfg), 'operation': op, 'parameters': selectors,
        'omitted_parameters': sorted(set(arguments) - set(selectors)),
        'error_category': category,
        'retry': 'Inspect the receipt and current capability_status; reobserve before retrying a mutation.' if category else None,
        'alternative': 'Use host_service/host_logs for systemd; host_exec has no system bus.' if op == 'host_exec' and category else None,
    }
