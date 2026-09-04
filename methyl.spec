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
    a.binaries,
    a.datas,
    name="methyl",
    console=True,
    upx=False,
)
