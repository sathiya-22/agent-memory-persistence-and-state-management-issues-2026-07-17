2026-07-27: Replaced mutable default arguments in Pydantic models with `Field(default_factory=...)` to prevent unexpected shared state across instances.
2026-07-27: Introduced error handling and logging for agent state persistence and loading to improve robustness and debugging capabilities.
