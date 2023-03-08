from dotenv import dotenv_values

config: dict[str, str | None] = {
    # Load the configuration without impacting the environment
    **dotenv_values("./env")
}