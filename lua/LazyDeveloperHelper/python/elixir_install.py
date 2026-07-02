#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from shutil import which
from logger import logger

ELIXIR_PATH = which("elixir")
MIX_EXS_FILE = "mix.exs"

if not ELIXIR_PATH:
    logger("Elixir CLI are NOT found! Install it!", "error")
else:
    logger("Elixir is here, nice", "success")
#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def default_exs_file(deps: list):
    """
    Args:
        deps: list - List of all your dependencies u want to install,
    """
    file_template = f"""defmodule LazyDeveloperHelperTemplate.MixProject do
    use Mix.Project

    def project do
      [
        app: :lazy_developer_helper_template,
        version: "0.1.0",
        elixir: "~> 1.20.2",
        start_permanent: Mix.env() == :prod,
        deps: deps()
      ]
    end

    def application do
        [
            extra_applications: [:logger]
        ]
    end

  defp deps do
    [
        {deps}
    ]   end

    end

    """
    return file_template
