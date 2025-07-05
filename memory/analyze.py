import os
import json
from volatility3 import framework
from volatility3.framework import contexts, interfaces
from volatility3.framework.configuration import requirements
from volatility3.cli import text_renderer
from volatility3.plugins.linux import pslist, lsmod

def analyze_memory(memory_path, output_path):
    """
    Analyzes a Linux memory image for hidden processes and modules.
    """
    results = {
        "memory_path": memory_path,
        "pslist": [],
        "lsmod": []
    }

    try:
        ctx = contexts.ContextInterface()
        base_config_path = "plugins"

        # Example config, in real use case you must set layer + OS
        ctx.config[base_config_path + ".automagic.LayerStacker.primary"] = memory_path
        ctx.config[base_config_path + ".kernel"] = "Linux"

        # Run pslist
        pslist_plugin = pslist.PsList(ctx, base_config_path + ".pslist")
        for proc in pslist_plugin.list_processes():
            results["pslist"].append({
                "pid": proc.pid,
                "name": proc.comm,
                "ppid": proc.ppid
            })

        # Run lsmod
        lsmod_plugin = lsmod.Lsmod(ctx, base_config_path + ".lsmod")
        for mod in lsmod_plugin.list_modules():
            results["lsmod"].append({
                "name": mod.name,
                "size": mod.size,
                "addr": mod.address
            })

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Memory analysis saved to {output_path}")

    except Exception as e:
        print(f"Error analyzing memory: {e}")
