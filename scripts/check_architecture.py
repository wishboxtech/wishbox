"""Check dependency direction without importing Django or application code."""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INNER_LAYERS = {"domain", "dto", "interfaces", "services", "helpers"}
FRAMEWORK_MODULES = {
    "django",
    "rest_framework",
    "settings",
    "jwt",
    "magic",
    "nats",
    "asgiref",
}


def imports(source):
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            yield from (alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.level:
                yield "<relative-import>"
            yield node.module
            # Include child modules re-exported by packages in cycle checks.
            yield from (
                f"{node.module}.{alias.name}"
                for alias in node.names
                if alias.name != "*"
            )
        elif isinstance(node, ast.ImportFrom) and node.level:
            yield "<relative-import>"


def layer(module):
    parts = module.split(".")
    if parts[:2] == ["src", "apps"] and len(parts) > 3:
        return parts[3]
    if parts[:2] == ["src", "shared"]:
        return (
            "domain"
            if ".domain" in module
            else "interfaces"
            if module.endswith("interfaces")
            else "dto"
            if module.endswith("dto")
            else None
        )
    return None


def check_modules(modules):
    violations = set()
    graph = {name: set() for name in modules}
    for module, source in modules.items():
        owner_layer = layer(module)
        parts = module.split(".")
        if owner_layer == "serializers":
            violations.add(
                f"{module}: app serializers belong beside their view in src.api.views"
            )
        for dependency in imports(source):
            if layer(dependency) == "serializers":
                violations.add(
                    f"{module}: imports app serializer {dependency}; use endpoint-local serializers"
                )
            target_layer = layer(dependency)
            if dependency in modules:
                graph[module].add(dependency)
            if owner_layer in INNER_LAYERS:
                if dependency.split(".")[
                    0
                ] in FRAMEWORK_MODULES or dependency.startswith(
                    (
                        "src.core",
                        "src.api",
                        "src.utils.exceptions",
                        "src.utils.otp",
                        "src.shared.transactions",
                    )
                ):
                    violations.add(
                        f"{module}: inner layer imports outer dependency {dependency}"
                    )
                if target_layer in {
                    "models",
                    "repositories",
                    "serializers",
                    "selectors",
                    "functions",
                    "backends",
                }:
                    violations.add(f"{module}: inner layer imports {dependency}")
                if dependency == "<relative-import>":
                    violations.add(
                        f"{module}: use absolute imports so dependency checks remain explicit"
                    )
                if owner_layer == "domain" and target_layer not in {None, "domain"}:
                    violations.add(f"{module}: domain imports {dependency}")
                if owner_layer in {"dto", "interfaces"} and target_layer == "services":
                    violations.add(
                        f"{module}: contract imports concrete service {dependency}"
                    )
                if (
                    owner_layer == "services"
                    and target_layer == "services"
                    and dependency.split(".")[2:3] != parts[2:3]
                ):
                    violations.add(
                        f"{module}: cross-app service must be injected through an interface ({dependency})"
                    )
            if owner_layer == "repositories" and (
                target_layer in {"services", "serializers"}
                or dependency.startswith("src.api")
            ):
                violations.add(
                    f"{module}: repository imports presentation/application {dependency}"
                )
            if (
                owner_layer == "repositories"
                and target_layer in {"models", "repositories"}
                and dependency.split(".")[2:3] != parts[2:3]
            ):
                violations.add(
                    f"{module}: imports another app's private data layer {dependency}"
                )
            if module.startswith("src.api") or owner_layer == "serializers":
                if target_layer in {"models", "repositories", "selectors"}:
                    violations.add(
                        f"{module}: presentation imports persistence {dependency}"
                    )

    visiting, visited = set(), set()

    def visit(module, chain):
        if module in visiting:
            violations.add("Circular dependency: " + " -> ".join(chain + [module]))
            return
        if module in visited:
            return
        visiting.add(module)
        for child in sorted(graph[module]):
            visit(child, chain + [module])
        visiting.remove(module)
        visited.add(module)

    for module in sorted(graph):
        visit(module, [])
    return sorted(violations)


def check_project(root=ROOT):
    modules = {}
    for path in (root / "src").rglob("*.py"):
        if any(part in {"tests", "migrations"} for part in path.parts):
            continue
        parts = list(path.relative_to(root).with_suffix("").parts)
        if parts[-1] == "__init__":
            parts.pop()
        modules[".".join(parts)] = path.read_text()
    return check_modules(modules)


if __name__ == "__main__":
    errors = check_project()
    if errors:
        raise SystemExit("\n".join(errors))
    print("Architecture dependency checks passed.")
