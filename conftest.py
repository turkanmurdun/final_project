import sys, os

# ensure src/ is on PYTHONPATH so `import src.xxx` works in tests
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, "src"))
