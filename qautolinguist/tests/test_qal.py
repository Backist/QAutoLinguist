import pytest
import qautolinguist.exceptions as qal_excs
from qautolinguist.qal import QAutoLinguist
from qautolinguist.config import Config
from qautolinguist.consts import VALID_PYLRELEASE_OPTIONS, VALID_PYLUPDATE_OPTIONS
from pathlib import Path
from contextlib import contextmanager

ROOT = Path(__file__).parent
VALID_ROOT = ROOT / "valid"
INVALID_ROOT = ROOT / "invalid"
VALID_TARGETS = [
    pytest.param(p, id=p.stem)
    for p in INVALID_ROOT.glob("*.ini") 
]

WRONG_SAMPLE = {
            'source_file': "self.tr", 
            'default_language': 'en', 
            'available_languages': ['es'], 
            'translations_folder': "C:_this/folder/dont/exist", 
            'source_files_folder': None, 
            'translatables_folder': None, 
            'use_default_on_failure': True, 
            'revise_after_build': False, 
            'clean': True, 
            'debug_mode': True, 
            'verbose': False
}


    
    

class TestTranslator:
    
    def test_source_file_not_found(self):
        with pytest.raises(qal_excs.IOFailure):
            QAutoLinguist(
                source_file="C:_this/folder/dont/exist",  # should raise IOFailure
                available_languages= ['en'],
            )
    
    def test_source_file_not_file(self):
        with pytest.raises(qal_excs.RequiredFileError):
            QAutoLinguist(
                source_file= ROOT,  # expected file
                available_languages= ['en'],
            )
    
    def test_folder_not_found(self):
        with pytest.raises(qal_excs.IOFailure):
            QAutoLinguist(
                source_file= ROOT / "targets" / "test.ts",  # thats valid source
                available_languages= ['en'],
                translatables_folder= "C:_1234/path/that/dont/.exist"    # should raise IOFailure
            )
            
    def test_required_dir(self):
        with pytest.raises(qal_excs.RequiredDirError):
            QAutoLinguist(
                source_file= ROOT / "targets" / "test.ts",  
                available_languages= ['en'],
                translatables_folder= ROOT / "targets" / "test.ts"   # expected dir
            )
    
    def test_invalid_langs(self):
        with pytest.raises(qal_excs.InvalidLanguage):
            QAutoLinguist(**Config().load_config(INVALID_ROOT / "invalid_list_elems.ini"))

    def test_on_wrong_pylupdate_options(self):
        with pytest.raises(qal_excs.InvalidOptions):
            QAutoLinguist(
                **Config().load_config(VALID_ROOT / "good_config.ini")
            )._validate_options([
                "-invalid-option",
                "-obzolete"
                ], VALID_PYLUPDATE_OPTIONS
            )
             
    def test_on_wrong_pyrelease_options(self):
        with pytest.raises(qal_excs.InvalidOptions):
            QAutoLinguist(
                **Config().load_config(VALID_ROOT / "good_config.ini")
            )._validate_options(
                [
                "-invalid-option",
                "-obzolete"
                ], VALID_PYLRELEASE_OPTIONS
            )   
            
    def test_generates_child_folders_when_none(self):
        inst = QAutoLinguist(
            **Config().load_config(VALID_ROOT / "good_config.ini")  # this config does not pass any path to optional paths
        )
        assert inst.source_files_folder.parent == inst.translations_folder
        assert inst.translatables_folder.parent == inst.translations_folder


    def test_sanitize_created_files(self):
        """
        Como el constructor crea carpetas vacias, nos aseguramos de que no se quedan
        archivos residuales eliminando las carpetas.
        """
        from os import remove
        from qautolinguist.consts import CMD_CWD 
        
        remove(CMD_CWD / QAutoLinguist._TRANSLATIONS_FOLDER_NAME)