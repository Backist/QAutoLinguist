import pytest
import os
import qautolinguist.exceptions as qal_excs
from qautolinguist.qal import QAutoLinguist
from qautolinguist.config import Config
from pathlib import Path

ROOT = Path(__file__).parent
VALID_ROOT = ROOT / "valid"
INVALID_ROOT = ROOT / "invalid"
VALID_CONFIG_FILE = VALID_ROOT / "good_config.ini"

class TestConfig:
    "Test class which provides some tests to check all config process works correctly."
    def test_assert_valid_config(self):
        assert Config().load_config(VALID_CONFIG_FILE) == {
            'source_file': r'qautolinguist\tests\targets\test.ui', 
            'default_locale': 'en', 
            'available_locales': ['es'], 
            'translations_folder': None, 
            'source_files_folder': None, 
            'translatables_folder': None, 
            'use_default_on_failure': True, 
            'revise_after_build': False, 
            'clean': True, 
            'debug_mode': True, 
            'verbose': False
        }

    def test_uncompleted_required_params(self):
        with pytest.raises(qal_excs.UncompletedConfig):
            Config().load_config(INVALID_ROOT / "uncompleted_required_section.ini")
            
    def test_same_params(self):
        try:
            qal_inst = QAutoLinguist(**Config().load_config(VALID_CONFIG_FILE))
        except TypeError as e:
            pytest.fail(f"Config.ini does not contain the same parameters as QAutoLinguist. Failed parameter: '{e.args}'.") 
        qal_inst.restore()

    def test_wrong_param_type(self):
        with pytest.raises(qal_excs.ConfigWrongParamFormat):
            Config().load_config(INVALID_ROOT / "miswritten_booleans.ini")

    def test_load_missing_config(self):
        with pytest.raises(qal_excs.MissingConfigFile):
            Config().load_config() # raises MissingConfigFile because neither .create() was called nor path was passed to load_config 

    def test_load_not_exist_config(self):
        with pytest.raises(qal_excs.IOFailure):
            Config().load_config("Z:/test/1234.r")
            
    def test_load_from_dir_path(self):
        with pytest.raises(qal_excs.RequiredFileError):
            Config().load_config(ROOT)    # loading path that points to a directory
    
    def test_create_from_dir_path(self):
        with pytest.raises(qal_excs.RequiredFileError):
            Config().create(ROOT, overwrite=True)    # creating a config file with a path that points to a directory

    def test_create_without_overwrite(self):
        inst = Config()
        inst.create(VALID_ROOT / "testing_config_overwrites.ini")
        with pytest.raises(qal_excs.ConfigFileAlreadyCreated):
            inst.create(VALID_ROOT / "testing_config_overwrites.ini", overwrite=False)
        os.remove(VALID_ROOT / "testing_config_overwrites.ini")
    
    @pytest.mark.skip(reason="Being developed")
    def test_create_with_overwrite(self):
        inst = Config()
        inst.create(VALID_ROOT / "testing_config_overwrites.ini")
        expected_data = inst.load_config()
        
        inst.create(VALID_ROOT / "testing_config_overwrites.ini", overwrite=True)
        assert inst.load_config() == expected_data
        
        os.remove(VALID_ROOT / "testing_config_overwrites.ini")
