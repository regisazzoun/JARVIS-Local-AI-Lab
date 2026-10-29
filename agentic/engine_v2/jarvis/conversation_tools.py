"""Shared API default for ordinary conversation; never widen explicit authority.

JL03 already offered this bounded set. Apply it to direct API callers as well,
without changing the durable mission engine or increasing an inference window.
"""
DEFAULT_CONVERSATION_TOOLS = (
    'active_memories', 'system_status', 'jarvis_services', 'web_search',
    'web_fetch', 'compute_status', 'compute_escalate', 'capability_status',
    'host_policy', 'host_read_file', 'skill_list', 'host_github',
)

def bounded_conversation_tools(payload, available, config):
    if payload.get('allowed_tools') is not None:
        return payload['allowed_tools']
    if payload.get('mission_id') or payload.get('agent_mode'):
        return None
    configured = config.get('conversation_tools')
    if configured is None:
        return [name for name in DEFAULT_CONVERSATION_TOOLS if name in available]
    if not isinstance(configured, (list, tuple)) or any(not isinstance(n, str) for n in configured):
        raise ValueError('conversation_tools must be a list of registered tool names')
    unknown = set(configured) - set(available)
    if unknown:
        raise ValueError('Unknown conversation tools: ' + ', '.join(sorted(unknown)))
    return list(configured)
