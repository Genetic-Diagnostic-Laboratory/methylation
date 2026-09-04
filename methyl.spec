# PyInstaller build: pyinstaller methyl.spec  ->  dist/methyl.exe

a = Analysis(
    ["methyl.py"],
    pathex=["."],
    hiddenimports=["win32timezone"],
    excludes=["matplotlib", "scipy", "IPython", "pytest", "numpy.random._examples"],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name="methyl",
    console=True,
    upx=False,
)

# A folder build, not onefile: nothing is unpacked to temp on each launch
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="methyl",
)
