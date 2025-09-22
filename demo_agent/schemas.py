from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class CompletionMode(Enum):
    COMPLETE = "complete"
    NEEDS_MORE_INFO = "needs_more_info"
    ERROR = "error"


class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IssueType(Enum):
    PERFORMANCE = "performance"
    QUERY_OPTIMIZATION = "query_optimization"
    SCHEMA_DESIGN = "schema_design"
    INDEXING = "indexing"
    N_PLUS_ONE = "n_plus_one"
    MEMORY_USAGE = "memory_usage"
    SECURITY = "security"


class Issue(BaseModel):
    type: IssueType
    severity: Severity
    line_number: Optional[int] = None
    description: str
    code_snippet: Optional[str] = None
    impact: str = Field(..., description="Explanation of the performance impact")


class Recommendation(BaseModel):
    issue_type: IssueType
    title: str
    description: str
    code_example: Optional[str] = None
    priority: Severity
    estimated_impact: str = Field(..., description="Expected performance improvement")


class FileAnalysis(BaseModel):
    file_path: str
    purpose: str = Field(..., description="Why this file was analyzed")
    lines_read: int
    relevant_patterns_found: List[str] = Field(default_factory=list)


class ReviewResult(BaseModel):
    target_file: str
    completion_status: CompletionMode
    issues_found: List[Issue] = Field(default_factory=list)
    recommendations: List[Recommendation] = Field(default_factory=list)
    files_analyzed: List[FileAnalysis] = Field(default_factory=list)
    summary: str = Field(..., description="Executive summary of the analysis")
    tokens_used: Optional[int] = None
    error_message: Optional[str] = None

    class Config:
        use_enum_values = True