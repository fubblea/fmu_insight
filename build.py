import PyInstaller.__main__

PyInstaller.__main__.run([
    'src/main.py',
    '--onefile',
    '--noconfirm',
    '--noconsole',
    '--name',
    'FMU Insight'
])
