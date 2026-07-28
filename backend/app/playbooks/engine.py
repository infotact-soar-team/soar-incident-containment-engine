"""
Core Playbook Engine — loads a playbook definition (from Week 1's schema/loader)
and executes its action steps in order, calling the right mock integration
for each action type.
"""
from app.schemas.playbook import PlaybookDefinition
from app.integrations.mock_firewall import block_ip
from app.integrations.mock_edr import isolate_host
from app.integrations.aws_sg import isolate_via_security_group

ACTION_DISPATCH = {
    "BLOCK_IP": lambda target, **kwargs: block_ip(target),
    "ISOLATE_HOST": lambda target, **kwargs: isolate_host(target),
    "AWS_SG_ISOLATE": lambda target, **kwargs: isolate_via_security_group(target),
    "NOTIFY_ANALYST": lambda target, message=None, **kwargs: {
        "action": "NOTIFY_ANALYST", "target": target, "message": message, "success": True
    },
    "LOG_ONLY": lambda target, **kwargs: {
        "action": "LOG_ONLY", "target": target, "success": True
    },
}


class PlaybookEngine:
    def __init__(self, playbook: PlaybookDefinition):
        self.playbook = playbook

    def execute(self, ioc_value: str) -> list:
        """
        Runs every action defined in the playbook, in order, substituting
        {{ ioc_value }} with the actual IoC value. Returns a list of
        results, one per action, in execution order.
        """
        results = []
        for step in self.playbook.actions:
            action_fn = ACTION_DISPATCH.get(step.type)
            if not action_fn:
                results.append({"action": step.type, "success": False, "error": "Unknown action type"})
                continue

            target = ioc_value
            message = step.message.replace("{{ ioc_value }}", ioc_value) if step.message else None

            result = action_fn(target=target, message=message)
            results.append(result)

        return results
