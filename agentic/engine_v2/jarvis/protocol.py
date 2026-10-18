"""Shared Ollama native/textual tool protocol; identical authorization path."""
import json
import re


def normalize_message(message, known_tools):
    if isinstance(message,str):message={'role':'assistant','content':message}
    if not isinstance(message,dict):raise ValueError('Message modèle invalide')
    if not message.get('tool_calls') and isinstance(message.get('content'),str):
        encoded=re.fullmatch(r'\s*([a-z_][a-z_0-9]*)\[ARGS\](\{.*\})\s*',message['content'],flags=re.S)
        if encoded and encoded[1] in known_tools:
            try:
                arguments=json.loads(encoded[2])
                if isinstance(arguments,dict):
                    return {'role':'assistant','content':'','tool_calls':[{'function':{'name':encoded[1],'arguments':arguments}}]}
            except json.JSONDecodeError:pass
    return message
