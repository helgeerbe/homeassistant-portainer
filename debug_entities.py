#!/usr/bin/env python3
"""Debug script to check entity creation."""

import sys
import os

# Add the custom_components path to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "custom_components"))

try:
    from portainer.sensor_types import SENSOR_TYPES
    from portainer.const import (
        PLATFORMS,
        CONF_FEATURE_UPDATE_CHECK,
        DEFAULT_FEATURE_UPDATE_CHECK,
    )

    print("=== PLATFORMS ===")
    for platform in PLATFORMS:
        print(f"  {platform}")

    print("\n=== SENSOR_TYPES ===")
    for sensor in SENSOR_TYPES:
        print(f"  Key: {sensor.key}")
        print(f"  Name: {sensor.name}")
        print(f"  ha_group: {sensor.ha_group}")
        print(f"  data_path: {sensor.data_path}")
        print(f"  data_attribute: {sensor.data_attribute}")
        print(f"  func: {sensor.func}")
        print(f"  data_reference: {sensor.data_reference}")
        print("  ---")

    print(f"\n=== FEATURE CONFIG ===")
    print(f"CONF_FEATURE_UPDATE_CHECK: {CONF_FEATURE_UPDATE_CHECK}")
    print(f"DEFAULT_FEATURE_UPDATE_CHECK: {DEFAULT_FEATURE_UPDATE_CHECK}")

    print("\n=== BUTTON PLATFORM CHECK ===")
    try:
        from portainer.button import async_setup_entry, ForceUpdateCheckButton

        print("Button platform imports successfully")
        print(f"ForceUpdateCheckButton class exists: {ForceUpdateCheckButton}")
    except Exception as e:
        print(f"Button platform import error: {e}")

    print("\n=== All imports successful ===")

except Exception as e:
    print(f"Import error: {e}")
    import traceback

    traceback.print_exc()
