from pydantic import BaseModel, Field


class AnalysisConfig(BaseModel):
    primary_repo_focus: str = "agent-workflow"
    max_file_bytes: int = Field(default=250_000)
    exclude_globs: list[str] = Field(
        default_factory=lambda: [
            ".git/**",
            "**/node_modules/**",
            "**/.venv/**",
            "**/__pycache__/**",
        ]
    )
