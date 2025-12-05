import yaml
from dotenv import load_dotenv

from utils.argument_utils import ArgumentUtils


class ProjectConfig:
    """
    统一处理整个项目的配置，项目的配置对象设置为单例模式，只配置一次就可以了
    """
    _instance = None  # 当前类的示例

    # 重写 __new__函数来实现单例模式
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProjectConfig, cls).__new__(cls)  # 调用父类的构造函数，创建ProjectConfig
            cls._instance._config = None
            cls._instance._args = None
        return cls._instance

    def initialize(self):
        """
        初始化所有项目配置
        """
        # load环境变量
        load_dotenv()

        # 命令行参数配置的初始化
        if self._args is None:
            arg_utils = ArgumentUtils
            self._args = arg_utils.parse_arg()

        # YAML配置文件的初始化：如果YAML和命令行都包含参数，以命令行为准
        if self._config is None:
            with open(self._args.config, 'r') as f:
                config = yaml.safe_load(f)  # 读取文件配置
            overridden_config = {
                key: value for key, value in vars(self._args).items() if key in config and value is not None
            }  # 列表生成式
            config.update(overridden_config)  # 把命令行的参数覆盖config文件的配置
            self._config = config

    # 重写 函数__getattr__， 当访问当前对象示例属性时，自动调用
    def __getattr__(self, item):
        if self._config and item in self._config:
            return self._config[item]
        raise AttributeError(f'项目属性中没有名字为{item}的属性。')

