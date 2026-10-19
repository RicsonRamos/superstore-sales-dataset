import pathlib
import shutil

import kagglehub


def load_data():
    # Obtém o diretório onde este script está localizado
    project_dir = pathlib.Path(__file__).resolve().parent

    # Sobe até à raiz Superstore-Sales-Dataset
    project_root = project_dir.parents[1]

    # Define a pasta dos dados brutos na raiz do projeto
    raw_dir = project_root / "data" / "01_raw"

    # Define o caminho completo do ficheiro CSV de destino
    destination = raw_dir / "superstore_sales_dataset.csv"

    # Verifica se o dataset já existe na pasta de destino
    if destination.exists():
        print(f"Dataset já existe em: {destination}")
        return

    # Cria a pasta data/01_raw caso ainda não exista
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Descarrega o dataset do KaggleHub
    # O retorno é o caminho da pasta de cache onde os ficheiros ficam guardados
    dataset_dir = pathlib.Path(
        kagglehub.dataset_download("vivek468/superstore-dataset-final")
    )

    # Procura ficheiros CSV dentro da pasta descarregada,
    # incluindo eventuais subpastas
    csv_files = list(dataset_dir.rglob("*.csv"))

    # Verifica se foi encontrado algum ficheiro CSV
    if not csv_files:
        raise FileNotFoundError(  # noqa: TRY003
            f"Nenhum ficheiro CSV encontrado em: {dataset_dir}"
        )

    # Seleciona o primeiro ficheiro CSV encontrado
    # (o dataset pode ter um nome diferente do esperado)
    source = csv_files[0]

    # Copia o ficheiro CSV para data/01_raw com o nome pretendido
    shutil.copy2(source, destination)

    # Confirma que o ficheiro foi guardado no destino
    print(f"Dataset copiado de: {source}")
    print(f"Dataset guardado em: {destination}")


if __name__ == "__main__":
    load_data()
