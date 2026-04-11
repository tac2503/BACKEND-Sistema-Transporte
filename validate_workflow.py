import yaml
import sys

try:
    with open(".github/workflows/ci_push.yml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    print("✅ YAML válido - no errores de sintaxis")
    print(f"Workflow: {data.get('name')}")
    print(f"Trigger: {list(data.get('on', {}).keys())}")
    print(f"Jobs: {list(data.get('jobs', {}).keys())}")
    job_steps = data.get("jobs", {}).get("lint-and-test", {}).get("steps", [])
    print(f"Pasos: {len(job_steps)}")
    for i, step in enumerate(job_steps, 1):
        print(f"  {i}. {step.get('name')}")
except yaml.YAMLError as e:
    print(f"❌ ERROR YAML: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
