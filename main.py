# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import sys, site, importlib.util

    print("=== interpreter ===")
    print("sys.executable:", sys.executable)

    print("\n=== site ===")
    print("ENABLE_USER_SITE:", site.ENABLE_USER_SITE)
    print("usersite:", site.getusersitepackages())
    try:
        print("sitepackages:", site.getsitepackages())
    except Exception as e:
        print("site.getsitepackages() error:", e)

    print("\n=== sys.path (where python searches packages) ===")
    print("\n".join(sys.path))

    print("\n=== sample package location ===")
    pkg = "pydantic"  # 换成你关心的包名
    spec = importlib.util.find_spec(pkg)
    print(f"{pkg} spec:", spec)
    if spec and spec.origin:
        print(f"{pkg} origin:", spec.origin)

