import rtoml
from pathlib import Path

try:
    print(rtoml.load(Path(r"C:\Users\Usuario\Desktop\Coding\Projects\Halted\QAutoLinguist\tests\model1.toml")))
    print(rtoml.load(Path(r"C:\Users\Usuario\Desktop\Coding\Projects\Halted\QAutoLinguist\tests\model2.toml")))
except Exception as e:
    raise TypeError("Error") from e

try:
    
    test={
        'Groups': 
        {
        '1': {
            'TRANSLATION':  'Texto label',
            'SOURCE':  'Texto label'
        },
        '2': {
            'TRANSLATION': """Lorem ipsum dolor sit amet, \ 
             consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
            Sed augue lacus viverra vitae congue eu consequat ac. Dolor morbi non arcu risus quis.""",
            'SOURCE':  'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed augue lacus viverra vitae congue eu consequat ac. Dolor morbi non arcu risus quis.'
        },
        '3': {
            'TRANSLATION':  'Texto de prueba para comprobar que hace saltos de linea y que se puedem colar simbolos como <html> o &^',
            'SOURCE':  'Texto de prueba para comprobar que hace saltos de linea y que se puedem colar simbolos como <html> o &^'
        }
        }
    }
    print(rtoml.dump(test, Path(r"C:\Users\Usuario\Desktop\Coding\Projects\Halted\QAutoLinguist\tests\model2.toml"), pretty=True))
except Exception as e:
    raise TypeError("Error") from e