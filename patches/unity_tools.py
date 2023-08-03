#!/usr/bin/env python

import os
import re
from pathlib import Path

unity_batch_size = 32


def generate_unity_build(src, prefix="", gen_folder="obj", batch_size=unity_batch_size):
    if os.environ.get("FORCE_DISABLE_UNITY", "").lower() not in ["", "no", "false", "n"]:
        return src

    from pathlib import Path
    import math

    print("Generating source files for unity build:")
    res = [Path(str(f)).absolute().as_posix()
           for f in src if str(f).endswith(".cpp")]
    unity_dir = Path(gen_folder)
    unity_dir.mkdir(parents=True, exist_ok=True)
    unity_files = []
    for i in range(math.ceil(len(res) / batch_size)):
        u_path = unity_dir / (prefix + ("unity_%d.cpp" % i))
        print(u_path)
        unity_files.append(u_path.as_posix())
        with u_path.open("w+") as unity_file:
            unity_file.write("\n".join(
                ["/* generated by Scons */\n"] + ["#include \"%s\"\n" % f for f in res[:batch_size]]))
            res = res[batch_size:]

    print()
    return [f for f in src if not str(f).endswith(".cpp")] + [Path(f).absolute().as_posix() for f in unity_files]