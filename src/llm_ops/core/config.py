import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class AppSettings(BaseSettings):
    app_name: str = "merchmix-llm-ops"
    app_env: str = "local"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_log_level: str = "INFO"
    app_debug: bool = False

class ModelSettings(BaseSettings):
    model_provider: str = "llama_cpp"
    model_name: str = "qwen_1_5b_sft_v2_q5_k_m"
    llama_cpp_model_path: str = "models/gguf/qwen_1_5b_sft_v2_merged.Q5_K_M.gguf"
    llama_cpp_base_url: str = "http://localhost:8080"
    vllm_base_url: str = "http://localhost:8001/v1"
    vllm_api_key: str = "dummy"
    vllm_model_name: str = "qwen_1_5b_sft_v2_merged"
    llm_temperature: float = 0.0
    llm_top_p: float = 1.0
    llm_max_tokens: int = 1024
    llm_context_window: int = 8192
    llm_timeout_seconds: int = 120

class RAGSettings(BaseSettings):
    rag_mode: str = "hybrid"
    rag_top_k_dense: int = 20
    rag_top_k_sparse: int = 20
    rag_top_k_final: int = 8
    rag_chunk_size: int = 900
    rag_chunk_overlap: int = 120
    rag_require_citations: bool = True
    rag_min_confidence: float = 0.65
    rag_enable_query_rewrite: bool = True
    rag_enable_context_compression: bool = True
    rag_corpus_dir: str = "data/rag_corpus"

class QdrantSettings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection_docs: str = "merchmix_docs"
    qdrant_collection_sql: str = "merchmix_sql"
    qdrant_collection_model_registry: str = "merchmix_model_registry"
    qdrant_collection_eval_reports: str = "merchmix_eval_reports"
    qdrant_collection_lineage: str = "merchmix_data_lineage"
    qdrant_vector_size: int = 768
    qdrant_distance: str = "Cosine"
    qdrant_use_hybrid: bool = True
    qdrant_fusion_method: str = "RRF"

class PineconeSettings(BaseSettings):
    pinecone_api_key: str = ""
    pinecone_index_name: str = "merchmix-rag"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"
    pinecone_namespace: str = "local"
    pinecone_use_rerank: bool = False
    pinecone_rerank_model: str = ""

class LangfuseSettings(BaseSettings):
    langfuse_enabled: bool = False
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "http://localhost:3000"
    langfuse_environment: str = "local"
    langfuse_release: str = "phase8-rag-v1"

class GuardrailSettings(BaseSettings):
    guardrails_enabled: bool = True
    block_unsafe_sql: bool = True
    block_prompt_injection: bool = True
    require_citations_for_facts: bool = True
    allow_missing_citations_if_low_confidence: bool = False

class SelfEvalSettings(BaseSettings):
    self_eval_enabled: bool = True
    self_eval_min_grounding_score: float = 0.8
    self_eval_min_sql_safety_score: float = 1.0
    self_eval_min_answer_quality_score: float = 0.85
    self_eval_require_human_review_below: float = 0.75
    self_eval_low_confidence_action: str = "retry_retrieval"

class HarnessSettings(BaseSettings):
    harness_enabled: bool = True
    run_regression_before_promotion: bool = True

class LearningLoopSettings(BaseSettings):
    learning_loop_enabled: bool = True
    auto_training_enabled: bool = False
    auto_promotion_enabled: bool = False
    failure_inbox_path: str = "data/failures/failure_inbox.jsonl"

class AgentSettings(BaseSettings):
    agents_enabled: bool = False
    agent_max_steps: int = 8
    agent_timeout_seconds: int = 180
    agent_require_human_approval_for_writes: bool = True
    agent_memory_enabled: bool = False
    agent_state_db_url: str = "sqlite:///data/agent_state.db"

class MCPSettings(BaseSettings):
    mcp_enabled: bool = False
    mcp_server_name: str = "merchmix-tools"
    mcp_transport: str = "stdio"
    mcp_tool_timeout_seconds: int = 60
    mcp_allow_write_tools: bool = False
    mcp_require_auth: bool = True

class BigQuerySettings(BaseSettings):
    google_application_credentials: str = ""
    gcp_project_id: str = "merchmix"
    bigquery_default_location: str = "US"
    bigquery_max_bytes_billed: int = 1000000000
    bigquery_read_only: bool = True
    bigquery_dry_run_default: bool = True
    bigquery_timeout_seconds: int = 60

class SecuritySettings(BaseSettings):
    allow_destructive_sql: bool = False
    allow_shell_tools: bool = False
    allow_file_delete: bool = False
    allow_git_push: bool = False
    allow_prod_write: bool = False
    api_auth_enabled: bool = False
    api_auth_token: str = ""

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app: AppSettings = Field(default_factory=AppSettings)
    model: ModelSettings = Field(default_factory=ModelSettings)
    rag: RAGSettings = Field(default_factory=RAGSettings)
    qdrant: QdrantSettings = Field(default_factory=QdrantSettings)
    pinecone: PineconeSettings = Field(default_factory=PineconeSettings)
    langfuse: LangfuseSettings = Field(default_factory=LangfuseSettings)
    guardrail: GuardrailSettings = Field(default_factory=GuardrailSettings)
    self_eval: SelfEvalSettings = Field(default_factory=SelfEvalSettings)
    harness: HarnessSettings = Field(default_factory=HarnessSettings)
    learning_loop: LearningLoopSettings = Field(default_factory=LearningLoopSettings)
    agent: AgentSettings = Field(default_factory=AgentSettings)
    mcp: MCPSettings = Field(default_factory=MCPSettings)
    bigquery: BigQuerySettings = Field(default_factory=BigQuerySettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)

settings = Settings()
