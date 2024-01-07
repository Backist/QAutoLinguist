
import pytest
import qautolinguist.exceptions as qal_excs
from qautolinguist.qal import QAutoLinguist
from qautolinguist.config import Config
from pathlib import Path

ROOT = Path(__file__).parent
VALID_ROOT = ROOT / "valid"
INVALID_ROOT = ROOT / "invalid"
INVALID_CONFIG_FILES = [
    pytest.param(p, id=p.stem)
    for p in INVALID_ROOT.glob("*.ini")
]
EXPECTED_CONFIG_DATA = {
    'source_file': r'qautolinguist\tests\targets\test.ui', 
    'default_language': 'en', 
    'available_languages': ['<complete>'], 
    'translations_folder': None, 
    'source_files_folder': None, 
    'translatables_folder': None, 
    'use_default_on_failure': True, 
    'revise_after_build': False, 
    'clean': True, 
    'debug_mode': True, 
    'verbose': False
}



class TestConfig:

    VALID_CONFIG_FILE = VALID_ROOT / "good_config.ini"
    
    @classmethod
    def setup_class(cls):
        # Lógica de configuración que se ejecuta antes de todas las pruebas en la clase
        cls.inst = Config()

    def test_assert_valid_config(self):
        assert self.inst.load_config(self.VALID_CONFIG_FILE) == EXPECTED_CONFIG_DATA

    def test_uncompleted_required_params(self):
        with pytest.raises(qal_excs.UncompletedConfig):
            self.inst.load_config(INVALID_ROOT / "uncompleted_required_section.ini")
    def test_same_params(self):
        try:
            QAutoLinguist(**self.inst.load_config(self.VALID_CONFIG_FILE))
        except TypeError as e:
            pytest.fail(f"Config.ini does not contain the same parameters as QAutoLinguist. Parameter failed: '{e.args}'.") 
        
    @pytest.mark.parametrize("config_file", INVALID_CONFIG_FILES)
    def test_wrong_param_type(self, config_file):
        with pytest.raises(qal_excs.ConfigWrongParamFormat):
            self.inst.load_config(config_file)

    def test_load_missing_config(self):
        with pytest.raises(qal_excs.MissingConfigFile):
            self.inst.load_config()

    def test_load_not_exist_config(self):
        with pytest.raises(qal_excs.IOFailure):
            self.inst.load_config("Z:/test/1234.r")
            
    def test_load_from_dir_path(self):
        with pytest.raises(qal_excs.RequiredFileError):
            self.inst.load_config(ROOT)    # loading path that points to a directory

    def test_create_from_dir_path(self):
        with pytest.raises(qal_excs.IOFailure):
            self.inst.create(ROOT, overwrite=True)    # creating a config file with a path that points to a directory
            
    def test_create_without_overwrite(self):
        with pytest.raises(qal_excs.ConfigFileAlreadyCreated):
            self.inst.create(self.VALID_CONFIG_FILE, overwrite=False)

    def test_create_with_overwrite(self):
        self.inst.create(self.VALID_CONFIG_FILE, overwrite=True) 
        assert self.inst.load_config() == EXPECTED_CONFIG_DATA
        