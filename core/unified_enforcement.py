from __future__ import annotations

import importlib
import inspect
import logging
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import yaml

try:
    from core.system_integration import SystemBus  # type: ignore
except Exception:  # pragma: no cover - SystemBus provided separately
    SystemBus = None  # type: ignore


def _structured_response(
    status: str,
    data: Any = None,
    metadata: Optional[Dict[str, Any]] = None,
    blocked: bool = False,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a structured response dictionary.

    Args:
        status: Status string (e.g., "ok", "blocked", "error", "reused").
        data: Arbitrary data associated with the response.
        metadata: Additional metadata for context.
        blocked: Whether the operation is blocked.
        reason: Optional human-readable reason.

    Returns:
        Structured dict with required fields.
    """
    return {
        "status": status,
        "data": data,
        "metadata": metadata or {},
        "blocked": blocked,
        "reason": reason,
    }


def _safe_load_yaml(path: Path) -> Any:
    """Safely load YAML from a file.

    Args:
        path: Path to YAML file.

    Returns:
        Parsed Python object or empty dict if empty.

    Raises:
        OSError: If file cannot be read.
        yaml.YAMLError: If YAML is invalid.
    """
    with path.open("r", encoding="utf-8") as f:
        content = yaml.safe_load(f)
    return content if content is not None else {}


def _similarity(a: str, b: str) -> float:
    """Compute a simple similarity metric between two strings.

    Uses a token overlap Jaccard-like approach.

    Args:
        a: First string.
        b: Second string.

    Returns:
        Similarity in [0.0, 1.0].
    """
    set_a = set(a.lower().split())
    set_b = set(b.lower().split())
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return inter / union if union else 0.0


class UnifiedEnforcementPipeline:
    """Unified Enforcement Pipeline for the Manus Global Knowledge System.

    This pipeline enforces a strict, six-level process for all Manus operations:
    1) Initialization Check
    2) Cost Gate
    3) Knowledge Lookup
    4) Execution Router
    5) Quality Validator
    6) Continuous Learning

    The pipeline loads configurations from YAML files in the "rules/" directory,
    integrates with a SystemBus for event-driven communication, and provides a
    monkey-patching facility to intercept and enforce policies on Manus tools.

    Attributes:
        base_path: Base directory for configuration and state.
        rules_path: Path to the "rules" directory containing YAML files.
        config: Aggregated configuration loaded from YAML files.
        bus: Instance of SystemBus if available.
        logger: Logger instance for the pipeline.
        patched_registry: Registry of monkey-patched callables for idempotency.
    """

    def __init__(self, base_path: Path):
        """Initialize the UnifiedEnforcementPipeline.

        Loads all YAML configurations from the "rules/" directory, initializes
        the SystemBus, and prepares internal state.

        Args:
            base_path: Base directory path for rules, knowledge, state, and learning.

        Raises:
            FileNotFoundError: If the rules directory does not exist.
            RuntimeError: If configuration loading fails catastrophically.
        """
        self.base_path: Path = Path(base_path).resolve()
        self.rules_path: Path = self.base_path / "rules"
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            # Avoid duplicate handlers in embedded environments
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        if not self.rules_path.exists() or not self.rules_path.is_dir():
            raise FileNotFoundError(f"Rules directory not found: {self.rules_path}")

        try:
            self.config: Dict[str, Any] = self._load_configs(self.rules_path)
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.exception("Failed to load configurations from rules directory.")
            raise RuntimeError("Failed to initialize pipeline configuration.") from exc

        self.bus = None
        if SystemBus is not None:
            try:
                self.bus = SystemBus()  # type: ignore[call-arg]
            except Exception as exc:  # pragma: no cover - SystemBus may differ
                self.logger.warning("SystemBus initialization failed: %s", exc)

        self.patched_registry: Dict[str, Callable[..., Any]] = {}

        self.logger.info("UnifiedEnforcementPipeline initialized at %s", self.base_path)

    def enforce(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Run the main enforcement pipeline for a given action.

        Executes all six levels in strict priority order. If a level blocks
        the operation, returns immediately with a blocked response.

        Args:
            action: Action dictionary describing the intended operation. Expected
                fields:
                - type: str, action type or tool identifier.
                - payload: Any, input payload for the action.
                - metadata: dict, optional metadata including:
                    - cost_estimate: float (0..1) or numeric
                    - tool: str
                    - requires_manus: bool
                    - manus_callable: callable (if using monkey-patching)
                    - module: str
                    - any other relevant context

        Returns:
            Structured dict with keys: {status, data, metadata, blocked, reason}
        """
        if not isinstance(action, dict):
            msg = "Action must be a dict."
            self.logger.error(msg)
            return _structured_response("error", None, {}, True, msg)

        metadata = dict(action.get("metadata") or {})
        metadata.setdefault("type", action.get("type"))
        metadata.setdefault("module", metadata.get("module", ""))
        metadata.setdefault("cost_estimate", metadata.get("cost_estimate", 0.0))

        self._emit("uep.enforce.start", {"action": action})

        # Level 1: Initialization Check
        try:
            if not self._check_initialization():
                reason = "System not initialized. Initialization check failed."
                self._emit("uep.level1.blocked", {"reason": reason})
                return _structured_response(
                    status="blocked",
                    data=None,
                    metadata=metadata,
                    blocked=True,
                    reason=reason,
                )
        except Exception as exc:
            self.logger.exception("Initialization check failed unexpectedly.")
            return _structured_response("error", None, metadata, True, str(exc))

        # Level 2: Cost Gate
        try:
            cost_gate = self._check_cost({"action": action})
            if cost_gate.get("blocked"):
                self._emit("uep.level2.blocked", {"result": cost_gate})
                return cost_gate
            # Allow metadata updates from cost gate
            gate_meta = cost_gate.get("metadata") or {}
            metadata.update(gate_meta)
        except Exception as exc:
            self.logger.exception("Cost gate failed unexpectedly.")
            return _structured_response("error", None, metadata, True, str(exc))

        # Level 3: Knowledge Lookup
        result: Optional[Dict[str, Any]] = None
        try:
            lookup = self._lookup_knowledge({"action": action})
            if lookup.get("status") == "reused":
                self._emit("uep.level3.reused", {"lookup": lookup})
                result = lookup
                metadata.update(lookup.get("metadata") or {})
        except Exception as exc:
            self.logger.exception("Knowledge lookup failed unexpectedly.")
            return _structured_response("error", None, metadata, True, str(exc))

        # Level 4: Execution Router (and simulated/actual execution)
        routed_target = None
        try:
            if result is None:
                routing = self._route_execution({"action": action})
                routed_target = ((routing.get("metadata") or {}).get("execution_target")) or "openai"
                metadata.update(routing.get("metadata") or {})
                result = routing
                self._emit("uep.level4.routed", {"routing": routing})
        except Exception as exc:
            self.logger.exception("Execution routing failed unexpectedly.")
            return _structured_response("error", None, metadata, True, str(exc))

        # Level 5: Quality Validator
        try:
            validation = self._validate_quality(result or {})
            metadata.update(validation.get("metadata") or {})
            if validation.get("blocked"):
                self._emit("uep.level5.validation_failed", {"validation": validation})

                # Escalation path: if OpenAI route failed quality, try Manus once
                if routed_target == "openai":
                    # Force Manus routing
                    action_escalated = dict(action)
                    meta_escalated = dict(action.get("metadata") or {})
                    meta_escalated["requires_manus"] = True
                    action_escalated["metadata"] = meta_escalated

                    try:
                        routing2 = self._route_execution({"action": action_escalated})
                        metadata.update(routing2.get("metadata") or {})
                        self._emit("uep.level4.routed_escalated", {"routing": routing2})
                        validation2 = self._validate_quality(routing2)
                        metadata.update(validation2.get("metadata") or {})
                        if validation2.get("blocked"):
                            return validation2
                        # Learning
                        try:
                            self._learn_from_outcome(action_escalated, validation2)
                        except Exception as learn_exc:  # pragma: no cover - defensive
                            self.logger.warning("Learning failed: %s", learn_exc)
                        return validation2
                    except Exception as exc2:  # pragma: no cover - defensive
                        self.logger.exception("Escalation to Manus failed.")
                        return _structured_response("error", None, metadata, True, str(exc2))

                return validation
            else:
                result = validation
        except Exception as exc:
            self.logger.exception("Quality validation failed unexpectedly.")
            return _structured_response("error", None, metadata, True, str(exc))

        # Level 6: Continuous Learning
        try:
            self._learn_from_outcome(action, result or {})
        except Exception as exc:
            # Do not block on learning failures; just log and proceed.
            self.logger.warning("Continuous learning failed: %s", exc)

        final = _structured_response(
            status=result.get("status", "ok"),
            data=result.get("data"),
            metadata={**metadata, **(result.get("metadata") or {})},
            blocked=False,
            reason=None,
        )
        self._emit("uep.enforce.complete", {"result": final})
        return final

    def _check_initialization(self) -> bool:
        """Level 1: Initialization Check.

        Verifies that the system is properly initialized. Uses configuration
        flags and/or the presence of an initialization flag file.

        Returns:
            True if initialized; False otherwise.
        """
        init_conf = self.config.get("initialization", {}) or {}
        require_flag = bool(init_conf.get("require_flag_file", True))
        flag_file_rel = init_conf.get("flag_file", "state/initialized.flag")
        flag_file = self.base_path / flag_file_rel

        # Optionally also check a YAML-configured boolean
        conf_flag = bool(init_conf.get("initialized", False))

        initialized = conf_flag or (flag_file.exists() if require_flag else True)

        self._emit("uep.level1.checked", {"initialized": initialized})
        if not initialized:
            self.logger.warning(
                "Initialization check failed. Flag file expected at: %s", flag_file
            )
        return initialized

    def _check_cost(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Level 2: Cost Gate.

        Blocks expensive operations if a cheaper alternative exists based on
        configured thresholds and alternatives.

        Args:
            action: Wrapper dict containing the action under key "action".

        Returns:
            Structured dict indicating pass/block, with possible recommendations
            in data and enriched metadata.
        """
        act = action.get("action", {})
        meta = dict(act.get("metadata") or {})
        tool = meta.get("tool") or act.get("type") or "unknown"
        cost_estimate = meta.get("cost_estimate", 0.0)

        cost_conf = self.config.get("cost_gate", {}) or {}
        threshold = float(cost_conf.get("threshold", 0.75))
        alternatives: Dict[str, Any] = cost_conf.get("alternatives", {}) or {}
        cheaper_for_tool = alternatives.get(tool)

        metadata = {
            "checked_cost": True,
            "cost_estimate": cost_estimate,
            "cost_threshold": threshold,
            "cheaper_alternative": cheaper_for_tool,
        }

        if (cost_estimate or 0.0) > threshold and cheaper_for_tool:
            reason = f"Operation '{tool}' is expensive (cost={cost_estimate}). Cheaper alternative available."
            self.logger.info("Cost gate blocking expensive operation: %s", reason)
            self._emit("uep.level2.blocked", {"tool": tool, "reason": reason})
            data = {"suggested_alternative": cheaper_for_tool}
            return _structured_response(
                status="blocked", data=data, metadata=metadata, blocked=True, reason=reason
            )

        return _structured_response(
            status="ok", data=None, metadata=metadata, blocked=False, reason=None
        )

    def _lookup_knowledge(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Level 3: Knowledge Lookup.

        Reuses existing knowledge if the action matches a known item with
        similarity > configured threshold.

        Args:
            action: Wrapper dict containing the action under key "action".

        Returns:
            Structured dict; status "reused" if match found, else "ok".
        """
        act = action.get("action", {})
        payload = act.get("payload")
        query_text = ""
        if isinstance(payload, str):
            query_text = payload
        elif isinstance(payload, dict) and "text" in payload and isinstance(payload["text"], str):
            query_text = payload["text"]
        else:
            query_text = str(payload)

        know_conf = self.config.get("knowledge", {}) or {}
        sim_threshold = float(know_conf.get("similarity_threshold", 0.80))

        # Expect "index" to be a list of dicts: {"query": str, "answer": Any, "tags": [..]}
        index: List[Dict[str, Any]] = know_conf.get("index", []) or []

        best_item: Optional[Dict[str, Any]] = None
        best_score = 0.0

        for item in index:
            q = str(item.get("query", ""))
            s = _similarity(query_text, q)
            if s > best_score:
                best_item = item
                best_score = s

        metadata = {
            "similarity_threshold": sim_threshold,
            "similarity_score": best_score,
            "knowledge_reused": False,
        }

        if best_item and best_score >= sim_threshold:
            data = {
                "output": best_item.get("answer"),
                "source": "knowledge_base",
                "tags": best_item.get("tags", []),
                "similarity": best_score,
            }
            metadata["knowledge_reused"] = True
            self._emit(
                "uep.level3.matched",
                {"score": best_score, "item": {"query": best_item.get("query")}},
            )
            return _structured_response(
                status="reused", data=data, metadata=metadata, blocked=False, reason=None
            )

        return _structured_response(
            status="ok", data=None, metadata=metadata, blocked=False, reason=None
        )

    def _route_execution(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Level 4: Execution Router.

        Routes execution to OpenAI (cheap) or Manus (necessary). If a Manus callable
        is provided in action metadata (via monkey-patching), will execute it when
        routing to Manus. OpenAI path is simulated here and should be integrated with
        actual services in production.

        Args:
            action: Wrapper dict containing the action under key "action".

        Returns:
            Structured dict with execution results and routing metadata.
        """
        act = action.get("action", {})
        meta = dict(act.get("metadata") or {})
        requires_manus = bool(meta.get("requires_manus", False))
        tool = meta.get("tool") or act.get("type") or "unknown"
        manus_callable: Optional[Callable[..., Any]] = meta.get("manus_callable")
        manus_args = None
        manus_kwargs = None
        if isinstance(act.get("payload"), dict) and "args" in act["payload"] and "kwargs" in act["payload"]:
            manus_args = act["payload"]["args"]
            manus_kwargs = act["payload"]["kwargs"]

        router_conf = self.config.get("router", {}) or {}
        default_target = str(router_conf.get("default", "openai"))
        manus_list = router_conf.get("manus_tools", []) or []

        # Heuristics: if explicitly required or tool in manus_list -> Manus else OpenAI
        execution_target = "manus" if requires_manus or tool in manus_list else default_target

        # Simulated execution results; real integrations should replace this.
        if execution_target == "manus":
            output, quality = self._execute_manus(manus_callable, manus_args, manus_kwargs, act)
        else:
            output, quality = self._execute_openai(act)

        metadata = {
            "execution_target": execution_target,
            "tool": tool,
            "requires_manus": requires_manus,
            "estimated_quality": quality,
        }
        data = {"output": output, "quality": quality}

        return _structured_response(
            status="ok", data=data, metadata=metadata, blocked=False, reason=None
        )

    def _validate_quality(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Level 5: Quality Validator.

        Ensures output quality meets or exceeds the configured threshold. If not,
        blocks the operation.

        Args:
            result: Structured dict from previous level containing 'data' and 'metadata'.

        Returns:
            Structured dict indicating validation success or block.
        """
        qual_conf = self.config.get("quality", {}) or {}
        threshold = float(qual_conf.get("threshold", 0.80))
        data = result.get("data") or {}
        quality = float(data.get("quality", 1.0))

        metadata = dict(result.get("metadata") or {})
        metadata.update({"quality_threshold": threshold, "observed_quality": quality})

        if quality < threshold:
            reason = f"Output quality below threshold ({quality:.2f} < {threshold:.2f})."
            self.logger.info("Quality validation failed: %s", reason)
            self._emit("uep.level5.blocked", {"reason": reason})
            return _structured_response(
                status="blocked", data=data, metadata=metadata, blocked=True, reason=reason
            )

        return _structured_response(
            status="ok", data=data, metadata=metadata, blocked=False, reason=None
        )

    def _learn_from_outcome(self, action: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Level 6: Continuous Learning.

        Records outcomes and adapts routing or knowledge for future improvements.
        In this implementation, outcomes are appended to a YAML records file.

        Args:
            action: Original action dict.
            result: Final result dict after validation.

        Raises:
            OSError: If unable to write learning records.
            yaml.YAMLError: If serialization fails.
        """
        learn_conf = self.config.get("learning", {}) or {}
        if not bool(learn_conf.get("enabled", True)):
            return

        rel_path = learn_conf.get("records_file", "learning/records.yaml")
        records_path = self.base_path / rel_path
        records_path.parent.mkdir(parents=True, exist_ok=True)

        # Compose record
        record = {
            "action_type": action.get("type"),
            "metadata": action.get("metadata") or {},
            "result_status": result.get("status"),
            "result_meta": result.get("metadata") or {},
            "timestamp": None,  # Could set to datetime.now().isoformat() if allowed
        }

        # Load existing records
        existing: List[Dict[str, Any]] = []
        if records_path.exists():
            try:
                obj = _safe_load_yaml(records_path)
                if isinstance(obj, list):
                    existing = obj
                else:
                    existing = []
            except Exception as exc:  # pragma: no cover - defensive
                self.logger.warning("Failed to read existing learning records: %s", exc)
                existing = []

        existing.append(record)
        try:
            with records_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(existing, f, sort_keys=False)
        except Exception as exc:  # pragma: no cover - I/O errors are environmental
            self.logger.warning("Failed to write learning records: %s", exc)
            raise

        self._emit("uep.level6.learned", {"recorded": True})

    def enforce_all_manus_tools(self) -> None:
        """Monkey-patch all Manus tools to pass through the enforcement pipeline.

        Attempts to import 'manus' and 'manus.tools' modules. Wraps top-level callables
        so that each invocation is processed via self.enforce(). If routing decides to
        execute Manus, the original callable is invoked; otherwise, a simulated output
        is returned.

        Notes:
            - This operation is idempotent; already patched callables will be skipped.
            - Only non-private (not starting with '_') callables are patched.

        Raises:
            ImportError: If Manus modules cannot be imported.
        """
        modules_to_scan: List[Any] = []
        module_names = ["manus.tools", "manus"]

        for name in module_names:
            try:
                mod = importlib.import_module(name)
                modules_to_scan.append(mod)
            except Exception as exc:
                self.logger.debug("Module not available for patching: %s (%s)", name, exc)

        if not modules_to_scan:
            raise ImportError("No Manus modules found to patch (manus or manus.tools).")

        for mod in modules_to_scan:
            for attr_name in dir(mod):
                if attr_name.startswith("_"):
                    continue
                try:
                    obj = getattr(mod, attr_name)
                except Exception:
                    continue
                if not (inspect.isfunction(obj) or inspect.ismethod(obj)):
                    continue

                fq_name = f"{mod.__name__}.{attr_name}"
                if fq_name in self.patched_registry:
                    continue  # Already patched

                original = obj

                @wraps(original)
                def wrapper(*args: Any, __orig=original, __name=attr_name, __mod=mod, **kwargs: Any) -> Any:
                    action = {
                        "type": f"{__mod.__name__}.{__name}",
                        "payload": {"args": args, "kwargs": kwargs},
                        "metadata": {
                            "tool": __name,
                            "module": __mod.__name__,
                            "manus_callable": __orig,
                            # Allow functions to define a cost estimate attribute
                            "cost_estimate": getattr(__orig, "cost_estimate", 0.5),
                        },
                    }
                    result = self.enforce(action)
                    if result.get("blocked"):
                        raise RuntimeError(
                            f"Operation blocked by UnifiedEnforcementPipeline: {result.get('reason')}"
                        )
                    # Prefer output key if available
                    data = result.get("data") or {}
                    if isinstance(data, dict) and "output" in data:
                        return data["output"]
                    return data

                try:
                    setattr(mod, attr_name, wrapper)
                    self.patched_registry[fq_name] = original
                    self.logger.info("Patched Manus tool: %s", fq_name)
                except Exception as exc:  # pragma: no cover - environment specific
                    self.logger.warning("Failed to patch %s: %s", fq_name, exc)

    # Internal helpers

    def _load_configs(self, rules_path: Path) -> Dict[str, Any]:
        """Load all YAML configurations from the rules directory.

        Files are mapped by stem name into the config dict.

        Args:
            rules_path: Path to rules directory.

        Returns:
            Aggregated configuration dictionary.

        Raises:
            RuntimeError: If no config files are found or parsing fails.
        """
        config: Dict[str, Any] = {}
        found = False
        for ext in ("*.yaml", "*.yml"):
            for f in rules_path.glob(ext):
                try:
                    cfg = _safe_load_yaml(f)
                    config[f.stem] = cfg
                    found = True
                    self.logger.debug("Loaded config: %s", f.name)
                except Exception as exc:
                    self.logger.error("Failed to load YAML %s: %s", f, exc)
                    raise

        if not found:
            raise RuntimeError(f"No YAML configs found in {rules_path}")

        return config

    def _execute_openai(self, act: Dict[str, Any]) -> Tuple[Any, float]:
        """Simulate OpenAI execution.

        A simple deterministic heuristic based on payload complexity is used
        to estimate quality. Replace with actual OpenAI integration in production.

        Args:
            act: Action dictionary.

        Returns:
            Tuple of (output, quality).
        """
        payload = act.get("payload")
        text = ""
        if isinstance(payload, str):
            text = payload
        elif isinstance(payload, dict) and "text" in payload and isinstance(payload["text"], str):
            text = payload["text"]
        else:
            text = str(payload)

        complexity = max(1, len(text.split()))
        # Heuristic: more complex -> lower quality for OpenAI path in this stub.
        quality = max(0.60, 0.95 - min(complexity, 50) * 0.005)
        output = {
            "result": f"Simulated OpenAI response for: {act.get('type')}",
            "payload_echo": text[:256],
        }
        return output, quality

    def _execute_manus(
        self,
        manus_callable: Optional[Callable[..., Any]],
        args: Optional[Tuple[Any, ...]],
        kwargs: Optional[Dict[str, Any]],
        act: Dict[str, Any],
    ) -> Tuple[Any, float]:
        """Execute Manus callable if available, otherwise simulate.

        Manus execution is assumed to produce higher quality in this stub.

        Args:
            manus_callable: Original callable to invoke.
            args: Positional arguments tuple.
            kwargs: Keyword arguments dict.
            act: Action dictionary.

        Returns:
            Tuple of (output, quality).
        """
        if manus_callable is not None:
            try:
                res = manus_callable(*(args or ()), **(kwargs or {}))
                # Heuristic: Manus produces high-quality results
                quality = 0.95
                return res, quality
            except Exception as exc:
                self.logger.exception("Manus callable execution failed: %s", exc)
                # Fallback to simulation on failure
        # Simulated Manus output
        output = {"result": f"Simulated Manus execution for: {act.get('type')}"}
        quality = 0.92
        return output, quality

    def _emit(self, event: str, payload: Dict[str, Any]) -> None:
        """Publish an event to the SystemBus if available.

        Args:
            event: Event name.
            payload: Event payload.

        Note:
            Silently ignores if bus is not available or publish fails.
        """
        if not self.bus:
            return
        try:
            # Assuming SystemBus has a publish method (topic, payload)
            self.bus.publish(event, payload)  # type: ignore[attr-defined]
        except Exception as exc:  # pragma: no cover - depends on external bus
            self.logger.debug("Event publish failed (%s): %s", event, exc)