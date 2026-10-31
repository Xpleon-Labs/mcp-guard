import functools
import logging
from .policy import Policy

logger = logging.getLogger(__name__)

class Interceptor:
    def __init__(self, policy: Policy):
        self.policy = policy

    def guard(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            is_safe, reason = self._evaluate_static_rules(args, kwargs)
            if not is_safe:
                raise PermissionError(f"Execution blocked by mcp-guard: {reason}")
            return func(*args, **kwargs)
        return wrapper

    def _evaluate_static_rules(self, args, kwargs) -> tuple[bool, str]:
        arg_str = str(args) + str(kwargs)
        for path in self.policy.block_paths:
            if path in arg_str:
                return False, f"Blocked path detected: {path}"
        if args and isinstance(args[0], str):
            cmd_parts = args[0].strip().split()
            if cmd_parts:
                base_cmd = cmd_parts[0]
                if base_cmd not in self.policy.allowed_programs:
                    return False, f"Command not in allowlist: {base_cmd}"
        destructive = ["rm -rf", "curl", "wget", "chmod 777"]
        for pattern in destructive:
            if pattern in arg_str:
                return False, f"Destructive pattern detected: {pattern}"
        return True, "Safe"
