import enum


class Language(enum.Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    JAVA = "java"
    C = "c"
    CPP = "cpp"
    CSHARP = "csharp"
    RUBY = "ruby"
    PHP = "php"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    RUST = "rust"

class Framework(enum.Enum):
    DJANGO = "django"
    FLASK = "flask"
    FASTAPI = "fastapi"
    REACT = "react"
    ANGULAR = "angular"
    VUE = "vue"
    RUBY_ON_RAILS = "ruby_on_rails"
    EXPRESS = "express"
    NEXTJS = "nextjs"
    SPRING_BOOT = "spring_boot"
    GIN = "gin"
    LARAVEL = "laravel"
    NESTJS = "nestjs"


class DatabaseType(enum.Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    REDIS = "redis"
    MARIADB = "mariadb"


class ORM(enum.Enum):
    SQLALCHEMY = "sqlalchemy"
    DJANGO_ORM = "django_orm"
    PRISMA = "prisma"
    TYPEORM = "typeorm"
    SEQUELIZE = "sequelize"
    MONGOOSE = "mongoose"
    GORM = "gorm"
    HIBERNATE = "hibernate"
    ELOQUENT = "eloquent"
