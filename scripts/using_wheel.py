import subprocess
from pathlib import Path

DISTS = Path(__file__).parent.parent / "third-party" / "pytomlpp-dists" 


def install_dependencies():
    try:
        # Intenta instalar desde ruedas precompiladas
        subprocess.run(['pip', 'install', '--no-deps', '--find-links=wheels/', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError:
        print("Instalación desde ruedas precompiladas fallida. Instalando dependencias normalmente.")
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

if __name__ == "__main__":
    install_dependencies()