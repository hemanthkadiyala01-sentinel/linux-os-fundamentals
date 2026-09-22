import importlib.util
from pathlib import Path

path = Path(__file__).parent / "07-detection-engineering" / "detection_logic.py"

spec = importlib.util.spec_from_file_location("detection_logic", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

should_alert = module.should_alert
